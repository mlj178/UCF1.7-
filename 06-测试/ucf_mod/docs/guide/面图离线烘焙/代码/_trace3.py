
import glob, json, collections
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/_inbox/trace/level9_20261128-140400.jsonl")[0]
bots, kinds = {}, collections.Counter()
jumps = 0
for line in open(p, encoding="utf-8", errors="replace"):
    s = line.strip()
    if not s: continue
    try: j = json.loads(s)
    except: continue
    k = j.get("k") or j.get("ev") or ("end" if "end" in j else "?")
    kinds[k] += 1
    if k == "b": bots.setdefault(j["id"], []).append(j)
    if k == "jump": jumps += 1
print("kinds", dict(kinds))
print("jump events", jumps)
stats = []
for b, rs in bots.items():
    xs = [r["x"] for r in rs]; ys = [r["y"] for r in rs]; zs = [r["z"] for r in rs]
    dist = max(max(xs)-min(xs), max(zs)-min(zs))
    dy = max(ys) - min(ys)
    stats.append((b, dist, dy, min(ys), max(ys)))
stats.sort(key=lambda x: x[1])
print("%-10s %8s %8s %8s %8s" % ("bot", "move", "dy", "ymin", "ymax"))
for s in stats[:6] + stats[-3:]:
    print("%-10s %8.2f %8.2f %8.2f %8.2f" % s)
