#!/usr/bin/env python3
"""Automated screening only: face detection is not a substitute for visual review."""
import json,pathlib,cv2
root=pathlib.Path(__file__).resolve().parents[1]/"images"/"players"
credits=json.loads((root/"credits.json").read_text(encoding="utf-8"))
detector=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
results=[]
for entry in credits:
 path=root/entry["file"]
 img=cv2.imread(str(path))
 if img is None:
  results.append({"player":entry["player"],"faces":None,"status":"missing_or_unreadable"})
  continue
 gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 faces=detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=4,minSize=(35,35))
 count=len(faces)
 results.append({"player":entry["player"],"faces":count,"status":"review" if count!=1 else "one_face_detected"})
report={"method":"OpenCV Haar frontal face detection; false positives and missed profiles possible; manual visual verification still required","total":len(results),"flagged":[x for x in results if x["status"]!="one_face_detected"],"results":results}
(root/"photo-audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PHOTO AUDIT:",len(results),"photos,",len(report["flagged"]),"need manual review")
for x in report["flagged"]:print("REVIEW",x)
