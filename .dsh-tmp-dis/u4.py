
import UnityPy, struct, binascii
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
env = UnityPy.load(p)
sf = list(env.files.values())[0]
objs = sf.objects
for pid_ in (2265, 2296, 2273):
    o = objs[pid_]
    raw = o.get_raw_data()
    print("== ", pid_, len(raw))
    print(binascii.hexlify(raw[:96]).decode())
    print("ascii:", "".join(chr(c) if 32<=c<127 else "." for c in raw[:96]))
print("external refs:", getattr(sf, "externals", None))
import json
try:
    print(json.dumps([str(e.path) for e in sf.externals], ensure_ascii=False)[:500])
except Exception as e: print("ext err", e)
