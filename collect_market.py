"""Build auditable TW stock market snapshot from mature TWSE MCP and FinMind sources.

Output is a *data snapshot*, not a forecast. Every source retains its own date,
units and failure status. Does not require tokens for small public requests.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")
UA = "tw-stock-agent/1.0 (GitHub Actions; market data research)"
MCP_URL = "https://twse-mcp.taux.io/mcp"
FINMIND_URL = "https://api.finmindtrade.com/api/v4/data"
STOCKS = {"2313": "tse", "2330": "tse", "0050": "tse",
          "5483": "otc", "3707": "otc", "2367": "tse", "3491": "otc"}


def http_json(url, payload=None):
    headers = {"User-Agent": UA, "Accept": "application/json, text/event-stream"}
    if payload is not None:
        headers.update({"Content-Type": "application/json",
                        "MCP-Protocol-Version": "2025-06-18"})
    req = urllib.request.Request(url, headers=headers,
                                 data=json.dumps(payload).encode() if payload else None)
    with urllib.request.urlopen(req, timeout=35) as res:
        raw = res.read().decode()
        if "text/event-stream" in res.headers.get("Content-Type", ""):
            events = [json.loads(x[6:]) for x in raw.splitlines()
                      if x.startswith("data: ") and x[6:].strip() != "[DONE]"]
            if not events:
                raise ValueError("empty MCP event stream")
            return events[-1]
        return json.loads(raw)


def mcp(method, params, call_id):
    response = http_json(MCP_URL, {"jsonrpc": "2.0", "id": call_id,
                                   "method": method, "params": params})
    if response.get("error") or response.get("result", {}).get("isError"):
        raise ValueError(str(response.get("error") or response["result"]))
    return response.get("result", {}).get("structuredContent", response.get("result", {}))


def finmind(dataset, code, start, end):
    params = {"dataset": dataset, "data_id": code,
              "start_date": start, "end_date": end}
    if os.environ.get("FINMIND_TOKEN"):
        params["token"] = os.environ["FINMIND_TOKEN"]
    data = http_json(FINMIND_URL + "?" + urllib.parse.urlencode(params))
    if data.get("status") != 200:
        raise ValueError("FinMind status " + str(data.get("status")) + ": " + str(data.get("msg")))
    rows = data.get("data") or []
    if not isinstance(rows, list):
        raise ValueError("FinMind data not list")
    return rows


def attempt(fn):
    try:
        return {"status": "PASS", "data": fn()}
    except Exception as exc:
        return {"status": "FAIL", "data": None,
                "error": type(exc).__name__ + ": " + str(exc)[:400]}


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
    try:
        age = (asof - datetime.strptime(date, "%Y-%m-%d").date()).days
        item["status"] = ("PASS" if age == 0 else
                          "PRIOR_SESSION" if 0 < age <= max_age_days else "STALE")
    except ValueError:
        item["status"] = "FAIL"
        item["error"] = "Invalid source date"
    return item


def main():
    now = datetime.now(TZ)
    slot = os.environ.get("REPORT_SLOT", "evening")
    if slot not in ("morning", "evening"):
        raise ValueError("REPORT_SLOT must be morning/evening")
    asof = now.date()
    start = (asof - timedelta(days=45)).isoformat()
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
                if not q:
                    item["mcp_quote"]["status"] = "EMPTY"
                elif q.get("date") != end:
                    item["mcp_quote"]["status"] = "STALE"
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
    out = Path("out") / end / (slot + ".json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OUTPUT_PATH", out, "BYTES", out.stat().st_size)
    print("FETCH_COMPLETED_WITH_PARTIAL_FAILURES_POSSIBLE")
    if "All market quote sources failed" in result["warnings"]:
        raise SystemExit("No valid quote source: refusing to publish")


if __name__ == "__main__":
    main()
