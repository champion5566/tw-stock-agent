"""Deterministic report previews: source dates and live observations stay separate.

This is a data/report acceptance experiment, not scheduled message delivery.
"""
import argparse
import json
import hashlib
import os
from datetime import datetime, time
from pathlib import Path

from instruments import STOCKS, REPORT_STOCKS, WATCH_STOCKS
from quote_quality import TW, quote_status
from session_calendar import completed_session
from stock_metrics import metrics
from report_contract import evaluate, DELIVERY_TIMES


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
    report = {"schema_version": "scenario-report-v2", "scenario": mode,
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
        session = completed_session("XTAI", datetime.combine(checked.date(), DELIVERY_TIMES[mode], TW))
        target = session["date"]
        report["session_calendar"] = session
        report["target_session_date"] = target
        report["warnings"].append("交易日使用 exchange_calendars XTAI；臨時停市以來源實際狀態另行核對。")
        for code in STOCKS:
            stock = market.get("stocks", {}).get(code, {})
            report["stocks"][code] = {key: daily_selection(stock.get(key, {}), target, checked, mode)
                                      for key in ("daily_ohlcv", "institutional", "margin")}
            report["stocks"][code]["metrics"] = metrics(stock, target)
            report["stocks"][code]["role"] = "report_required" if code in REPORT_STOCKS else "watch_only"
        for area, assets in cross.get("assets", {}).items():
            report["cross_market"][area] = {}
            for name, observation in assets.items():
                # Expose only source-level fields, never label a Yahoo bar as live/official close.
                report["cross_market"][area][name] = {k: observation.get(k) for k in (
                    "price", "status", "source", "latest_bar_at_taipei", "data_kind", "is_formal_close")}
    future = (cross.get("taifex", {}).get("shioaji_session_tx") if mode == "morning" else None) or intraday.get("futures", {}).get("TXFR1") or cross.get("taifex", {}).get("shioaji_live_tx") or {}
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
    report["stock_data_status"] = "COMPLETE" if complete else "PARTIAL"
    report["readiness"] = evaluate(report, market, cross, checked, experiment)
    report["status"] = report["readiness"]["data_readiness"]
    if mode == "morning" and report["readiness"]["sections"].get("tx_completed_night", {}).get("status") == "PASS":
        report["futures"]["TXFR1"].update({"price":future.get("price"), "status":"COMPLETED_NIGHT_LAST_OBSERVATION", "is_live":False})
    report["delivery_status"] = "NOT_ACKNOWLEDGED"
    report["required_stocks"] = list(REPORT_STOCKS)
    report["watch_stocks"] = list(WATCH_STOCKS)
    return report


def display(value):
    return "—" if value is None else str(value)


def render_markdown(report):
    names = {"morning": "晨報", "evening": "夜報", "intraday": "即時行情"}
    lines = [f"# {names[report['scenario']]}情境實驗", "",
             f"執行時間：{report['generated_at_taipei']}｜資料驗收：{report['status']}｜送達：{report['delivery_status']}", "",
             *report["warnings"], "",
             "必備資料驗收：", "", "| 項目 | 狀態 | 缺漏／異常 |", "|---|---|---|"]
    for name, section in report["readiness"]["sections"].items():
        failures = ", ".join(f"{key}={value}" for key,value in section["items"].items() if value != "PASS") or "—"
        lines.append(f"| {name} | {section['status']} | {failures} |")
    lines += ["", "持股／觀察清單的行情資料完整，不代表跨市場、帳本或送達驗收完成。", ""]
    if report["scenario"] == "intraday":
        lines += ["| 標的 | 價格 | 來源 | 資料種類 | 來源時間 | 狀態 |", "|---|---:|---|---|---|---|"]
        for code, q in report["stocks"].items():
            lines.append(f"| {code} | {display(q.get('price'))} | {display(q.get('source'))} | {display(q.get('data_kind'))} | {display(q.get('trade_time'))} | {q['status']} |")
    else:
        lines += [f"台股基準交易日：{display(report.get('target_session_date'))}", "",
                  "| 股票／角色 | 日期 | 開 | 高 | 低 | 收 | 成交股數 | OHLC狀態 | 法人資料日期／狀態 | 融資券日期／狀態 |",
                  "|---|---|---:|---:|---:|---:|---:|---|---|---|"]
        for code, item in report["stocks"].items():
            daily, inst, margin = (item[k] for k in ("daily_ohlcv", "institutional", "margin"))
            row = daily["data"] or {}
            cells = [code + ("（必備）" if code in REPORT_STOCKS else "（觀察）"), daily["source_date"], *[row.get(k) for k in ("open", "max", "min", "close", "Trading_Volume")], daily["status"],
                     f"{display(inst['source_date'])} / {inst['status']}", f"{display(margin['source_date'])} / {margin['status']}"]
            lines.append("| " + " | ".join(display(v) for v in cells) + " |")
        lines += ["", "六檔必備衍生欄位（同一 FinMind 來源；法人單位為股，融資券為來源原生張數）：", "",
                  "| 股票 | 前收 | 成交值TWD | 振幅% | 5日量比 | 20日量比 | 外資淨買 | 投信淨買 | 自營淨買 | 法人5日合計 | 融資增減 | 融券增減 |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for code in REPORT_STOCKS:
            f = report["stocks"][code]["metrics"]
            inst, credit = f["institutional"], f["credit"]
            cells = [code, *[f.get(k) for k in ("previous_close", "turnover_twd", "amplitude_pct", "volume_ratio_5d", "volume_ratio_20d")],
                     *[inst.get(k) for k in ("foreign_net_shares", "trust_net_shares", "dealer_net_shares", "net_5d_shares")],
                     credit.get("margin_change"), credit.get("short_change")]
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
    parser.add_argument("--market-root", default="out")
    parser.add_argument("--output-root", default="out")
    args = parser.parse_args()
    now = datetime.now(TW)
    directory = Path(args.output_root) / now.date().isoformat()
    fingerprints = {}
    def read(name, root=None):
        path = (Path(root) / now.date().isoformat() if root else directory) / (name + ".json")
        if not path.exists():
            return {}
        raw = path.read_bytes()
        fingerprints[("market/" if root else "current/") + name] = {
            "snapshot":str(path.relative_to(Path(root) if root else Path(args.output_root))),
            "sha256":hashlib.sha256(raw).hexdigest()}
        return json.loads(raw)
    report = build_report(args.scenario, read(args.scenario, args.market_root), read("intraday"), read("cross-" + args.scenario),
                          checked_at=now, experiment=args.experiment)
    report["input_fingerprints"] = fingerprints
    report["data_report_id"] = "DATA-" + now.date().isoformat() + "-" + args.scenario + "-" + os.getenv("GITHUB_RUN_ID", now.strftime("%H%M%S"))
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ("report-" + args.scenario + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    markdown = render_markdown(report)
    (directory / ("report-" + args.scenario + ".md")).write_text(markdown, encoding="utf-8")
    # Small, public-data-only consumer artifact. No positions/account values/LLM ledger.
    bundle = Path(args.output_root) / "reports" / now.date().isoformat()
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / (args.scenario + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("SCENARIO_REPORT", json.dumps({k:report[k] for k in ("scenario", "generated_at_taipei", "status", "coverage")}, ensure_ascii=False))
    print(markdown)


if __name__ == "__main__":
    main()
