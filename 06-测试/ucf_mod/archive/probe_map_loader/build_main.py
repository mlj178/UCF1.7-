# -*- coding: utf-8 -*-
import sys, json, os
import re
sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/原始地图标准数据"
PTS  = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/probe_map_loader/_points"
HEAD = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/probe_map_loader/head2.md"
TAIL = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/probe_map_loader/tail2.md"
DOC  = BASE + "/点位与区域标准.md"

META = [(0,"GameStart","大厅"),(1,"TransportShip","运输船"),(2,"Factory","小型工厂"),(3,"Cebu_City","椰岛之巅"),(4,"NY_TM","胜利广场"),(5,"Arena","竞技场"),(6,"GrimReaperKM","刀锋寨"),(7,"DesertFort","沙漠要塞"),(8,"NanoResort","生化酒店"),(9,"Nano30_Storm","飓风危城"),(10,"Nano_DawnVillage","新寂静村"),(11,"DeathRing","死亡擂台")]
KEYS = {0:[],1:["BL","GR"],2:["BL","GR"],3:["BL","GR"],4:["Neutral"],5:["BL","GR"],6:["BL","GR"],7:["BL","GR","SupplyBox"],8:["BL","GR","SupplyBox"],9:["BL","GR","SupplyBox"],10:["BL","GR","SupplyBox","RedBox","BlueBox"],11:["BL","GR"]}
GROUPS = [("4.1 团队模式（TeamDeath）",[1,2,3]),("4.2 特殊战（Special）",[5,6,11]),("4.3 个人竞技（DeathMatch）",[4]),("4.4 终结者 / 生化剑客（Nano4 / Nano6）",[7,8]),("4.5 多人终结者（Nano4_Terminator）",[9,10]),("4.6 大厅",[0])]
MODE_COLS = [("TeamDeath<br>团队模式",[1,2,3]),("DeathMatch<br>个人竞技",[4]),("Special<br>特殊战",[5,6,11]),("Nano4<br>终结者模式",[7,8]),("Nano6<br>生化剑客模式",[7,8]),("Nano4_Terminator<br>多人终结者",[9,10])]

data = {}
for n, en, cn in META:
    rows = json.load(open(os.path.join(PTS, "full_level%d.json" % n), encoding="utf-8"))
    t22 = sum(1 for r in rows if r.get("tag") == 20022)
    t24 = sum(1 for r in rows if r.get("tag") == 20024)
    sc = {}
    for r in rows:
        for s in (r.get("scripts") or []): sc[s] = sc.get(s,0)+1
    links = sum(1 for r in rows if any(s in ("NodeLink","NodeLink2","Bot_JumpLink") for s in (r.get("scripts") or [])) and r.get("link_to"))
    data[n] = {"wp": t22, "climb": t24, "sc": sc, "links": links, "keys": KEYS[n]}

TYPES = [
 ("出生点 BL/GR","点","pointDic 键 BL、GR"),
 ("出生点 Neutral","点","pointDic 键 Neutral"),
 ("补给箱点 SupplyBox","点","pointDic 键 SupplyBox"),
 ("红箱点 RedBox","点","pointDic 键 RedBox"),
 ("蓝箱点 BlueBox","点","pointDic 键 BlueBox"),
 ("路点 WayPoint","可走性","tag == 20022"),
 ("攀爬区 ClimbArea","区域","tag == 20024"),
 ("蹲点 Bot_CrouchPos","目的","脚本 Bot_CrouchPos"),
 ("守卫点 Bot_GuardPos","目的","脚本 Bot_GuardPos"),
 ("守卫点 Bot_NanoGuardPos","目的","脚本 Bot_NanoGuardPos"),
 ("守卫区 Bot_GuardArea","目的","脚本 Bot_GuardArea（空类）"),
 ("守卫区 Bot_NanoGuardArea","目的","脚本 Bot_NanoGuardArea"),
 ("速度锁区 LockVelocityArea","玩法","脚本 LockVelocityArea（只对玩家）"),
 ("连线 NodeLink","连线","脚本 NodeLink"),
 ("端点连线 NodeLink2","连线","脚本 NodeLink2"),
 ("跳跃连线 Bot_JumpLink","连线","脚本 Bot_JumpLink"),
]
def cnt(n, name):
    d = data[n]
    if name.startswith("出生点 BL"): return 1 if "BL" in d["keys"] and "GR" in d["keys"] else 0
    if name.startswith("出生点 Neutral"): return 1 if "Neutral" in d["keys"] else 0
    if name.startswith("补给箱"): return 1 if "SupplyBox" in d["keys"] else 0
    if name.startswith("红箱"): return 1 if "RedBox" in d["keys"] else 0
    if name.startswith("蓝箱"): return 1 if "BlueBox" in d["keys"] else 0
    if name.startswith("路点"): return d["wp"]
    if name.startswith("攀爬区"): return d["climb"]
    if "CrouchPos" in name: return d["sc"].get("Bot_CrouchPos",0)
    if "NanoGuardPos" in name: return d["sc"].get("Bot_NanoGuardPos",0)
    if name.startswith("守卫点"): return d["sc"].get("Bot_GuardPos",0)
    if "NanoGuardArea" in name: return d["sc"].get("Bot_NanoGuardArea",0)
    if name.startswith("守卫区"): return d["sc"].get("Bot_GuardArea",0)
    if "LockVelocity" in name: return d["sc"].get("LockVelocityArea",0)
    if name.startswith("端点连线"): return d["sc"].get("NodeLink2",0)
    if name.startswith("跳跃连线"): return d["sc"].get("Bot_JumpLink",0)
    if name.startswith("连线"): return d["sc"].get("NodeLink",0)
    return 0

out = [open(HEAD, encoding="utf-8").read().rstrip(), ""]
out += ["### 3.3 点位种类 × 模式（本表核心）", "",
  "**同一种点位不是每个模式都有。** 下表按模式列出「这类点位在不在」，再按地图列出「具体几个」。", "",
  "#### 3.3.1 存在性", "",
  "| 点位种类 | 类别 | 判定依据 | " + " | ".join(c[0] for c in MODE_COLS) + " |",
  "|---|---|---|" + "---|" * len(MODE_COLS)]
for name, cat, rule in TYPES:
    cells = []
    for _, maps in MODE_COLS:
        tot = sum(cnt(m, name) for m in maps)
        cells.append("✅" if tot > 0 else "—")
    out.append("| %s | %s | %s | %s |" % (name, cat, rule, " | ".join(cells)))
out += ["", "> **一眼能看出的差异**：",
  "> - **红箱 / 蓝箱只有多人终结者模式（新寂静村）有**；",
  "> - **补给箱点只出现在三个生化系模式（终结者 / 生化剑客 / 多人终结者）**；",
  "> - 团队、特殊战、个人竞技**只有出生点 + 路点 + 连线**，没有任何补给/箱子点；",
  "> - 个人竞技（胜利广场）连路点都没有，只有一个 `Neutral` 出生点。", "",
  "#### 3.3.2 按地图的数量", "",
  "| 点位种类 | " + " | ".join("L%d<br>%s" % (n, cn) for n, en, cn in META) + " |",
  "|---|" + "---|" * len(META)]
for name, cat, rule in TYPES:
    cells = []
    for n, en, cn in META:
        if name.startswith(("出生点","补给箱","红箱","蓝箱")):
            cells.append("✅" if cnt(n,name) else "—")
        else:
            v = cnt(n,name); cells.append(str(v) if v else "—")
    out.append("| %s | %s |" % (name, " | ".join(cells)))
out += ["", "> L0 大厅不对战，全部为空。", "", "---", "", "## 4. 地图索引", "",
  "每张图的详细数据（来源 / 摘要 / 区域表 / 标记点表 / 线表 / 分组 / 路点全量坐标）已拆到各自的地图文件夹。", ""]

for grp, maps in GROUPS:
    out.append("### " + grp)
    out.append("")
    out.append("| level | 地图 | 路点 | 标记点 | 区域 | 连线 | 详情 |")
    out.append("|---|---|---|---|---|---|---|")
    for n in maps:
        en = dict((m[0], m[1]) for m in META)[n]; cn = dict((m[0], m[2]) for m in META)[n]
        rows = json.load(open(os.path.join(PTS, "full_level%d.json" % n), encoding="utf-8"))
        t22 = sum(1 for r in rows if r.get("tag") == 20022)
        nm = "level%d-%s-%s" % (n, en, cn)
        mdoc = os.path.join(BASE, "maps", nm, nm + ".md")
        txt = open(mdoc, encoding="utf-8").read()
        import re as _re
        pts = int(_re.search(r"\| 标记点对象 \| (\d+) \|", txt).group(1))
        areas = int(_re.search(r"\| 区域对象 \| (\d+) \|", txt).group(1))
        out.append("| %d | %s | %s | %d | %d | %s | [打开](maps/%s/%s.md) |" % (n, cn, format(t22, ","), pts, areas, format(data[n]["links"], ","), nm, nm))
    out.append("")

out.append("---")
out.append("")
out.append(open(TAIL, encoding="utf-8").read().rstrip())
out.append("")
open(DOC, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("MAIN OK", os.path.getsize(DOC))