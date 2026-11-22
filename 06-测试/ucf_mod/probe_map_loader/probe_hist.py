# -*- coding: utf-8 -*-
import sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy

DC = "C:/Users/17242/Downloads/DC穿越火线挑战版本/DC穿越火线挑战版本/DC穿越火线挑战版本_Data/"
UCF = "D:/ucf_test_level12/game/UnityCrossFire_Data/"

print("===== DC: globalgamemanagers 场景表 =====")
b = open(DC + "globalgamemanagers", "rb").read()
for m in re.finditer(rb"[ -~]{6,}\.unity", b):
    print("  ", m.group().decode("latin1"))

def hist(path, label):
    try:
        env = UnityPy.load(path)
    except Exception as e:
        print(f"\n  {label}: 打开失败 {type(e).__name__} {e}"); return
    sf = list(env.files.values())[0]
    c = collections.Counter()
    for pid, oi in sf.objects.items():
        c[getattr(oi.type, "name", str(oi.type))] += 1
    print(f"\n  --- {label}  objects={len(sf.objects)} ---")
    for k, v in c.most_common(35):
        print(f"     {k:28s} {v}")

for p, l in [
    (DC+"level2", "DC level2"),
    (DC+"level3", "DC level3"),
    (DC+"sharedassets2.assets", "DC sharedassets2"),
    (UCF+"level1", "UCF level1"),
    (UCF+"sharedassets1.assets", "UCF sharedassets1"),
]:
    hist(p, l)
