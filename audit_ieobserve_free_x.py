#!/usr/bin/env python3
"""Zero-cost public X syndication audit. No API key, login, cookies or proxy."""
import json
from datetime import datetime,timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

POSTS={
"PHP": "2112939723467681940",
"KenGriffinReply":"2112835917060927731",
"KenGriffin":"2112834883571822880",
"Netflix":"2112799667838992889",
"SpaceXReply":"2112678564197957984",
"SpaceX":"2112678369695605027",
}
HOST="https://cdn.syndication.twimg.com/tweet-result"
def check(s,name,url):
 r={"name":name,"url":url}
 try:
  res=s.get(url,timeout=15,headers={"User-Agent":"Mozilla/5.0 (compatible; IEObserveSourceAudit/1.0)","Accept":"application/json,text/html;q=0.9,*/*;q=0.8"})
  r.update({"http":res.status_code,"bytes":len(res.content),"content_type":res.headers.get("Content-Type",""),"preview":res.text[:160]})
  try:
   data=res.json()
   if isinstance(data,dict):
    r.update({"id":str(data.get("id_str") or data.get("id") or ""),"text_chars":len(str(data.get("text") or data.get("full_text") or "")),"text_excerpt":str(data.get("text") or data.get("full_text") or "")[:160],"created_at":data.get("created_at"),"user_screen_name":(data.get("user") or {}).get("screen_name") if isinstance(data.get("user"),dict) else None,"keys":list(data.keys())[:20]})
  except ValueError:
   soup=BeautifulSoup(res.text,"html.parser")
   for tag in soup(["script","style","noscript"]):tag.decompose()
   r["visible_text"]=soup.get_text(" ",strip=True)[:180]
 except Exception as e:r["error"]=f"{type(e).__name__}: {str(e)[:160]}"
 return r

def main():
 with requests.Session() as s:
  results=[]
  for topic,pid in POSTS.items():
   results.append(check(s,"syndication_tweet_"+topic,f"{HOST}?id={pid}&lang=zh"))
  results.append(check(s,"syndication_timeline","https://syndication.twitter.com/srv/timeline-profile/screen-name/IEObserve"))
  results.append(check(s,"publish_oembed","https://publish.twitter.com/oembed?url=https%3A%2F%2Fx.com%2FIEObserve%2Fstatus%2F2112799667838992889&omit_script=true"))
  results.append(check(s,"syndication_embed","https://platform.twitter.com/embed/Tweet.html?id=2112799667838992889"))
 report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"results":results,"notes":"No auth; public-only. Single tweet retrieval is not evidence of complete 48h timeline."}
 p=Path("out/kol/ieobserve-free-x-audit.json");p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
