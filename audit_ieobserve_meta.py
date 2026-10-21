#!/usr/bin/env python3
"""Check IEObserve Facebook/Instagram public page availability and screenshot topics."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

URLS = {
 "facebook_www": "https://www.facebook.com/intleconobserve",
 "facebook_posts": "https://www.facebook.com/intleconobserve/posts",
 "facebook_mobile": "https://m.facebook.com/intleconobserve",
 "facebook_mbasic": "https://mbasic.facebook.com/intleconobserve",
 "facebook_public_plugins": "https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fintleconobserve&tabs=timeline&width=500&height=800",
 "instagram_www": "https://www.instagram.com/ieobserve/",
 "instagram_reels": "https://www.instagram.com/ieobserve/reels/",
 "instagram_embed": "https://www.instagram.com/ieobserve/?__a=1&__d=dis",
 "official_wordpress_feed": "https://ieobserve.com/feed/",
 "official_wordpress_api": "https://ieobserve.com/wp-json/wp/v2/posts?per_page=5",
}
TOPICS = {
 "SpaceX_Q3": ["spacex", "spcx"],
 "Netflix_Q3": ["netflix", "廣告收入下修"],
 "Ken_Griffin_GPU": ["ken griffin", "gpu過剩", "citadel"],
 "PHP_AI_Japan": ["php漏洞", "cloudflare", "高市早苗"],
}
def check(s, name, url):
 out={"source":name,"url":url}
 try:
  r=s.get(url,timeout=20,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36","Accept-Language":"zh-TW,zh;q=0.9,en;q=0.8"})
  soup=BeautifulSoup(r.text,"html.parser")
  for el in soup(["script","style","noscript"]):el.decompose()
  txt=" ".join(soup.stripped_strings)
  low=txt.lower().replace(" ","")
  out.update({"status":r.status_code,"final_host":urlparse(r.url).hostname,"bytes":len(r.content),"visible_chars":len(txt),"title":soup.title.get_text(" ",strip=True)[:130] if soup.title else None,"topics":{k:any(t.replace(" ","") in low for t in terms) for k,terms in TOPICS.items()},"challenge":any(t in low for t in ["justamoment","checkingyourbrowser","verifyyouarehuman"]),"login_wall":any(t in low for t in ["logintofacebook","登入facebook","logininstagram","loginto instagram"]),"post_links":len(set(re.findall(r'(?:https?:)?//(?:www\\.)?(?:facebook\\.com|instagram\\.com)/[^"\\s<>]{1,160}',r.text)))})
 except Exception as e:out["error"]=str(e)[:200]
 return out

def main():
 with requests.Session() as s:results=[check(s,n,u) for n,u in URLS.items()]
 result={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"results":results,"caveat":"HTTP 200 does not prove accessible recent post content. Topic matching only checks visible public HTML. Do not infer absence of a post from no match."}
 p=Path("out/kol/ieobserve-meta-audit.json");p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
