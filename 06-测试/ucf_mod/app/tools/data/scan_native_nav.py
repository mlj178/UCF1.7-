# -*- coding: utf-8 -*-
r"""scan_native_nav.py — 读游戏自己的场景文件，列出每张图【原生】的 A* 可通行空间。

回答的问题：这张图原版到底给了什么可走面？
  * PointGraph    —— A* 按 tag "WayPoint"(20022) 扫场景物体，节点数 = 激活的 WayPoint 物体数
  * NavMeshGraph  —— A* 烘焙的三角网格，顶点/三角形从 resources.assets 里 *_NavMesh 网格读
（不含插件 auto_waypoints 铺的、也不含 nav\*.txt 编辑清单加的）

用法：
    python scan_native_nav.py                 # 自动找游戏目录（读 tools\deploy.json 的上一级）
    python scan_native_nav.py --data "D:\...\UnityCrossFire_Data"
    python scan_native_nav.py --json out.json # 同时写一份机器可读的

依赖：UnityPy（用系统 Python：C:\Users\...\Python312\python.exe）
"""
import argparse, base64, io, json, os, re, struct, sys, zipfile

try:
    import UnityPy
except ImportError:
    sys.exit("缺少 UnityPy：pip install UnityPy（用装过 UnityPy 的那个 python 跑本脚本）")

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记
MAP_MD = os.path.join(UCF_ROOT, "docs", "guide", "地图对照表.md")
WAYPOINT_TAG = 20022


def find_data_dir(cli):
    if cli:
        return cli
    dep = os.path.join(UCF_ROOT, "tools", "deploy.json")
    if os.path.exists(dep):
        moddir = json.load(open(dep, encoding="utf-8"))["deploy"]
        cand = os.path.join(os.path.dirname(moddir), "UnityCrossFire_Data")
        if os.path.isdir(cand):
            return cand
    sys.exit("找不到 UnityCrossFire_Data，请用 --data 指定")


def load_map_table():
    """从 地图对照表.md 读 序号/关卡/中文名/场景名（它是唯一权威表）。

    只读第一张表：本文件自带的结果表也在同一份 md 里，一起读会把每张图读两遍。
    """
    rows = []
    if not os.path.exists(MAP_MD):
        return rows
    started = False
    for line in open(MAP_MD, encoding="utf-8"):
        s = line.strip()
        if not s:
            if started:
                break
            continue
        m = re.match(r"\|\s*(\d+)\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", s)
        if not m:
            if started and not s.startswith("|"):
                break
            continue
        started = True
        rows.append({"no": m.group(1), "level": m.group(2),
                     "cn": m.group(3).strip(), "scene": m.group(4).strip()})
    return rows


def astar_graphs(env):
    """场景里的 AstarData：一段 base64(zip) 里装着 graphN.json。"""
    out = []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        raw = obj.get_raw_data()
        idx = raw.find(b"UEsDBBQ")
        if idx < 0:
            continue
        ln = struct.unpack("<I", raw[idx - 4:idx])[0]
        try:
            z = zipfile.ZipFile(io.BytesIO(base64.b64decode(raw[idx:idx + ln].decode("ascii", "replace"))))
        except Exception:
            continue
        for n in z.namelist():
            if not n.startswith("graph"):
                continue
            try:
                j = json.loads(z.read(n))
            except Exception:
                continue
            if "sourceMesh" in j:
                out.append(("NavMeshGraph", j))
            elif "searchTag" in j:
                out.append(("PointGraph", j))
            else:
                out.append(("OtherGraph", j))
    return out


def count_waypoints(env):
    total = active = 0
    for obj in env.objects:
        if obj.type.name != "GameObject":
            continue
        try:
            go = obj.read()
        except Exception:
            continue
        if getattr(go, "m_Tag", -1) == WAYPOINT_TAG:
            total += 1
            if getattr(go, "m_IsActive", 1):
                active += 1
    return total, active


def mesh_stats(data_dir):
    """resources.assets 里所有 *NavMesh* 网格：顶点 / 索引 / 三角形 / 去重位置数。"""
    stats = {}
    env = UnityPy.load(os.path.join(data_dir, "resources.assets"))
    for obj in env.objects:
        if obj.type.name != "Mesh":
            continue
        try:
            m = obj.read()
        except Exception:
            continue
        name = (getattr(m, "m_Name", "") or "").strip()
        if not name.lower().endswith(("navmesh", "navmesh_", "navmesh1")):
            continue
        if "nav" not in name.lower():
            continue
        vd = m.m_VertexData
        vc = int(vd.m_VertexCount)
        subs = m.m_SubMeshes or []
        idx_count = sum(int(getattr(s, "indexCount", 0)) for s in subs)
        # 去重顶点位置：A* 的 NavMeshGraph 会把坐标相同的顶点并成一个
        stride = 0
        for c in vd.m_Channels:
            if getattr(c, "stream", 0) == 0:
                stride = max(stride, int(getattr(c, "offset", 0)) + (int(getattr(c, "dimension", 0)) & 0xF) * 4)
        data = bytes(vd.m_DataSize)
        pos = set()
        for i in range(vc):
            pos.add(struct.unpack_from("<fff", data, i * stride))
        stats[name] = {"mesh_verts": vc, "index_count": idx_count,
                       "tris": idx_count // 3, "astar_verts": len(pos)}
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    ap.add_argument("--json")
    a = ap.parse_args()
    data_dir = find_data_dir(a.data)
# 输出按对照表的顺序排（表里怎么排，打印出来的表就怎么排）
    rows = load_map_table()
    table = {r["level"]: r for r in rows}
    order = {r["level"]: i for i, r in enumerate(rows)}
    meshes = mesh_stats(data_dir)

    result = []
    for n in range(1, 12):
        lv = "level%d" % n
        path = os.path.join(data_dir, lv)
        if not os.path.exists(path):
            continue
        env = UnityPy.load(path)
        graphs = astar_graphs(env)
        wp_total, wp_active = count_waypoints(env)
        pg = [(k, j) for k, j in graphs if k == "PointGraph"]
        ng = [(k, j) for k, j in graphs if k == "NavMeshGraph"]
        row = table.get(lv, {})
        item = {
            "no": row.get("no", ""), "level": lv,
            "cn": row.get("cn", ""), "scene": row.get("scene", ""),
            "graphs": [k for k, _ in graphs],
            "pointgraph": [{
                "name": j.get("name"), "searchTag": j.get("searchTag"),
                "maxDistance": j.get("maxDistance"), "mask": (j.get("mask") or {}).get("value"),
                "waypoint_objects": wp_total, "waypoint_active": wp_active,
            } for _, j in pg],
            "navmeshgraph": [],
        }
        for _, j in ng:
            src = (j.get("sourceMesh") or {}).get("Name", "")
            ms = meshes.get(src, {})
            item["navmeshgraph"].append({
                "mesh": src, "scale": j.get("scale"),
                "offset": j.get("offset"), "rotation": j.get("rotation"),
                "mesh_verts": ms.get("mesh_verts"), "astar_verts": ms.get("astar_verts"),
                "tris": ms.get("tris"), "index_count": ms.get("index_count"),
            })
        result.append(item)
    result.sort(key=lambda it: order.get(it["level"], 99))

    # 人看的表
    print("| 序号 | 关卡 | 中文名 | 原生 A* 图 | PointGraph 原生节点 | NavMeshGraph 网格 | 顶点(网格→A*) | 三角形 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for it in result:
        pg = it["pointgraph"][0] if it["pointgraph"] else None
        ng = it["navmeshgraph"][0] if it["navmeshgraph"] else None
        if pg:
            if "node link" in (pg.get("name") or "").lower():
                pg_txt = "0 路点（node link 专用）"
            else:
                pg_txt = "%d（WayPoint）" % pg["waypoint_active"]
        else:
            pg_txt = "—（没有 PointGraph）"
        if ng:
            ng_txt = ng["mesh"]
            v_txt = ("%d → %d" % (ng["mesh_verts"], ng["astar_verts"])) if ng["mesh_verts"] != ng["astar_verts"] else str(ng["mesh_verts"])
            t_txt = str(ng["tris"])
        else:
            ng_txt, v_txt, t_txt = "—", "—", "—"
        print("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            it["no"], it["level"], it["cn"], " + ".join(it["graphs"]), pg_txt, ng_txt, v_txt, t_txt))

    if a.json:
        json.dump(result, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("\n[written]", a.json)


if __name__ == "__main__":
    main()
