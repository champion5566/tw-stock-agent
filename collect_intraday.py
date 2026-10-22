"""One-shot, read-only intraday quote verification. Never places orders."""
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime

from quote_quality import TW, positive_price, quote_status, select_stock_quote
from shioaji_quotes import collect_quotes
from snapshot_io import write_snapshot
from instruments import STOCKS
SYMBOLS = {"tse_t00.tw": "TAIEX", "otc_o00.tw": "TPEX",
           **{f"{market}_{code}.tw": code for code, market in STOCKS.items()}}
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
              "status":quote_status(row.get("z"), stamp, now()),
              "is_live":quote_status(row.get("z"), stamp, now()) == "PASS",
              "data_kind":"quote_observation", "units":{"price":"TWD/share" if code not in ("t00", "o00") else "index_points"}}
    return output

def shioaji():
    return collect_quotes(tuple(STOCKS))


def main():
    result={"checked_at_taipei":now().isoformat(),"mode":"read_only_one_shot","quotes":{},"futures":{}}
    # Broker is requested first; MIS remains an independent observation/fallback.
    broker = shioaji()
    result["futures"]["TXFR1"] = broker
    try:
        observations = mis()
    except Exception as exc:
        observations = {}
        result["mis_error_type"] = type(exc).__name__
    result["quotes"] = dict(observations)
    broker_stocks = broker.get("stock_quotes", broker.get("stock_snapshots", {}))
    for code in STOCKS:
        result["quotes"][code] = select_stock_quote(broker_stocks.get(code), observations.get(code))
    for code in SYMBOLS.values():
        result["quotes"].setdefault(code, {"status": "MISSING", "price": None, "is_live": False})
    result["completed_at_taipei"]=now().isoformat()
    result["schema_version"] = "1.2"
    result["source_priority"] = ["Shioaji_tick", "Shioaji_snapshot", "TWSE_MIS"]
    write_snapshot(result, result["checked_at_taipei"][:10], "intraday")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
