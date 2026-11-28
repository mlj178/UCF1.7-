
import glob, json, math, collections
import numpy as np

p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/_inbox/trace/level9_20261128-140400.jsonl")[0]
bots = {}
for line in open(p, encoding="utf-8", errors="replace"):
    line = line.strip()
    if not line: continue
    try: j = json.loads(line)
    except: continue
    if j.get("k") == "b":
        bots.setdefault(j["id"], []).append(j)
print("bots", len(bots))
moved = tgt = 0
near0 = 0
for b, rows in bots.items():
    xs = [r["x"] for r in rows]; zs = [r["z"] for r in rows]
    if max(max(xs)-min(xs), max(zs)-min(zs)) > 0.5: moved += 1
    if any(abs(r.get("tgt",[0,0,0])[0]) + abs(r.get("tgt",[0,0,0])[2]) > 0.01 for r in rows): tgt += 1
    if rows[0].get("near") in ("00000000", "", None): near0 += 1
print("moved>0.5m", moved, "| with tgt", tgt, "| near=0 at first sample", near0)

# nearest node distance for idle bots
mp = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*/n0-*.txt")[0]
mp = [f for f in mp if not f.endswith(("196","2030","2115","20261127-194925"))][0]
nodes = []
for line in open(mp, encoding="utf-8", errors="replace"):
    s = line.strip()
    if s.startswith("node add "):
        v = [float(x) for x in s.split()[2:5]]
        nodes.append(v)
N = np.array(nodes)
print("graph nodes", len(N))
rows = []
for b, ss in bots.items():
    r0 = ss[0]
    xs = [r["x"] for r in ss]; zs = [r["z"] for r in ss]
    moved_d = max(max(xs)-min(xs), max(zs)-min(zs))
    P = np.array([r0["x"], r0["y"], r0["z"]])
    d = np.linalg.norm(N - P, axis=1)
    dxz = np.linalg.norm(N[:, [0,2]] - P[[0,2]], axis=1)
    rows.append((b, moved_d, d.min(), dxz.min(), r0.get("near")))
idle = [r for r in rows if r[1] <= 0.5]
print("idle bots", len(idle))
print("%-10s %8s %8s %8s %10s" % ("bot", "moved", "d3d", "dxz", "near"))
for r in sorted(idle, key=lambda x: x[2])[:15]:
    print("%-10s %8.2f %8.2f %8.2f %10s" % (r[0], r[1], r[2], r[3], r[4]))
