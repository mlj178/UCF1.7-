
import base64, io, zipfile, json, os, sys
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
for lvl in ["level1","level2","level3","level4","level5","level6","level7","level8","level9","level10","level11"]:
    try:
        data = open(os.path.join(base,lvl),"rb").read()
        i = data.find(b"UEsDBBQ")
        e = i
        while e < len(data) and (data[e:e+1].isalnum() or data[e:e+1] in b"+/="): e += 1
        b64 = data[i:e]
        raw = base64.b64decode(b64 + b"="*((4-len(b64)%4)%4))
        z = zipfile.ZipFile(io.BytesIO(raw))
        meta = json.loads(z.read("meta.json"))
        info = []
        for n in z.namelist():
            if not n.startswith("graph"): continue
            g = json.loads(z.read(n))
            info.append((n, meta["typeNames"][int(n[5])].split(".")[-1], g.get("searchTag"), g.get("root"), g.get("maxDistance"), g.get("raycast")))
        print(lvl, meta.get("version"), info, flush=True)
    except Exception as ex:
        print(lvl, "FAIL", type(ex).__name__, str(ex)[:100], flush=True)
