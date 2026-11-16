
import base64, io, zipfile, json, os
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
for lvl in ["level1","level2","level3","level4","level5","level6","level7","level8","level9","level10","level11"]:
    data = open(os.path.join(base,lvl),"rb").read()
    i = data.find(b"UEsDBBQ")
    if i < 0: print(lvl,"no blob"); continue
    e = i
    while e < len(data) and (data[e:e+1].isalnum() or data[e:e+1] in b"+/="): e += 1
    raw = base64.b64decode(data[i:e] + b"="*((4-len(data[i:e])%4)%4))
    z = zipfile.ZipFile(io.BytesIO(raw))
    meta = json.loads(z.read("meta.json"))
    info = []
    for n in z.namelist():
        if n.startswith("graph"):
            g = json.loads(z.read(n))
            info.append((n, meta["typeNames"][int(n[5])], g.get("searchTag"), g.get("root"), g.get("maxDistance"), g.get("raycast")))
    print(lvl, meta["version"], info)
