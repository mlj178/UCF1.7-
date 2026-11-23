# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
# 1) MonoScript 表
env = UnityPy.load(SRC + "globalgamemanagers.assets")
ms = {}
for o in env.objects:
    if o.type.name != "MonoScript": continue
    try:
        d = o.read()
        ms[o.path_id] = (getattr(d,"m_ClassName",None) or "", getattr(d,"m_Namespace",None) or "", getattr(d,"m_AssemblyName",None) or "")
    except Exception as e:
        ms[o.path_id] = ("<ERR>", str(e)[:30], "")
print("MonoScript count:", len(ms))
for k in list(ms)[:10]:
    print("  ", k, ms[k])

# 2) 从 MonoBehaviour 原始字节取 m_Script
env2 = UnityPy.load(SRC + "level2")
buf = open(SRC + "level2","rb").read()
sf = list(env2.files.values())[0]
cnt = 0
for o in env2.objects:
    if o.type.name != "MonoBehaviour": continue
    try:
        start = o.byte_offset if hasattr(o,'byte_offset') else None
    except Exception:
        start = None
    cnt += 1
print("MonoBehaviour in level2:", cnt)
# 用 reader 读原始
for o in env2.objects:
    if o.type.name != "MonoBehaviour": continue
    raw = o.get_raw_data()
    go_fid, go_pid = struct.unpack_from("<iq", raw, 0)
    en = raw[12]
    sc_fid, sc_pid = struct.unpack_from("<iq", raw, 16)
    print(f"  MB path_id={o.path_id} script_file={sc_fid} script_pid={sc_pid} -> {ms.get(sc_pid)}")
    break
