#!/usr/bin/env python3
"""Download a 10-player pilot from Wikimedia Commons, with attribution."""
import json, re, time, urllib.parse, urllib.request, io, pathlib, html
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"images"/"players"
OUT.mkdir(parents=True,exist_ok=True)
PLAYERS={
"Lionel Messi":"messi.webp","Cristiano Ronaldo":"cristiano-ronaldo.webp",
"Kylian Mbappé":"mbappe.webp","Erling Haaland":"haaland.webp",
"Son Heung-min":"son-heung-min.webp","Mohamed Salah":"salah.webp",
"Harry Kane":"harry-kane.webp","Jude Bellingham":"bellingham.webp",
"Kevin De Bruyne":"de-bruyne.webp","Zinedine Zidane":"zidane.webp"}
HEADERS={"User-Agent":"FootballIQ/1.0 (educational image attribution pilot; https://github.com/dlwnstj827/football-iq)"}
def api(base,params):
 url=base+"?"+urllib.parse.urlencode(params)
 req=urllib.request.Request(url,headers=HEADERS)
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def strip(value):return re.sub(r"<[^>]+>","",html.unescape(value or "")).strip()
credits=[]
for title,filename in PLAYERS.items():
 try:
  page=api("https://en.wikipedia.org/w/api.php",{"action":"query","titles":title,"prop":"pageimages","format":"json","piprop":"name"})
  entry=next(iter(page["query"]["pages"].values()))
  image=entry.get("pageimage")
  if not image:raise ValueError("No lead image")
  info=api("https://commons.wikimedia.org/w/api.php",{"action":"query","titles":"File:"+image,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":"900","format":"json"})
  entry=next(iter(info["query"]["pages"].values()))
  if "imageinfo" not in entry:raise ValueError("Image not hosted on Commons")
  item=entry["imageinfo"][0];meta=item.get("extmetadata",{})
  get=lambda k:strip(meta.get(k,{}).get("value",""))
  license_name=get("LicenseShortName");license_url=get("LicenseUrl")
  if not (re.search(r"CC BY(?:-SA)?(?: [234]\.0|-[234]\.0| 4\.0|-4\.0)?",license_name,re.I) or "public domain" in license_name.lower() or license_name.upper() in ("CC0","CC ZERO")):
   raise ValueError("License not in allowed list: "+license_name)
  source=item.get("thumburl") or item.get("url")
  req=urllib.request.Request(source,headers=HEADERS)
  with urllib.request.urlopen(req,timeout=45) as r:raw=r.read()
  pic=Image.open(io.BytesIO(raw)).convert("RGB")
  pic.thumbnail((900,1000))
  pic.save(OUT/filename,"WEBP",quality=83,method=5)
  credits.append({"player":title,"file":filename,"source":item.get("descriptionurl"),"author":get("Artist"),"license":license_name,"license_url":license_url,"modified":"Resized and converted to WebP"})
  print("SAVED",title,filename)
 except Exception as e:print("SKIPPED",title,str(e))
 time.sleep(1)
(ROOT/"images"/"players"/"credits.json").write_text(json.dumps(credits,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("TOTAL",len(credits))
