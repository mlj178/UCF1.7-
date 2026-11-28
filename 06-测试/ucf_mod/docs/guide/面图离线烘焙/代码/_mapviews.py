
import glob, struct
import numpy as np
from PIL import Image, ImageDraw

# 地图几何
z = np.load(glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/nano30_storm.npz")[0], allow_pickle=True)
V, F = z["v"].astype(np.float64), z["f"].astype(np.int64)
tri = V[F]
xmin, zmin = V[:,0].min(), V[:,2].min()
xmax, zmax = V[:,0].max(), V[:,2].max()
cs = 1.0
W = int((xmax-xmin)/cs)+1; H = int((zmax-zmin)/cs)+1
low = np.full((H,W), 1e9); high = np.full((H,W), -1e9)
for t in tri:
    i0=int((t[:,0].min()-xmin)/cs); i1=int((t[:,0].max()-xmin)/cs)
    j0=int((t[:,2].min()-zmin)/cs); j1=int((t[:,2].max()-zmin)/cs)
    for j in range(j0,j1+1):
        for i in range(i0,i1+1):
            if 0<=j<H and 0<=i<W:
                ys=t[:,1]
                low[j,i]=min(low[j,i], ys.min()); high[j,i]=max(high[j,i], ys.max())
valid = low < 1e8
lo = np.where(valid, low, np.nan); hi = np.where(valid, high, np.nan)
print("map bbox %.0f..%.0f x %.0f..%.0f, cells %d" % (xmin,xmax,zmin,zmax,valid.sum()))

def to_img(arr, name, vmin, vmax, cmap):
    a = np.nan_to_num(arr, nan=np.nan)
    t = np.clip((a - vmin)/(vmax-vmin+1e-9), 0, 1)
    img = (cmap(t)*255).astype(np.uint8)
    img[~valid] = 0
    Image.fromarray(np.flipud(img)).resize((W*2,H*2), Image.NEAREST).save(name)

def viridis(t):
    r = np.clip(0.27 + 0.6*t, 0, 1); g = np.clip(0.0 + 0.9*t, 0, 1); b = np.clip(0.33 + 0.4*(1-t), 0, 1)
    return np.stack([r,g,b], axis=-1)
def inferno(t):
    r = np.clip(0.0 + 1.0*t, 0, 1); g = np.clip(0.0 + 0.85*(t**2), 0, 1); b = np.clip(0.2*(1-t), 0, 1)
    return np.stack([r,g,b], axis=-1)
to_img(low, r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/map_low.png", float(np.nanmin(lo)), float(np.nanmax(lo)), viridis)
to_img(high, r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/map_high.png", float(np.nanmin(hi)), float(np.nanmax(hi)), inferno)
print("saved map_low.png / map_high.png")

# 地面（<=4m）覆盖率
ground = valid & (low <= 4.0)
img = np.zeros((H,W,3), np.uint8)
img[valid] = (60,60,60)
img[ground] = (60,180,90)
Image.fromarray(np.flipud(img)).resize((W*2,H*2), Image.NEAREST).save(r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/map_ground.png")
print("ground cells", int(ground.sum()), "=", int(ground.sum()*cs*cs), "m2")
