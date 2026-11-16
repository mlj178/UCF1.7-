
import json, urllib.request
d = json.load(urllib.request.urlopen("http://127.0.0.1:8765/api/maps"))
for s in d["snapshots"]:
    if s["file"].startswith("00_"):
        print("snapshot:", json.dumps({k: s.get(k) for k in ("file","level","label","nodes","edges","bytes","dir")}, ensure_ascii=False))
print("geo practice:", [g["level"] for g in d["geo"] if g["level"]=="practice"])
print("total snapshots:", len(d["snapshots"]))
