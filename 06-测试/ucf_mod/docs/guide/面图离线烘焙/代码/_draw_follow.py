import numpy as np
from PIL import Image

NEW = 'D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/log/ground_samples_10_Nano30_Storm飓风危城.txt'
OLD = 'D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/ground_low.txt'
OUT = 'D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/follow_storm_map.png'

def load(p):
    out = []
    for ln in open(p, encoding='utf-8', errors='replace'):
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        a = s.split()
        if len(a) < 3:
            continue
        out.append((float(a[0]), float(a[1]), float(a[2])))
    return out

new = load(NEW)
old = load(OLD)
xs = [q[0] for q in new] + [q[0] for q in old]
zs = [q[1] for q in new] + [q[1] for q in old]
x0, x1 = min(xs) - 2, max(xs) + 2
z0, z1 = min(zs) - 2, max(zs) + 2
S = 6.0
W = int((x1 - x0) * S); H = int((z1 - z0) * S)
img = np.zeros((H, W, 3), dtype=np.uint8)
for q in old:
    px = int((q[0] - x0) * S); pz = int((q[1] - z0) * S)
    if 0 <= px < W - 2 and 0 <= pz < H - 2:
        img[pz:pz+2, px:px+2] = (80, 80, 80)
def col(y):
    t = max(0.0, min(1.0, (y + 1.0) / 16.0))
    r = max(0.0, min(1.0, 1.6 - abs(4*t - 2.0)))
    g = max(0.0, min(1.0, 1.6 - abs(4*t - 1.0)))
    b = max(0.0, min(1.0, 1.6 - abs(4*t - 3.0)))
    return (int(r*255), int(g*255), int(b*255))
h = max(2, int(S * 1.0))
for x, z, y in new:
    px = int((x - x0) * S); pz = int((z - z0) * S)
    img[pz:pz+h, px:px+h] = col(y)
Image.fromarray(img).save(OUT)
print('saved', OUT, img.shape)