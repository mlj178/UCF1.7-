
import UnityPy, struct
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
env = UnityPy.load(p)
sf = list(env.files.values())[0]
print("sf:", sf.name, "version", getattr(sf,"version",None), getattr(sf,"unity_version",None))
objs = sf.objects
print("has objects dict:", type(objs))
def script_of(data):
    for off in (16,12,20):
        if len(data) >= off+12:
            fid, pid = struct.unpack_from("<iq", data, off)
            if pid in objs:
                return off, fid, pid
    return None
res = {}
for pid_, o in objs.items():
    if o.type.name != "MonoBehaviour": continue
    raw = o.get_raw_data()
    s = script_of(raw)
    if not s: 
        res[pid_]=("??", None); continue
    off, fid, spid = s
    try:
        ms = objs[spid].read()
        cn = getattr(ms, "m_ClassName", "?")
        asm = getattr(ms, "m_AssemblyName", "?")
        ns = getattr(ms, "m_Namespace", "")
    except Exception as e:
        cn, asm, ns = "ERR:"+type(e).__name__, "", ""
    res[pid_] = (asm, ns, cn, imm:=len(raw))
for k,v in sorted(res.items(), key=lambda kv: str(kv[1][2])):
    print(k, v)
