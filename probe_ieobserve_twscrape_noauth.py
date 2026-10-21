#!/usr/bin/env python3
"""One-shot no-credential test of maintained twscrape (no login/session)."""
import asyncio
import json
import importlib.metadata
from datetime import datetime,timezone
from pathlib import Path

async def main():
 from twscrape import API
 result={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"package":"twscrape","version":importlib.metadata.version("twscrape"),"has_x_credentials":False,"attempts":[]}
 db=Path("/tmp/ieobserve_twscrape_noauth.sqlite")
 api=API(str(db))
 for kind in ("user_by_login","search"):
  row={"method":kind}
  try:
   if kind=="user_by_login":
    val=await asyncio.wait_for(api.user_by_login("IEObserve"),timeout=12)
    row["result"]={"username":getattr(val,"username",None),"id":getattr(val,"id",None)} if val else None
   else:
    items=[]
    async def read():
     async for tweet in api.search("from:IEObserve since:2026-10-20",limit=2):
      items.append({"id":tweet.id,"text":tweet.rawContent[:150]})
    await asyncio.wait_for(read(),timeout=12)
    row["posts"]=items
  except Exception as e:
   row["error_type"]=type(e).__name__
   row["error"]=str(e)[:350]
  result["attempts"].append(row)
 p=Path("out/kol/ieobserve-twscrape-noauth.json");p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":asyncio.run(main())
