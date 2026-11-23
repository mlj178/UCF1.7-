#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 AssetRipper.GUI 拉「这张图用到的贴图」 -> geo/tex/<关卡>/<贴图文件名>.png

为什么用它而不是 UnityPy：AssetRipper 已经把整个游戏数据目录加载好了
（默认 http://127.0.0.1:60840），它自己解 DXT/BC7/贴图翻转，出的就是 PNG，
和 UnityPy 解出来的东西可以互相核对。这里只读它的 HTTP 接口，不碰游戏文件。

用法：
    python tools/fetch_tex.py level1              # 只取 level1.npz 里引用到的贴图
    python tools/fetch_tex.py --all               # 所有 npz 引用到的贴图
    python tools/fetch_tex.py level1 --force      # 覆盖已有 png
    python tools/fetch_tex.py level1 --url http://127.0.0.1:60840
    python tools/fetch_tex.py level1 --refresh    # 重建资源索引（默认缓存）

流程：
    1) 读 geo/<level>.npz 的 meta.mats，收集 tex 文件名（如 TSHIP_038_12.png）
    2) 遍历 AssetRipper 的资源包，建「贴图名 -> (包号, 资源号)」索引
       （索引缓存到 geo/tex/_assetripper.json，第二次起秒开）
    3) 逐个下载 /Assets/Image?Path=...&Extension=png，按 npz 里的文件名落盘
       —— 落盘名和 geo2web / navview 用的完全一致，不用再改名
    4) 用 PIL 核对宽高和 npz 里记的 tex_w/tex_h 是否吻合

拉不到的贴图只警告，不中断：3D 里那块会退回纯色。
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

TOOLS = os.path.dirname(os.path.abspath(__file__))
UCF = os.path.dirname(TOOLS)
GEO = os.path.join(UCF, "geo")
TEXROOT = os.path.join(GEO, "tex")
INDEX_FILE = os.path.join(TEXROOT, "_assetripper.json")
DEFAULT_URL = "http://127.0.0.1:60840"

ROW_RE = re.compile(
    r'<tr data-class="([^"]+)"><td>(\d+)</td><td>[^<]*</td>'
    r'<td><a href="([^"]+)"[^>]*>([^<]*)</a></td></tr>')
COLL_RE = re.compile(r'href="(/Collections/View\?Path=[^"]+)"')


def _setup_console():
    out = sys.stdout
    enc = (getattr(out, "encoding", "") or "").lower().replace("-", "")
    try:
        if getattr(out, "isatty", lambda: False)() and enc not in ("utf8", "cp65001"):
            out.reconfigure(errors="replace")
        else:
            out.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def http_get(url, timeout=60):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def _path_param(obj):
    return urllib.parse.quote(json.dumps(obj, separators=(",", ":")), safe="")


def bundles(base):
    """根节点下的资源包（返回 [(序号, 名字)]）。"""
    html = http_get(base + "/Bundles/View?Path=" + _path_param({"P": []}), 60).decode("utf-8", "replace")
    out = []
    for href in COLL_RE.findall(html):
        q = urllib.parse.urlparse(href).query
        try:
            p = json.loads(urllib.parse.parse_qs(q)["Path"][0])
        except Exception:
            continue
        if isinstance(p, dict) and isinstance(p.get("I"), int):
            out.append(p["I"])
    return out


def collection_rows(base, idx):
    """一个包里的全部资源：[(class, 资源号, 名字)]。"""
    url = base + "/Collections/View?Path=" + _path_param({"B": {"P": []}, "I": idx})
    html = http_get(url, 120).decode("utf-8", "replace")
    rows = []
    for cls, d, href, name in ROW_RE.findall(html):
        rows.append((cls, int(d), name))
    return rows


def build_index(base, progress=print):
    idx = {}
    got = bundles(base)
    progress("资源包 %d 个，逐包读资源表…" % len(got))
    for k, b in enumerate(got):
        try:
            rows = collection_rows(base, b)
        except Exception as exc:
            progress("  包 #%d 读取失败：%s" % (b, exc))
            continue
        for cls, d, name in rows:
            if cls != "Texture2D":
                continue
            key = name.strip().lower()
            if key and key not in idx:          # 同名贴图取第一个
                idx[key] = {"b": b, "d": d, "name": name}
        if (k + 1) % 5 == 0 or k + 1 == len(got):
            progress("  已读 %d/%d 包，贴图 %d 张" % (k + 1, len(got), len(idx)))
    return idx


def load_index(base, refresh=False, progress=print):
    if not refresh and os.path.isfile(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                j = json.load(f)
            if j.get("url") == base and j.get("items"):
                return j["items"]
        except Exception:
            pass
    items = build_index(base, progress)
    os.makedirs(TEXROOT, exist_ok=True)
    tmp = INDEX_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"url": base, "items": items}, f, ensure_ascii=False)
    os.replace(tmp, INDEX_FILE)
    return items


def npz_textures(level):
    """从 geo/<level>.npz 里取所有引用到的贴图：[(落盘文件名, 原始名字, w, h)]。"""
    import numpy as np
    p = os.path.join(GEO, level + ".npz")
    if not os.path.isfile(p):
        return []
    z = np.load(p, allow_pickle=True)
    if "meta" not in z.files:
        return []
    try:
        meta = json.loads(str(z["meta"][0]))
    except Exception:
        return []
    out = []
    seen = set()
    for m in meta.get("mats") or []:
        fn = str(m.get("tex") or "").strip()
        if not fn or fn in seen:
            continue
        seen.add(fn)
        out.append((fn, str(m.get("name") or ""), int(m.get("tex_w") or 0), int(m.get("tex_h") or 0)))
    return out


def image_url(base, bundle, asset):
    path = {"C": {"B": {"P": []}, "I": bundle}, "D": asset}
    return base + "/Assets/Image?Path=" + _path_param(path) + "&Extension=png"


def main():
    _setup_console()
    ap = argparse.ArgumentParser(description="从 AssetRipper 拉贴图 -> geo/tex/<关卡>/")
    ap.add_argument("levels", nargs="*", help="关卡名（level1 等），默认全部 npz")
    ap.add_argument("--all", action="store_true", help="所有 npz 用到的贴图")
    ap.add_argument("--url", default=DEFAULT_URL, help="AssetRipper 地址（默认 %s）" % DEFAULT_URL)
    ap.add_argument("--force", action="store_true", help="已有 png 也重下")
    ap.add_argument("--refresh", action="store_true", help="重建资源索引缓存")
    args = ap.parse_args()

    levels = args.levels
    if args.all or not levels:
        levels = sorted(fn[:-4] for fn in os.listdir(GEO) if fn.lower().endswith(".npz"))
    base = args.url.rstrip("/")

    want = {}
    for lv in levels:
        for fn, mat, w, h in npz_textures(lv):
            want.setdefault(lv, []).append((fn, mat, w, h))
    n_all = sum(len(v) for v in want.values())
    if not n_all:
        sys.exit("这些 npz 里没有贴图引用")
    print("要拉 %d 张贴图（%d 张图）" % (n_all, len(want)))

    try:
        idx = load_index(base, refresh=args.refresh)
    except Exception as exc:
        sys.exit("连不上 AssetRipper（%s）。先打开 AssetRipper.GUI 把游戏数据目录加载好，再跑这条命令。\n  %s"
                 % (base, exc))
    print("资源索引：%d 张贴图" % len(idx))

    ok = skipped = missing = 0
    bad = []
    for lv, items in want.items():
        outdir = os.path.join(TEXROOT, lv)
        os.makedirs(outdir, exist_ok=True)
        for fn, mat, w, h in items:
            dst = os.path.join(outdir, fn)
            if os.path.isfile(dst) and not args.force:
                skipped += 1
                continue
            stem = re.sub(r"_\d+\.png$", "", fn)
            rec = idx.get(stem.lower()) or idx.get(fn.lower())
            if not rec:
                missing += 1
                bad.append((lv, fn, "索引里没有这个名字"))
                continue
            try:
                body = http_get(image_url(base, rec["b"], rec["d"]), 60)
            except Exception as exc:
                missing += 1
                bad.append((lv, fn, "下载失败 %s" % exc))
                continue
            if not body.startswith(b"\x89PNG"):
                missing += 1
                bad.append((lv, fn, "不是 PNG"))
                continue
            tmp = dst + ".tmp"
            with open(tmp, "wb") as f:
                f.write(body)
            os.replace(tmp, dst)
            ok += 1
            if w and h:
                try:
                    from PIL import Image
                    with Image.open(dst) as im:
                        if im.size != (w, h):
                            bad.append((lv, fn, "尺寸 %s != npz %dx%d" % (im.size, w, h)))
                except Exception:
                    pass
    print("完成：新下载 %d，已存在 %d，失败 %d" % (ok, skipped, missing))
    for lv, fn, why in bad[:20]:
        print("  !! %-8s %-32s %s" % (lv, fn, why))
    if bad:
        print("  （失败的贴图在 3D 里会退回纯色，不影响其它块）")
    print("输出目录：%s" % TEXROOT)


if __name__ == "__main__":
    main()
