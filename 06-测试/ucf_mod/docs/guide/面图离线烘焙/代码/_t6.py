
import glob, json, collections
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/_inbox/trace/level9_20261128-150931.jsonl")[0]
bots = {}; jumps = 0
for line in open(p, encoding="utf-8", errors="replace"):
    s=line.strip()
    if not s: continue
    try: j=json.loads(s)
    except: continue
    if j.get("k")=="b": bots.setdefault(j["id"],[]).append(j)
    if j.get("ev")=="jump": jumps+=1
rows=[]
for b,rs in bots.items():
    xs=[r["x"] for r in rs]; zs=[r["z"] for r in rs]
    d=max(max(xs)-min(xs), max(zs)-min(zs))
    rows.append((b,d,rs[0]["x"],rs[0]["y"],rs[0]["z"]))
rows.sort(key=lambda r:r[1])
print("bots",len(rows),"jumps",jumps,"stuck(<0.5m)",sum(1 for r in rows if r[1]<=0.5),"moved>5m",sum(1 for r in rows if r[1]>5))
for r in rows[:8]: print("  %-10s %6.2f  (%.1f, %.1f, %.1f)"%r)
