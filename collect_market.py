"""Build auditable TW stock market snapshot from mature TWSE MCP and FinMind sources.

Output is a *data snapshot*, not a forecast. Every source retains its own date,
units and failure status. Does not require tokens for small public requests.
"""
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")
from market_sources import MCP_URL, FINMIND_URL, mcp, finmind, attempt
from quote_quality import daily_status, parse_source_time, quote_status
from snapshot_io import write_snapshot

STOCKS = {"2313": "tse", "2330": "tse", "0050": "tse",
          "5483": "otc", "3707": "otc", "2367": "tse", "3491": "otc"}

def latest(rows):
    return max(rows, key=lambda row: str(row.get("date", ""))) if rows else None


def quality(item, asof, max_age_days):
    if item["status"] != "PASS":
        return item
    row = item.get("data")
    date = row.get("date") if isinstance(row, dict) else None
    if not date:
        item["status"] = "EMPTY"
        return item
    item["status"] = daily_status(date, asof, max_age_days)
    return item


def main():
    now = datetime.now(TZ)
    slot = os.environ.get("REPORT_SLOT", "evening")
    if slot not in ("morning", "evening"):
        raise ValueError("REPORT_SLOT must be morning/evening")
    asof = now.date()
    start = (asof - timedelta(days=260)).isoformat()
    end = asof.isoformat()
    result = {
        "schema_version": "1.1",
        "fetched_at_taipei": now.isoformat(),
        "trade_date_requested": end,
        "slot": slot,
        "sources": {
            "mcp": MCP_URL,
            "finmind": FINMIND_URL,
            "note": "TWSE MCP quote volume in lots; FinMind Trading_Volume in shares. Values may differ by source/coverage."
        },
        "stocks": {}, "warnings": [],
    }

    init = attempt(lambda: mcp("initialize", {"protocolVersion": "2025-06-18",
                    "capabilities": {}, "clientInfo": {"name": "tw-stock-agent",
                    "version": "1.0"}}, 1))
    result["mcp_initialize"] = {"status": init["status"],
                                 "error": init.get("error")}
    for code, market in STOCKS.items():
        item = {"market": market}
        if init["status"] == "PASS":
            item["mcp_quote"] = attempt(lambda c=code, m=market: mcp(
                "tools/call", {"name": "quote.realtime",
                               "arguments": {"codes": [c], "market": m}}, 2))
            if item["mcp_quote"]["status"] == "PASS":
                q = item["mcp_quote"]["data"]
                q = (q.get("quotes") or [None])[0] if isinstance(q, dict) else None
                item["mcp_quote"]["data"] = q
                item["mcp_quote"]["source_date"] = q.get("date") if q else None
                item["mcp_quote"]["units"] = {"price": "TWD/share", "volume": "lots"}
                item["mcp_quote"]["data_kind"] = "quote_observation"
                item["mcp_quote"]["is_live"] = False
                if not q:
                    item["mcp_quote"]["status"] = "EMPTY"
                else:
                    stamp = parse_source_time(q.get("date"), q.get("time"))
                    status = quote_status(q.get("last"), stamp, datetime.now(TZ))
                    item["mcp_quote"].update({"status": status,
                        "trade_time": stamp.isoformat() if stamp else None,
                        "is_live": status == "PASS"})

        else:
            item["mcp_quote"] = {"status": "FAIL", "error": "MCP initialize failed", "data": None}

        for key, dataset in (("daily_ohlcv", "TaiwanStockPrice"),
                             ("institutional", "TaiwanStockInstitutionalInvestorsBuySellWide"),
                             ("margin", "TaiwanStockMarginPurchaseShortSale")):
            rows = attempt(lambda d=dataset, c=code: finmind(d, c, start, end))
            if rows["status"] == "PASS":
                last = latest(rows["data"])
                history = sorted(rows["data"], key=lambda r: str(r.get("date", "")))
                rows["row_count"] = len(history)
                rows["history"] = history
                rows["history_start"] = history[0].get("date") if history else None
                rows["history_end"] = history[-1].get("date") if history else None
                rows["data"] = last
                rows["source_date"] = last.get("date") if last else None
                rows["dataset"] = dataset
                rows["data_kind"] = "daily"
                rows["is_live"] = False
                rows["units"] = ("Trading_Volume: shares" if key == "daily_ohlcv"
                                 else "buy/sell volume: shares; inspect fields" if key == "institutional"
                                 else "provider-native units; inspect fields")
                # 08:25/20:40: no expectation that institutional data is same day in morning.
                rows = quality(rows, asof, 4 if slot == "morning" else 3)
            item[key] = rows
            time.sleep(0.12)
        result["stocks"][code] = item
        print("STOCK", code, "MCP", item["mcp_quote"]["status"],
              "OHLCV", item["daily_ohlcv"]["status"], item["daily_ohlcv"].get("source_date"),
              "INST", item["institutional"]["status"], item["institutional"].get("source_date"),
              flush=True)

    # The source data is still useful when individual datasets are delayed.
    if all(s["daily_ohlcv"]["status"] == "FAIL" and
           s["mcp_quote"]["status"] == "FAIL" for s in result["stocks"].values()):
        result["warnings"].append("All market quote sources failed")
    result["coverage"] = {
        "stocks_total": len(result["stocks"]),
        "daily_available": sum(s["daily_ohlcv"]["status"] in ("PASS", "PRIOR_SESSION")
                               for s in result["stocks"].values()),
        "live_quotes": sum(s["mcp_quote"].get("is_live", False)
                           for s in result["stocks"].values()),
    }
    out = write_snapshot(result, end, slot)
    print("OUTPUT_PATH", out, "BYTES", out.stat().st_size)
    print("FETCH_COMPLETED_WITH_PARTIAL_FAILURES_POSSIBLE")
    if "All market quote sources failed" in result["warnings"]:
        raise SystemExit("No valid quote source: refusing to publish")


if __name__ == "__main__":
    main()
