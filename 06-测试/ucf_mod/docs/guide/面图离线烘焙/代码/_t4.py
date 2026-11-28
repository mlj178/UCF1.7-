
import glob, json, collections
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/_inbox/trace/level9_20261128-141525.jsonl")[0]
bots = {}; n = 0
for line in open(p, encoding="utf-8", errors="replace"):
    s = line.strip()
    if not s: continue
    try: j = json.loads(s)
    except: continue
    n += 1
    if j.get("k") == "b": bots.setdefault(j["id"], []).append(j)
moved = 0
near0 = 0
for b, rs in bots.items():
    xs=[r["x"] for r in rs]; zs=[r["z"] for r in rs]
    if max(max(xs)-min(xs), max(zs)-min(zs)) > 0.5: moved += 1
    if rs[0].get("near") in ("00000000", None, ""): near0 += 1
print("lines", n, "bots", len(bots), "moved", moved, "near0", near0)
r0 = list(bots.values())[0][0]
print("sample", {k: r0.get(k) for k in ("id","x","y","z","spd","near","tgt","act")})
