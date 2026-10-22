"""Deterministic research feature ledger. No LLM guesses, no trading orders.

Outputs timestamped, auditable *hypotheses* and data coverage, not backtested alpha.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")
WATCH = {"2330": "台積電", "0050": "元大台灣50", "5483": "中美晶",
         "3707": "漢磊", "2313": "華通", "2367": "燿華", "3491": "昇達科"}


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def analyze(stock):
    q = stock.get("mcp_quote", {})
    d = stock.get("daily_ohlcv", {})
    history = d.get("history") or []
    bars = []
    for row in history:
        close = number(row.get("close"))
        volume = number(row.get("Trading_Volume"))
        if close is not None and volume is not None:
            bars.append((row.get("date"), close, volume))
    latest = bars[-1] if bars else None
    prev = bars[-2] if len(bars) > 1 else None
    prior_vols = [x[2] for x in bars[-21:-1]]
    features = {
        "quote_status": q.get("status"), "quote_source_date": q.get("source_date"),
        "daily_status": d.get("status"), "daily_source_date": d.get("source_date"),
        "bars_available": len(bars), "latest_close": latest[1] if latest else None,
        "latest_volume_shares": latest[2] if latest else None,
        "previous_close": prev[1] if prev else None,
        "one_day_return_pct": (round((latest[1] / prev[1] - 1) * 100, 3)
                               if latest and prev and prev[1] else None),
        "volume_ratio_20d": (round(latest[2] / (sum(prior_vols) / len(prior_vols)), 3)
                             if latest and prior_vols and sum(prior_vols) else None),
        "close_vs_sma20_pct": (round((latest[1] / (sum(x[1] for x in bars[-20:]) / 20) - 1) * 100, 3)
                               if latest and len(bars) >= 20 else None),
        "institutional_status": stock.get("institutional", {}).get("status"),
        "institutional_source_date": stock.get("institutional", {}).get("source_date"),
        "margin_status": stock.get("margin", {}).get("status"),
        "margin_source_date": stock.get("margin", {}).get("source_date"),
    }
    return features


def main():
    now = datetime.now(TZ)
    date = now.date().isoformat()
    slot = os.environ.get("REPORT_SLOT", "evening")
    path = Path(os.getenv("SOURCE_SNAPSHOT", str(Path("out") / date / (slot + ".json"))))
    date = path.parent.name
    if not path.exists():
        raise SystemExit("Missing input market snapshot")
    market = json.loads(path.read_text(encoding="utf-8"))
    features = {code: analyze(market.get("stocks", {}).get(code, {})) for code in WATCH}
    coverage = {
        "stocks_total": len(features),
        "daily_ohlcv_available": sum(x["latest_close"] is not None for x in features.values()),
        "institutional_current_day": sum(x["institutional_source_date"] == date for x in features.values()),
        "margin_current_day": sum(x["margin_source_date"] == date for x in features.values()),
    }
    hypotheses = []
    for code, f in features.items():
        # Never call an old close a real-time signal.
        if f["daily_source_date"] != date or f["daily_status"] != "PASS":
            continue
        ret, vol = f["one_day_return_pct"], f["volume_ratio_20d"]
        if ret is None or vol is None:
            continue
        if ret >= 2 and vol >= 1.5:
            label = "PRICE_VOLUME_EXPANSION"
            rationale = "當日漲幅>=2%，成交量>=過去20交易日均量1.5倍"
        elif ret <= -2 and vol >= 1.5:
            label = "SELL_PRESSURE_ALERT"
            rationale = "當日跌幅<=-2%，成交量>=過去20交易日均量1.5倍"
        else:
            continue
        hypotheses.append({
            "id": date.replace("-", "") + "-" + slot + "-" + code,
            "status": "UNTESTED", "label": label, "code": code, "name": WATCH[code],
            "observed_on": date, "return_pct": ret, "volume_ratio_20d": vol,
            "basis": rationale, "invalidation": "下一交易日觀察是否反轉；不構成買賣指令",
            "verify_on": "NEXT_TRADING_SESSION",
            "warning": "研究假設，尚無樣本外勝率、交易成本或統計顯著性證據",
        })
    output = {
        "schema_version": "research-v1", "created_at_taipei": now.isoformat(),
        "slot": slot, "source_snapshot": str(path.relative_to("out")),
        "trade_date": date, "coverage": coverage, "features": features,
        "hypotheses": hypotheses,
        "methodology": "歷史收盤與20日量比，僅當同日資料PASS時發出假設；沒有假設也正常。",
        "disclaimer": "NOT_BACKTESTED; NOT_TRADING_ADVICE; no claims of alpha",
    }
    dest = Path("out") / date / ("research-" + slot + ".json")
    dest.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("RESEARCH_RESULT", json.dumps({"path": str(dest), "coverage": coverage,
                                          "hypotheses": len(hypotheses)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
