"""One-shot, read-only intraday quote verification. Never places orders."""
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TW = ZoneInfo("Asia/Taipei")
SYMBOLS = {"tse_t00.tw": "TAIEX", "tse_2330.tw": "2330", "tse_0050.tw": "0050",
           "otc_o00.tw": "TPEX"}
def now(): return datetime.now(TW)
def number(v):
    try:
        x = float(v)
        return x if x > 0 else None
    except (ValueError, TypeError): return None

def fresh(ts):
    if not ts: return False
    if ts.tzinfo is None: ts = ts.replace(tzinfo=TW)
    age = (now() - ts.astimezone(TW)).total_seconds() / 60
    return ts.astimezone(TW).date() == now().date() and -2 <= age <= 10

def mis():
    params = urllib.parse.urlencode({"ex_ch": "|".join(SYMBOLS), "json": "1", "delay": "0",
                                      "_": str(int(time.time()*1000))})
    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?" + params
    req = urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Referer":"https://mis.twse.com.tw/","Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=20) as response:
        rows = json.load(response).get("msgArray", [])
    output = {}
    for row in rows:
        ex = row.get("ex"); code = row.get("c")
        key = ("otc" if ex == "otc" else "tse") + "_" + str(code) + ".tw"
        if key not in SYMBOLS: continue
        stamp = None
        try: stamp = datetime.strptime(str(row["d"])+" "+str(row["t"]), "%Y%m%d %H:%M:%S").replace(tzinfo=TW)
        except (KeyError,ValueError,TypeError): pass
        output[SYMBOLS[key]] = {"source":"TWSE_MIS","price":number(row.get("z")), "raw_last_trade":row.get("z"), "raw_previous_trade":row.get("pz"),
              "open":number(row.get("o")),"high":number(row.get("h")),"low":number(row.get("l")),
              "previous_close":number(row.get("y")),"volume_raw":row.get("v"),
              "trade_time":stamp.isoformat() if stamp else None,
              "status":"PASS" if number(row.get("z")) and fresh(stamp) else "STALE_OR_NO_TRADE"}
    return output

def shioaji():
    output = {"status":"NOT_CONFIGURED","source":"Shioaji","is_live":False}
    if not os.getenv("SHIOAJI_API_KEY") or not os.getenv("SHIOAJI_SECRET_KEY"): return output
    api = None
    try:
        import shioaji as sj
        api = sj.Shioaji(simulation=False)
        api.login(api_key=os.environ["SHIOAJI_API_KEY"],secret_key=os.environ["SHIOAJI_SECRET_KEY"])
        contract = api.Contracts.Futures.TXF.TXFR1
        stock_results = {}
        try:
            contracts = [api.Contracts.Stocks["2330"], api.Contracts.Stocks["0050"]]
            for snap in api.snapshots(contracts):
                code = str(getattr(snap, "code", ""))
                stamp = getattr(snap, "ts", None)
                dt = datetime.fromtimestamp(stamp / 1e9, TW) if isinstance(stamp, (int, float)) and stamp > 1e12 else (datetime.fromtimestamp(stamp, TW) if isinstance(stamp, (int, float)) and stamp > 0 else None)
                price = number(getattr(snap, "close", None))
                stock_results[code] = {"source":"Shioaji_snapshot","price":price,"trade_time":dt.isoformat() if dt else None,"status":"PASS" if price and fresh(dt) else "STALE_OR_NO_TRADE"}
        except Exception as e:
            stock_results["error_type"] = type(e).__name__
        output["stock_snapshots"] = stock_results
        ticks = []
        def callback(exchange,tick):
            try:
                price = number(getattr(tick,"close",None))
                ts = datetime.fromisoformat(str(getattr(tick,"datetime","")))
                if price: ticks.append((price,ts,str(getattr(tick,"volume",""))))
            except (TypeError,ValueError): pass
        api.quote.set_on_tick_fop_v1_callback(callback)
        api.quote.subscribe(contract,quote_type=sj.constant.QuoteType.Tick,version=sj.constant.QuoteVersion.v1)
        time.sleep(25)
        if ticks:
            price,ts,volume=ticks[-1]
            output.update({"price":price,"trade_time":ts.isoformat(),"volume":volume,
                           "ticks_observed":len(ticks),"status":"PASS" if fresh(ts) else "STALE",
                           "is_live":fresh(ts),"contract_code":str(contract.code)})
        else: output["status"]="NO_TICKS_IN_WINDOW"
        try: api.quote.unsubscribe(contract,quote_type=sj.constant.QuoteType.Tick,version=sj.constant.QuoteVersion.v1)
        except Exception: pass
    except Exception as e:
        output.update({"status":"ERROR","error_type":type(e).__name__})
    finally:
        if api:
            try: api.logout()
            except Exception: pass
    return output

def main():
    result={"checked_at_taipei":now().isoformat(),"mode":"read_only_one_shot","quotes":{},"futures":{}}
    try: result["quotes"]=mis()
    except Exception as e: result["mis_error_type"]=type(e).__name__
    result["futures"]["TXFR1"]=shioaji()
    for code, q in result["futures"]["TXFR1"].get("stock_snapshots", {}).items():
        if code in ("2330", "0050") and q.get("status") == "PASS":
            current = result["quotes"].get(code)
            if current is None or current.get("status") != "PASS":
                result["quotes"][code] = {**(current or {}), "mis_diagnostic":current, **q}
    result["completed_at_taipei"]=now().isoformat()
    path=Path("out")/now().date().isoformat()/"intraday.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
