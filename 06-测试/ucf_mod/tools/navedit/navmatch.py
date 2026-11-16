'''把一份点云/导航面判给某个 level（用缓存的关卡几何做匹配）。

不依赖 scipy：把几何顶点塞进 2 m 的体素哈希，查询时只看邻域体素。
'''

from __future__ import annotations

import os

import numpy as np

GEO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'geo')


class LevelGeo:
    def __init__(self, name, path):
        d = np.load(path)
        self.name = name
        self.p = d['p'].astype(np.float64)
        self.i = d['i']
        self.cell = 2.0
        self.key = np.floor(self.p / self.cell).astype(np.int64)
        order = np.lexsort((self.key[:, 2], self.key[:, 1], self.key[:, 0]))
        self.key = self.key[order]
        self.p = self.p[order]
        self.index = {}
        for idx, k in enumerate(map(tuple, self.key)):
            self.index.setdefault(k, []).append(idx)
        self.lo = self.p.min(axis=0)
        self.hi = self.p.max(axis=0)

    def support(self, pts, tol=2.5):
        '''pts 中落在几何表面 tol 米以内的比例。'''
        if len(pts) == 0:
            return 0.0, 0, 0
        k = np.floor(pts / self.cell).astype(np.int64)
        hit = 0
        tol2 = tol * tol
        offs = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)]
        for n, key in enumerate(map(tuple, k)):
            best = 1e18
            for dx, dy, dz in offs:
                ids = self.index.get((key[0] + dx, key[1] + dy, key[2] + dz))
                if not ids:
                    continue
                d = self.p[ids] - pts[n]
                d2 = (d * d).sum(axis=1).min()
                if d2 < best:
                    best = d2
            if best <= tol2:
                hit += 1
        return hit / float(len(pts)), hit, len(pts)


_CACHE = {}


def load_levels(geo_dir=None):
    geo_dir = geo_dir or GEO_DIR
    global _CACHE
    if _CACHE:
        return _CACHE
    for fn in sorted(os.listdir(geo_dir)):
        if not fn.endswith('.npz'):
            continue
        name = fn[:-4]
        try:
            _CACHE[name] = LevelGeo(name, os.path.join(geo_dir, fn))
        except Exception as exc:  # noqa: BLE001
            print('skip', fn, exc)
    return _CACHE


def rank(pts, tol=2.5, top=4):
    '''返回 [(score, level, hit, total), ...]，按分数降序。'''
    levels = load_levels()
    rows = []
    for name, geo in levels.items():
        ratio, hit, total = geo.support(pts, tol)
        rows.append((ratio, name, hit, total))
    rows.sort(reverse=True)
    return rows[:top]


if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        pts = np.load(f)['p'] if f.endswith('.npz') else None
        if pts is None:
            print('unsupported', f)
            continue
        for row in rank(pts):
            print('%-8s ratio=%.3f (%d/%d)' % (row[1], row[0], row[2], row[3]))
