
import glob, json
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/_inbox/trace/level9_20261128-140400.jsonl")[0]
bots = {}
for line in open(p, encoding="utf-8", errors="replace"):
    s = line.strip()
    if not s: continue
    try: j = json.loads(s)
    except: continue
    if j.get("k") == "b": bots.setdefault(j["id"], []).append(j)
for b, rs in bots.items():
    xs=[r["x"] for r in rs]; zs=[r["z"] for r in rs]
    if max(max(xs)-min(xs), max(zs)-min(zs)) <= 0.5:
        r0=rs[0]
        print(b, "pos", round(r0["x"],1), round(r0["y"],2), round(r0["z"],1), "near", r0.get("near"), "tgt", r0.get("tgt"))
