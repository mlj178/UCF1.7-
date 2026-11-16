
import base64, io, zipfile, json, os, re
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
for lvl in [f"level{i}" for i in range(1,12)]:
    data = open(os.path.join(base,lvl),"rb").read()
    i = data.find(b"UEsDBBQ"); e = i
    while e < len(data) and (data[e:e+1].isalnum() or data[e:e+1] in b"+/="): e += 1
    b64 = data[i:e]
    raw = base64.b64decode(b64 + b"="*((4-len(b64)%4)%4))
    z = zipfile.ZipFile(io.BytesIO(raw))
    meta = json.loads(re.sub(rb'"version":\s*([0-9.]+)', rb'"version": "\1"', z.read("meta.json")))
    out = []
    for n in z.namelist():
        if not n.startswith("graph"): continue
        g = json.loads(z.read(n))
        out.append(dict(file=n, type=meta["typeNames"][int(n[5])].split(".")[-1], tag=g.get("searchTag"),
                        root=g.get("root"), maxd=g.get("maxDistance"), ray=g.get("raycast"), mask=g.get("mask")))
    print(lvl, meta.get("version"), json.dumps(out, ensure_ascii=False))
