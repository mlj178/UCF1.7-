
import glob, re, collections
cands = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*/*.bak-route196")
print("cands", cands)
if cands:
    ys = []
    for line in open(cands[0], encoding="utf-8", errors="replace"):
        m = re.match(r"node add ([-\d.]+) ([-\d.]+) ([-\d.]+)", line.strip())
        if m: ys.append(float(m.group(2)))
    print("n", len(ys))
    if ys:
        c = collections.Counter(int(round(y)) for y in ys)
        for k in sorted(c): print("  y~%4d : %d" % (k, c[k]))
