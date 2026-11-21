vis/ —— 游戏内 Ctrl+E 的导出（按性质分类）

raw/      每次导出的原始扫描，按地图分文件夹：<级别>_<中文名>/<时间>_<指纹>.json
          _非原生_插件铺点/ = 插件自己铺的点，不是游戏原生（不要当原始数据用）
          _未识别_*/        = 指纹不在 navdata/dev/maps/_index.json 里
navmesh/  去重后的 A* 可走面 navmesh_nm<顶点数>-<指纹>.bin
_state/   插件内部去重标记 _seen_*（不用看）

新导出仍会先落在 vis/ 根目录；跑一次 tools/tidy_vis.py 就归位。

当前收录：
  _未识别_n786_疑似运输船                20261117-223731_n786-c652328e7ff697ce__可疑0边.json   n786-c652328e7ff697ce     786 点  game
  _非原生_插件铺点                      20261117-134856_n694-c904835721dddfde__插件铺点.json   n694-c904835721dddfde     694 点  ours
  level10_新寂静村                   20261117-110149_n180-03b43b7ee737fcdc.json         n180-03b43b7ee737fcdc     180 点  game
  level1_运输船                     20261117-135205_n786-57a46e3465c847cb.json         n786-57a46e3465c847cb     786 点  game
  level2_小型工厂                    20261117-135241_n12-0e2829fa03c469e3.json          n12-0e2829fa03c469e3       12 点  game
  level3_椰岛之巅                    20261118-101800_n2-24a647eff15d6ca4.json           n2-24a647eff15d6ca4         2 点  game
  level5_竞技场                     20261117-113600_n17-f352f68820fae99c.json          n17-f352f68820fae99c       17 点  game
  level7_沙漠要塞                    20261117-105759_n12-17a93cfb246913e1.json          n12-17a93cfb246913e1       12 点  game
