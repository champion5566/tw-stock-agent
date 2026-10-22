"""One-shot, read-only intraday quote verification. Never places orders."""
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime

from quote_quality import TW, positive_price, quote_status, select_stock_quote
from shioaji_quotes import collect_quotes
from snapshot_io import write_snapshot
SYMBOLS = {"tse_t00.tw": "TAIEX", "tse_2330.tw": "2330", "tse_0050.tw": "0050",
           "otc_o00.tw": "TPEX"}
def now(): return datetime.now(TW)
def number(v):
    return positive_price(v)

def fresh(ts):
    return quote_status(1, ts, now()) == "PASS"

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
              "status":quote_status(row.get("z"), stamp, now())}
    return output

def shioaji():
    return collect_quotes(("2330", "0050"))


def main():
    result={"checked_at_taipei":now().isoformat(),"mode":"read_only_one_shot","quotes":{},"futures":{}}
    try: result["quotes"]=mis()
    except Exception as e: result["mis_error_type"]=type(e).__name__
    result["futures"]["TXFR1"]=shioaji()
    for code, q in result["futures"]["TXFR1"].get("stock_snapshots", {}).items():
        if code in ("2330", "0050") and q.get("status") == "PASS":
            current = result["quotes"].get(code)
            if current is None or current.get("status") != "PASS":
                result["quotes"][code] = select_stock_quote(current, q)
    for code in SYMBOLS.values():
        result["quotes"].setdefault(code, {"status": "MISSING", "price": None, "is_live": False})
    result["completed_at_taipei"]=now().isoformat()
    result["schema_version"] = "1.1"
    write_snapshot(result, result["checked_at_taipei"][:10], "intraday")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
