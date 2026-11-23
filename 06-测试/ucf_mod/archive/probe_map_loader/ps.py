# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
env = UnityPy.load(r"D:\ucf_test_level12\game\UnityCrossFire_Data\globalgamemanagers")
o = [x for x in env.objects if x.type.name=="PlayerSettings"][0]
d = o.get_raw_data()
# 前 400 字节里找可打印串
import re
print("strings:", [s.decode('latin1') for s in re.findall(rb'[ -~]{4,}', d)][:20])
