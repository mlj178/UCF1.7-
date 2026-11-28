
import UnityPy, collections, os
base = "D:/BaiduNetdiskDownload/ucf_test_level12/game/UnityCrossFire_Data"
env = UnityPy.load(base + "/level9", base + "/sharedassets9.assets")
c = collections.Counter()
for o in env.objects:
    c[o.type.name] += 1
for k, v in c.most_common(40):
    print("  %-24s %d" % (k, v))
