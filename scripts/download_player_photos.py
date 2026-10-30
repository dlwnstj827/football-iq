#!/usr/bin/env python3
"""Download the 100-player roster from Wikimedia Commons, with attribution."""
import json, re, time, urllib.parse, urllib.request, io, pathlib, html
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"images"/"players"
OUT.mkdir(parents=True,exist_ok=True)
PLAYERS={
 "Lionel Messi": "messi.webp",
 "Cristiano Ronaldo": "cristiano-ronaldo.webp",
 "Kylian Mbappé": "mbappe.webp",
 "Erling Haaland": "haaland.webp",
 "Son Heung-min": "son-heung-min.webp",
 "Mohamed Salah": "salah.webp",
 "Harry Kane": "harry-kane.webp",
 "Jude Bellingham": "bellingham.webp",
 "Kevin De Bruyne": "de-bruyne.webp",
 "Zinedine Zidane": "zidane.webp",
 "Vinícius Júnior": "player-009.webp",
 "Ronaldinho": "player-012.webp",
 "Ronaldo (Brazilian footballer)": "player-013.webp",
 "David Beckham": "player-014.webp",
 "Andrea Pirlo": "player-015.webp",
 "Kaká": "player-016.webp",
 "Thierry Henry": "player-017.webp",
 "Steven Gerrard": "player-018.webp",
 "Frank Lampard": "player-019.webp",
 "Wayne Rooney": "player-020.webp",
 "Lamine Yamal": "player-021.webp",
 "Pedri": "player-022.webp",
 "Gavi (footballer)": "player-023.webp",
 "Raphinha": "player-024.webp",
 "Robert Lewandowski": "player-025.webp",
 "Bukayo Saka": "player-026.webp",
 "Declan Rice": "player-027.webp",
 "Martin Ødegaard": "player-028.webp",
 "Phil Foden": "player-029.webp",
 "Bernardo Silva": "player-030.webp",
 "Rodri (footballer, born 1996)": "player-031.webp",
 "Florian Wirtz": "player-032.webp",
 "Jamal Musiala": "player-033.webp",
 "Cole Palmer": "player-034.webp",
 "Viktor Gyökeres": "player-035.webp",
 "Lautaro Martínez": "player-036.webp",
 "Julián Álvarez (footballer)": "player-037.webp",
 "Federico Valverde": "player-038.webp",
 "Trent Alexander-Arnold": "player-039.webp",
 "Gianluigi Donnarumma": "player-040.webp",
 "Pelé": "player-041.webp",
 "Diego Maradona": "player-042.webp",
 "Johan Cruyff": "player-043.webp",
 "Franz Beckenbauer": "player-044.webp",
 "Paolo Maldini": "player-045.webp",
 "Andrés Iniesta": "player-046.webp",
 "Xavi": "player-047.webp",
 "Carles Puyol": "player-048.webp",
 "Sergio Agüero": "player-049.webp",
 "Zlatan Ibrahimović": "player-050.webp",
 "Luis Suárez (footballer, born 1987)": "player-051.webp",
 "Neymar": "player-052.webp",
 "Gareth Bale": "player-053.webp",
 "Luka Modrić": "player-054.webp",
 "Toni Kroos": "player-055.webp",
 "Iker Casillas": "player-056.webp",
 "Gianluigi Buffon": "player-057.webp",
 "Didier Drogba": "player-058.webp",
 "Samuel Eto'o": "player-059.webp",
 "Roberto Carlos (footballer)": "player-060.webp",
 "Achraf Hakimi": "player-061.webp",
 "Virgil van Dijk": "player-062.webp",
 "Alisson Becker": "player-063.webp",
 "Thibaut Courtois": "player-064.webp",
 "William Saliba": "player-065.webp",
 "Rúben Dias": "player-066.webp",
 "Nicolò Barella": "player-067.webp",
 "Enzo Fernández": "player-068.webp",
 "Alexis Mac Allister": "player-069.webp",
 "Victor Osimhen": "player-070.webp",
 "Ousmane Dembélé": "player-071.webp",
 "Bradley Barcola": "player-072.webp",
 "Désiré Doué": "player-073.webp",
 "Marquinhos": "player-074.webp",
 "Manuel Neuer": "player-075.webp",
 "Kim Min-jae": "player-076.webp",
 "Lee Kang-in": "player-077.webp",
 "Michel Platini": "player-078.webp",
 "Ruud Gullit": "player-079.webp",
 "Marco van Basten": "player-080.webp",
 "Alessandro Del Piero": "player-081.webp",
 "Francesco Totti": "player-082.webp",
 "Gabriel Batistuta": "player-083.webp",
 "Miroslav Klose": "player-084.webp",
 "Bastian Schweinsteiger": "player-085.webp",
 "Arjen Robben": "player-086.webp",
 "Franck Ribéry": "player-087.webp",
 "Eden Hazard": "player-088.webp",
 "Mesut Özil": "player-089.webp",
 "David Silva": "player-090.webp",
 "Yaya Touré": "player-091.webp",
 "Clarence Seedorf": "player-092.webp",
 "Nemanja Vidić": "player-093.webp",
 "Rio Ferdinand": "player-094.webp",
 "John Terry": "player-095.webp",
 "Ashley Cole": "player-096.webp",
 "Philipp Lahm": "player-097.webp",
 "Javier Mascherano": "player-098.webp",
 "Fernando Torres": "player-099.webp",
 "David Villa": "player-100.webp"
}
HEADERS={"User-Agent":"FootballIQ/1.0 (educational image attribution pilot; https://github.com/dlwnstj827/football-iq)"}
def api(base,params):
 url=base+"?"+urllib.parse.urlencode(params)
 req=urllib.request.Request(url,headers=HEADERS)
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def strip(value):return re.sub(r"<[^>]+>","",html.unescape(value or "")).strip()
credits_path=OUT/"credits.json"
credits=json.loads(credits_path.read_text(encoding="utf-8")) if credits_path.exists() else []
for title,filename in PLAYERS.items():
 if (OUT/filename).exists() and any(c.get("file")==filename for c in credits):
  print("EXISTS",title)
  continue
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
  credits=[c for c in credits if c.get("file")!=filename]
  credits.append({"player":title,"file":filename,"source":item.get("descriptionurl"),"author":get("Artist"),"license":license_name,"license_url":license_url,"modified":"Resized and converted to WebP"})
  print("SAVED",title,filename)
 except Exception as e:print("SKIPPED",title,str(e))
 time.sleep(1)
(ROOT/"images"/"players"/"credits.json").write_text(json.dumps(credits,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("TOTAL",len(credits))
