'''A* NavMeshGraph 导出文件（UCFNM3）读取器。

格式（小端）::

    UCFNM3 魔数                     7 B
    int32  nv, nt, ntile           12 B
    uint8  identity/onlyTranslational/isXY/isXZ   4 B
    float  matrix[16]              64 B   (Unity Matrix4x4, 列主序)
    float  translation[3]          12 B
    int32  verts[nv*3]             世界坐标 (Int3, 1/1000 m)
    int32  gverts[nv*3]            图空间坐标
    int32  tris[nt*3]              顶点索引

A* 里 NavmeshTile.verts 是已经过 GraphTransform 的世界坐标，
vertsInGraphSpace 是烘焙时的图空间坐标。两份都写进文件，方便离线互相校验。
'''

from __future__ import annotations

import struct
from dataclasses import dataclass

import numpy as np

MAGIC = b'UCFNM3\x00'  # C 侧写的是 7 字节，第 7 字节是 NUL
HEADER_LEN = 7 + 12 + 4 + 64 + 12


@dataclass
class NavMesh:
    verts: np.ndarray        # (nv,3) float64，米
    gverts: np.ndarray       # (nv,3) float64，米
    tris: np.ndarray         # (nt,3) int32
    ntile: int
    matrix: np.ndarray       # (16,) float32
    translation: np.ndarray  # (3,) float32
    flags: tuple

    @property
    def identity(self) -> bool:
        return bool(self.flags[0])

    def bbox(self, which: str = 'world'):
        v = self.verts if which == 'world' else self.gverts
        return v.min(axis=0), v.max(axis=0)

    def size(self, which: str = 'world'):
        lo, hi = self.bbox(which)
        return hi - lo

    def world_via_matrix(self) -> np.ndarray:
        m = self.matrix.astype(np.float64)
        v = self.gverts
        x, y, z = v[:, 0], v[:, 1], v[:, 2]
        return np.stack([
            m[0] * x + m[4] * y + m[8] * z + m[12],
            m[1] * x + m[5] * y + m[9] * z + m[13],
            m[2] * x + m[6] * y + m[10] * z + m[14],
        ], axis=1)

    def centroids(self) -> np.ndarray:
        v = self.verts
        return (v[self.tris[:, 0]] + v[self.tris[:, 1]] + v[self.tris[:, 2]]) / 3.0

    def edge_graph(self):
        '''三角形相邻关系 -> 路点/连线：节点=三角形重心，边=共边的两个三角形。'''
        tris = self.tris
        edge_map = {}
        for i, (a, b, c) in enumerate(tris):
            for u, w in ((a, b), (b, c), (c, a)):
                key = (u, w) if u < w else (w, u)
                edge_map.setdefault(key, []).append(i)
        edges = []
        for ids in edge_map.values():
            for k in range(1, len(ids)):
                edges.append((ids[0], ids[k]))
        edges = np.asarray(edges, dtype=np.int32).reshape(-1, 2)
        return self.centroids(), edges


def load(path: str) -> NavMesh:
    with open(path, 'rb') as f:
        buf = f.read()
    if buf[:7] != MAGIC:
        raise ValueError('不是 UCFNM3 文件: %s (%r)' % (path, buf[:7]))
    nv, nt, ntile = struct.unpack_from('<iii', buf, 7)
    if nv <= 0 or nt <= 0 or nv > 3000000 or nt > 3000000:
        raise ValueError('顶点/三角形数异常: nv=%d nt=%d' % (nv, nt))
    flags = tuple(buf[19:23])
    matrix = np.frombuffer(buf, '<f4', 16, 23).copy()
    translation = np.frombuffer(buf, '<f4', 3, 87).copy()
    off = HEADER_LEN
    need = off + nv * 12 + nv * 12 + nt * 12
    if len(buf) < need:
        raise ValueError('文件被截断: %d < %d' % (len(buf), need))
    verts = np.frombuffer(buf, '<i4', nv * 3, off).reshape(nv, 3).astype(np.float64) / 1000.0
    off += nv * 12
    gverts = np.frombuffer(buf, '<i4', nv * 3, off).reshape(nv, 3).astype(np.float64) / 1000.0
    off += nv * 12
    tris = np.frombuffer(buf, '<i4', nt * 3, off).reshape(nt, 3).astype(np.int32)
    if tris.max() >= nv or tris.min() < 0:
        raise ValueError('三角形索引越界: max=%d nv=%d' % (tris.max(), nv))
    return NavMesh(verts=verts, gverts=gverts, tris=tris, ntile=ntile,
                   matrix=matrix, translation=translation, flags=flags)


def describe(nm: NavMesh, name: str = '') -> str:
    out = []
    if name:
        out.append('== ' + name)
    out.append('   verts=%d tris=%d tiles=%d flags=%s' % (len(nm.verts), len(nm.tris), nm.ntile, nm.flags))
    for tag, v in (('world', nm.verts), ('graph', nm.gverts), ('matrix', nm.world_via_matrix())):
        lo, hi = v.min(axis=0), v.max(axis=0)
        out.append('   %-6s lo=%s hi=%s size=%s' % (tag, np.round(lo, 2), np.round(hi, 2), np.round(hi - lo, 2)))
    n, e = nm.edge_graph()
    out.append('   triangle graph: nodes=%d edges=%d' % (len(n), len(e)))
    return chr(10).join(out)


if __name__ == '__main__':
    import sys
    for a in sys.argv[1:]:
        print(describe(load(a), a))
