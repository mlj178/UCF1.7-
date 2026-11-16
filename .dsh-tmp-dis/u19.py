
import numpy as np, json
d = np.load(r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\\geo\\level10.npz", allow_pickle=True)
print(list(d.keys()))
for k in d.keys():
    a = d[k]
    print(k, getattr(a,'shape',None), getattr(a,'dtype',None))
