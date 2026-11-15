
from PIL import Image
import numpy as np
im = Image.open(r"C:\Users\17242\.dsh\attachments\v1\objects\08\088af5ea1b130eaa39769c33950354f9992d4d7710ba0050f4e058785e5d1a46").convert("RGB")
a = np.asarray(im).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
mask = (B>140)&(B-R>70)&(B-G>30)&(R<130)
print("blue px", int(mask.sum()))
vis = a.copy()
vis[mask] = [255,0,0]
Image.fromarray(vis.astype("uint8")).save(r"D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\screenshots\bluemask.png")
# also crop same region with mask
Image.fromarray(vis[300:800,200:900].astype("uint8")).resize((1400,1000), Image.NEAREST).save(r"D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\screenshots\bluemask_crop.png")
