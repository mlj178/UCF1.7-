# -*- coding: utf-8 -*-
# 只读探测：globalgamemanagers 里的场景名单结构
# 不写任何文件到游戏目录
import UnityPy, traceback, sys

GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"

env = UnityPy.load(GAME)
print("== objects ==")
objs = list(env.objects)
for o in objs:
    try:
        bs = o.byte_size if hasattr(o, "byte_size") else -1
    except Exception:
        bs = -1
    print(f"  {o.type.name:32s} path_id={o.path_id:<22d} size={bs}")

print()
print("== BuildSettings typetree ==")
for o in objs:
    if o.type.name not in ("BuildSettings",):
        continue
    print("path_id:", o.path_id)
    try:
        tt = o.read_typetree()
        import json
        print(json.dumps(tt, indent=1, ensure_ascii=False)[:8000])
    except Exception as e:
        traceback.print_exc()
