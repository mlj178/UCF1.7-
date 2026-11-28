
import glob, json, collections
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/_inbox/trace/level9_20261128-145118.jsonl")[0]
bots = {}; jumps = 0; kinds = collections.Counter()
for line in open(p, encoding="utf-8", errors="replace"):
    s = line.strip()
    if not s: continue
    try: j = json.loads(s)
    except: continue
    k = j.get("k") or j.get("ev") or ("end" if "end" in j else "?")
    kinds[k] += 1
    if k == "b": bots.setdefault(j["id"], []).append(j)
    if k == "jump": jumps += 1
print("kinds", dict(kinds), "jumps", jumps)
rows = []
for b, rs in bots.items():
    xs=[r["x"] for r in rs]; zs=[r["z"] for r in rs]
    d = max(max(xs)-min(xs), max(zs)-min(zs))
    r0 = rs[0]
    rows.append((b, d, r0["x"], r0["y"], r0["z"], r0.get("near"), r0.get("spd")))
rows.sort(key=lambda r: r[1])
print("bots", len(rows))
print("%-10s %7s %8s %7s %8s %10s %6s" % ("bot","move","x","y","z","near","spd"))
for r in rows[:12]:
    print("%-10s %7.2f %8.1f %7.2f %8.1f %10s %6s" % r)
print("stuck(<0.5m):", sum(1 for r in rows if r[1] <= 0.5), "| moved>5m:", sum(1 for r in rows if r[1] > 5))
