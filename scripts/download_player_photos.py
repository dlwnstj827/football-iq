#!/usr/bin/env python3
"""Download licensed roster photos from Wikimedia Commons, with attribution."""
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
 "David Villa": "player-100.webp",
 "Juan Musso": "player-101.webp",
 "Jan Oblak": "player-102.webp",
 "Marcos Llorente": "player-103.webp",
 "Dávid Hancko": "player-104.webp",
 "Cristian Romero (footballer, born 1998)": "player-105.webp",
 "Marc Pubill": "player-107.webp",
 "Johnny Cardoso": "player-108.webp",
 "Koke (footballer, born 1992)": "player-109.webp",
 "Álex Baena": "player-111.webp",
 "Giuliano Simeone": "player-113.webp",
 "Alejandro Grimaldo": "player-114.webp",
 "Morten Hjulmand": "player-115.webp",
 "Alexander Sørloth": "player-116.webp",
 "Jonathan David": "player-117.webp"
}
HEADERS={"User-Agent":"FootballIQ/1.0 (educational image attribution pilot; https://github.com/dlwnstj827/football-iq)"}
def api(base,params):
 url=base+"?"+urllib.parse.urlencode(params)
 req=urllib.request.Request(url,headers=HEADERS)
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def strip(value):return re.sub(r"<[^>]+>","",html.unescape(value or "")).strip()
# Alternative Wikimedia Commons search queries for players whose lead photo failed.
ALTERNATES={
 "Rodri (footballer, born 1996)":"Rodri Manchester City football",
 "Julián Álvarez (footballer)":"Julián Álvarez Argentina football",
 "Xavi":"Xavi Hernández Barcelona football",
 "Luis Suárez (footballer, born 1987)":"Luis Suárez Uruguay football",
 "Roberto Carlos (footballer)":"Roberto Carlos Brazil football",
 "Kim Min-jae":"Kim Min-jae Bayern football",
 "Michel Platini":"Michel Platini France football",
 "Diego Maradona":"Diego Maradona Argentina portrait",
 "Juan Musso": "Juan Musso football portrait",
 "Jan Oblak": "Jan Oblak football portrait",
 "Marcos Llorente": "Marcos Llorente football portrait",
 "Dávid Hancko": "David Hancko football portrait",
 "Cristian Romero (footballer, born 1998)": "Cristian Romero Argentina portrait",
 "Marc Pubill": "Marc Pubill football portrait",
 "Johnny Cardoso": "Johnny Cardoso football portrait",
 "Koke (footballer, born 1992)": "Koke Atletico Madrid football portrait",
 "Álex Baena": "Alex Baena football portrait",
 "Giuliano Simeone": "Giuliano Simeone football portrait",
 "Alejandro Grimaldo": "Alejandro Grimaldo Bayer Leverkusen",
 "Morten Hjulmand": "Morten Hjulmand Sporting Portugal",
 "Alexander Sørloth": "Alexander Sorloth football portrait",
 "Jonathan David": "Jonathan David football football portrait"
}
def photo_candidates(title,lead):
 if lead:yield lead
 if title not in ALTERNATES:return
 result=api("https://commons.wikimedia.org/w/api.php",{"action":"query","generator":"search","gsrsearch":"filetype:bitmap "+ALTERNATES[title],"gsrnamespace":6,"gsrlimit":30,"format":"json"})
 for entry in result.get("query",{}).get("pages",{}).values():
  name=entry.get("title","")
  if name.startswith("File:"):yield name[5:]

REPLACE_PHOTOS={
 "Diego Maradona":("maradona",),
 "Xavi":("xavi","hernandez","hernández"),
 "Roberto Carlos (footballer)":("roberto carlos","roberto_carlos","roberto-carlos"),
 "Kim Min-jae":("kim min","kim_min","kim-min","min-jae","min_jae","minjae"),
 "Michel Platini":("platini",),
 "Cristian Romero (footballer, born 1998)":("romero","cuti"),
 "Julián Álvarez (footballer)":("julian alvarez","julian_alvarez","julián álvarez"),
 "Alejandro Grimaldo":("grimaldo",),
 "Morten Hjulmand":("hjulmand",)
}
# Manually selected replacement candidates. Never silently reuse the rejected image.
PREFERRED_REPLACEMENTS={
 "Julián Álvarez (footballer)":["Julian Alvarez Argentina v Spain 19 July 2026-052 (cropped).jpg","Julian Alvarez Argentina v Spain 19 July 2026-173 (cropped).jpg"],
 "Alejandro Grimaldo":["Alex Grimaldo Argentina v Spain 19 July 2026-314 (face crop).jpg","Alex Grimaldo France v Spain 7.24.26-002.jpg"],
 "Morten Hjulmand":["Hjulmand.png","Milan Lecce 2023 Hjulmand 1.jpg"],
}
# The only categorized Commons image for Pablo Barrios is a group pre-match photo.
# Leave him unfilled until a licensed individual portrait is available.
credits_path=OUT/"credits.json"
credits=json.loads(credits_path.read_text(encoding="utf-8")) if credits_path.exists() else []
for title,filename in PLAYERS.items():
 if title not in REPLACE_PHOTOS and (OUT/filename).exists() and any(c.get("file")==filename for c in credits):
  print("EXISTS",title)
  continue
 try:
  page=api("https://en.wikipedia.org/w/api.php",{"action":"query","titles":title,"prop":"pageimages","format":"json","piprop":"name"})
  entry=next(iter(page["query"]["pages"].values()))
  image=entry.get("pageimage")
  saved=False
  for candidate in (PREFERRED_REPLACEMENTS[title] if title in PREFERRED_REPLACEMENTS else photo_candidates(title,None if title in REPLACE_PHOTOS else image)):
   try:
    info=api("https://commons.wikimedia.org/w/api.php",{"action":"query","titles":"File:"+candidate,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":"900","format":"json"})
    entry=next(iter(info["query"]["pages"].values()))
    if "imageinfo" not in entry:raise ValueError("Image not hosted on Commons")
    item=entry["imageinfo"][0];meta=item.get("extmetadata",{})
    get=lambda k:strip(meta.get(k,{}).get("value",""))
    license_name=get("LicenseShortName");license_url=get("LicenseUrl")
    if not (re.search(r"CC BY(?:-SA)?(?: [234]\.0|-[234]\.0| 4\.0|-4\.0)?",license_name,re.I) or "public domain" in license_name.lower() or license_name.upper() in ("CC0","CC ZERO")):
     raise ValueError("License not in allowed list: "+license_name)
    if title in REPLACE_PHOTOS and title not in PREFERRED_REPLACEMENTS:
     label=candidate.lower()
     required=REPLACE_PHOTOS[title]
     if not any(word in label for word in required):raise ValueError("Filename does not identify target player")
     if any(word in label for word in (" and "," vs "," versus "," with "," team "," group "," squad "," starting "," xi "," lineup "," haaland "," montes ")):
      raise ValueError("Possible multi-person image")
    source=item.get("thumburl") or item.get("url")
    req=urllib.request.Request(source,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=45) as r:raw=r.read()
    pic=Image.open(io.BytesIO(raw)).convert("RGB")
    if title in REPLACE_PHOTOS:
     import cv2, numpy as np
     rgb=np.array(pic)
     gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
     cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
     faces=cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=4,minSize=(35,35))
     if len(faces)!=1:raise ValueError("Portrait requires exactly one detectable face; found "+str(len(faces)))
     x,y,w,h=faces[0]
     if w < pic.width*0.075 or h < pic.height*0.075:raise ValueError("Face too small for guessing game")
     # Crop around the verified single face so the game shows a recognizable portrait.
     cx,cy=x+w/2,y+h/2
     crop_w=min(pic.width,max(w*3.2,240))
     crop_h=min(pic.height,max(h*4.0,320))
     left=max(0,min(pic.width-crop_w,cx-crop_w/2))
     top=max(0,min(pic.height-crop_h,cy-crop_h*0.36))
     pic=pic.crop((int(left),int(top),int(left+crop_w),int(top+crop_h)))
    pic.thumbnail((900,1000))
    pic.save(OUT/filename,"WEBP",quality=83,method=5)
    credits=[c for c in credits if c.get("file")!=filename]
    credits.append({"player":title,"file":filename,"source":item.get("descriptionurl"),"author":get("Artist"),"license":license_name,"license_url":license_url,"modified":"Single-face crop, resized and converted to WebP"})
    saved=True
    break
   except Exception as error:
    print("CANDIDATE FAILED",title,candidate,str(error))
  if not saved:raise ValueError("No verified single-face Commons photo found")
  print("SAVED",title,filename)
 except Exception as e:print("SKIPPED",title,str(e))
 time.sleep(1)
(ROOT/"images"/"players"/"credits.json").write_text(json.dumps(credits,ensure_ascii=False,indent=2)+chr(10),encoding="utf-8")
print("TOTAL",len(credits))
