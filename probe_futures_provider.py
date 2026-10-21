"""Probe documented FinMind futures tick overview without assuming access or freshness."""
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from collect_market import http_json, FINMIND_URL
from urllib.parse import urlencode

now=datetime.now(ZoneInfo("Asia/Taipei"))
out={"fetched_at_taipei":now.isoformat(),"dataset":"TaiwanFutOptTickInfo"}
try:
    obj=http_json(FINMIND_URL+"?"+urlencode({"dataset":"TaiwanFutOptTickInfo"}))
    rows=obj.get("data") or []
    out.update({"http_api_status":obj.get("status"),"message":obj.get("msg"),
                "count":len(rows),"sample":rows[:3],
                "field_names":list(rows[0]) if rows else []})
    print("FINMIND_FUTURES_STATUS",out["http_api_status"],"ROWS",out["count"])
    print("FINMIND_FUTURES_FIELDS",json.dumps(out["field_names"],ensure_ascii=False))
    print("FINMIND_FUTURES_SAMPLE",json.dumps(out["sample"],ensure_ascii=False)[:4000])
except Exception as e:
    out["error"]=type(e).__name__+": "+str(e)
    print("FINMIND_FUTURES_ERROR",out["error"])
from pathlib import Path
p=Path("out")/now.date().isoformat()/"futures-source-probe.json"
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(out,ensure_ascii=False,indent=2))
if out.get("http_api_status")!=200 or out.get("count",0)==0:
    raise SystemExit(1)
