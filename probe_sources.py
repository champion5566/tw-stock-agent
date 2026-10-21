"""Probe mature free data providers; never treat stale data as current."""
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

UA = "tw-stock-agent/0.3 (GitHub Actions; public research)"
TW = ZoneInfo("Asia/Taipei")


def request(url, payload=None):
    headers = {"User-Agent": UA, "Accept": "application/json, text/event-stream"}
    if payload is not None:
        headers.update({"Content-Type": "application/json", "MCP-Protocol-Version": "2025-06-18"})
    req = urllib.request.Request(url, headers=headers,
                                 data=json.dumps(payload).encode() if payload else None)
    with urllib.request.urlopen(req, timeout=35) as response:
        body = response.read().decode()
        if "text/event-stream" in response.headers.get("Content-Type", ""):
            lines = [json.loads(line[6:]) for line in body.splitlines()
                     if line.startswith("data: ") and line[6:].strip() != "[DONE]"]
            return lines[-1] if lines else {}
        return json.loads(body)


def mcp(method, params, call_id):
    return request("https://twse-mcp.taux.io/mcp", {
        "jsonrpc": "2.0", "id": call_id, "method": method, "params": params
    })


def probe_mcp():
    init = mcp("initialize", {"protocolVersion": "2025-06-18",
                               "capabilities": {}, "clientInfo": {"name": "tw-stock-agent",
                               "version": "0.3"}}, 1)
    if "error" in init:
        raise ValueError(str(init["error"]))
    for term in ("三大法人", "買賣超"):
        result = mcp("tools/call", {"name": "dataset.search",
                     "arguments": {"query": term, "limit": 12}}, 2)
        print("MCP_DATASET_SEARCH", term, json.dumps(result, ensure_ascii=False)[:5500])


def probe_finmind():
    now = datetime.now(TW)
    start = (now - timedelta(days=7)).date().isoformat()
    for dataset in ("TaiwanStockPrice", "TaiwanStockInstitutionalInvestorsBuySellWide"):
        params = urllib.parse.urlencode({
            "dataset": dataset, "data_id": "2313", "start_date": start,
            "end_date": now.date().isoformat()
        })
        data = request("https://api.finmindtrade.com/api/v4/data?" + params)
        rows = data.get("data") or []
        dates = sorted(set(str(row.get("date")) for row in rows))
        print("FINMIND", dataset, "status", data.get("status"), "msg",
              data.get("msg"), "rows", len(rows), "dates", dates[-5:],
              "latest_sample", json.dumps(rows[-1] if rows else None, ensure_ascii=False)[:2000])
        if data.get("status") != 200:
            raise ValueError("FinMind API status not 200: " + str(data.get("msg")))
        if not rows:
            raise ValueError("FinMind returned no rows for " + dataset)


if __name__ == "__main__":
    failed = False
    for label, fn in (("MCP", probe_mcp), ("FINMIND", probe_finmind)):
        try:
            fn()
            print(label + "_PROBE_PASS")
        except Exception as exc:
            failed = True
            print(label + "_PROBE_FAIL", type(exc).__name__, str(exc))
    if failed:
        raise SystemExit(1)
