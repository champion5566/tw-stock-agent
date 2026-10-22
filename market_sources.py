"""Shared public-data clients. Collectors orchestrate; this module only fetches."""
import json
import os
import urllib.parse
import urllib.request

UA = "tw-stock-agent/1.0 (GitHub Actions; market data research)"
MCP_URL = "https://twse-mcp.taux.io/mcp"
FINMIND_URL = "https://api.finmindtrade.com/api/v4/data"


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

