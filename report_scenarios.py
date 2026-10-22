"""Deterministic report previews: source dates and live observations stay separate.

This is a data/report acceptance experiment, not scheduled message delivery.
"""
import argparse
import json
from datetime import datetime, time
from pathlib import Path

from instruments import STOCKS
from quote_quality import TW, quote_status


def dated_rows(item):
    rows = item.get("history") or ([item["data"]] if item.get("data") else [])
    return [row for row in rows if isinstance(row, dict) and isinstance(row.get("date"), str)]


def daily_selection(item, target, checked, mode):
    rows = [r for r in dated_rows(item) if target and r["date"] <= target]
    row = max(rows, key=lambda r: r["date"]) if rows else None
    available = row is not None and row["date"] == target
    status = "PASS" if available else "MISSING_TARGET_SESSION"
    if mode == "evening" and checked.time() < time(13, 30):
        status, available = "SESSION_NOT_CLOSED", False
    return {"status": status, "target_session": target,
            "source_date": row.get("date") if row else None,
            "data": row if available else None,
            "prior_reference": row if not available else None,
            "data_kind": "daily", "is_live": False,
            "provider_status": item.get("status", "MISSING")}


def build_report(mode, market=None, intraday=None, cross=None, *, checked_at=None, experiment=False):
    if mode not in ("morning", "evening", "intraday"):
        raise ValueError("Unknown report scenario")
    checked = checked_at or datetime.now(TW)
    checked = checked.replace(tzinfo=TW) if checked.tzinfo is None else checked.astimezone(TW)
    market, intraday, cross = market or {}, intraday or {}, cross or {}
    today = checked.date().isoformat()
    report = {"schema_version": "scenario-report-v1", "scenario": mode,
              "generated_at_taipei": checked.isoformat(),
              "execution_kind": "CURRENT_TIME_PREVIEW" if experiment else "REPORT",
              "point_in_time_verified": False,
              "source_fetched_at": {"market": market.get("fetched_at_taipei"),
                                    "intraday": intraday.get("checked_at_taipei"),
                                    "cross": cross.get("fetched_at_taipei")},
              "stocks": {}, "cross_market": {}, "futures": {}, "warnings": []}
    if experiment:
        report["warnings"].append("現時資料流程試跑；不代表已在08:20或23:00執行或送達，亦非歷史時點回放。")
    if mode == "intraday":
        for code, raw in intraday.get("quotes", {}).items():
            quote = dict(raw)
            try:
                stamp = datetime.fromisoformat(quote["trade_time"])
            except (KeyError, ValueError, TypeError):
                stamp = None
            quote["status"] = quote_status(quote.get("price"), stamp, checked)
            quote["is_live"] = raw.get("data_kind") == "tick" and quote["status"] == "PASS"
            if quote["status"] != "PASS":
                quote["last_observation_price"] = quote.get("price")
                quote["price"] = None
            report["stocks"][code] = quote
    else:
        previous = [r["date"] for stock in market.get("stocks", {}).values()
                    for r in dated_rows(stock.get("daily_ohlcv", {})) if r["date"] < today]
        target = max(previous) if mode == "morning" and previous else today if mode == "evening" else None
        report["target_session_date"] = target
        report["warnings"].append("晨報基準日由可取得的前一交易日資料推得；未以交易所休市日曆驗證。")
        for code in STOCKS:
            stock = market.get("stocks", {}).get(code, {})
            report["stocks"][code] = {key: daily_selection(stock.get(key, {}), target, checked, mode)
                                      for key in ("daily_ohlcv", "institutional", "margin")}
        for area, assets in cross.get("assets", {}).items():
            report["cross_market"][area] = {}
            for name, observation in assets.items():
                # Expose only source-level fields, never label a Yahoo bar as live/official close.
                report["cross_market"][area][name] = {k: observation.get(k) for k in (
                    "price", "status", "source", "latest_bar_at_taipei", "data_kind", "is_formal_close")}
    future = intraday.get("futures", {}).get("TXFR1") or cross.get("taifex", {}).get("shioaji_live_tx") or {}
    if future:
        obs = {k: future.get(k) for k in ("price", "trade_time", "source", "contract_code", "data_kind")}
        try:
            stamp = datetime.fromisoformat(obs["trade_time"])
        except (ValueError, TypeError):
            stamp = None
        obs["status"] = quote_status(obs.get("price"), stamp, checked)
        obs["is_live"] = obs["status"] == "PASS" and obs.get("data_kind") == "tick"
        if not obs["is_live"]:
            obs["last_observation_price"], obs["price"] = obs.get("price"), None
        report["futures"]["TXFR1"] = obs
    if mode == "intraday":
        coverage = {"requested_stocks": len(STOCKS),
                    "fresh_stocks": sum(report["stocks"].get(code, {}).get("status") == "PASS" for code in STOCKS),
                    "shioaji_selected": sum(report["stocks"].get(code, {}).get("source", "").startswith("Shioaji") for code in STOCKS),
                    "stock_ticks": sum(report["stocks"].get(code, {}).get("data_kind") == "tick" for code in STOCKS)}
        complete = coverage["fresh_stocks"] == len(STOCKS)
    else:
        coverage = {"stocks_total": len(STOCKS)}
        for key in ("daily_ohlcv", "institutional", "margin"):
            coverage[key + "_target_session"] = sum(s[key]["status"] == "PASS" for s in report["stocks"].values())
        complete = all(value == len(STOCKS) for value in coverage.values())
    report["coverage"] = coverage
    report["status"] = "COMPLETE" if complete else "PARTIAL"
    return report


def display(value):
    return "—" if value is None else str(value)


def render_markdown(report):
    names = {"morning": "晨報", "evening": "夜報", "intraday": "即時行情"}
    lines = [f"# {names[report['scenario']]}情境實驗", "",
             f"執行時間：{report['generated_at_taipei']}｜資料完整度：{report['status']}", "",
             *report["warnings"], ""]
    if report["scenario"] == "intraday":
        lines += ["| 標的 | 價格 | 來源 | 資料種類 | 來源時間 | 狀態 |", "|---|---:|---|---|---|---|"]
        for code, q in report["stocks"].items():
            lines.append(f"| {code} | {display(q.get('price'))} | {display(q.get('source'))} | {display(q.get('data_kind'))} | {display(q.get('trade_time'))} | {q['status']} |")
    else:
        lines += [f"台股基準交易日：{display(report.get('target_session_date'))}", "",
                  "| 股票 | 日期 | 開 | 高 | 低 | 收 | 成交股數 | OHLC狀態 | 法人資料日期／狀態 | 融資券日期／狀態 |",
                  "|---|---|---:|---:|---:|---:|---:|---|---|---|"]
        for code, item in report["stocks"].items():
            daily, inst, margin = (item[k] for k in ("daily_ohlcv", "institutional", "margin"))
            row = daily["data"] or {}
            cells = [code, daily["source_date"], *[row.get(k) for k in ("open", "max", "min", "close", "Trading_Volume")], daily["status"],
                     f"{display(inst['source_date'])} / {inst['status']}", f"{display(margin['source_date'])} / {margin['status']}"]
            lines.append("| " + " | ".join(display(v) for v in cells) + " |")
        lines += ["", "跨市場觀測（依來源時間；Yahoo K線不等於正式收盤）：", "",
                  "| 市場／標的 | 價格 | 來源時間 | 狀態 |", "|---|---:|---|---|"]
        for area, assets in report["cross_market"].items():
            for name, obs in assets.items():
                lines.append(f"| {area}/{name} | {display(obs.get('price'))} | {display(obs.get('latest_bar_at_taipei'))} | {display(obs.get('status'))} |")
    lines += ["", "台指期：" + json.dumps(report["futures"], ensure_ascii=False), "",
              "涵蓋狀態：" + json.dumps(report["coverage"], ensure_ascii=False), ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("morning", "evening", "intraday"), required=True)
    parser.add_argument("--experiment", action="store_true")
    args = parser.parse_args()
    now = datetime.now(TW)
    directory = Path("out") / now.date().isoformat()
    def read(name):
        path = directory / (name + ".json")
        return json.loads(path.read_text()) if path.exists() else {}
    report = build_report(args.scenario, read(args.scenario), read("intraday"), read("cross-" + args.scenario),
                          checked_at=now, experiment=args.experiment)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ("report-" + args.scenario + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    markdown = render_markdown(report)
    (directory / ("report-" + args.scenario + ".md")).write_text(markdown, encoding="utf-8")
    print("SCENARIO_REPORT", json.dumps({k:report[k] for k in ("scenario", "generated_at_taipei", "status", "coverage")}, ensure_ascii=False))
    print(markdown)


if __name__ == "__main__":
    main()
