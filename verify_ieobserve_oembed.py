#!/usr/bin/env python3
"""Verify Grok's six IEObserve tweet IDs using free public X oEmbed."""
import json
from datetime import datetime,timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup
POSTS={"PHP":"2112939723467681940","KenGriffinReply":"2112835917060927731","KenGriffin":"2112834883571822880","Netflix":"2112799667838992889","SpaceXReply":"2112678564197957984","SpaceX":"2112678369695605027"}
EXPECTED={"PHP":["php","漏洞"],"KenGriffinReply":["amazon","泡沫"],"KenGriffin":["gpu","griffin"],"Netflix":["netflix","q3"],"SpaceXReply":["財報","電話"],"SpaceX":["spacex","q3"]}
def main():
 out=[]
 with requests.Session() as s:
  for topic,pid in POSTS.items():
   url="https://publish.twitter.com/oembed"
   row={"topic":topic,"id":pid,"snowflake_utc":datetime.fromtimestamp(((int(pid)>>22)+1288834974657)/1000,timezone.utc).isoformat()}
   try:
    r=s.get(url,params={"url":f"https://x.com/IEObserve/status/{pid}","omit_script":"true"},timeout=20)
    row["http"]=r.status_code
    if r.ok:
     d=r.json();soup=BeautifulSoup(d.get("html",""),"html.parser")
     text=soup.get_text(" ",strip=True)
     row.update({"author":d.get("author_name"),"author_url":d.get("author_url"),"post_url":d.get("url"),"embed_text":text[:1500],"embed_chars":len(text),"expected_terms_found":{k:k in text.lower() for k in EXPECTED[topic]}})
    else:row["error_excerpt"]=r.text[:160]
   except Exception as e:row["error"]=str(e)[:200]
   out.append(row)
 report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"results":out,"caveat":"oEmbed validates accessible post links and extracts embed excerpts, not complete timeline or necessarily full text."}
 p=Path("out/kol/ieobserve-oembed-verification.json");p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
