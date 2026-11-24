/* UCF 路点工作台 · 七页只读版（2026-11-18）
 * 数据全部来自 console/navserver.py 的 GET 接口：
 *   /api/workbench  地图统计 / 三版（成品·编辑中·收件箱）/ 测试包 / 配置 / 事件 / 日志
 *   /api/raw        地图 JSON（②开发版 maps/）
 *   /api/txt        编辑清单 nav/<指纹>.txt（有就套用）
 * 本文件不发 POST，不写任何文件。
 */
(function () {
'use strict';

var $ = function (id) { return document.getElementById(id); };

window.addEventListener('error', function (e) {
  try {
    var t = $('toast');
    if (t) { t.textContent = '脚本错误：' + (e.message || e.type); t.className = 'on err'; }
  } catch (x) {}
});
window.addEventListener('unhandledrejection', function (e) {
  try {
    var t = $('toast');
    var m = (e.reason && (e.reason.message || e.reason)) || 'promise';
    if (t) { t.textContent = '请求失败：' + m; t.className = 'on err'; }
  } catch (x) {}
});

/* =====================================================================
 * 0. 常量 / 工具
 * ===================================================================*/
var COLORS = {
  node_walk: '#9fb0c7', node_block: '#64748b', edge: '#5d7fa3',
  spawn_gr: '#4f8cff', spawn_bl: '#ff5c5c', spawn_neutral: '#8a97a8', supply: '#f59e0b',
  crouch_bl: '#f5b942', crouch_gr: '#e07b39', jump: '#38d9f5',
  nano_area: '#a78bfa', nano_pos: '#c4b5fd', guard_area: '#7c6bd4', guard: '#8d7fd6',
  tag_region: '#f97316', route: '#3ecf8e', zone: '#a78bfa'
};
var SPAWN_NAMES = { 0: '幽灵出生', 1: '保卫者出生', 2: '中立点', 3: '补给箱', 4: '红箱', 5: '蓝箱' };
var SPAWN_SUB = { 0: 'SP_BL · MapManager', 1: 'SP_GR · MapManager', 2: 'SP_Netural', 3: 'SP_SupplyBox', 4: 'SP_RedBox', 5: 'SP_BlueBox' };
var KIND_LABEL = {
  nano_area: '幽灵守区', nano_pos: '幽灵守点', crouch: '蹲守点', guard: '旧守卫点',
  guard_area: '旧守卫区', spawn: '出生 / 补给', jump: '跳跃链接', tag_region: '标签区'
};
var PAGE_TITLE = {
  overview: '总览', waypoints: '路点库', routes: '路线', zones: '区域',
  auto: '自动铺设', maps: '地图数据', logs: '日志'
};
var VIEW_ORDER = ['native', 'final', 'pack'];
var VIEW_LABELS = { native: '① 备份版', final: '② 成品', pack: '② 编辑中' };
var VIEW_FULL = {
  native: '备份版（原生快照·只读对照）',
  final: '成品（final 每图一份·只读）',
  pack: '编辑中（packs 测试包·只读）'
};
var STORAGE_VIEW = 'ucf.wb.view';
var STORAGE_PACKS = 'ucf.wb.packs';
var CORE_LAYERS = ['node_walk', 'node_block', 'edge'];
/* 旧守卫：Bot_GuardArea 是空类、Bot_GuardPos 只当 Bot_CrouchPos 基类 —— 所有模式都不使用 */
var LEGACY_LAYERS = { guard_area: 1, guard: 1 };
/* 模式 → 本模式真正生效的图层。依据：
 *   Bot.SpawnDelayEvent(0x10B32550)：只有 gameMode==0（团队）才加 GoCrouchPos
 *   Bot.Awake(0x10B2CEF0)：IsNanoMode 才加 NanoGuard，否则 CrabStep；gameMode==6 才有 BA_PickUpUpgradeBox
 *   MapManager.GetSpawnPoint(0x10AEB6E0)：team0=SP_BL、team1=SP_GR、其他=SP_Netural */
var MODE_LAYERS = {
  '团队模式': ['spawn_bl', 'spawn_gr', 'spawn_neutral', 'crouch_bl', 'crouch_gr', 'jump', 'tag_region'],
  '个人竞技': ['spawn_neutral', 'spawn_bl', 'spawn_gr', 'jump', 'tag_region'],
  '特殊战': ['spawn_bl', 'spawn_gr', 'spawn_neutral', 'jump', 'tag_region'],
  '生化模式': ['spawn_bl', 'spawn_gr', 'nano_area', 'nano_pos', 'jump', 'supply', 'tag_region'],
  '生化剑客模式': ['spawn_bl', 'spawn_gr', 'nano_area', 'nano_pos', 'jump', 'supply', 'tag_region'],
  '多人生化模式': ['spawn_bl', 'spawn_gr', 'nano_area', 'nano_pos', 'jump', 'supply', 'tag_region'],
  '终结者模式': ['spawn_bl', 'spawn_gr', 'nano_area', 'nano_pos', 'jump', 'supply', 'tag_region']
};
var MODE_NOTES = {
  '团队模式': '蹲守 BL/GR、双方出生点生效',
  '个人竞技': '主要用中立出生点，蹲守不生效',
  '特殊战': '出生点 + 跳跃链路为主，蹲守/守区不生效',
  '生化模式': '幽灵守区/守点 + 补给箱生效，蹲守不生效',
  '生化剑客模式': '幽灵守区/守点 + 补给箱生效，蹲守不生效',
  '多人生化模式': '守区/守点 + 补给箱 + 升级箱生效，蹲守不生效',
  '终结者模式': '守区/守点 + 补给箱 + 升级箱生效，蹲守不生效'
};
var SPAWN_LABEL = { 0: '幽灵出生（BL）', 1: '保卫者出生（GR）', 2: '中立出生', 3: '补给箱', 4: '红箱', 5: '蓝箱' };
/* 数据档：① 备份版 / ② 成品 / ② 编辑中。
 * 成品 = dev\final\<当前版本>；编辑中 = dev\packs\<图>\<包>；备份 = navdata\native。
 * ③ 部署版只是游戏运行目录（日志/配置用），不再作为可查看的数据档。 */

var ST = {
  wb: null,
  maps: [],
  cur: null,
  doc: null,
  nodes: [],
  edges: [],
  feats: [],
  routes: [],
  zones: [],
  jumpLinks: [],
  jumpOrphans: [],
  stats: null,
  nm: null,
  bounds: { lo: [-10, -10], hi: [10, 10] },
  cam: { cx: 0, cz: 0, zoom: 1 },
  show: { edges: true, grid: true, navmesh: true, labels: true, height: false, compass: true },
  layerVis: {},
  showAllLayers: false,
  focus: null,
  selLayer: null,
  selRoute: null,
  selZone: null,
  page: 'waypoints',
  logs: [],
  logFilter: '全部',
  showResolve: false,
  logTimer: null,
  busy: false,
  startPage: 'waypoints',
  startMap: '',
  startView: '',
  startPack: '',
  view: 'final',
  profileInfo: null,
  pack: '',
  packByFolder: {},
  pendingPack: '',
  pendingMap: '',
  dockUrl: '',
  dockOpen: false,
  dockHover: false,
  dockW: 480,
  dockWantOpen: false,
  autoDock: false
};

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
function pad2(n) { return n < 10 ? '0' + n : '' + n; }
function fmtBytes(n) {
  n = Number(n) || 0;
  if (n > 1048576) return (n / 1048576).toFixed(2) + ' MB';
  if (n > 1024) return (n / 1024).toFixed(0) + ' KB';
  return n + ' B';
}
function fmtNum(n) { return String(Math.round(Number(n) || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
function int(v) { return Math.round(Number(v) || 0); }
/* "2026-11-21 14:15:37" -> "11-21 14:15"；空串给 "—" */
function shortTime(s) {
  var m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/.exec(String(s || ''));
  return m ? (m[2] + '-' + m[3] + ' ' + m[4] + ':' + m[5]) : (s || '—');
}
function pct(n, d) { return d ? Math.round(n / d * 1000) / 10 : 0; }
function hexA(hex, a) {
  var m = String(hex || '#888').replace('#', '');
  if (m.length === 3) m = m[0] + m[0] + m[1] + m[1] + m[2] + m[2];
  var n = parseInt(m, 16);
  return 'rgba(' + ((n >> 16) & 255) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
}
function toast(msg, kind) {
  var t = $('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = 'on ' + (kind || '');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(function () { t.className = ''; }, kind === 'err' ? 5200 : 2800);
}
function setConn(ok, text) {
  var c = $('conn');
  if (!c) return;
  c.innerHTML = '<i style="background:' + (ok ? '#3ecf8e' : '#ff5c5c') +
    ';box-shadow:0 0 0 3px ' + (ok ? 'rgba(62,207,142,.14)' : 'rgba(255,92,92,.14)') +
    '"></i><span>' + esc(text) + '</span>';
}
function api(path) {
  return fetch(path, { cache: 'no-store' }).then(function (r) {
    return r.text().then(function (txt) {
      var j;
      try { j = JSON.parse(txt); } catch (e) { j = { ok: false, error: '返回不是 JSON（HTTP ' + r.status + '）' }; }
      if (!r.ok && (j.ok === undefined || j.ok === true)) j = { ok: false, error: 'HTTP ' + r.status };
      return j;
    });
  });
}

/* =====================================================================
 * 1. 模型
 * ===================================================================*/
function f3(v) { return (Math.round(Number(v) * 1000) / 1000).toFixed(3); }
function posKey(p) { return f3(p[0]) + ' ' + f3(p[1]) + ' ' + f3(p[2]); }
function dist2D(a, b) {
  var dx = a[0] - b[0], dz = a[2] - b[2];
  return Math.sqrt(dx * dx + dz * dz);
}
function dist3(a, b) {
  var dx = a[0] - b[0], dy = a[1] - b[1], dz = a[2] - b[2];
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

function buildModel(doc, txt) {
  ST.doc = doc;
  ST.nodes = [];
  ST.edges = [];
  ST.feats = [];
  ST.routes = [];
  ST.zones = [];
  ST.jumpLinks = [];
  ST.jumpOrphans = [];

  var rawNodes = doc.nodes || [];
  var id2uid = new Map();
  for (var i = 0; i < rawNodes.length; i++) {
    var n = rawNodes[i] || {};
    var p = n.p || [0, 0, 0];
    var node = {
      uid: ST.nodes.length, id: String(n.id || ('n' + i)),
      x: +p[0] || 0, y: +p[1] || 0, z: +p[2] || 0,
      tag: n.tag | 0, walk: n.walk === 0 ? 0 : 1, pen: n.pen | 0,
      alive: true, src: 0
    };
    ST.nodes.push(node);
    if (!id2uid.has(node.id)) id2uid.set(node.id, node.uid);
  }

  var seen = new Set();
  (doc.edges || []).forEach(function (e) {
    if (!e || e.length < 2) return;
    var a = id2uid.has(String(e[0])) ? id2uid.get(String(e[0])) : null;
    var b = id2uid.has(String(e[1])) ? id2uid.get(String(e[1])) : null;
    if (a == null || b == null || a === b) return;
    var k = a < b ? a + '|' + b : b + '|' + a;
    if (seen.has(k)) return;
    seen.add(k);
    ST.edges.push([a, b]);
  });

  (doc.features || []).forEach(function (f, k) {
    var kind = String(f.kind || '');
    var p = f.p || [0, 0, 0];
    ST.feats.push({
      i: k, id: String(f.id || ''), kind: kind, name: String(f.name || ''),
      aux: f.aux | 0, x: +p[0] || 0, y: +p[1] || 0, z: +p[2] || 0
    });
  });

  ST.routes = (doc.routes || []).map(function (r, k) {
    return {
      id: String(r.id || ('R' + (k + 1))), name: String(r.name || ('路线 ' + (k + 1))),
      color: String(r.color || COLORS.route), team: String(r.team || ''),
      closed: !!r.closed,
      pts: (r.pts || []).map(function (q) { return [+q[0] || 0, +q[1] || 0, +q[2] || 0]; })
    };
  });
  ST.zones = (doc.zones || []).map(function (z, k) {
    return {
      id: String(z.id || ('Z' + (k + 1))), name: String(z.name || ('区域 ' + (k + 1))),
      color: String(z.color || COLORS.zone), kind: String(z.kind || 'area'),
      shape: String(z.shape || 'poly'),
      pts: (z.pts || []).map(function (q) { return [+q[0] || 0, +q[1] || 0, +q[2] || 0]; })
    };
  });

  /* 跳跃链路：lines.jump 是插件真正导出的成对端点；先建好，
   * applyTxt 里的 jump add（测试包/成品清单里的手工跳链）再追加到同一个数组。 */
  var lines = doc.lines || {};
  var jumpLines = (lines.jump || []).filter(function (p) {
    return p && p.length >= 2 && p[0] && p[1];
  });
  ST.jumpLinks = jumpLines.map(function (pair, k) {
    return {
      id: 'J' + (k + 1), type: 'jump',
      a: [+pair[0][0] || 0, +pair[0][1] || 0, +pair[0][2] || 0],
      b: [+pair[1][0] || 0, +pair[1][1] || 0, +pair[1][2] || 0]
    };
  });
  ST.jumpOrphans = ST.feats.filter(function (f) { return f.kind === 'jump'; });

  if (txt && txt.exists && txt.text) applyTxt(txt.text);

  rebuild();
  ST.stats = modelStats();
  ST.bounds = modelBounds();
}

function applyTxt(text) {
  var rows = String(text || '').split(/\r?\n/);
  var replaceBase = false, keepNative = false;
  rows.forEach(function (line) {
    var s = line.trim();
    if (s === 'blank' || s === 'grow') replaceBase = true;
    else if (s === 'keep') keepNative = true;
  });
  /* C 侧：keep 与 blank/grow 互斥（keep 不被残留的 blank/grow 降级）。 */
  if (keepNative) replaceBase = false;
  /* grow / blank：原生点全禁、原生边全断，文件里的 node/edge add 就是全部路线。
   * keep：原生点保留，只把 add 加到图上（可视化结果 = 原生 + 增量）。 */
  if (replaceBase) {
    ST.nodes.forEach(function (n) { n.alive = false; });
    ST.edges = [];
  }
  var byPos = new Map();
  ST.nodes.forEach(function (n) {
    if (n.alive) byPos.set(posKey([n.x, n.y, n.z]), n.uid);
  });
  function find(p) {
    var k = posKey(p);
    if (byPos.has(k)) return byPos.get(k);
    var best = -1, bd = 0.35 * 0.35;
    ST.nodes.forEach(function (n) {
      if (!n.alive) return;
      var dx = n.x - p[0], dy = n.y - p[1], dz = n.z - p[2];
      var d = dx * dx + dy * dy + dz * dz;
      if (d <= bd) { bd = d; best = n.uid; }
    });
    return best;
  }
  var extraEdges = [];
  var extraJumps = [];
  rows.forEach(function (line) {
    var s = line.trim();
    if (!s || s.charAt(0) === '#') return;
    var t = s.split(/\s+/);
    if (t[0] === 'node' && (t[1] === 'add' || t[1] === 'del')) {
      var p = [+t[2], +t[3], +t[4]];
      if (!isFinite(p[0]) || !isFinite(p[1]) || !isFinite(p[2])) return;
      var u = find(p);
      if (t[1] === 'add') {
        if (u >= 0) { ST.nodes[u].alive = true; ST.nodes[u].walk = 1; }
        else {
          var nn = { uid: ST.nodes.length, id: 'txt' + ST.nodes.length, x: p[0], y: p[1], z: p[2],
                     tag: 0, walk: 1, pen: 0, alive: true, src: 1 };
          ST.nodes.push(nn);
          byPos.set(posKey(p), nn.uid);
        }
      } else if (u >= 0) {
        ST.nodes[u].alive = false;
      }
    } else if (t[0] === 'edge') {
      var op = String(t[1] || '');
      var add = op === 'add' || op === 'addout' || op === 'addin' || op === 'out' || op === 'in';
      var del = op === 'del' || op === 'delout' || op === 'delin';
      if (!add && !del) return;
      var a = find([+t[2], +t[3], +t[4]]);
      var b = find([+t[5], +t[6], +t[7]]);
      if (a < 0 || b < 0 || a === b) return;
      /* 2D 图不画方向：out/in 也按一条边显示；删边同理按无向删 */
      extraEdges.push([a, b, add]);
    } else if (t[0] === 'jump' && (t[1] === 'add' || t[1] === 'jumpadd')) {
      var a3 = [+t[2], +t[3], +t[4]], b3 = [+t[5], +t[6], +t[7]];
      if (!isFinite(a3[0]) || !isFinite(a3[1]) || !isFinite(a3[2]) ||
          !isFinite(b3[0]) || !isFinite(b3[1]) || !isFinite(b3[2])) return;
      extraJumps.push({ type: 'jump', a: a3, b: b3, fromTxt: true });
    }
  });
  if (extraEdges.length) {
    var set = new Set(ST.edges.map(function (e) { return Math.min(e[0], e[1]) + '|' + Math.max(e[0], e[1]); }));
    extraEdges.forEach(function (e) {
      var k = Math.min(e[0], e[1]) + '|' + Math.max(e[0], e[1]);
      if (e[2]) { if (!set.has(k)) { set.add(k); ST.edges.push([e[0], e[1]]); } }
      else if (set.has(k)) {
        set.delete(k);
        ST.edges = ST.edges.filter(function (x) {
          return !((x[0] === e[0] && x[1] === e[1]) || (x[0] === e[1] && x[1] === e[0]));
        });
      }
    });
  }
  extraJumps.forEach(function (j) {
    j.id = 'J' + (ST.jumpLinks.length + 1);
    ST.jumpLinks.push(j);
  });
}

function rebuild() {
  ST.adj = new Map();
  ST.nodes.forEach(function (n) { if (n.alive) ST.adj.set(n.uid, []); });
  ST.edges = ST.edges.filter(function (e) {
    var a = ST.nodes[e[0]], b = ST.nodes[e[1]];
    return a && b && a.alive && b.alive;
  });
  ST.edges.forEach(function (e) {
    if (ST.adj.has(e[0]) && ST.adj.has(e[1])) {
      ST.adj.get(e[0]).push(e[1]);
      ST.adj.get(e[1]).push(e[0]);
    }
  });
}

function modelStats() {
  var alive = 0, walkable = 0, isolated = 0, degreeGt6 = 0, maxDegree = 0;
  ST.nodes.forEach(function (n) {
    if (!n.alive) return;
    alive++;
    if (n.walk) walkable++;
    var d = (ST.adj.get(n.uid) || []).length;
    if (!d) isolated++;
    if (d > 6) degreeGt6++;
    if (d > maxDegree) maxDegree = d;
  });
  var comps = 0, seen = new Set();
  ST.nodes.forEach(function (n) {
    if (!n.alive || seen.has(n.uid)) return;
    comps++;
    var q = [n.uid];
    seen.add(n.uid);
    while (q.length) {
      var u = q.pop();
      (ST.adj.get(u) || []).forEach(function (v) {
        if (!seen.has(v)) { seen.add(v); q.push(v); }
      });
    }
  });
  var kinds = {};
  ST.feats.forEach(function (f) { kinds[f.kind] = (kinds[f.kind] || 0) + 1; });
  return {
    nodes: alive, walkable: walkable, edges: ST.edges.length,
    isolated: isolated, components: comps, degreeGt6: degreeGt6, maxDegree: maxDegree,
    features: ST.feats.length, kinds: kinds,
    routes: ST.routes.length, zones: ST.zones.length,
    jumpLinks: ST.jumpLinks.length, jumpEndpoints: ST.jumpOrphans.length
  };
}

function modelBounds() {
  var lo = [1e9, 1e9], hi = [-1e9, -1e9], any = false;
  function add(x, z) {
    any = true;
    if (x < lo[0]) lo[0] = x;
    if (z < lo[1]) lo[1] = z;
    if (x > hi[0]) hi[0] = x;
    if (z > hi[1]) hi[1] = z;
  }
  ST.nodes.forEach(function (n) { if (n.alive) add(n.x, n.z); });
  ST.feats.forEach(function (f) { add(f.x, f.z); });
  ST.routes.forEach(function (r) { r.pts.forEach(function (p) { add(p[0], p[2]); }); });
  ST.zones.forEach(function (z) { z.pts.forEach(function (p) { add(p[0], p[2]); }); });
  if (!any) {
    var b = (ST.doc && ST.doc.map && ST.doc.map.bbox) || null;
    if (b && b.length >= 2) {
      lo = [+b[0][0] || 0, +b[0][2] || 0];
      hi = [+b[1][0] || 0, +b[1][2] || 0];
      any = true;
    }
  }
  if (!any) { lo = [-10, -10]; hi = [10, 10]; }
  if (hi[0] - lo[0] < 2) { lo[0] -= 1; hi[0] += 1; }
  if (hi[1] - lo[1] < 2) { lo[1] -= 1; hi[1] += 1; }
  return { lo: lo, hi: hi };
}

function auxCount(kind, aux) {
  var n = 0;
  ST.feats.forEach(function (f) { if (f.kind === kind && f.aux === aux) n++; });
  return n;
}
function featKey(f) {
  if (f.kind === 'spawn') {
    /* aux 跟 MapManager 偏移一一对应：0=SP_BL@0x10，1=SP_GR@0x14，2=SP_Netural@0x18 */
    if (f.aux === 0) return 'spawn_bl';
    if (f.aux === 1) return 'spawn_gr';
    if (f.aux === 2) return 'spawn_neutral';
    return 'supply';
  }
  if (f.kind === 'crouch') return f.aux === 0 ? 'crouch_bl' : 'crouch_gr';
  return f.kind;
}
function featLabel(f) {
  if (f.kind === 'spawn') return SPAWN_LABEL[f.aux] || '出生点';
  if (f.kind === 'crouch') return f.aux === 0 ? '蹲守 BL' : '蹲守 GR';
  if (f.kind === 'guard') return '旧守卫点（游戏未使用）';
  if (f.kind === 'guard_area') return '旧守卫区（游戏未使用）';
  return f.name || KIND_LABEL[f.kind] || '';
}
function curMode() { return (ST.cur && ST.cur.mode) || ''; }
function modeAllows(key) {
  if (CORE_LAYERS.indexOf(key) >= 0) return true;
  if (LEGACY_LAYERS[key]) return true;          /* 保留但标「游戏未使用」 */
  var allow = MODE_LAYERS[curMode()];
  if (!allow) return true;                      /* 隐藏地图 / 未识别：不筛 */
  return allow.indexOf(key) >= 0;
}
function layerVisible(key) { return ST.layerVis[key] !== false; }

function layerDefs() {
  var s = ST.stats || modelStats();
  var k = s.kinds;
  return [
    { group: '点图 / 寻路（A）', letter: 'A', items: [
      { key: 'node_walk', name: '可走路点', sub: 'PointNode · walkable=1', color: COLORS.node_walk, count: s.walkable, cls: 'PointNode' },
      { key: 'node_block', name: '不可走路点', sub: 'GraphNode.flags bit0=0', color: COLORS.node_block, count: s.nodes - s.walkable, cls: 'GraphNode.flags' },
      { key: 'edge', name: '自动连边', sub: 'PointNode.connections', color: COLORS.edge, count: s.edges, cls: 'Connection' }
    ] },
    { group: '出生 / 补给（D 层）', letter: 'B', items: [
      { key: 'spawn_bl', name: '幽灵出生', sub: 'SP_BL · Team.BlackList', color: COLORS.spawn_bl, count: auxCount('spawn', 0), cls: 'MapManager.SP_BL' },
      { key: 'spawn_gr', name: '保卫者出生', sub: 'SP_GR · Team.GlobalRisk', color: COLORS.spawn_gr, count: auxCount('spawn', 1), cls: 'MapManager.SP_GR' },
      { key: 'spawn_neutral', name: '中立出生', sub: 'SP_Netural · 个人竞技主要用', color: COLORS.spawn_neutral, count: auxCount('spawn', 2), cls: 'MapManager.SP_Netural' },
      { key: 'supply', name: '补给箱 / 红蓝箱', sub: 'SP_SupplyBox / RedBox / BlueBox', color: COLORS.supply, count: auxCount('spawn', 3) + auxCount('spawn', 4) + auxCount('spawn', 5), cls: 'SP_SupplyBox + SupplyBox' }
    ] },
    { group: '人机行为点（B 层）', letter: 'C', items: [
      { key: 'crouch_bl', name: '蹲守点 · 幽灵', sub: 'Bot_CrouchPos team=0', color: COLORS.crouch_bl, count: auxCount('crouch', 0), cls: 'Bot_CrouchPos' },
      { key: 'crouch_gr', name: '蹲守点 · 保卫', sub: 'Bot_CrouchPos team=1', color: COLORS.crouch_gr, count: auxCount('crouch', 1), cls: 'Bot_CrouchPos' },
      { key: 'jump', name: '跳跃链接端点', sub: 'Bot_JumpLink · links[]', color: COLORS.jump, count: (k.jump || 0), cls: 'Bot_JumpLink' }
    ] },
    { group: '区域类（C 层）', letter: 'D', items: [
      { key: 'nano_area', name: '幽灵守区', sub: 'Bot_NanoGuardArea', color: COLORS.nano_area, count: (k.nano_area || 0), cls: 'Bot_NanoGuardArea' },
      { key: 'nano_pos', name: '幽灵守点', sub: 'Bot_NanoGuardPos', color: COLORS.nano_pos, count: (k.nano_pos || 0), cls: 'Bot_NanoGuardPos' },
      { key: 'guard_area', name: '旧守卫区', sub: 'Bot_GuardArea · 游戏未使用', color: COLORS.guard_area, count: (k.guard_area || 0), cls: 'Bot_GuardArea' },
      { key: 'guard', name: '旧守卫点', sub: 'Bot_GuardPos · 游戏未使用', color: COLORS.guard, count: (k.guard || 0), cls: 'Bot_GuardPos' },
      { key: 'tag_region', name: '标签区', sub: 'PointNodeTagModifier', color: COLORS.tag_region, count: (k.tag_region || 0), cls: 'PointNodeTagModifier' }
    ] }
  ];
}

/* =====================================================================
 * 2. 画布
 * ===================================================================*/
function ctxOf(cv) {
  var r = cv.getBoundingClientRect();
  var w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
  var dpr = window.devicePixelRatio || 1;
  if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) {
    cv.width = Math.round(w * dpr);
    cv.height = Math.round(h * dpr);
  }
  var c = cv.getContext('2d');
  c.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { c: c, w: w, h: h };
}
function viewOf(cv) {
  var r = cv.getBoundingClientRect();
  var w = Math.max(1, r.width), h = Math.max(1, r.height);
  var b = ST.bounds;
  var dx = Math.max(1e-3, b.hi[0] - b.lo[0]), dz = Math.max(1e-3, b.hi[1] - b.lo[1]);
  var pad = 26;
  var s0 = Math.min(Math.max(1, w - pad * 2) / dx, Math.max(1, h - pad * 2) / dz);
  return { w: w, h: h, s: Math.max(0.04, Math.min(80, s0 * ST.cam.zoom)) };
}
function w2s(x, z, v) {
  return [ (x - ST.cam.cx) * v.s + v.w / 2, (z - ST.cam.cz) * v.s + v.h / 2 ];
}
function s2w(px, py, v) {
  return [ (px - v.w / 2) / v.s + ST.cam.cx, (py - v.h / 2) / v.s + ST.cam.cz ];
}
function niceStep(s) {
  var want = 46 / s;
  var steps = [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200];
  for (var i = 0; i < steps.length; i++) if (steps[i] >= want) return steps[i];
  return 500;
}
function fitCam() {
  var b = ST.bounds;
  ST.cam.cx = (b.lo[0] + b.hi[0]) / 2;
  ST.cam.cz = (b.lo[1] + b.hi[1]) / 2;
  ST.cam.zoom = 1;
}
function fitToPoints(pts) {
  if (!pts || !pts.length) { fitCam(); return; }
  var lo = [1e9, 1e9], hi = [-1e9, -1e9];
  pts.forEach(function (p) {
    if (p[0] < lo[0]) lo[0] = p[0];
    if (p[2] < lo[1]) lo[1] = p[2];
    if (p[0] > hi[0]) hi[0] = p[0];
    if (p[2] > hi[1]) hi[1] = p[2];
  });
  if (hi[0] - lo[0] < 2) { lo[0] -= 2; hi[0] += 2; }
  if (hi[1] - lo[1] < 2) { lo[1] -= 2; hi[1] += 2; }
  ST.cam.cx = (lo[0] + hi[0]) / 2;
  ST.cam.cz = (lo[1] + hi[1]) / 2;
  var b = ST.bounds;
  var dx = Math.max(2, hi[0] - lo[0]), dz = Math.max(2, hi[1] - lo[1]);
  var bdx = Math.max(2, b.hi[0] - b.lo[0]), bdz = Math.max(2, b.hi[1] - b.lo[1]);
  ST.cam.zoom = Math.min(6, Math.max(1, Math.min(bdx / dx, bdz / dz) * 0.85));
  drawAll();
}

function drawEmpty(c, w, h, text) {
  c.fillStyle = '#33404f';
  c.font = '11px "Microsoft YaHei UI",sans-serif';
  c.textAlign = 'center';
  c.fillText(text, w / 2, h / 2);
}

/* ---- 方向（东南西北）--------------------------------------------------
 * 全工具只有这一套约定，改这里要连 navview.html 的罗盘、控制台说明、
 * src/editor.c 的游戏内罗盘一起改：
 *
 *   北 = 世界 -Z（平面图 / 3D 俯视的正上方）   东 = 世界 +X（右）
 *   南 = 世界 +Z（下）                        西 = 世界 -X（左）
 *
 * 为什么北是 -Z：平面图把世界 x 画到屏幕右、z 画到屏幕下，3D 俯视
 * （navview 的「俯视」按钮 yaw=0）屏幕上方同样是 -Z。这样「图的上方 = 北」
 * 在平面图和 3D 里是同一件事，游戏内罗盘也照这个算。
 * yaw = 视线朝向（弧度，0 = 朝 -Z；与 navview 的 S.v3.yaw 同义）。 */
var DIR4 = [
  { name: '北', x: 0, z: -1 },
  { name: '东', x: 1, z: 0 },
  { name: '南', x: 0, z: 1 },
  { name: '西', x: -1, z: 0 }
];
var DIR8 = ['北', '东北', '东', '东南', '南', '西南', '西', '西北'];
var DIR_GOLD = '#ffd24a';
var DIR_DIM = 'rgba(168,190,214,.92)';

/* 世界方向 (dx,dz) 在画面上从「正上方」顺时针的落点：返回单位向量 [右, 上] */
function dirScreen(dx, dz, yaw) {
  var cy = Math.cos(yaw || 0), sy = Math.sin(yaw || 0);
  var right = dx * cy - dz * sy;
  var up = -(dx * sy + dz * cy);
  var l = Math.sqrt(right * right + up * up) || 1;
  return [right / l, up / l];
}
/* 画面上方正对着的世界方向（八向中文名） */
function dirHeading(yaw) {
  var best = 0, bestUp = -2;
  for (var i = 0; i < 8; i++) {
    var a = i * Math.PI / 4;
    var v = dirScreen(Math.sin(a), -Math.cos(a), yaw);
    if (v[1] > bestUp) { bestUp = v[1]; best = i; }
  }
  return DIR8[best];
}
function dirCss(size, weight) {
  return (weight || 600) + ' ' + Math.round(size) + 'px "Microsoft YaHei UI","Segoe UI",sans-serif';
}
/* 罗盘：四方位字 + 中心当前朝向 + 顶部三角（画面正上方） */
function drawCompassRose(c, cx, cy, R, yaw) {
  var head = dirHeading(yaw);
  var fs = Math.max(9, R * 0.36);
  var rr = R + fs * 0.95;          /* 圆环比方位字再外一圈，字不压线 */
  c.save();
  c.beginPath();
  c.arc(cx, cy, rr, 0, Math.PI * 2);
  c.fillStyle = 'rgba(8,12,17,.68)';
  c.fill();
  c.strokeStyle = 'rgba(126,158,196,.32)';
  c.lineWidth = 1;
  c.stroke();
  c.textAlign = 'center';
  c.textBaseline = 'middle';
  /* 圆环外面的小三角：它指着哪，就是「你正对着哪」 */
  c.beginPath();
  c.moveTo(cx, cy - rr - fs * 0.98);
  c.lineTo(cx - fs * 0.36, cy - rr - fs * 0.22);
  c.lineTo(cx + fs * 0.36, cy - rr - fs * 0.22);
  c.closePath();
  c.fillStyle = DIR_GOLD;
  c.fill();
  c.font = dirCss(fs * 0.92);
  /* 最靠近正上方的那一格点亮（正好 45° 时取先出现的那个；游戏内罗盘同一规则） */
  var v4 = DIR4.map(function (d) { return dirScreen(d.x, d.z, yaw); });
  var lit = 0, k;
  for (k = 1; k < 4; k++) if (v4[k][1] > v4[lit][1]) lit = k;
  DIR4.forEach(function (d, i) {
    c.fillStyle = (i === lit) ? DIR_GOLD : DIR_DIM;
    c.fillText(d.name, cx + v4[i][0] * R, cy - v4[i][1] * R);
  });
  c.font = dirCss(fs * 1.05, 700);
  c.fillStyle = '#e8f2ff';
  c.fillText(head, cx, cy + 0.5);
  c.restore();
}
/* 平面图四条边上的方位字（俯视图固定「上 = 北」） */
function drawCompassEdges(c, w, h) {
  var fs = '600 11px "Microsoft YaHei UI","Segoe UI",sans-serif';
  c.save();
  c.textAlign = 'center';
  c.textBaseline = 'middle';
  c.font = fs;
  c.fillStyle = DIR_GOLD;
  c.fillText('北', w / 2, 13);
  c.fillStyle = 'rgba(150,176,206,.75)';
  c.fillText('南', w / 2, h - 11);
  c.fillText('东', w - 13, h / 2);
  c.fillText('西', 13, h / 2);
  c.restore();
}
/* 2D 地图上的方向层：角落罗盘 + 四边方位字；由「方向」开关控制。
 * 俯视图不会转镜头，所以 yaw 恒为 0（北永远在图的上方）。 */
function drawCompass(c, v) {
  drawCompassEdges(c, v.w, v.h);
  var R = Math.max(20, Math.min(34, Math.min(v.w, v.h) * 0.062));
  var pad = R + 26;
  drawCompassRose(c, v.w - pad, v.h - pad, R, 0);
}

/* ---- 可走面（A* NavMeshGraph）：插件导出的 UCFNM3，格式同 navview.html ----
 *   "UCFNM3\0" | int32 nv | int32 索引数 | int32 ntile | uint8 flags[4]
 *   | float matrix[16] | float translation[3]
 *   | int32 verts[nv*3] | int32 gverts[nv*3] | tris[nt*3]
 * 顶点 1/1000 m，已是世界坐标；索引是绝对下标。 */
function parseNavm(buf) {
  var dv = new DataView(buf);
  var magic = String.fromCharCode(dv.getUint8(0), dv.getUint8(1), dv.getUint8(2),
                                   dv.getUint8(3), dv.getUint8(4), dv.getUint8(5));
  if (magic !== 'UCFNM3') throw new Error('文件头不是 UCFNM3');
  var nv = dv.getInt32(7, true), nti = dv.getInt32(11, true), ntile = dv.getInt32(15, true);
  if (nv <= 0 || nti <= 0 || nv > 3000000 || nti > 9000000) throw new Error('顶点/索引数不合理');
  var nt = Math.floor(nti / 3);
  var off = 99;
  var verts = new Float32Array(nv * 3);
  var lo = [1e9, 1e9], hi = [-1e9, -1e9];
  for (var i = 0; i < nv * 3; i += 3) {
    var x = dv.getInt32(off + i * 4, true) / 1000;
    var y = dv.getInt32(off + (i + 1) * 4, true) / 1000;
    var z = dv.getInt32(off + (i + 2) * 4, true) / 1000;
    verts[i] = x; verts[i + 1] = y; verts[i + 2] = z;
    if (x < lo[0]) lo[0] = x; if (x > hi[0]) hi[0] = x;
    if (z < lo[1]) lo[1] = z; if (z > hi[1]) hi[1] = z;
  }
  off += nv * 12 * 2;   // 跳过 gverts
  var idx = new Uint32Array(nt * 3);
  for (var k = 0; k < nt * 3; k++) idx[k] = dv.getUint32(off + k * 4, true);
  return { nv: nv, tri: nt, ntile: ntile, verts: verts, idx: idx, lo: lo, hi: hi };
}

function loadNavmesh(level) {
  ST.nm = null;
  if (!level) return Promise.resolve(null);
  var want = level;
  return fetch('/api/navmesh?level=' + encodeURIComponent(level), { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.arrayBuffer(); })
    .then(function (buf) {
      var nm = parseNavm(buf);
      if (ST.cur && ST.cur.level === want) ST.nm = nm;
      return nm;
    })
    .catch(function () { return null; });
}

function nmBounds(nm) {
  var lo = [nm.lo[0], nm.lo[1]], hi = [nm.hi[0], nm.hi[1]];
  if (hi[0] - lo[0] < 2) { lo[0] -= 1; hi[0] += 1; }
  if (hi[1] - lo[1] < 2) { lo[1] -= 1; hi[1] += 1; }
  return { lo: lo, hi: hi };
}

function drawNavmesh(c, v) {
  if (!ST.nm || !ST.nm.idx.length) return;
  var verts = ST.nm.verts, idx = ST.nm.idx;
  c.beginPath();
  for (var i = 0; i < idx.length; i += 3) {
    var a = idx[i] * 3, b = idx[i + 1] * 3, d = idx[i + 2] * 3;
    if (a + 2 >= verts.length || b + 2 >= verts.length || d + 2 >= verts.length) continue;
    var pa = w2s(verts[a], verts[a + 2], v);
    var pb = w2s(verts[b], verts[b + 2], v);
    var pd = w2s(verts[d], verts[d + 2], v);
    c.moveTo(pa[0], pa[1]);
    c.lineTo(pb[0], pb[1]);
    c.lineTo(pd[0], pd[1]);
    c.closePath();
  }
  c.fillStyle = 'rgba(38,224,142,.055)';
  c.fill();
  c.strokeStyle = 'rgba(38,224,142,.22)';
  c.lineWidth = Math.max(0.35, Math.min(1, v.s * 0.05));
  c.stroke();
}

function drawGrid(c, v) {
  var step = niceStep(v.s);
  var b = ST.bounds;
  var x0 = Math.floor(b.lo[0] / step) * step, x1 = Math.ceil(b.hi[0] / step) * step;
  var z0 = Math.floor(b.lo[1] / step) * step, z1 = Math.ceil(b.hi[1] / step) * step;
  c.lineWidth = 0.5;
  for (var x = x0; x <= x1; x += step) {
    c.strokeStyle = Math.abs(x) < 1e-6 ? '#1b2938' : '#101720';
    var p = w2s(x, 0, v);
    c.beginPath(); c.moveTo(p[0], 0); c.lineTo(p[0], v.h); c.stroke();
  }
  for (var z = z0; z <= z1; z += step) {
    c.strokeStyle = Math.abs(z) < 1e-6 ? '#1b2938' : '#101720';
    var q = w2s(0, z, v);
    c.beginPath(); c.moveTo(0, q[1]); c.lineTo(v.w, q[1]); c.stroke();
  }
}

function drawGraph(c, v, dim) {
  var alpha = dim == null ? 1 : dim;
  if (!ST.nodes.length) return;
  if (ST.show.edges && layerVisible('edge')) {
    c.strokeStyle = 'rgba(126,152,183,' + (0.2 * alpha) + ')';
    c.lineWidth = Math.max(0.4, Math.min(1.1, v.s * 0.12));
    c.beginPath();
    for (var i = 0; i < ST.edges.length; i++) {
      var e = ST.edges[i];
      var a = ST.nodes[e[0]], b = ST.nodes[e[1]];
      if (!a || !b || !a.alive || !b.alive) continue;
      var pa = w2s(a.x, a.z, v), pb = w2s(b.x, b.z, v);
      c.moveTo(pa[0], pa[1]); c.lineTo(pb[0], pb[1]);
    }
    c.stroke();
  }
  var yLo = 1e9, yHi = -1e9;
  ST.nodes.forEach(function (n) {
    if (!n.alive) return;
    if (n.y < yLo) yLo = n.y;
    if (n.y > yHi) yHi = n.y;
  });
  var rad = Math.max(1.4, Math.min(3.2, v.s * 0.32));
  for (var k = 0; k < ST.nodes.length; k++) {
    var n = ST.nodes[k];
    if (!n.alive) continue;
    var key = n.walk ? 'node_walk' : 'node_block';
    if (!layerVisible(key)) continue;
    var q = w2s(n.x, n.z, v);
    if (q[0] < -20 || q[1] < -20 || q[0] > v.w + 20 || q[1] > v.h + 20) continue;
    var col = n.walk ? COLORS.node_walk : COLORS.node_block;
    if (ST.show.height && yHi > yLo + 0.5) {
      var t = (n.y - yLo) / (yHi - yLo);
      col = 'hsl(' + Math.round(200 - t * 190) + ',72%,' + Math.round(42 + t * 18) + '%)';
    }
    c.globalAlpha = alpha;
    c.beginPath();
    c.arc(q[0], q[1], n.walk ? rad : rad * 0.72, 0, Math.PI * 2);
    c.fillStyle = col;
    c.fill();
    c.globalAlpha = 1;
  }
}

function drawRoutes(c, v, kind) {
  ST.routes.forEach(function (r, i) {
    if (!r.pts.length) return;
    var active = kind === 'route' && ST.selRoute && ST.selRoute.type === 'route' && ST.selRoute.index === i;
    c.beginPath();
    r.pts.forEach(function (p, j) {
      var q = w2s(p[0], p[2], v);
      if (j === 0) c.moveTo(q[0], q[1]); else c.lineTo(q[0], q[1]);
    });
    if (r.closed) c.closePath();
    c.strokeStyle = hexA(r.color, active ? 0.98 : 0.55);
    c.lineWidth = active ? 2.4 : 1.2;
    c.stroke();
    r.pts.forEach(function (p) {
      var q = w2s(p[0], p[2], v);
      c.beginPath(); c.arc(q[0], q[1], active ? 2.8 : 1.8, 0, Math.PI * 2);
      c.fillStyle = hexA(r.color, active ? 1 : 0.75); c.fill();
    });
    if (ST.show.labels) {
      var q0 = w2s(r.pts[0][0], r.pts[0][2], v);
      c.fillStyle = hexA(r.color, 0.95);
      c.font = '9px Consolas,monospace';
      c.textAlign = 'left';
      c.fillText(r.id + ' ' + r.name, q0[0] + 6, q0[1] - 8);
    }
  });
}

function drawZones(c, v) {
  ST.zones.forEach(function (z, i) {
    if (!z.pts.length) return;
    var active = ST.selZone && ST.selZone.type === 'zone' && ST.selZone.index === i;
    c.beginPath();
    z.pts.forEach(function (p, j) {
      var q = w2s(p[0], p[2], v);
      if (j === 0) c.moveTo(q[0], q[1]); else c.lineTo(q[0], q[1]);
    });
    c.closePath();
    c.fillStyle = hexA(z.color, active ? 0.22 : 0.08);
    c.fill();
    c.strokeStyle = hexA(z.color, active ? 0.95 : 0.5);
    c.lineWidth = active ? 1.8 : 1;
    c.setLineDash([4, 3]);
    c.stroke();
    c.setLineDash([]);
    if (ST.show.labels) {
      var q0 = w2s(z.pts[0][0], z.pts[0][2], v);
      c.fillStyle = hexA(z.color, 0.95);
      c.font = '9px Consolas,monospace';
      c.textAlign = 'left';
      c.fillText(z.id + ' ' + z.name, q0[0] + 5, q0[1] - 6);
    }
  });
}

function drawFeature(c, f, v, alpha) {
  var key = featKey(f);
  if (!layerVisible(key)) return;
  var q = w2s(f.x, f.z, v);
  if (q[0] < -30 || q[1] < -30 || q[0] > v.w + 30 || q[1] > v.h + 30) return;
  var col = COLORS[key] || '#ffd633';
  var focus = ST.focus === key;
  var a = alpha == null ? 1 : alpha;
  if (ST.focus && !focus) a = Math.min(a, 0.22);
  c.globalAlpha = a;
  c.strokeStyle = hexA(col, 0.95);
  c.fillStyle = hexA(col, 0.9);
  c.lineWidth = focus ? 1.8 : 1.1;

  if (f.kind === 'spawn') {
    c.beginPath();
    c.rect(q[0] - 3.2, q[1] - 3.2, 6.4, 6.4);
    c.fillStyle = hexA(col, focus ? 0.9 : 0.65);
    c.fill();
    c.stroke();
    if (focus) {
      c.beginPath(); c.arc(q[0], q[1], 8, 0, Math.PI * 2);
      c.strokeStyle = hexA(col, 0.5); c.setLineDash([2, 2]); c.stroke(); c.setLineDash([]);
    }
  } else if (f.kind === 'crouch') {
    c.beginPath();
    c.moveTo(q[0], q[1] - 4.6);
    c.lineTo(q[0] + 4.2, q[1] + 3.4);
    c.lineTo(q[0] - 4.2, q[1] + 3.4);
    c.closePath();
    c.fillStyle = hexA(col, focus ? 0.85 : 0.55);
    c.fill();
    c.stroke();
  } else if (f.kind === 'jump') {
    c.beginPath();
    c.moveTo(q[0], q[1] - 5);
    c.lineTo(q[0] + 5, q[1]);
    c.lineTo(q[0], q[1] + 5);
    c.lineTo(q[0] - 5, q[1]);
    c.closePath();
    c.fillStyle = hexA(col, focus ? 0.9 : 0.6);
    c.fill();
    c.stroke();
  } else if (f.kind === 'nano_area' || f.kind === 'guard_area') {
    c.beginPath();
    c.arc(q[0], q[1], focus ? 9 : 6.5, 0, Math.PI * 2);
    c.fillStyle = hexA(col, focus ? 0.22 : 0.1);
    c.fill();
    c.stroke();
    c.beginPath(); c.arc(q[0], q[1], 1.6, 0, Math.PI * 2);
    c.fillStyle = col; c.fill();
  } else if (f.kind === 'tag_region') {
    c.beginPath();
    c.moveTo(q[0], q[1] - 6);
    c.lineTo(q[0] + 5, q[1] - 3);
    c.lineTo(q[0], q[1]);
    c.lineTo(q[0], q[1] + 5);
    c.stroke();
  } else {
    c.beginPath();
    c.arc(q[0], q[1], focus ? 4 : 2.6, 0, Math.PI * 2);
    c.fillStyle = hexA(col, focus ? 0.95 : 0.7);
    c.fill();
    c.stroke();
  }
  if (ST.show.labels && (focus || f.kind === 'nano_area' || f.kind === 'guard_area' || v.s > 9)) {
    c.globalAlpha = Math.min(1, a + 0.1);
    c.fillStyle = hexA(col, 0.95);
    c.font = '8.5px Consolas,monospace';
    c.textAlign = 'left';
    c.fillText(featLabel(f), q[0] + 7, q[1] - 6);
  }
  c.globalAlpha = 1;
}

function drawJumpLinks(c, v, kind) {
  ST.jumpLinks.forEach(function (j, i) {
    var active = kind === 'route' && ST.selRoute && ST.selRoute.type === 'jump' && ST.selRoute.index === i;
    if (!active && kind === 'route') {
      // 其他链路仍画淡一点
    }
    var a = w2s(j.a[0], j.a[2], v), b = w2s(j.b[0], j.b[2], v);
    c.strokeStyle = active ? '#e8fbff' : 'rgba(56,217,245,.75)';
    c.lineWidth = active ? 2.2 : 1;
    c.setLineDash(active ? [] : [4, 3]);
    c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke();
    c.setLineDash([]);
    [a, b].forEach(function (q) {
      c.beginPath(); c.arc(q[0], q[1], active ? 3 : 2, 0, Math.PI * 2);
      c.fillStyle = active ? '#e8fbff' : '#38d9f5'; c.fill();
    });
    if (ST.show.labels && (kind === 'route' || v.s > 2)) {
      var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
      c.fillStyle = active ? '#e8fbff' : 'rgba(95,211,230,.9)';
      c.font = '8px Consolas,monospace';
      c.textAlign = 'center';
      c.fillText(j.id, mx, my - 6);
    }
  });
  if (kind === 'route' && ST.jumpOrphans.length && !ST.jumpLinks.length) {
    ST.jumpOrphans.forEach(function (f) {
      var q = w2s(f.x, f.z, v);
      c.beginPath();
      c.moveTo(q[0], q[1] - 4);
      c.lineTo(q[0] + 4, q[1]);
      c.lineTo(q[0], q[1] + 4);
      c.lineTo(q[0] - 4, q[1]);
      c.closePath();
      c.strokeStyle = 'rgba(56,217,245,.8)';
      c.stroke();
    });
  }
}

function drawMap(cv, kind) {
  if (!cv) return;
  var g = ctxOf(cv), c = g.c, W = g.w, H = g.h;
  c.clearRect(0, 0, W, H);
  c.fillStyle = '#080c12'; c.fillRect(0, 0, W, H);
  if (!ST.nm && !ST.nodes.length && !ST.feats.length) {
    var emptyText = !ST.cur ? '请选择地图'
      : (ST.cur.noPointGraph ? '这张图没有可走面导出'
      : (ST.cur.status === 'missing' ? '这张图还没有采集数据' : '没有载入地图'));
    drawEmpty(c, W, H, emptyText);
    return;
  }
  var v = viewOf(cv);
  if (ST.show.grid) drawGrid(c, v);
  if (ST.show.navmesh) drawNavmesh(c, v);
  if (kind !== 'route') drawZones(c, v);
  if (kind !== 'zone') drawRoutes(c, v, kind);
  var dim = ST.focus ? 1 : 1;
  drawGraph(c, v, dim);
  if (kind === 'route') drawJumpLinks(c, v, kind);
  ST.feats.forEach(function (f) { drawFeature(c, f, v, 1); });
  if (kind === 'zone') drawZoneGroups(c, v);
  if (kind === 'main' && ST.focus && (ST.focus === 'jump')) drawJumpLinks(c, v, 'main');
  if (ST.show.compass) drawCompass(c, v);
}

/* =====================================================================
 * 3. 区域分组（守区 + 最近的守点）
 * ===================================================================*/
function zoneGroups() {
  var areas = [];
  ST.feats.forEach(function (f, i) {
    if (f.kind === 'nano_area' || f.kind === 'guard_area') {
      areas.push({ type: 'area', kind: f.kind, fid: i, name: f.name || KIND_LABEL[f.kind],
                   x: f.x, y: f.y, z: f.z, aux: f.aux, pts: [] });
    }
  });
  ST.feats.forEach(function (f) {
    if (f.kind !== 'nano_pos' && f.kind !== 'guard') return;
    var family = f.kind === 'nano_pos' ? 'nano_area' : 'guard_area';
    var best = null, bd = 1e18;
    areas.forEach(function (a) {
      if (a.kind !== family) return;
      var dx = a.x - f.x, dz = a.z - f.z;
      var d = dx * dx + dz * dz;
      if (d < bd) { bd = d; best = a; }
    });
    if (best) best.pts.push(f);
    else {
      var key = f.kind === 'nano_pos' ? 'nano_pos' : 'guard';
      var g = areas.filter(function (a) { return a.type === 'loose' && a.kind === key; })[0];
      if (!g) {
        g = { type: 'loose', kind: key, name: f.kind === 'nano_pos' ? '未归属幽灵守点' : '未归属旧守卫点',
              x: f.x, y: f.y, z: f.z, pts: [] };
        areas.push(g);
      }
      g.pts.push(f);
    }
  });
  return areas;
}

function convexHull(points) {
  var pts = points.map(function (f) { return [f.x, f.z]; }).sort(function (a, b) {
    return a[0] - b[0] || a[1] - b[1];
  });
  if (pts.length <= 2) return pts;
  function cross(o, a, b) { return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]); }
  var lower = [];
  pts.forEach(function (p) {
    while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], p) <= 0) lower.pop();
    lower.push(p);
  });
  var upper = [];
  for (var i = pts.length - 1; i >= 0; i--) {
    var p = pts[i];
    while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], p) <= 0) upper.pop();
    upper.push(p);
  }
  lower.pop(); upper.pop();
  return lower.concat(upper);
}

function drawZoneGroups(c, v) {
  var groups = zoneGroups();
  groups.forEach(function (g, i) {
    if (!g.pts.length) return;
    var active = ST.selZone && ST.selZone.type === 'area' && ST.selZone.index === i;
    var hull = convexHull(g.pts);
    if (hull.length >= 3) {
      c.beginPath();
      hull.forEach(function (p, k) {
        var q = w2s(p[0], p[1], v);
        if (k === 0) c.moveTo(q[0], q[1]); else c.lineTo(q[0], q[1]);
      });
      c.closePath();
      c.fillStyle = hexA(COLORS[g.kind] || '#a78bfa', active ? 0.18 : 0.07);
      c.fill();
      c.strokeStyle = hexA(COLORS[g.kind] || '#a78bfa', active ? 0.95 : 0.4);
      c.lineWidth = active ? 1.6 : 1;
      c.setLineDash(active ? [] : [3, 3]);
      c.stroke();
      c.setLineDash([]);
    }
    if (g.x != null) {
      var qc = w2s(g.x, g.z, v);
      c.beginPath(); c.arc(qc[0], qc[1], active ? 5 : 3, 0, Math.PI * 2);
      c.fillStyle = hexA(COLORS[g.kind] || '#a78bfa', 0.9); c.fill();
    }
    if (ST.show.labels && (active || v.s > 2.5)) {
      var first = g.pts[0];
      var q0 = w2s(first.x, first.z, v);
      c.fillStyle = hexA(COLORS[g.kind] || '#a78bfa', 0.95);
      c.font = '9px Consolas,monospace';
      c.textAlign = 'left';
      c.fillText(g.name + ' · ' + g.pts.length + ' 点', q0[0] + 6, q0[1] - 7);
    }
  });
}

/* =====================================================================
 * 4. 顶栏 / 侧栏 / 导航
 * ===================================================================*/
function viewLabel() { return VIEW_LABELS[ST.view] || ST.view || '—'; }
function viewFull() { return VIEW_FULL[ST.view] || viewLabel(); }
function shortPack(name) { return String(name || '').split('/').pop(); }
function winPath(p) { return String(p || '').replace(/\//g, String.fromCharCode(92)); }

function lsGet(k, d) {
  try { var v = localStorage.getItem(k); return v == null ? d : v; } catch (e) { return d; }
}
function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
function lsJSON(k, d) {
  try {
    var v = JSON.parse(localStorage.getItem(k) || 'null');
    return v && typeof v === 'object' ? v : d;
  } catch (e) { return d; }
}

/* 这张图能套的包：wb.packs 是全部包的完整清单（folder/name/fp/grow/keep/created/ops）。
 * 指纹和当前地图对不上的旧包标 stale —— 插件按 <指纹>.txt 找文件，对不上就是不会读。 */
function packsForMap(m) {
  if (!m) return [];
  var all = (ST.wb && ST.wb.packs) || [];
  return all.filter(function (p) {
    if (p.folder) return p.folder === m.folder;
    return p.level && p.level === m.level;
  }).map(function (p) {
    return {
      name: String(p.name || ''), label: String(p.label || ''),
      level: String(p.level || ''), fp: String(p.fp || ''),
      grow: !!p.grow, keep: !!p.keep, blank: !!p.blank,
      created: String(p.created || ''), ops: int(p.ops) || 0,
      nogen: !!p.nogen,
      stale: !!(p.fp && m.fp && p.fp !== m.fp)
    };
  }).sort(function (a, b) {
    return String(b.created || '').localeCompare(String(a.created || '')) ||
           String(b.name || '').localeCompare(String(a.name || ''));
  });
}

function choosePackForMap(m) {
  var valid = packsForMap(m).filter(function (p) { return !p.stale; });
  if (!valid.length) return '';
  var wants = [ST.pendingPack, ST.packByFolder[m.folder], ST.pack];
  for (var i = 0; i < wants.length; i++) {
    if (!wants[i]) continue;
    for (var j = 0; j < valid.length; j++) {
      if (valid[j].name === wants[i]) return valid[j].name;
    }
  }
  return valid[0].name;
}

function updatePackSel() {
  var sel = $('packSel');
  if (!sel) return;
  // 2026-11-24：一张图只有一个草稿，界面不再提供“选包”下拉。
  sel.style.display = 'none';
  if (ST.view !== 'pack') return;
  sel.style.display = '';
  var m = ST.cur;
  if (!m) {
    sel.innerHTML = '<option value="">先选地图</option>';
    sel.value = '';
    sel.disabled = true;
    sel.title = '先在上面的「选择地图」里挑一张，再选它的测试包';
    return;
  }
  var packs = packsForMap(m);
  var valid = packs.filter(function (p) { return !p.stale; });
  var stale = packs.filter(function (p) { return p.stale; });
  if (!valid.length) {
    sel.innerHTML = '<option value="">' +
      (packs.length ? '包都指纹失效了' : '这张图还没有包') + '</option>';
    sel.value = '';
    sel.disabled = true;
    sel.title = packs.length
      ? '这张图重新扫过，旧包的指纹对不上，插件不会读它们'
      : '进游戏 F2 改完存包，或控制台「编辑中」新建包';
    ST.pack = '';
    return;
  }
  var html = valid.map(function (p) {
    return '<option value="' + esc(p.name) + '">' + esc(shortPack(p.name)) +
      (p.created ? ' · ' + esc(shortTime(p.created)) : '') + '</option>';
  }).join('');
  html += stale.map(function (p) {
    return '<option value="" disabled>✖ 指纹失效 · ' + esc(shortPack(p.name)) + '</option>';
  }).join('');
  sel.innerHTML = html;
  sel.disabled = false;
  if (!ST.pack || !valid.some(function (p) { return p.name === ST.pack; })) {
    ST.pack = choosePackForMap(m);
  }
  sel.value = ST.pack;
  var cur = valid.filter(function (p) { return p.name === ST.pack; })[0];
  sel.title = '当前图的测试包：' + (cur ? shortPack(cur.name) : '—') +
    '（只读；切包只改查看，不写文件）';
}

function updateFinalChip() {
  var chip = $('finalChip');
  if (!chip) return;
  if (ST.view !== 'final') { chip.style.display = 'none'; return; }
  chip.style.display = '';
  var f = (ST.wb && ST.wb.versions && ST.wb.versions.dev && ST.wb.versions.dev.final) || {};
  var n = int(f.maps) || 0;
  chip.className = 'vchip' + (n ? ' ok' : '');
  chip.innerHTML = n
    ? '成品 · <b>' + n + ' 张图</b>' +
      (f.latest ? ' · ' + esc(shortTime(f.latest)) : '')
    : '成品 · <b>还没有发布</b>（启动 = 全原生）';
  chip.title = n
    ? ('成品目录：' + (f.path || '') + '（每张图一份，只读）')
    : '成品里还没有发布任何图：发布后这里显示张数。游戏启动 = 全原生。';
}

function updateViewControls() {
  var sel = $('viewSel');
  if (sel) sel.value = ST.view;
  updatePackSel();
  updateFinalChip();
}

function syncURL() {
  try {
    var u = new URL(location.href);
    u.searchParams.set('view', ST.view);
    u.searchParams.delete('profile');
    if (ST.view === 'pack' && ST.pack) u.searchParams.set('pack', ST.pack);
    else u.searchParams.delete('pack');
    if (ST.cur && ST.cur.file) u.searchParams.set('map', ST.cur.file);
    else if (ST.cur && ST.cur.level) u.searchParams.set('map', 'level:' + ST.cur.level);
    else u.searchParams.delete('map');
    history.replaceState(null, '', u);
  } catch (e) {}
}

function applyView(wb) {
  if (wb && wb.profile) {
    var mode0 = wb.profile.mode || wb.profile.profile || ST.view;
    if (mode0 === 'dev' || mode0 === 'deploy') mode0 = 'final';   /* 旧服务的兼容 */
    ST.view = mode0;
    ST.profileInfo = wb.profile;
  }
  var sel = $('viewSel');
  if (sel) {
    if (!sel.options.length) {
      sel.innerHTML = VIEW_ORDER.map(function (k) {
        return '<option value="' + k + '">' + VIEW_LABELS[k] + '</option>';
      }).join('');
    }
    sel.value = ST.view;
    sel.title = '当前查看：' + viewFull() + '（切换只改查看，不写文件）';
  }
  updateViewControls();
  var top = $('topVer');
  if (top) top.textContent = viewLabel() + ' · 只读';
  document.title = 'UCF 路点工作台 · ' + viewLabel();
  var chip = $('ovVerChip');
  if (chip) chip.textContent = '只读 · ' + viewLabel();
  lsSet(STORAGE_VIEW, ST.view);
  syncURL();
}

function updateHeader() {
  var m = ST.cur;
  var s = ST.stats;
  var title = m ? (m.label || m.level || m.file || '未命名地图') : '未加载';
  $('mapTitle').childNodes[0].nodeValue = title + ' ';
  $('mapMeta').textContent = m ?
    ((m.level || '—') + ' · ' + (m.scene || '—') + ' · ' + (m.fp || '无指纹')) : '—';
  $('pageName').textContent = PAGE_TITLE[ST.page] || ST.page;
  var sub = '';
  if (s && !s.nodes && ST.nm) {
    sub = '仅可走面 · ' + ST.nm.tri + ' 三角 / ' + ST.nm.nv + ' 顶点（原生没有点图）';
  } else if (s) {
    var bits = [];
    bits.push(s.nodes + ' 节点');
    bits.push(s.edges + ' 边');
    if (s.features) bits.push(s.features + ' 特征点');
    bits.push(s.components + ' 连通块');
    sub = bits.join(' · ');
  } else if (m && m.status === 'missing') {
    sub = m.navmesh ? '只有可走面（没有点图）' : '这张图还没有采集数据';
  } else if (m) {
    sub = '正在载入…';
  } else {
    sub = ST.wb ? '未选择地图 · 从「选择地图」里挑一张' : '正在连接本地服务…';
  }
  if (ST.page === 'routes') sub = s ? (s.jumpLinks + ' 条跳跃链路 · ' + s.jumpEndpoints + ' 个跳跃端点 · 路线由点图自动连通') : sub;
  if (ST.page === 'zones') {
    var k = (s && s.kinds) || {};
    sub = s ? ('幽灵守区 ' + (k.nano_area || 0) + ' · 幽灵守点 ' + (k.nano_pos || 0) +
      ' · 旧守卫区 ' + (k.guard_area || 0) + ' · 标签区 ' + (k.tag_region || 0)) : sub;
  }
  if (ST.page === 'auto') {
    sub = m ? ('进图时按 PointGraph 节点数判断是否自动铺：当前 ' + m.nodes + ' 点') : sub;
  }
  if (ST.page === 'maps') sub = ST.maps.length + ' 张图 · ' + viewLabel() +
    (ST.view === 'pack' && ST.pack ? ' · ' + shortPack(ST.pack) : '');
  if (ST.page === 'logs') sub = 'ucf_mod.log 尾部 · 只读';
  $('pageSub').textContent = sub;

  $('badgeNodes').textContent = s ? s.nodes : '—';
  $('badgeRoutes').textContent = s ? (s.jumpLinks || 0) : '0';
  $('badgeZones').textContent = s ? ((s.kinds.nano_area || 0) + (s.kinds.guard_area || 0) + (s.kinds.tag_region || 0)) : '0';

  if (m) {
    var kind = viewLabel();
    if (m.status === 'missing') kind = m.navmesh ? '仅可走面' : '待采集';
    else if (ST.view === 'pack') kind = ST.pack ? '② 编辑中 · 包' : '② 编辑中 · 无包';
    else if (ST.view === 'final') {
      var fcur0 = (ST.wb && ST.wb.versions && ST.wb.versions.dev && ST.wb.versions.dev.final || {}).current;
      kind = !fcur0 ? '② 成品 · 没发布'
        : ((m.final && m.final.has) ? '② 成品 · 已发布' : '② 成品 · 本图无');
    }
    else if (ST.view === 'native') kind = '① 备份版';
    $('sideKind').textContent = kind;
    $('sideName').textContent = (m.label || m.level || '未命名');
    $('sideFp').textContent = (m.fp || '—') + (m.file ? ' · ' + m.file : (m.navmeshFile ? ' · ' + m.navmeshFile : ''));
    $('sideSrc').innerHTML = '<i style="background:' + (m.status === 'ok' ? '#3ecf8e' : '#f5b942') + '"></i><span>' +
      (m.status === 'missing' ? (m.navmesh ? '只有可走面' : '没有文件') : (m.mtime || '已读取')) + '</span>';
  } else {
    $('sideKind').textContent = '—';
    $('sideName').textContent = '未加载';
    $('sideFp').textContent = '—';
    $('sideSrc').innerHTML = '<i></i><span>等待选择</span>';
  }
  $('stMap').textContent = m ? ((m.label || m.level) + ' · ' + (m.fp || '无指纹')) : '未加载地图';
  $('stData').textContent = viewLabel() + ' · 只读';
  if (ST.wb && ST.wb.server) $('stServer').textContent = ST.wb.server;
  $('stProfile').textContent = '查看 ' + viewLabel();

  var dir = (m && m.dir) || 'maps';
  ST.dockUrl = '/navview.html?view=1&embed=1&notour=1&profile=' + encodeURIComponent(ST.view) +
    (m && m.level ? '&level=' + encodeURIComponent(m.level) : '') +
    (m && m.file ? '&open=' + encodeURIComponent(dir + '/' + m.file) : '') +
    (ST.view === 'pack' && ST.pack ? '&pack=' + encodeURIComponent(ST.pack) : '') +
    '&compass=' + (ST.show.compass ? 1 : 0);   /* 3D 侧栏的罗盘跟着工作台的「方向」开关 */
  var dm = $('dockMap');
  if (dm) dm.textContent = m && m.file ? ((m.label || m.level) + ' · ' + m.file) : '未载入地图';
}

function showPage(name) {
  if (!PAGE_TITLE[name]) name = 'waypoints';
  ST.page = name;
  document.querySelectorAll('.nav[data-page]').forEach(function (n) {
    n.classList.toggle('on', n.dataset.page === name);
  });
  document.querySelectorAll('.page[data-page]').forEach(function (p) {
    p.classList.toggle('on', p.dataset.page === name);
  });
  updateHeader();
  requestAnimationFrame(function () {
    if (name === 'overview') renderOverview();
    if (name === 'waypoints') { renderWaypoints(); drawAll(); }
    if (name === 'routes') { renderRoutes(); drawAll(); }
    if (name === 'zones') { renderZones(); drawAll(); }
    if (name === 'auto') renderAuto();
    if (name === 'maps') renderMaps();
    if (name === 'logs') renderLogs();
  });
  if (name === 'logs') startLogTimer(); else stopLogTimer();
}

/* =====================================================================
 * 5. 总览
 * ===================================================================*/
function renderOverview() {
  var m = ST.cur, s = ST.stats, wb = ST.wb;
  if (!m || !s) return;
  var sync = '';
  var curFin = (wb && wb.versions && wb.versions.dev && wb.versions.dev.final) || {};
  if (ST.view === 'pack' && ST.pack) sync = ' · ' + shortPack(ST.pack);
  else if (ST.view === 'final') sync = curFin.maps ? (' · ' + curFin.maps + ' 张图') : ' · 成品还没有发布';
  else if (ST.view === 'native') sync = ' · 原生无编辑';
  $('ovSub').textContent = (m.label || m.level) + ' · ' + (m.level || '') + ' · ' + viewLabel() + sync;
  var k = s.kinds;
  $('ovTitle').innerHTML = (m.label || m.level) + ' <em>' + s.nodes + '</em> 点 / <em>' + s.edges + '</em> 边';
  $('ovDesc').textContent = '这张图的可走面' + (m.navmesh ? '有导出' : '没有导出') + '；' +
    '出生点 ' + ((k.spawn || 0)) + ' 个、蹲守点 ' + ((k.crouch || 0)) + ' 个、跳跃端点 ' + ((k.jump || 0)) + ' 个、守区 ' +
    ((k.nano_area || 0) + (k.guard_area || 0)) + ' 个。人机真正跑的是 PointNode 点图，路线不是手画线。';

  var boxes = [
    { v: fmtNum(s.nodes), l: '路点 NODES' },
    { v: fmtNum(s.edges), l: '连边 EDGES' },
    { v: (k.spawn || 0), l: '出生 / 补给' },
    { v: s.jumpLinks || ((k.jump || 0) ? (k.jump || 0) + ' 端点' : 0), l: '跳跃链路' },
    { v: ((k.nano_area || 0) + (k.guard_area || 0)), l: '区域' }
  ];
  $('ovStats').innerHTML = boxes.map(function (b) {
    return '<div class="statbox"><div class="v">' + esc(b.v) + '</div><div class="l">' + esc(b.l) + '</div></div>';
  }).join('');

  var dev = (wb && wb.versions && wb.versions.dev) || {};
  var nat = (wb && wb.versions && wb.versions.native) || {};
  var dFinal = dev.final || {}, dPacks = dev.packs || {}, dInbox = dev.inbox || {};
  var edits = ST.maps.reduce(function (a, x) { return a + ((x.final && x.final.ops) || 0); }, 0);
  /* 数据流：收件箱 → 编辑中（packs）→ 成品（final）。 */
  $('ovFlow').innerHTML =
    '<div class="fstep"><b><em>01</em>收件箱</b><span>' + fmtNum(dInbox.exports || 0) + ' 份导出 · ' + shortTime(dInbox.latest) + '</span></div>' +
    '<div class="fstep"><b><em>02</em>编辑中</b><span>' + (dPacks.n || 0) + ' 张图有草稿 · ' + fmtBytes(dPacks.bytes || 0) + '</span></div>' +
    '<div class="fstep"><b><em>03</em>成品</b><span>' + (dFinal.maps || 0) + ' 张图' +
      (edits ? ' · ' + edits + ' 条改动' : '') + '</span></div>';

  /* 数据档：① 备份版（对照）/ ② 成品 / ② 编辑中。③ 部署版不是数据档。 */
  var vers = [
    { key: 'native', n: '① 备份版', d: nat, c: '#8fa5c0',
      txt: (nat.maps || 0) + ' 图 / ' + (nat.navmesh || 0) + ' 面' },
    { key: 'final', n: '② 成品', d: { path: dFinal.path || '' }, c: '#d6b676',
      txt: (dFinal.maps || 0) + ' 张图' + (dFinal.latest ? (' · 最近 ' + shortTime(dFinal.latest)) : ' · 还没有发布') },
    { key: 'pack', n: '② 编辑中', d: { path: (wb.profile && wb.profile.packs) || '' }, c: '#8fb7d9',
      txt: (dPacks.n || 0) + ' 包 / ' + (dPacks.maps || 0) + ' 图' }
  ];
  $('ovVersions').innerHTML = vers.map(function (v) {
    return '<span class="preset' + (v.key === ST.view ? ' on' : '') + '" data-view="' + v.key + '"' +
      ' title="' + esc(v.d.path || '') + '" style="color:' + v.c + '">' + v.n + '<b>' + esc(v.txt) + '</b></span>';
  }).join('');
  var curPath = '';
  if (ST.view === 'native') curPath = (wb.profile && wb.profile.native) || '';
  else if (ST.view === 'pack') {
    var pkBase = (wb.profile && wb.profile.packs) || '';
    curPath = ST.pack ? winPath(pkBase + '/' + ST.pack) : pkBase;
  } else {
    curPath = dFinal.path || (wb.profile && wb.profile.data) || '';
  }
  $('ovPaths').textContent = '当前查看：' + viewLabel() +
    (ST.view === 'pack' && ST.pack ? (' · ' + shortPack(ST.pack)) : '') + ' · ' + curPath;

  var events = (wb && wb.events) || [];
  $('ovActions').innerHTML = events.slice(0, 8).map(function (e) {
    return '<div class="act"><time>' + esc(e.time || '') + '</time><span><b>' + esc(e.kind) + '</b> ' + esc(e.text) + '</span></div>';
  }).join('') || '<div class="act"><time>—</time><span>还没有文件事件</span></div>';

  $('ovTips').innerHTML = buildTips().map(function (t) {
    return '<div class="tip" style="--c:' + t.c + '"><i></i><span>' + esc(t.text) + '</span></div>';
  }).join('');
}

function buildTips() {
  var m = ST.cur, s = ST.stats, wb = ST.wb, out = [];
  if (!m) return out;
  if (ST.view === 'native') {
    out.push({ c: '#8fa5c0', text: '当前是①备份版的只读快照（原生数据），游戏不读它；对照用，看游戏实际读哪份请切「② 成品」或「② 编辑中」。' });
  } else if (ST.view === 'final') {
    var fin0 = (wb && wb.versions && wb.versions.dev && wb.versions.dev.final) || {};
    if (!fin0.current) {
      out.push({ c: '#f5b942', text: '成品里还没有发布任何图：游戏启动 = 全原生；现在看到的是 ② 的基准点图。要试改法去「② 编辑中」改草稿。' });
    } else if (!(m.final && m.final.has)) {
      out.push({ c: '#f5b942', text: '这张图还没发布到成品：游戏会用原版 / 没有编辑。' });
    }
  } else if (ST.view === 'pack') {
    var allPk = (wb && wb.packs ? wb.packs : []).filter(function (p) { return p.folder === m.folder; });
    var stalePk = allPk.filter(function (p) { return p.fp && m.fp && p.fp !== m.fp; });
    if (!ST.pack) {
      out.push({ c: '#f5b942', text: allPk.length && stalePk.length === allPk.length
        ? '这张图的包都指纹失效了（图重新扫过），插件不会读；去控制台「编辑中」新建一个包。'
        : '这张图还没有包：进游戏 F2 改完存包，或控制台「编辑中」新建包；现在看到的是基准点图。' });
    }
  }
  if (m.status === 'missing') {
    out.push({ c: '#f5b942', text: '这张图还没有采集数据：进图导出一份，或用测试包从空白底图画。' });
    return out;
  }
  if (s.nodes === 0) {
    out.push({ c: '#a78bfa', text: '点图 0 节点：进图时插件会尝试自动铺设（需要 auto_waypoints 开，且可走面有地面命中）。' });
  } else if (s.nodes < 50) {
    out.push({ c: '#f5b942', text: '点图只有 ' + s.nodes + ' 个节点，通常是 NodeLink2 端点/不完整点图；自动铺设只在 0 节点时触发，不会补这张图。' });
  }
  if (s.isolated) out.push({ c: '#ff5c5c', text: s.isolated + ' 个孤立点（没有连边），人机走到这里会卡住；可在游戏内 Ctrl+Shift+J 补连。' });
  if (s.components > 1) out.push({ c: '#f5b942', text: s.components + ' 个连通块：块与块之间人机过不去，检查跳跃链接或补边。' });
  if (!m.navmesh) out.push({ c: '#8fa5c0', text: '这张图没有可走面导出（NavMeshGraph），3D 视图只能画点；自动铺设不看这份导出，仍按 A* 图跑。' });
  if (!(s.kinds.crouch)) out.push({ c: '#38d9f5', text: '蹲守点 0：进图时 auto_crouch 开就会自动补一批 Bot_CrouchPos。' });
  if (!(s.kinds.nano_area)) out.push({ c: '#a78bfa', text: '幽灵守区 0：ghost_areas 开时插件会按采样点凭空造守区；旧 guard_area 不算。' });
  var c = wb && wb.consistency;
  if (c && c.nativeDev && c.nativeDev.maps &&
      ((c.nativeDev.maps.diff || []).length || (c.nativeDev.maps.onlyA || []).length || (c.nativeDev.maps.onlyB || []).length)) {
    out.push({ c: '#3ecf8e', text: '②开发版的 map.json 和①备份版有文件不同：这些就是改过的成品数据，控制台「开始游戏 · 成品」按包读它。' });
  }
  if (m.final && m.final.has) {
    out.push({ c: '#3ecf8e', text: '这张图已发布，成品里有 ' + (m.final.ops || 0) + ' 条改动；要试新改法去控制台「编辑中」改草稿。' });
  }
  if (ST.view === 'pack' && ST.pack) {
    var curPk = packsForMap(m).filter(function (p) { return p.name === ST.pack; })[0];
    out.unshift({ c: '#3ecf8e', text: '当前查看的是包 ' + shortPack(ST.pack) +
      (curPk ? ('（' + curPk.ops + ' 条）') : '') + '；网页只读，游戏里要在控制台「编辑中」选这个包才生效。' });
  }
  if (!out.length) out.push({ c: '#3ecf8e', text: '当前地图数据没有明显缺口：点图、出生点、特征点都读到了。' });
  return out.slice(0, 5);
}

/* =====================================================================
 * 6. 路点库
 * ===================================================================*/
function renderLayerList() {
  var defs = layerDefs();
  var html = '';
  defs.forEach(function (g) {
    var rows = '';
    g.items.forEach(function (it, i) {
      var allowed = modeAllows(it.key);
      if (!ST.showAllLayers && !allowed) return;
      var on = ST.selLayer === it.key;
      var vis = layerVisible(it.key);
      var tag = LEGACY_LAYERS[it.key] ? '<em class="tag-dead">游戏未使用</em>'
        : (allowed ? '' : '<em class="tag-off">本模式不使用</em>');
      rows += '<div class="trow' + (on ? ' on' : '') + (allowed ? '' : ' offmode') + '" data-layer="' + it.key + '" style="--c:' + it.color + '">' +
        '<div class="key">' + g.letter + (i + 1) + '</div><i class="tdot"></i>' +
        '<div><div class="tname">' + esc(it.name) + tag + '</div><div class="tsub">' + esc(it.sub) + '</div></div>' +
        '<div class="tcount">' + (it.key === 'edge' ? fmtNum(it.count) : it.count) + '</div>' +
        '<svg class="teye' + (vis ? '' : ' off') + '" data-eye="' + it.key + '" viewBox="0 0 24 24" fill="none" stroke="#cfd9e6" stroke-width="1.6">' +
        '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.4"/></svg>' +
        '</div>';
    });
    if (rows) html += '<div class="glabel">' + esc(g.group) + '<span>' + g.letter + ' 组</span></div>' + rows;
  });
  $('layerList').innerHTML = html;
  $('layerSum').textContent = (ST.stats ? ST.stats.nodes : 0) + ' 点';
  var mode = curMode();
  $('layerMode').textContent = mode
    ? (mode + ' · ' + (MODE_NOTES[mode] || '只列生效图层'))
    : '点眼睛显隐';
  var btn = $('btnShowAllLayers');
  if (btn) {
    btn.textContent = ST.showAllLayers ? '只看本模式' : '显示全部';
    btn.classList.toggle('on', ST.showAllLayers);
  }
}

function selectedLayerDef() {
  var defs = layerDefs();
  for (var i = 0; i < defs.length; i++) {
    for (var j = 0; j < defs[i].items.length; j++) {
      if (defs[i].items[j].key === ST.selLayer) return { group: defs[i], item: defs[i].items[j], code: defs[i].letter + (j + 1) };
    }
  }
  return { group: defs[0], item: defs[0].items[0], code: 'A1' };
}

function layerDetailHtml() {
  var d = selectedLayerDef(), it = d.item, s = ST.stats, m = ST.cur;
  var share = '—';
  if (s) {
    share = it.key.indexOf('spawn') === 0 || it.key === 'supply' || it.key.indexOf('crouch') === 0
      ? (s.features ? pct(it.count, s.features) + '% 的特征点' : '—')
      : (s.nodes ? pct(it.count, s.nodes) + '% 的节点' : '—');
  }
  var note = '';
  if (!s) note = '还没有载入地图：数量 / 占比等选一张图后再算，字段说明和颜色不受影响。';
  else if (it.key === 'node_walk') note = 'A* 真正能走的点。可走率 ' + pct(s.walkable, s.nodes) + '%，图里 support=' + (m && m.support ? m.support : '—') + '。';
  else if (it.key === 'node_block') note = 'GraphNode.flags bit0=0，寻路会绕开；一般是手动禁用的点。';
  else if (it.key === 'edge') note = 'PointGraph.Scan 按 maxDistance + 射线自动连的边，不是手画线。运输船 1391 条边就是它自己连的。';
  else if (it.key === 'jump') note = 'Bot_JumpLink 的端点 ' + ((s.kinds.jump) || 0) + ' 个；插件导出的成对链路 ' + s.jumpLinks + ' 条。人机路径经过时会插入跳跃段。';
  else if (it.key === 'nano_area' || it.key === 'nano_pos') note = '生化/终结者模式真正使用的守区/守点；守点必须挂在守区下才会被 NanoGuard 收集。';
  else if (it.key === 'guard_area' || it.key === 'guard') note = '旧 Bot_GuardArea / Bot_GuardPos：Bot_GuardArea 是空类、Bot_GuardPos 只当 Bot_CrouchPos 基类，所有模式都不使用。';
  else if (it.key === 'tag_region') note = 'PointNodeTagModifier 把节点打 tag；只有人机 Seeker.traversableTags / tagPenalties 认它才有意义。';
  else if (it.key === 'supply') note = '普通/红/蓝补给箱点位；生化/终结者模式里优先级 51，人机会突然不打了去抢箱。';
  else if (it.key === 'spawn_bl') note = 'SP_BL（Team.BlackList / 幽灵）出生点；团队、特殊战、生化类模式使用。';
  else if (it.key === 'spawn_gr') note = 'SP_GR（Team.GlobalRisk / 保卫）出生点；团队、特殊战、生化类模式使用。';
  else if (it.key === 'spawn_neutral') note = 'SP_Netural（中立）出生点；个人竞技主要用它，团队/生化缺 BL/GR 时也会回退借用。';
  else if (it.key.indexOf('crouch') === 0) note = 'Bot_CrouchPos 静态表，GoCrouchPos 随机取；只有团队模式会给人机加这个 Action。team=0 是幽灵，team=1 是保卫。';

  return '' +
    '<div class="dhead"><div class="ddot" style="--c:' + it.color + '"></div>' +
    '<div><div class="dname">' + esc(it.name) + '</div><div class="dsub">' + esc(it.sub) + '</div></div>' +
    '<div class="dkey" style="--c:' + it.color + '">' + d.code + '</div></div>' +
    '<div class="comp">' + esc(it.cls) + ' · count ' + it.count + '</div>' +
    '<div class="meta">' +
    '<div><div class="l">数量</div><div class="v">' + it.count + '</div></div>' +
    '<div><div class="l">占比</div><div class="v">' + share + '</div></div>' +
    '<div><div class="l">颜色</div><div class="v">' + it.color.toUpperCase() + '</div></div>' +
    '<div><div class="l">图层可见</div><div class="v">' + (layerVisible(it.key) ? '是' : '否') + '</div></div>' +
    '</div>' +
    '<div class="note">' + esc(note) + '</div>';
}

function renderLayerDetail() {
  var d = selectedLayerDef();
  $('layerSub').textContent = d.item.name;
  $('layerKey').textContent = d.code;
  $('layerKey').style.background = d.item.color;
  $('layerKey').style.color = '#0a1119';
  $('layerDetail').innerHTML = layerDetailHtml();
}

function renderMapInfo() {
  var m = ST.cur, s = ST.stats;
  if (!m || !s) {
    $('mapSub2').textContent = '—';
    $('mapChip').textContent = '未加载';
    $('mapInfo').innerHTML = '<div class="note">还没有选择地图。点上方「选择地图」挑一张再查看统计。</div>';
    return;
  }
  $('mapSub2').textContent = m.level || m.file || '—';
  $('mapChip').textContent = m.status === 'missing' ? (m.navmesh ? '仅可走面' : '待采集') : viewLabel();
  /* ② 开发版里分 成品（final 当前版）/ 编辑中（packs）/ 收件箱（vis）；① 备份版是对照 */
  var fin = m.final || {};
  var finText = fin.has
    ? ('已发布 · ' + (fin.ops || 0) + ' 条' + (fin.sha ? ' · ' + String(fin.sha).slice(0, 8) : ''))
    : (ST.view === 'native' ? '① 备份版没有成品概念'
      : '这张图还没发布到成品');
  var packs = m.packs || [];
  var packsText = packs.length
    ? ('有草稿 · ' + packs.reduce(function (a, p) { return a + (p.ops || 0); }, 0) + ' 条改动')
    : '没有草稿';
  var edits = ST.view === 'native' ? (m.editsNative || 0) : (m.editsDev || 0);
  var viewText = viewLabel() + (ST.view === 'pack' && ST.pack ? (' · ' + shortPack(ST.pack)) : '');
  var nmText = m.navmesh ? (m.navmeshFile || '有') : '没有导出';
  if (ST.nm) nmText += ' · ' + ST.nm.tri + ' 三角 / ' + ST.nm.nv + ' 顶点';
  var html = '' +
    '<div class="kline"><span class="k">查看档</span><span class="v c" style="--c:#4f8cff">' + esc(viewText) + '</span></div>' +
    '<div class="kline"><span class="k">文件</span><span class="v">' + esc(m.file || '—（只有可走面）') + '</span></div>' +
    '<div class="kline"><span class="k">指纹</span><span class="v">' + esc(m.fp || '—') + '</span></div>' +
    '<div class="kline"><span class="k">大小 / 时间</span><span class="v">' + fmtBytes(m.size) + ' · ' + esc(m.mtime || '—') + '</span></div>' +
    '<div class="kline"><span class="k">可走面</span><span class="v">' + esc(nmText) + '</span></div>' +
    '<div class="kline"><span class="k">成品</span><span class="v">' + esc(finText) + '</span></div>' +
    '<div class="kline"><span class="k">编辑中</span><span class="v">' + esc(packsText) + '</span></div>' +
    '<div class="kline"><span class="k">导出（收件箱）</span><span class="v">' + (m.exports || 0) + ' 份</span></div>' +
    '<div class="kline"><span class="k">成品改动</span><span class="v">' + edits + ' 条</span></div>' +
    '<div class="kline"><span class="k">连通 / 孤立</span><span class="v">' + s.components + ' 块 · ' + s.isolated + ' 个</span></div>' +
    '<div class="note" style="margin-top:8px">网页只读。切换数据档/包只改查看的数据源，不写文件。加点/连线/禁用点：游戏内 Ctrl+Shift+N / Ctrl+Shift+J / Ctrl+Shift+D。升成品：控制台「发布到成品」或 python navdata.py pack promote。</div>';
  $('mapInfo').innerHTML = html;
}

function renderStats() {
  var s = ST.stats;
  if (!s) return;
  $('statRow').innerHTML =
    '<div class="stat"><div class="v">' + fmtNum(s.nodes) + '</div><div class="l">节点 NODES</div></div>' +
    '<div class="stat"><div class="v">' + fmtNum(s.edges) + '</div><div class="l">连边 EDGES</div></div>' +
    '<div class="stat good"><div class="v">' + s.components + '</div><div class="l">连通块</div></div>' +
    '<div class="stat ' + (s.isolated ? 'warn' : '') + '"><div class="v">' + s.isolated + '</div><div class="l">孤立点</div></div>' +
    '<div class="stat"><div class="v">' + s.features + '</div><div class="l">特征点</div></div>' +
    '<div class="stat mono"><div class="v">' + pct(s.walkable, s.nodes) + '%</div><div class="l">可走率</div></div>';
}

function renderLegend() {
  var keys = ['node_walk', 'node_block', 'spawn_bl', 'spawn_gr', 'spawn_neutral', 'crouch_bl', 'crouch_gr',
    'jump', 'nano_area', 'nano_pos', 'guard_area', 'guard', 'supply'];
  var names = { node_walk: '可走', node_block: '不可走', spawn_bl: '幽灵出生', spawn_gr: '保卫出生',
    spawn_neutral: '中立出生', crouch_bl: '蹲守BL', crouch_gr: '蹲守GR', jump: '跳跃',
    nano_area: '幽灵守区', nano_pos: '幽灵守点', guard_area: '旧守卫区*', guard: '旧守卫点*', supply: '补给' };
  $('legend').innerHTML = keys.map(function (k) {
    var allowed = modeAllows(k);
    if (!ST.showAllLayers && !allowed) return '';
    var tip = LEGACY_LAYERS[k] ? '旧守卫系统，游戏未使用' : (allowed ? '' : '本模式不使用');
    return '<div class="lg' + (allowed ? '' : ' off') + '" style="--c:' + COLORS[k] + '" title="' + esc(tip) + '"><i></i>' + names[k] + '</div>';
  }).join('');
}

function renderQuickLists() {
  var jumps = ST.jumpLinks.slice(0, 5);
  var html = jumps.map(function (j, i) {
    return '<div class="rrow" data-jump="' + i + '"><div class="rtag" style="--c:#38d9f5">J' + (i + 1) + '</div>' +
      '<div class="rname">跳跃链路 J' + (i + 1) + '</div><div class="rmeta">' + dist2D(j.a, j.b).toFixed(1) + ' m</div></div>';
  }).join('');
  if (!jumps.length) {
    html = '<div class="rtip">这张图没有成对的跳跃链路' + (ST.jumpOrphans.length ? '（只有 ' + ST.jumpOrphans.length + ' 个端点）' : '') + '。</div>';
  }
  $('quickRoutes').innerHTML = html;

  var k = (ST.stats && ST.stats.kinds) || {};
  var zs = [];
  if (k.nano_area) zs.push(['Z', '幽灵守区', k.nano_area, '#a78bfa']);
  if (k.guard_area) zs.push(['G', '旧守卫区', k.guard_area, '#7c6bd4']);
  if (k.tag_region) zs.push(['T', '标签区', k.tag_region, '#f97316']);
  if (k.nano_pos) zs.push(['P', '幽灵守点', k.nano_pos, '#c4b5fd']);
  $('quickZones').innerHTML = zs.map(function (z) {
    return '<div class="rrow" data-zonequick="1"><div class="rtag" style="--c:' + z[3] + '">' + z[0] + '</div>' +
      '<div class="rname">' + z[1] + '</div><div class="rmeta">' + z[2] + '</div></div>';
  }).join('') || '<div class="rtip">没有守区 / 标签区数据；可看「自动铺设」页的触发条件。</div>';
  $('rzSum').textContent = jumps.length + ' / ' + zs.length;
}

function renderWaypoints() {
  if (!ST.doc) return;
  renderLayerList();
  renderLayerDetail();
  renderMapInfo();
  renderStats();
  renderLegend();
  renderQuickLists();
  var m = ST.cur;
  $('mapCardTitle').textContent = (m ? (m.label || m.level) : '') + ' · 俯视图';
  $('mapCardSub').textContent = '抽样显示全部 · ' + (ST.stats ? ST.stats.nodes : 0) + ' 点 / ' + (ST.stats ? ST.stats.edges : 0) + ' 边';
}

function bindLayerList() {
  $('btnShowAllLayers').addEventListener('click', function () {
    ST.showAllLayers = !ST.showAllLayers;
    if (!ST.showAllLayers) {
      if (!modeAllows(ST.selLayer)) ST.selLayer = 'node_walk';
      if (ST.focus && !modeAllows(ST.focus)) ST.focus = null;
    }
    renderLayerList();
    renderLayerDetail();
    renderLegend();
    drawAll();
  });
  $('layerList').addEventListener('click', function (e) {
    var eye = e.target.closest('[data-eye]');
    if (eye) {
      e.stopPropagation();
      var k = eye.dataset.eye;
      ST.layerVis[k] = !layerVisible(k);
      renderLayerList();
      renderLayerDetail();
      drawAll();
      return;
    }
    var row = e.target.closest('[data-layer]');
    if (!row) return;
    ST.selLayer = row.dataset.layer;
    ST.focus = row.dataset.layer;
    renderLayerList();
    renderLayerDetail();
    drawAll();
  });
  $('quickRoutes').addEventListener('click', function (e) {
    var r = e.target.closest('[data-jump]');
    if (r) {
      ST.selRoute = { type: 'jump', index: +r.dataset.jump };
      showPage('routes');
    }
  });
  $('quickZones').addEventListener('click', function () {
    showPage('zones');
  });
}

/* =====================================================================
 * 7. 路线
 * ===================================================================*/
function routeItems() {
  var items = [];
  ST.jumpLinks.forEach(function (j, i) {
    items.push({
      type: 'jump', index: i,
      name: '跳跃链路 ' + j.id, color: '#38d9f5',
      meta: dist2D(j.a, j.b).toFixed(1) + ' m · Δy ' + (j.b[1] - j.a[1]).toFixed(1) + ' m'
    });
  });
  if (!ST.jumpLinks.length && ST.jumpOrphans.length) {
    items.push({
      type: 'orphan', index: 0,
      name: '跳跃端点（未导出链路）', color: '#38d9f5',
      meta: ST.jumpOrphans.length + ' 个端点'
    });
  }
  ST.routes.forEach(function (r, i) {
    var len = 0;
    for (var j = 1; j < r.pts.length; j++) len += dist3(r.pts[j - 1], r.pts[j]);
    if (r.closed && r.pts.length > 2) len += dist3(r.pts[r.pts.length - 1], r.pts[0]);
    items.push({
      type: 'route', index: i,
      name: r.id + ' ' + r.name, color: r.color,
      meta: r.pts.length + ' 点 · ' + len.toFixed(1) + ' m'
    });
  });
  return items;
}

function renderRoutes() {
  if (!ST.doc) return;
  var items = routeItems();
  $('routeSub').textContent = items.length + ' 项 · ' + (ST.routes.length ? ST.routes.length + ' 条数据层路线' : '没有手画路线');
  if (!ST.selRoute && items.length) ST.selRoute = { type: items[0].type, index: items[0].index };
  $('routeList').innerHTML = items.map(function (it, i) {
    var on = ST.selRoute && ST.selRoute.type === it.type && ST.selRoute.index === it.index;
    var tag = it.type === 'jump' ? 'J' + (it.index + 1) : (it.type === 'route' ? 'R' + (it.index + 1) : 'J');
    return '<div class="lrow' + (on ? ' on' : '') + '" data-route="' + i + '">' +
      '<div class="ltag" style="--c:' + it.color + '">' + tag + '</div>' +
      '<div><div class="lname">' + esc(it.name) + '</div><div class="lmeta">' + esc(it.meta) + '</div></div>' +
      '<div class="lgo">›</div></div>';
  }).join('') || '<div class="empty">这张图没有跳跃链路，也没有 routes[]。<b>这不是缺数据</b>：人机路线由 PointNode 点图 + 自动连边决定，不需要手画线。</div>';

  renderRouteDetail();
}

function renderRouteDetail() {
  var sel = ST.selRoute || {};
  var items = routeItems();
  var it = null;
  items.forEach(function (x) { if (x.type === sel.type && x.index === sel.index) it = x; });
  if (!it) {
    $('routeTitle').textContent = '链路预览';
    $('routeMeta').textContent = '—';
    $('mbRoute').innerHTML = '<b>—</b> 没有链路';
    $('mbRouteMeta').textContent = '—';
    $('routeTime').textContent = '—';
    $('routeSeq').innerHTML = '';
    $('routeKk').textContent = '—';
    $('routeDetail').innerHTML = '<div class="empty">没有选中项。<br>这个游戏里路线 = 点图节点 + A* 自动连边 + 少量手工补丁（跳跃 / NodeLink）；' +
      '跳跃链路是唯一“成对”的路线数据。</div>';
    return;
  }
  if (it.type === 'jump') {
    var j = ST.jumpLinks[it.index];
    var d2 = dist2D(j.a, j.b), d3 = dist3(j.a, j.b), dy = j.b[1] - j.a[1];
    $('routeTitle').textContent = '跳跃链路 ' + j.id;
    $('routeMeta').textContent = d2.toFixed(1) + ' m · Δy ' + dy.toFixed(1) + ' m';
    $('mbRoute').innerHTML = '<i style="--c:#38d9f5"></i><b>' + j.id + '</b> Bot_JumpLink';
    $('mbRouteMeta').textContent = d2.toFixed(1) + ' m · ' + d3.toFixed(1) + ' m 3D';
    $('routeTime').textContent = dy >= 0 ? '向上跳 +' + dy.toFixed(1) + ' m' : '向下落 ' + dy.toFixed(1) + ' m';
    $('routeSeq').innerHTML = '<div class="tlnode on" style="--c:#38d9f5"></div><div class="tlnode on" style="--c:#38d9f5"></div>';
    $('routeKk').textContent = j.id;
    $('routeDetail').innerHTML = '' +
      '<div class="kline"><span class="k">类型</span><span class="v c" style="--c:#38d9f5">Bot_JumpLink</span></div>' +
      '<div class="kline"><span class="k">来源</span><span class="v">' + (j.fromTxt ? '清单 jump add（测试包 / 成品）' : 'map.json · lines.jump') + '</span></div>' +
      '<div class="kline"><span class="k">起点</span><span class="v">' + j.a.map(function (v) { return v.toFixed(2); }).join(', ') + '</span></div>' +
      '<div class="kline"><span class="k">终点</span><span class="v">' + j.b.map(function (v) { return v.toFixed(2); }).join(', ') + '</span></div>' +
      '<div class="kline"><span class="k">水平距离</span><span class="v">' + d2.toFixed(2) + ' m</span></div>' +
      '<div class="kline"><span class="k">三维距离</span><span class="v">' + d3.toFixed(2) + ' m</span></div>' +
      '<div class="kline"><span class="k">高差</span><span class="v">' + dy.toFixed(2) + ' m</span></div>' +
      '<div class="kline"><span class="k">方向</span><span class="v">' + (dy >= 0 ? '向上' : '向下') + '</span></div>' +
      '<div class="sect">说明</div>' +
      '<div class="note">人机路径经过 Bot_JumpLink 时会在 OnPathComplete 插入跳跃段；needSpeed / accuracy / direction 在游戏内存里，<b>当前导出没有这些字段</b>。</div>';
    return;
  }
  if (it.type === 'orphan') {
    $('routeTitle').textContent = '跳跃端点';
    $('routeMeta').textContent = ST.jumpOrphans.length + ' 个端点';
    $('mbRoute').innerHTML = '<i style="--c:#38d9f5"></i><b>J</b> 未成对';
    $('mbRouteMeta').textContent = 'lines.jump 为空';
    $('routeTime').textContent = ST.jumpOrphans.length + ' 端点';
    $('routeSeq').innerHTML = ST.jumpOrphans.slice(0, 40).map(function () {
      return '<div class="tlnode on" style="--c:#38d9f5"></div>';
    }).join('');
    $('routeKk').textContent = '—';
    $('routeDetail').innerHTML = '<div class="empty">这张图导出到 <b>' + ST.jumpOrphans.length + '</b> 个 Bot_JumpLink 端点，但 <b>lines.jump</b> 为空，插件没把它们配成对。' +
      '端点位置是真的，成对关系不猜。</div>' +
      '<div class="sect">端点坐标</div>' +
      '<div class="tags">' + ST.jumpOrphans.slice(0, 20).map(function (f) {
        return '<span class="tag">' + f.x.toFixed(1) + ', ' + f.z.toFixed(1) + '</span>';
      }).join('') + '</div>';
    return;
  }
  var r = ST.routes[it.index];
  var len = 0;
  for (var i = 1; i < r.pts.length; i++) len += dist3(r.pts[i - 1], r.pts[i]);
  $('routeTitle').textContent = r.id + ' ' + r.name;
  $('routeMeta').textContent = r.pts.length + ' 点 · ' + len.toFixed(1) + ' m' + (r.closed ? ' · 闭环' : '');
  $('mbRoute').innerHTML = '<i style="--c:' + r.color + '"></i><b>' + r.id + '</b> ' + esc(r.name);
  $('mbRouteMeta').textContent = r.pts.length + ' 点 · ' + len.toFixed(1) + ' m';
  $('routeTime').textContent = r.closed ? '闭环' : '开放';
  $('routeSeq').innerHTML = r.pts.map(function () { return '<div class="tlnode on" style="--c:' + r.color + '"></div>'; }).join('');
  $('routeKk').textContent = r.id;
  $('routeDetail').innerHTML = '' +
    '<div class="kline"><span class="k">阵营</span><span class="v c" style="--c:' + r.color + '">' + esc(r.team || '—') + '</span></div>' +
    '<div class="kline"><span class="k">结构</span><span class="v">' + (r.closed ? '闭环' : '开放') + '</span></div>' +
    '<div class="kline"><span class="k">点数</span><span class="v">' + r.pts.length + '</span></div>' +
    '<div class="kline"><span class="k">长度</span><span class="v">' + len.toFixed(2) + ' m</span></div>' +
    '<div class="note" style="margin-top:8px">这是地图 JSON 里的 routes[]（工作台/旧编辑器写的图层）。<b>插件不读它</b>，不影响寻路。</div>';
}

function bindRouteList() {
  $('routeList').addEventListener('click', function (e) {
    var row = e.target.closest('[data-route]');
    if (!row) return;
    var items = routeItems();
    var it = items[+row.dataset.route];
    if (!it) return;
    ST.selRoute = { type: it.type, index: it.index };
    if (it.type === 'jump') fitToPoints([ST.jumpLinks[it.index].a, ST.jumpLinks[it.index].b]);
    else if (it.type === 'route') fitToPoints(ST.routes[it.index].pts);
    else if (it.type === 'orphan') fitToPoints(ST.jumpOrphans.map(function (f) { return [f.x, f.y, f.z]; }));
    renderRoutes();
    drawAll();
  });
}

/* =====================================================================
 * 8. 区域
 * ===================================================================*/
function zoneItems() {
  var items = [];
  zoneGroups().forEach(function (g, i) {
    if (g.type === 'area') {
      items.push({
        type: 'area', index: i,
        name: KIND_LABEL[g.kind] + (g.aux != null ? ' #' + g.aux : ''),
        color: COLORS[g.kind] || '#a78bfa',
        meta: g.kind + ' · ' + g.pts.length + ' 个守点'
      });
    } else if (g.type === 'loose') {
      items.push({
        type: 'loose', index: i,
        name: g.name, color: COLORS[g.kind] || '#8d7fd6',
        meta: g.kind + ' · ' + g.pts.length + ' 个'
      });
    }
  });
  ST.zones.forEach(function (z, i) {
    items.push({
      type: 'zone', index: i,
      name: z.id + ' ' + z.name, color: z.color,
      meta: z.kind + ' · ' + z.pts.length + ' 顶点'
    });
  });
  return items;
}

function renderZones() {
  if (!ST.doc) return;
  var items = zoneItems();
  $('zoneSub').textContent = items.length + ' 项';
  if (!ST.selZone && items.length) ST.selZone = { type: items[0].type, index: items[0].index };
  $('zoneList').innerHTML = items.map(function (it, i) {
    var on = ST.selZone && ST.selZone.type === it.type && ST.selZone.index === it.index;
    var tag = it.type === 'area' ? (it.name.indexOf('旧') === 0 ? 'G' : 'Z') : (it.type === 'loose' ? '·' : 'R');
    return '<div class="lrow' + (on ? ' on' : '') + '" data-zone="' + i + '">' +
      '<div class="ltag" style="--c:' + it.color + '">' + tag + '</div>' +
      '<div><div class="lname">' + esc(it.name) + '</div><div class="lmeta">' + esc(it.meta) + '</div></div>' +
      '<div class="lgo">›</div></div>';
  }).join('') || '<div class="empty">这张图没有幽灵守区（nano_area=0）、旧守卫区、标签区，也没有 zones[]。<br>' +
    '<b>不是坏数据</b>：很多图本来就不挂守区；ghost_areas 开时插件进图会自己造。</div>';

  renderZoneDetail();
}

function renderZoneDetail() {
  var sel = ST.selZone || {};
  var items = zoneItems();
  var it = null;
  items.forEach(function (x) { if (x.type === sel.type && x.index === sel.index) it = x; });
  if (!it) {
    $('zoneTitle').textContent = '区域预览';
    $('zoneMeta').textContent = '—';
    $('mbZone').innerHTML = '<b>—</b> 没有区域';
    $('zoneRule').textContent = '—';
    $('zoneKk').textContent = '—';
    $('zoneDetail').innerHTML = '<div class="empty">没有选中项。能用的守区是 Bot_NanoGuardArea；旧 Bot_GuardArea 游戏没用。</div>';
    return;
  }
  var groups = zoneGroups();
  if (it.type === 'area' || it.type === 'loose') {
    var g = groups[it.index];
    var pts = g.pts;
    $('zoneTitle').textContent = it.name;
    $('zoneMeta').textContent = g.kind + ' · ' + pts.length + ' 个守点';
    $('mbZone').innerHTML = '<i style="--c:' + it.color + '"></i><b>' + (it.type === 'area' ? 'Z' : '·') + '</b> ' + esc(it.name);
    $('zoneRule').textContent = it.type === 'area' ? '守区 / 守点（按最近距离分组）' : '未归属守点';
    $('zoneKk').textContent = pts.length + ' 点';
    var functional = g.kind === 'nano_area' || g.kind === 'nano_pos';
    $('zoneDetail').innerHTML = '' +
      '<div class="kline"><span class="k">类型</span><span class="v c" style="--c:' + it.color + '">' + esc(KIND_LABEL[g.kind] || g.kind) + '</span></div>' +
      '<div class="kline"><span class="k">游戏类</span><span class="v">' + esc(g.kind.indexOf('nano') === 0 ? 'Bot_NanoGuard' + (g.kind === 'nano_area' ? 'Area' : 'Pos') : 'Bot_Guard' + (g.kind === 'guard_area' ? 'Area' : 'Pos')) + '</span></div>' +
      '<div class="kline"><span class="k">中心</span><span class="v">' + g.x.toFixed(2) + ', ' + g.z.toFixed(2) + '</span></div>' +
      '<div class="kline"><span class="k">守点</span><span class="v">' + pts.length + ' 个</span></div>' +
      '<div class="kline"><span class="k">是否生效</span><span class="v" style="color:' + (functional ? '#68d9a6' : '#f5c56a') + '">' + (functional ? '是（NanoGuard）' : '否（旧类 / 未归属）') + '</span></div>' +
      '<div class="sect">守点列表</div>' +
      '<div class="tags">' + (pts.slice(0, 24).map(function (f) {
        return '<span class="tag">' + (f.aux != null ? '#' + f.aux + ' ' : '') + f.x.toFixed(1) + ', ' + f.z.toFixed(1) + '</span>';
      }).join('') || '<span class="tag">没有守点</span>') + '</div>' +
      '<div class="sect">说明</div>' +
      '<div class="note">' + (functional
        ? 'NanoGuard 会把这个守区下的守点收集起来；安全度 _safety、入口 entrancePos、逃跑 escapePos、邻区 neighborAreas 当前导出里没有，所以不画也不编。'
        : 'Bot_GuardArea / Bot_GuardPos 是旧类，docs 确认没人用；插件自动铺守区时查的是 NanoGuardArea，不会因为旧守卫区存在就跳过。') + '</div>' +
      '<div class="note">分组按“守点到守区中心的最近距离”算，只用于看图，不改游戏数据。</div>';
    return;
  }
  var z = ST.zones[it.index];
  $('zoneTitle').textContent = z.id + ' ' + z.name;
  $('zoneMeta').textContent = z.kind + ' · ' + z.pts.length + ' 顶点';
  $('mbZone').innerHTML = '<i style="--c:' + z.color + '"></i><b>' + z.id + '</b> ' + esc(z.name);
  $('zoneRule').textContent = z.shape === 'poly' ? '多边形' : z.shape;
  $('zoneKk').textContent = z.pts.length + ' 顶点';
  $('zoneDetail').innerHTML = '' +
    '<div class="kline"><span class="k">类型</span><span class="v c" style="--c:' + z.color + '">' + esc(z.kind) + '</span></div>' +
    '<div class="kline"><span class="k">形状</span><span class="v">' + esc(z.shape) + '</span></div>' +
    '<div class="kline"><span class="k">顶点</span><span class="v">' + z.pts.length + '</span></div>' +
    '<div class="note" style="margin-top:8px">地图 JSON 的 zones[] 图层；插件不读，不影响寻路。</div>';
}

function bindZoneList() {
  $('zoneList').addEventListener('click', function (e) {
    var row = e.target.closest('[data-zone]');
    if (!row) return;
    var items = zoneItems();
    var it = items[+row.dataset.zone];
    if (!it) return;
    ST.selZone = { type: it.type, index: it.index };
    if (it.type === 'area' || it.type === 'loose') {
      var g = zoneGroups()[it.index];
      var pts = (g.pts.length ? g.pts : [{ x: g.x, y: g.y, z: g.z }]).map(function (f) { return [f.x, f.y, f.z]; });
      fitToPoints(pts);
    } else {
      fitToPoints(ST.zones[it.index].pts);
    }
    renderZones();
    drawAll();
  });
}

/* =====================================================================
 * 9. 自动铺设
 * ===================================================================*/
function actionState(key) {
  var cfg = ST.wb && ST.wb.config;
  if (!cfg || !cfg.exists) return { on: null, text: '未知', why: '没找到 ucf_mod.json' };
  var v = cfg.features && cfg.features[key];
  return { on: !!v, text: v ? 'ON' : 'OFF', why: v ? '开关已开' : '开关关闭' };
}

function renderAuto() {
  var m = ST.cur, s = ST.stats, wb = ST.wb;
  if (!m || !s) return;
  var cfg = (wb && wb.config) || {};
  var feat = cfg.features || {};
  var k = s.kinds;
  var way = actionState('auto_waypoints');
  var cr = actionState('auto_crouch');
  var ga = actionState('ghost_areas');
  var dis = cfg.enabled === false;
  var co = !!feat.collect_only;
  var packNogen = false;
  if (cfg.pack && cfg.pack.on && cfg.pack.name) {
    (wb.packs || []).forEach(function (p) { if (p.name === cfg.pack.name) packNogen = !!p.nogen; });
  }

  function result(on, cond, yes, no) {
    if (on === null) return { cls: 'skip', text: '未知', desc: '没找到部署端的 ucf_mod.json。' };
    if (dis) return { cls: 'skip', text: '插件关', desc: '插件总开关关闭，什么都不会跑。' };
    if (on === false) return { cls: 'off', text: 'OFF', desc: '开关关闭。' };
    if (co) return { cls: 'skip', text: '跳过', desc: '只读采集开着，插件不创建对象。' };
    if (packNogen) return { cls: 'skip', text: '跳过', desc: '当前测试包有 nogen.txt，自动铺点被关掉。' };
    return cond ? { cls: 'on', text: yes.t, desc: yes.d } : { cls: 'off', text: no.t, desc: no.d };
  }

  var rw = result(way.on, m.auto.waypoints,
    { t: '会铺', d: '这张图 PointGraph 是 0 节点，进图会沿可走面铺点并连边。' },
    { t: '不会', d: '这张图已经有 ' + m.nodes + ' 个点，插件跳过自动铺点。' });
  var rc = result(cr.on, m.auto.crouch,
    { t: '会补', d: '这张图蹲守点是 0，进图会按 9 m 网格补 Bot_CrouchPos。' },
    { t: '不会', d: '这张图已经有 ' + ((k.crouch) || 0) + ' 个蹲守点，插件跳过。' });
  var rg = result(ga.on, m.auto.guard,
    { t: '会造', d: '这张图 NanoGuardArea 是 0，进图会从采样点里造守区并挂守点。' },
    { t: '不会', d: '这张图已经有 ' + ((k.nano_area) || 0) + ' 个幽灵守区，插件跳过。' });

  $('autoCfgChip').textContent = cfg.exists ? (cfg.enabled ? '插件开' : '插件关') : '无配置';
  $('autoActions').innerHTML =
    autoActHtml('W', '自动铺路点 + 连线', 'auto_waypoints', way, rw, 'PointGraph 节点数 = 0 才触发；已有路点的图不动。') +
    autoActHtml('C', '自动补蹲守点', 'auto_crouch', cr, rc, 'SpareList_BL 里没有蹲守点才触发。') +
    autoActHtml('G', '自动造幽灵守区', 'ghost_areas', ga, rg, 'NanoGuardArea.SpareAreaList 为空才触发；旧 guard_area 不算。');

  $('autoCfgNote').innerHTML = cfg.exists
    ? ('配置：<b>' + esc(cfg.path) + '</b><br>插件总开关 <b>' + (cfg.enabled ? '开' : '关') + '</b> · 场景 <b>' + esc(cfg.scene || '—') +
       '</b> · 草稿 <b>' + (cfg.pack && cfg.pack.on ? esc(cfg.pack.name) : '不启用') + '</b> · 只读采集 <b>' + (co ? '开' : '关') +
       '</b><br>开关改完写进 ucf_mod.json，<b>下次进图生效</b>；网页端不能触发。')
    : '没有找到部署端的 ucf_mod.json；自动铺设开关状态未知。';

  $('autoMapSub').textContent = (m.label || m.level) + ' · ' + m.level;
  $('autoMapChip').textContent = dis ? '插件关' : '只读';
  $('autoMapBody').innerHTML = '' +
    '<div class="kline"><span class="k">点图节点</span><span class="v">' + m.nodes + '</span></div>' +
    '<div class="kline"><span class="k">自动铺点</span><span class="v" style="color:' + (m.auto.waypoints ? '#7fe0b3' : '#8fa5c0') + '">' + (m.auto.waypoints ? '触发（0 点）' : '跳过（已有 ' + m.nodes + ' 点）') + '</span></div>' +
    '<div class="kline"><span class="k">蹲守点</span><span class="v">' + ((k.crouch) || 0) + ' · ' + (m.auto.crouch ? '会自动补' : '已存在，跳过') + '</span></div>' +
    '<div class="kline"><span class="k">幽灵守区</span><span class="v">' + ((k.nano_area) || 0) + ' · ' + (m.auto.guard ? '会自动造' : '已存在，跳过') + '</span></div>' +
    '<div class="kline"><span class="k">旧守卫区</span><span class="v">' + ((k.guard_area) || 0) + ' · 不参与判断</span></div>' +
    '<div class="kline"><span class="k">可走面</span><span class="v">' + (m.navmesh ? '有导出' : '没有导出') + '</span></div>' +
    '<div class="kline"><span class="k">结论</span><span class="v">' + (dis ? '插件关闭' : (co ? '只读采集，全部跳过' : (packNogen ? 'nogen.txt，铺点跳过' : '按上面三个开关跑'))) + '</span></div>' +
    '<div class="note" style="margin-top:8px">当前查看的是' + viewLabel() +
      (ST.view === 'pack' && ST.pack ? (' · ' + shortPack(ST.pack)) : '') +
      '；游戏实际读「② 成品」已发布的图，或「② 编辑中」当前草稿；下面的触发判断按当前这份的点数估算。</div>' +
    '<div class="note" style="margin-top:6px">自动铺设发生在<b>场景加载后</b>，由插件在主线程做；网页只读，不能点按钮触发。要立刻试：控制台改开关 → 开始游戏进图。</div>';

  $('autoPipe').innerHTML = [
    ['1', '粗扫地面', '20 m 网格，y=300 向下射线，确定 bbox'],
    ['2', '细扫 4 m', '每列最多追 5 层，y ∈ [-30, 15]'],
    ['3', '铺点', '每个命中点建一个 UCF_WayPoints 子物体'],
    ['4', '连边', 'maxDistance 4.6 m + raycast 挡视线'],
    ['5', '补蹲守', '9 m 网格，法线 ≥ 0.8'],
    ['6', '造守区', '每 11 个采样点取 1 个，≤64 个']
  ].map(function (x) {
    return '<div class="step on"><span class="n">' + x[0] + '</span><div><div class="t">' + x[1] + '</div><div class="d">' + x[2] + '</div></div></div>';
  }).join('');

  $('autoRules').innerHTML = '' +
    '<div class="kline"><span class="k">铺点条件</span><span class="v">PointGraph 节点数 == 0</span></div>' +
    '<div class="kline"><span class="k">蹲点条件</span><span class="v">SpareList_BL == 0</span></div>' +
    '<div class="kline"><span class="k">守区条件</span><span class="v">SpareAreaList == 0</span></div>' +
    '<div class="kline"><span class="k">连边半径</span><span class="v">4.6 m + raycast</span></div>' +
    '<div class="kline"><span class="k">跳点</span><span class="v">不自动生成</span></div>' +
    '<div class="sect">所有地图的触发判断</div>' +
    '<table class="mtable"><thead><tr><th>地图</th><th>点</th><th>蹲守</th><th>守区</th><th>铺点</th></tr></thead><tbody>' +
    (ST.maps || []).map(function (x) {
      var c = x.status === 'missing' ? '—' : (x.auto.waypoints ? '会' : '跳过');
      return '<tr><td>' + esc(x.label || x.level) + '</td><td class="mono">' + x.nodes + '</td><td class="mono">' +
        ((x.kinds && x.kinds.crouch) || 0) + '</td><td class="mono">' + ((x.kinds && x.kinds.nano_area) || 0) +
        '</td><td class="' + (x.auto.waypoints ? 'ok' : 'no') + '">' + c + '</td></tr>';
    }).join('') + '</tbody></table>' +
    '<div class="note" style="margin-top:8px">来源：src/navfix.c（survey / act_waypoints / act_crouch / act_guard）与 src/cfg.c。网页端只读，不执行。</div>';
}

function autoActHtml(code, title, key, st, r, desc) {
  return '<div class="autoact">' +
    '<div class="st ' + r.cls + '">' + esc(r.text) + '</div>' +
    '<div style="flex:1"><b>' + esc(title) + '</b><p>' + esc(desc) + '</p>' +
    '<p><code>' + key + '</code> · 配置 ' + esc(st.text) + ' · ' + esc(r.desc) + '</p></div></div>';
}

/* =====================================================================
 * 10. 地图数据
 * ===================================================================*/
function renderMaps() {
  var wb = ST.wb;
  if (!wb) return;
  var maps = wb.maps || [];
  $('mapsSub').textContent = maps.length + ' 张图 · ' + viewLabel() +
    (ST.view === 'pack' && ST.pack ? (' · ' + shortPack(ST.pack)) : '');
  $('mapTbody').innerHTML = maps.map(function (m) {
    var status = '—';
    var cls = 'no';
    if (m.status === 'ok') { status = '✓ 已采集'; cls = 'ok'; }
    else if (m.status === 'tiny') { status = '! 点图很小'; cls = 'warn'; }
    else if (m.status === 'empty') { status = '— 无点图'; cls = 'no'; }
    else if (m.status === 'missing') { status = m.navmesh ? '— 仅可走面' : '— 待采集'; cls = 'no'; }
    if (m.suspect) { status = '? 未识别'; cls = 'warn'; }
    var on = ST.cur && (ST.cur.file ? (ST.cur.file === m.file && (ST.cur.pack || '') === (m.pack || '')) : (!m.file && ST.cur.level === m.level));
    var key = m.pack ? ('pack:' + m.pack) : (m.file || ('level:' + (m.level || '')));
    /* 三版之后：成品（final 当前版本里有没有这张图）+ 编辑中（packs 里几个包）+ 收件箱导出份数 */
    var fin = m.final || {};
    var packs = m.packs || [];
    var packTitle = packs.length
      ? packs.map(function (p) {
          var stale = p.fp && m.fp && p.fp !== m.fp;
          return p.name + ' · ' + (p.ops || 0) + ' 条' + (stale ? ' · ✖ 指纹失效' : '') +
            ((p.full || p.name) === ST.pack ? ' · ← 正在看' : '');
        }).join('\n')
      : '没有编辑中的包';
    var mapCell = esc(m.label || '—') + (m.exports ? '<br><span style="color:#4f5d70">导出 ' + m.exports + ' 份</span>' : '');
    return '<tr' + (on ? ' class="on"' : '') + ' data-map="' + esc(key) + '">' +
      '<td class="mono">' + esc(m.no) + '</td>' +
      '<td><span class="dot" style="--c:' + (m.status === 'missing' ? '#64748b' : '#4f8cff') + '"></span>' + mapCell + '</td>' +
      '<td class="mono">' + esc(m.level || '—') + '<br><span style="color:#4f5d70">' + esc(m.scene || '') + '</span></td>' +
      '<td class="mono">' + esc((m.fp || '—').slice(0, 18)) + '</td>' +
      '<td class="mono">' + m.nodes + ' / ' + m.edges + '</td>' +
      '<td class="mono">' + m.features + '</td>' +
      '<td class="' + (m.navmesh ? 'ok' : 'no') + '">' + (m.navmesh ? '有' : '—') + '</td>' +
      '<td class="' + (fin.has ? 'ok' : 'no') + '" title="成品里这张图的改动条数">' +
        (fin.has ? ('✓ ' + (fin.ops || 0)) : '—') + '</td>' +
      '<td class="' + (packs.length ? 'ok' : 'no') + '" title="' + esc(packTitle) + '">' +
        (packs.length ? (packs.length + ' 包') : '—') + '</td>' +
      '<td class="' + cls + '">' + status + '</td></tr>';
  }).join('');

  var v = wb.versions || {};
  var c = wb.consistency || {};
  function cmp(g) {
    if (!g) return '—';
    var d = (g.diff || []).length + (g.onlyA || []).length + (g.onlyB || []).length;
    return d ? (d + ' 个文件不同') : '一致';
  }
  $('verChip').textContent = viewLabel() + ' · 只读';
  /* 数据档：① 只读对照 / ② 成品（final 当前版）/ ② 编辑中（packs）。③ 部署版不是数据档。 */
  var dV = v.dev || {}, dFin = dV.final || {}, dPk = dV.packs || {}, dIn = dV.inbox || {};
  var cards = [
    { key: 'native', t: '① 备份版（只读对照）', x: v.native || {}, sub: [
        ((v.native || {}).maps || 0) + ' 图 · ' + ((v.native || {}).navmesh || 0) + ' 可走面 · ' + fmtBytes((v.native || {}).bytes || 0),
        '最近写入 ' + shortTime((v.native || {}).latest),
        '原生快照，游戏不读它'] },
    { key: 'final', t: '② 成品（游戏启动用）', x: { path: dFin.path || '' }, sub: [
        dFin.maps ? ('已发布 ' + dFin.maps + ' 张图') : '成品还没有发布（启动 = 全原生）',
        '每张图一份 · ' + fmtBytes(dFin.bytes || 0),
        '只读；没有版本下拉'] },
    { key: 'pack', t: '② 编辑中（packs）', x: { path: (wb.profile && wb.profile.packs) || '' }, sub: [
        (dPk.n || 0) + ' 张图有草稿 · ' + fmtBytes(dPk.bytes || 0),
        '最近写入 ' + shortTime(dPk.latest),
        '可写沙盒；网页只读'] }
  ];
  $('verBody').innerHTML = cards.map(function (o) {
    var x = o.x || {};
    return '<div class="whitecard vercard' + (o.key === ST.view ? ' cur' : '') + '" data-view="' + o.key + '">' +
      '<div class="wt">' + o.t + (o.key === ST.view ? ' · 正在看' : '') + '</div><div class="wd">' +
      esc(x.path || '—') + '<br>' + o.sub.map(function (s) { return esc(s); }).join('<br>') + '</div></div>';
  }).join('') +
    '<div class="kline"><span class="k">① vs ② 地图</span><span class="v">' + cmp(c.nativeDev && c.nativeDev.maps) + '</span></div>' +
    '<div class="note" style="margin-top:6px">点上面的卡片切数据档；游戏目录（运行时）只供日志 / 配置，不在这里。</div>' +
    '<div class="kline"><span class="k">收件箱（vis）</span><span class="v">' + (dIn.exports || 0) + ' 份导出 · ' + fmtBytes(dIn.bytes || 0) + '</span></div>' +
    '<div class="sect">编辑中（草稿）</div>' +
    ((wb.packs || []).map(function (p) {
      var pn = shortPack(p.name);
      var mf = maps.filter(function (m) { return m.folder === p.folder; })[0] || {};
      var stale = !!(p.fp && mf.fp && p.fp !== mf.fp);
      var kind = p.grow ? 'grow' : (p.keep ? 'keep' : (p.blank ? '空白底图' : '增量'));
      return '<div class="whitecard vercard' + (p.name === ST.pack ? ' cur' : '') + (stale ? ' stale' : '') +
        '" title="' + esc(p.name || '') + '" data-pack-view="' + esc(p.name) + '">' +
        '<div class="wt">' + esc(pn) + ' · ' + esc(kind) +
        (stale ? ' · <span style="color:#ff7b7b">✖ 指纹失效</span>' : '') +
        (p.name === ST.pack ? ' · 正在看' : '') + '</div><div class="wd">' +
        esc(p.label || '') + ' · ' + esc(p.level || '') + ' · ' + (p.ops || 0) + ' 条 · ' +
        esc(shortTime(p.created)) + (p.nogen ? ' · nogen' : '') +
        '<br>' + (stale ? '旧草稿，插件不会读；去控制台「编辑中」重建' : '点这张卡片查看这个草稿') +
        '</div></div>';
    }).join('') || '<div class="note">② 开发版的 packs\\ 里还没有草稿。</div>') +
    '<div class="sect">成品（每图一份）</div>' +
    (dFin.maps
      ? '<div class="whitecard vercard' + (ST.view === 'final' ? ' cur' : '') + '" data-view="final">' +
        '<div class="wt">' + esc(dFin.maps + ' 张图') + (ST.view === 'final' ? ' · 正在看' : '') + '</div><div class="wd">' +
        '共 ' + (dFin.maps || 0) + ' 张图 · ' + fmtBytes(dFin.bytes || 0) +
        '<br>最近发布 ' + esc(shortTime(dFin.latest)) + ' · 每张图一份，没有版本' +
        '</div></div>'
      : '<div class="note">成品里还没有发布：控制台「人机路点 → 编辑中 → 发布这张图到成品」。</div>') +
    '<div class="sect">命令行（网页不执行）</div>' +
    '<div class="comp" style="white-space:normal;line-height:1.8">python core/navdata.py pack list<br>' +
    'python core/navdata.py pack promote 地图文件夹 &nbsp;→ 覆盖同图那份成品<br>' +
    'python core/navdata.py final list（撤销发布：final rm &lt;指纹&gt;）</div>';
}

function bindMapTable() {
  $('mapTbody').addEventListener('click', function (e) {
    var tr = e.target.closest('[data-map]');
    if (!tr) return;
    var file = tr.dataset.map;
    var m = ST.maps.filter(function (x) {
      return (x.pack ? ('pack:' + x.pack) : (x.file || ('level:' + (x.level || '')))) === file;
    })[0];
    if (!m) return;
    if (m.status === 'missing' && !m.navmesh) {
      toast('这张图还没有文件，先在游戏里 Ctrl+E 导出', 'err');
      return;
    }
    loadMap(m);
  });
}

/* =====================================================================
 * 11. 日志
 * ===================================================================*/
var LOG_CATS = ['全部', '自动铺设', '导航', '编辑', '导出', '测试包', '车测', '配置', '数据'];
function parseLogs() {
  var wb = ST.wb;
  var out = [];
  var re = /^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) \[([^\]]+)\] (.*)$/;
  ((wb && wb.log) || []).forEach(function (line) {
    var m = re.exec(line);
    if (!m) {
      if (line.trim()) out.push({ date: '', time: '', tag: '', msg: line, cat: '其它', color: '#8fa5c0' });
      return;
    }
    var tag = m[3], msg = m[4];
    var cat = '其它', color = '#8fa5c0';
    if (tag === 'at') { cat = '车测'; color = '#38d9f5'; }
    else if (tag === 'cfg') { cat = '配置'; color = '#8fa5c0'; }
    else if (tag === 'nav') {
      if (/setup:|waypoints:|crouch:|guard areas:|survey:/.test(msg)) { cat = '自动铺设'; color = '#a78bfa'; }
      else { cat = '导航'; color = '#4f8cff'; }
    } else if (tag === 'edit') {
      if (/export/i.test(msg)) { cat = '导出'; color = '#3ecf8e'; }
      else if (/pack/i.test(msg)) { cat = '测试包'; color = '#f5b942'; }
      else { cat = '编辑'; color = '#f5b942'; }
    }
    out.push({ date: m[1], time: m[2], tag: tag, msg: msg, cat: cat, color: color });
  });
  ((wb && wb.events) || []).forEach(function (e) {
    out.push({ date: '', time: e.time || '', tag: 'data', msg: e.text || '', cat: '数据', color: '#3ecf8e' });
  });
  out.sort(function (a, b) {
    var ta = a.date ? (a.date + ' ' + a.time) : (a.time || '');
    var tb = b.date ? (b.date + ' ' + b.time) : (b.time || '');
    return tb.localeCompare(ta);
  });
  ST.logs = out;
}

function renderLogs() {
  parseLogs();
  var filters = LOG_CATS.map(function (c) {
    return '<span class="preset' + (ST.logFilter === c ? ' on' : '') + '" data-logfilter="' + c + '">' + c + '</span>';
  }).join('') +
    '<span class="preset' + (ST.showResolve ? ' on' : '') + '" data-resolve="1">底层 resolve</span>' +
    '<span class="preset" data-copylog="1">复制日志</span>';
  $('logFilters').innerHTML = filters;
  var rows = ST.logs.filter(function (l) {
    if (!ST.showResolve && /resolve:|\[at\] resolve/.test(l.msg)) return false;
    if (ST.logFilter !== '全部' && l.cat !== ST.logFilter) return false;
    return true;
  }).slice(0, 300);
  $('logSub').textContent = 'ucf_mod.log · 游戏目录运行日志 · ' + rows.length + ' 行';
  $('logSub').title = (ST.wb && ST.wb.logFile) || 'ucf_mod.log';
  $('logList').innerHTML = rows.map(function (l) {
    var time = l.date ? (l.date + ' ' + l.time) : (l.time || '—');
    return '<div class="logrow"><time>' + esc(time) + '</time><span class="ty" style="--c:' + l.color + '">' +
      esc(l.cat) + '</span><span>' + esc(l.msg) + '</span><span class="det">' + esc(l.tag ? '[' + l.tag + ']' : '') + '</span></div>';
  }).join('') || '<div class="empty">没有匹配的日志。进游戏跑一次再回来刷新；日志只读，不改。</div>';
  if (ST.logFilter === '数据') {
    $('logChip').textContent = '文件事件';
  } else {
    $('logChip').textContent = '只读';
  }
}

function bindLogs() {
  $('logFilters').addEventListener('click', function (e) {
    var f = e.target.closest('[data-logfilter]');
    if (f) { ST.logFilter = f.dataset.logfilter; renderLogs(); return; }
    var r = e.target.closest('[data-resolve]');
    if (r) { ST.showResolve = !ST.showResolve; renderLogs(); return; }
    var cp = e.target.closest('[data-copylog]');
    if (cp) {
      var text = ST.logs.slice(0, 200).map(function (l) { return (l.date ? l.date + ' ' : '') + (l.time || '') + ' ' + l.msg; }).join('\n');
      try {
        navigator.clipboard.writeText(text).then(function () { toast('日志已复制', 'ok'); },
          function () { toast('复制失败：浏览器不允许', 'err'); });
      } catch (x) { toast('复制失败：浏览器不允许', 'err'); }
    }
  });
}

function startLogTimer() {
  stopLogTimer();
  ST.logTimer = setInterval(function () {
    if (ST.page !== 'logs' || ST.busy) return;
    refreshData(true);
  }, 5000);
}
function stopLogTimer() {
  if (ST.logTimer) { clearInterval(ST.logTimer); ST.logTimer = null; }
}

/* =====================================================================
 * 12. 载入 / 刷新 / 启动
 * ===================================================================*/
function splash(on, msg) {
  var s = $('mapSplash');
  if (!s) return;
  if (on) {
    s.classList.add('on');
    var p = $('splashMsg');
    if (p) p.textContent = msg || '';
  } else {
    s.classList.remove('on');
  }
}

function loadMap(entry) {
  ST.nm = null;
  if (!entry) {
    ST.cur = null;
    ST.doc = null;
    ST.nodes = []; ST.edges = []; ST.feats = [];
    ST.stats = null;
    updateHeader();
    showPage(ST.page);
    return;
  }
  ST.cur = entry;
  if (ST.view === 'pack') {
    ST.pack = choosePackForMap(entry);
    ST.pendingPack = '';
  } else {
    ST.pack = '';
  }
  updatePackSel();
  syncURL();
  /* 只有可走面的图（胜利广场 / 死亡擂台）：没有点图 JSON，直接读 navmesh */
  if (!entry.file) {
    if (!entry.navmesh) {
      ST.doc = null;
      ST.nodes = []; ST.edges = []; ST.feats = []; ST.routes = []; ST.zones = [];
      ST.jumpLinks = []; ST.jumpOrphans = [];
      rebuild();
      ST.stats = modelStats();
      updateHeader();
      showPage(ST.page);
      return;
    }
    ST.busy = true;
    splash(true, '读取可走面 ' + (entry.level || ''));
    ST.doc = null;
    ST.nodes = []; ST.edges = []; ST.feats = []; ST.routes = []; ST.zones = [];
    ST.jumpLinks = []; ST.jumpOrphans = [];
    rebuild();
    ST.stats = modelStats();
    loadNavmesh(entry.level).then(function (nm) {
      ST.busy = false;
      splash(false);
      if (!nm) {
        toast('这张图没有可走面导出（NavMeshGraph）', 'err');
        updateHeader();
        renderAll();
        drawAll();
        return;
      }
      ST.bounds = nmBounds(nm);
      ST.cam.zoom = 1;
      fitCam();
      updateHeader();
      if (ST.dockOpen) openDock(true);
      renderAll();
      drawAll();
      toast((entry.label || entry.level) + ' · 仅可走面 ' + nm.tri + ' 三角', 'ok');
    });
    return;
  }
  ST.busy = true;
  splash(true, '读取 ' + entry.file);
  var dir = entry.dir || 'maps';
  var q = '/api/raw?dir=' + encodeURIComponent(dir) + '&file=' + encodeURIComponent(entry.file);
  api(q).then(function (doc) {
    if (!doc || !doc.nodes) throw new Error((doc && doc.error) || '文件不是导航数据');
    var fp = (doc.map && doc.map.fingerprint) || entry.fp || '';
    /* 成品档读 final\<当前版本>\<指纹>.txt；编辑中档读 packs\<图>\<包>\<指纹>.txt。 */
    var txtP;
    if (ST.view === 'pack') {
      txtP = ST.pack
        ? api('/api/pack-txt?name=' + encodeURIComponent(ST.pack) + '&fp=' + encodeURIComponent(fp))
        : Promise.resolve({ text: '', exists: false });
    } else if (ST.view === 'final' && dir === 'maps' && fp) {
      txtP = api('/api/txt?fp=' + encodeURIComponent(fp));
    } else {
      txtP = Promise.resolve({ text: '', exists: false });
    }
    return txtP.then(function (txt) {
      if (ST.view === 'pack' && ST.pack && txt && txt.exists === false) {
        toast('这个包里没有当前指纹的清单：显示的是基准点图', 'err');
      }
      buildModel(doc, txt);
      ST.cur = entry;
      fitCam();
      ST.selLayer = ST.selLayer || 'node_walk';
      if (!modeAllows(ST.selLayer)) ST.selLayer = 'node_walk';
      ST.focus = ST.focus || null;
      if (ST.focus && !modeAllows(ST.focus)) ST.focus = null;
      ST.selRoute = null;
      ST.selZone = null;
      ST.busy = false;
      splash(false);
      updateHeader();
      if (ST.dockOpen) openDock(true);
      renderAll();
      drawAll();
      var s = ST.stats;
      toast((entry.label || entry.level) + ' · ' + s.nodes + ' 点 / ' + s.edges + ' 边', 'ok');
      loadNavmesh(entry.level).then(function (nm) {
        if (!nm) return;
        var mb = modelBounds();
        ST.bounds = {
          lo: [Math.min(mb.lo[0], nm.lo[0]), Math.min(mb.lo[1], nm.lo[1])],
          hi: [Math.max(mb.hi[0], nm.hi[0]), Math.max(mb.hi[1], nm.hi[1])]
        };
        fitCam();
        drawAll();
        renderMapInfo();
        if (ST.page === 'overview') renderOverview();
      });
      if (ST.autoDock) { ST.autoDock = false; openDock(); }
    });
  }).catch(function (e) {
    ST.busy = false;
    splash(false);
    toast('载入失败：' + e.message, 'err');
  });
}

function renderAll() {
  updateHeader();
  renderLayerList();
  renderLayerDetail();
  renderMapInfo();
  renderStats();
  renderLegend();
  renderQuickLists();
  if (ST.page === 'overview') renderOverview();
  if (ST.page === 'routes') renderRoutes();
  if (ST.page === 'zones') renderZones();
  if (ST.page === 'auto') renderAuto();
  if (ST.page === 'maps') renderMaps();
  if (ST.page === 'logs') renderLogs();
}

function drawAll() {
  if (ST.page === 'overview') drawHero();
  if (ST.page === 'waypoints') drawMap($('cvMain'), 'main');
  if (ST.page === 'routes') drawMap($('cvRoute'), 'route');
  if (ST.page === 'zones') drawMap($('cvZone'), 'zone');
  var z = $('zoomVal');
  if (z) z.textContent = Math.round(ST.cam.zoom * 100) + '%';
  var cv = $('cvMain');
  if (cv && cv.getBoundingClientRect().width > 2) {
    var st = $('scaleTxt');
    if (st) st.textContent = niceStep(viewOf(cv).s) + ' m';
  }
}

function drawHero() {
  var cv = $('cvHero');
  if (!cv) return;
  var g = ctxOf(cv), c = g.c, W = g.w, H = g.h;
  c.clearRect(0, 0, W, H);
  c.fillStyle = '#080c12'; c.fillRect(0, 0, W, H);
  if (!ST.nm && !ST.nodes.length) { drawEmpty(c, W, H, '没有载入地图'); return; }
  var b = ST.bounds;
  var dx = Math.max(1, b.hi[0] - b.lo[0]), dz = Math.max(1, b.hi[1] - b.lo[1]);
  var s = Math.min((W - 12) / dx, (H - 10) / dz);
  var cx = (b.lo[0] + b.hi[0]) / 2, cz = (b.lo[1] + b.hi[1]) / 2;
  function m(x, z) { return [ (x - cx) * s + W / 2, (z - cz) * s + H / 2 ]; }
  if (ST.nm) {
    var vi = ST.nm.verts, ii = ST.nm.idx;
    c.beginPath();
    for (var i = 0; i < ii.length; i += 3) {
      var a0 = ii[i] * 3, b0 = ii[i + 1] * 3, d0 = ii[i + 2] * 3;
      var qa = m(vi[a0], vi[a0 + 2]), qb = m(vi[b0], vi[b0 + 2]), qd = m(vi[d0], vi[d0 + 2]);
      c.moveTo(qa[0], qa[1]); c.lineTo(qb[0], qb[1]); c.lineTo(qd[0], qd[1]); c.closePath();
    }
    c.fillStyle = 'rgba(38,224,142,.06)';
    c.fill();
    c.strokeStyle = 'rgba(38,224,142,.2)';
    c.lineWidth = 0.4;
    c.stroke();
  }
  c.strokeStyle = 'rgba(126,152,183,.16)';
  c.lineWidth = 0.5;
  c.beginPath();
  ST.edges.forEach(function (e) {
    var a = ST.nodes[e[0]], d = ST.nodes[e[1]];
    if (!a || !d || !a.alive || !d.alive) return;
    var pa = m(a.x, a.z), pb = m(d.x, d.z);
    c.moveTo(pa[0], pa[1]); c.lineTo(pb[0], pb[1]);
  });
  c.stroke();
  c.fillStyle = '#7f93ab';
  ST.nodes.forEach(function (n) {
    if (!n.alive) return;
    var q = m(n.x, n.z);
    c.fillRect(q[0], q[1], 1.1, 1.1);
  });
  ST.jumpLinks.forEach(function (j) {
    var a = m(j.a[0], j.a[2]), d = m(j.b[0], j.b[2]);
    c.strokeStyle = 'rgba(56,217,245,.7)';
    c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(d[0], d[1]); c.stroke();
  });
}

function refreshData(quiet) {
  if (ST.busy) return;
  ST.busy = true;
  api('/api/workbench').then(function (wb) {
    if (!wb || !wb.ok) throw new Error((wb && wb.error) || '接口失败');
    var newMode = (wb.profile && (wb.profile.mode || wb.profile.profile)) || ST.view;
    var changed = newMode !== ST.view;
    ST.wb = wb;
    ST.maps = wb.maps || [];
    ST.busy = false;
    applyView(wb);
    setConn(true, '本地只读服务 · ' + (wb.profile ? wb.profile.cn : ''));
    if (changed) {
      /* 数据档被别处改了：保留当前地图，按新档重载；新档里没有这张图就清空 */
      toast('数据档已切换：' + viewLabel(), 'ok');
      var old0 = ST.cur;
      var pick0 = findMapLike(old0);
      if (!pick0) { showEmptyMap(); renderAll(); showPage(ST.page); return; }
      ST.cur = pick0;
      if (ST.view === 'pack') ST.pack = choosePackForMap(pick0);
      updateHeader(); updatePackSel(); renderMaps();
      loadMap(pick0);
      return;
    }
    if (!ST.cur) {
      updateHeader();
      updatePackSel();
      renderMaps();
      if (ST.page === 'overview') renderOverview();
      return;
    }
    var cur = findMapLike(ST.cur) || ST.cur;
    ST.cur = cur;
    if (ST.view === 'pack') ST.pack = choosePackForMap(cur);
    updateHeader();
    updatePackSel();
    renderMaps();
    if (ST.page === 'logs') renderLogs();
    if (ST.page === 'overview') renderOverview();
    if (ST.page === 'auto') renderAuto();
    if (!quiet) toast('已刷新', 'ok');
  }).catch(function (e) {
    ST.busy = false;
    setConn(false, 'navserver 未连接');
    toast('刷新失败：' + e.message + '（先开控制台 → 路点工作台）', 'err');
  });
}

function findMapLike(old) {
  if (!old) return null;
  if (old.file) {
    return ST.maps.filter(function (m) {
      return m.file === old.file && (m.dir || 'maps') === (old.dir || 'maps');
    })[0] || null;
  }
  return ST.maps.filter(function (m) { return !m.file && m.level === old.level; })[0] || null;
}

function savePackPrefs() {
  lsSet(STORAGE_PACKS, JSON.stringify(ST.packByFolder || {}));
}

function switchView(v, opts) {
  opts = opts || {};
  if (!v || (v === ST.view && !opts.force) || ST.busy) return;
  ST.busy = true;
  var old = ST.cur;
  api('/api/profile?set=' + encodeURIComponent(v)).then(function (j) {
    if (!j || !j.ok) throw new Error((j && j.error) || '切换数据档失败');
    ST.viewNote = (j.profile && j.profile.note) || '';
    return api('/api/workbench');
  }).then(function (wb) {
    if (!wb || !wb.ok) throw new Error((wb && wb.error) || '读取新数据档失败');
    ST.wb = wb;
    ST.maps = wb.maps || [];
    applyView(wb);                 /* applyView 里按 server 的 mode 校正 ST.view */
    setConn(true, '本地只读服务 · ' + (wb.profile ? wb.profile.cn : ''));

    var pick = null;
    if (opts.packName) {
      var pk = (wb.packs || []).filter(function (p) { return p.name === opts.packName; })[0];
      if (pk) {
        ST.pendingPack = pk.name;
        ST.packByFolder[pk.folder] = pk.name;
        savePackPrefs();
        pick = ST.maps.filter(function (m) { return m.folder === pk.folder; })[0] || null;
      }
    }
    if (!pick && opts.mapFile) {
      pick = ST.maps.filter(function (m) { return m.file === opts.mapFile; })[0] || null;
    }
    if (!pick) pick = findMapLike(old);

    if (ST.view === 'pack') {
      ST.pack = pick ? choosePackForMap(pick) : '';
    } else {
      ST.pack = '';
    }
    syncURL();
    ST.busy = false;
    var note = ST.viewNote ? ('（' + ST.viewNote + '）') : '';
    toast('已切到 ' + viewLabel() + (pick ? (' · ' + (pick.label || pick.level)) : '') + note, 'ok');
    if (pick) {
      ST.cam.zoom = 1;
      loadMap(pick);
    } else {
      /* 新档里没有当前这张图：整个模型清空，别让旧图的点留在画布上 */
      showEmptyMap();
      renderAll();
      showPage(ST.page);
      if (ST.dockOpen) openDock(true);   /* 没有对应地图也把 3D 换到新档 */
    }
  }).catch(function (e) {
    ST.busy = false;
    applyView(ST.wb);
    toast('切换数据档失败：' + e.message, 'err');
  });
}

function switchPack(name) {
  if (!name || name === ST.pack || ST.busy || !ST.cur) return;
  var valid = packsForMap(ST.cur).filter(function (p) { return !p.stale; });
  if (!valid.some(function (p) { return p.name === name; })) return;
  ST.pack = name;
  ST.packByFolder[ST.cur.folder] = name;
  savePackPrefs();
  syncURL();
  ST.cam.zoom = 1;
  updateHeader();
  loadMap(ST.cur);
}

/* 地图数据页点某个包：切到编辑中，并把那张图 + 那个包一起打开 */
function openPackView(name) {
  var pk = ((ST.wb && ST.wb.packs) || []).filter(function (p) { return p.name === name; })[0];
  if (!pk) return;
  var mf = ST.maps.filter(function (m) { return m.folder === pk.folder; })[0];
  if (!mf) { toast('没找到这个包对应的地图', 'err'); return; }
  if (pk.fp && mf.fp && pk.fp !== mf.fp) {
    toast('这个包的指纹和当前地图对不上，插件不会读它', 'err');
    return;
  }
  ST.pendingPack = pk.name;
  ST.packByFolder[pk.folder] = pk.name;
  savePackPrefs();
  if (ST.view !== 'pack') {
    switchView('pack', { packName: pk.name });
    return;
  }
  ST.pack = pk.name;
  ST.cam.zoom = 1;
  loadMap(mf);
}

function pickDefaultMap() {
  if (ST.startPack && ST.view === 'pack') {
    var pk0 = ((ST.wb && ST.wb.packs) || []).filter(function (p) { return p.name === ST.startPack; })[0];
    var mf0 = pk0 ? ST.maps.filter(function (m) { return m.folder === pk0.folder; })[0] : null;
    if (mf0) {
      ST.pendingPack = pk0.name;
      ST.packByFolder[pk0.folder] = pk0.name;
      savePackPrefs();
      loadMap(mf0);
      return;
    }
  }
  var want = ST.startMap || '';
  var pick = null;
  if (want) {
    pick = ST.maps.filter(function (m) {
      if (want.indexOf('level:') === 0) return !m.file && m.level === want.slice(6);
      return m.file === want;
    })[0];
  }
  if (pick) loadMap(pick);
  else showEmptyMap();
}

/* 没选地图：标题、画布、侧栏都回到空状态，不自动挑一张 */
function showEmptyMap() {
  ST.cur = null;
  ST.doc = null;
  ST.nm = null;
  ST.pack = '';
  ST.nodes = []; ST.edges = []; ST.feats = []; ST.routes = []; ST.zones = [];
  ST.jumpLinks = []; ST.jumpOrphans = [];
  ST.stats = null;
  ST.bounds = { lo: [-10, -10], hi: [10, 10] };
  updateHeader();
  updatePackSel();
  syncURL();
  drawAll();
}

function buildMapPicker() {
  var list = $('mapPick');
  var groups = [], byMode = {};
  (ST.maps || []).forEach(function (m) {
    var key = m.mode || '其他';
    if (!byMode[key]) {
      byMode[key] = { mode: key, order: (m.modeOrder == null ? 99 : m.modeOrder), rows: [] };
      groups.push(byMode[key]);
    }
    byMode[key].rows.push(m);
  });
  groups.sort(function (a, b) { return a.order - b.order; });
  list.innerHTML = groups.map(function (g) {
    var rows = g.rows.map(function (m) {
      var on = ST.cur && (ST.cur.file ? (ST.cur.file === m.file && (ST.cur.pack || '') === (m.pack || '')) : (!m.file && ST.cur.level === m.level));
      var off = m.status === 'missing';
      var mt = m.pack ? ((m.packBlank ? '空白底图' : '测试包') + ' · ' + m.nodes + ' 点')
        : (m.dir === 'vis') ? (m.mtime || '').slice(5, 16) : (m.nodes + ' 点');
      if (off) mt = m.navmesh ? '仅可走面' : '待采集';
      else if (ST.view === 'pack') mt += ' · ' + ((m.packs || []).length) + ' 包';
      var pickKey = m.pack ? ('pack:' + m.pack) : (m.file || '');
      return '<div class="pickrow' + (on ? ' on' : '') + (off && !m.navmesh ? ' off' : '') + '" data-pick="' + esc(pickKey) + '" data-level="' + esc(m.level || '') + '">' +
        '<span class="no">' + esc(m.no) + '</span><span class="nm">' + esc(m.label || m.level || '未命名') + '</span>' +
        '<span class="mt">' + esc(mt) + '</span></div>';
    }).join('');
    return '<div class="pickgroup">' + esc(g.mode) + '<span>' + g.rows.length + ' 张</span></div>' + rows;
  }).join('');
}

function bindTop() {
  $('viewSel').addEventListener('change', function () { switchView(this.value); });
  $('packSel').addEventListener('change', function () { switchPack(this.value); });
  $('ovVersions').addEventListener('click', function (e) {
    var card = e.target.closest('[data-view]');
    if (card) switchView(card.dataset.view);
  });
  $('verBody').addEventListener('click', function (e) {
    var pk = e.target.closest('[data-pack-view]');
    if (pk) { openPackView(pk.dataset.packView); return; }
    var card = e.target.closest('[data-view]');
    if (card) switchView(card.dataset.view);
  });
  $('btnPickMap').addEventListener('click', function (e) {
    e.stopPropagation();
    var p = $('mapPick');
    p.style.display = p.style.display === 'block' ? 'none' : 'block';
    buildMapPicker();
  });
  $('mapPick').addEventListener('click', function (e) {
    var row = e.target.closest('[data-pick]');
    if (!row) return;
    var file = row.dataset.pick;
    var m = ST.maps.filter(function (x) {
      if (file) return x.pack ? ('pack:' + x.pack) === file : x.file === file;
      return !x.file && !x.pack && (x.level || '') === row.dataset.level;
    })[0];
    if (!m) return;
    if (m.status === 'missing' && !m.navmesh) {
      toast('这张图还没有文件，先在游戏里 Ctrl+E 导出', 'err');
      return;
    }
    $('mapPick').style.display = 'none';
    ST.cam.zoom = 1;
    loadMap(m);
  });
  document.addEventListener('click', function () { $('mapPick').style.display = 'none'; });
  $('btnRefresh').addEventListener('click', function () {
    refreshData(false);
    if (ST.cur && ST.cur.file) setTimeout(function () { loadMap(ST.cur); }, 300);
  });
  $('btnReload').addEventListener('click', function () {
    refreshData(false);
    if (ST.cur && ST.cur.file) setTimeout(function () { loadMap(ST.cur); }, 300);
  });
  $('mapsReload').addEventListener('click', function () { refreshData(false); });
  $('logRefresh').addEventListener('click', function () { refreshData(false); });
  document.querySelectorAll('.nav[data-page]').forEach(function (n) {
    n.addEventListener('click', function () { showPage(n.dataset.page); });
  });
  document.querySelectorAll('[data-go]').forEach(function (b) {
    b.addEventListener('click', function () { showPage(b.dataset.go); });
  });
  document.querySelectorAll('.mapctl [data-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var k = b.dataset.toggle;
      ST.show[k] = !ST.show[k];
      b.classList.toggle('on', !!ST.show[k]);
      if (k === 'compass') syncCompassToDock();
      drawAll();
    });
  });
  $('zoomIn').addEventListener('click', function () { ST.cam.zoom = Math.min(40, ST.cam.zoom * 1.25); drawAll(); });
  $('zoomOut').addEventListener('click', function () { ST.cam.zoom = Math.max(0.08, ST.cam.zoom / 1.25); drawAll(); });
  $('zoomFit').addEventListener('click', function () { fitCam(); drawAll(); });
  $('nav3d').addEventListener('click', toggleDock);
  $('btnOpen3d').addEventListener('click', toggleDock);
  $('dockClose').addEventListener('click', closeDock);
  $('dockReload').addEventListener('click', function () { openDock(true); });
  $('dockFrame').addEventListener('load', function () {
    var s = $('dockSplash');
    if (s) s.classList.add('hide');
    syncCompassToDock();
  });
  bindDockGrip();
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ST.dockOpen) { e.preventDefault(); closeDock(); }
  });
  /* 3D 侧栏的 WASD：鼠标悬停在 iframe 上不会把键盘焦点给它，W/A/S/D 会落到本页。
   * 所以由本页转发（capture 阶段，先于本页其它按键处理），键值见 dockFlyKey。 */
  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (dockFlyKey(e, true)) e.preventDefault();
  }, true);
  document.addEventListener('keyup', function (e) {
    if (dockFlyKey(e, false)) e.preventDefault();
  }, true);
  window.addEventListener('blur', function () { dockPostMsg({ ucf: 'fly-stop' }); });
  /* 3D 画面里按 Esc：iframe 里的 navview 发消息回来，一起收起侧栏 */
  window.addEventListener('message', function (e) {
    if (e.origin !== 'null' && e.origin !== location.origin) return;
    var d = e.data || {};
    if (d.ucf === 'dock-close' && ST.dockOpen) closeDock();
    /* 3D 里的 navview 说「鼠标在/不在 3D 画面上」：只有鼠标在 3D 上时本页才转发 WASD */
    if (d.ucf === 'fly-hover') {
      ST.dockHover = !!d.on;
      if (!ST.dockHover) dockPostMsg({ ucf: 'fly-stop' });
      return;
    }
    /* 3D 侧栏里点了「方向」：平面图跟着一起开 / 关，两边永远是同一个状态 */
    if (d.ucf === 'compass' && typeof d.on === 'boolean' && ST.show.compass !== d.on) {
      ST.show.compass = d.on;
      var btn = document.querySelector('.mapctl [data-toggle="compass"]');
      if (btn) btn.classList.toggle('on', ST.show.compass);
      drawAll();
    }
  });
}

/* 3D 侧栏：停靠在当前页右侧，不跳页、不盖住工作台。
 * 宽度 / 是否打开记在 localStorage，下次打开工作台还是这个样子。 */
var DOCK_KEY = 'ucf_studio_dock_v1';
var DOCK_DEF = 480;

function dockPrefs() {
  try { return JSON.parse(localStorage.getItem(DOCK_KEY) || 'null') || {}; } catch (e) { return {}; }
}
function saveDockPrefs() {
  try { localStorage.setItem(DOCK_KEY, JSON.stringify({ open: !!ST.dockOpen, w: Math.round(ST.dockW) })); } catch (e) {}
}
function clampDockW(w) {
  var max = Math.max(360, Math.min(window.innerWidth * 0.56, 820));
  var min = Math.min(340, max);
  return Math.round(Math.max(min, Math.min(Number(w) || DOCK_DEF, max)));
}
function setDockWidth(w) {
  ST.dockW = clampDockW(w);
  document.documentElement.style.setProperty('--dockw', ST.dockW + 'px');
}
function initDockPrefs() {
  var j = dockPrefs();
  if (j && typeof j.w === 'number') ST.dockW = j.w;
  ST.dockWantOpen = !!(j && j.open);
  setDockWidth(ST.dockW);
}
function openDock(force) {
  var d = $('dock3d'), f = $('dockFrame'), sp = $('dockSplash');
  if (!d || !f) return;
  if (!ST.dockUrl) updateHeader();
  var url = ST.dockUrl || ('/navview.html?view=1&embed=1&notour=1&profile=' + encodeURIComponent(ST.view) +
    (ST.view === 'pack' && ST.pack ? '&pack=' + encodeURIComponent(ST.pack) : ''));
  d.classList.add('on');
  d.setAttribute('aria-hidden', 'false');
  var app = document.querySelector('.app');
  if (app) app.classList.add('docked');
  ST.dockOpen = true;
  setDockWidth(ST.dockW);
  $('nav3d').classList.add('on');
  $('btnOpen3d').classList.add('on');
  var bd = $('dockBadge');
  if (bd) { bd.textContent = '开'; bd.classList.add('on'); }
  var same = !force && f.dataset.src && f.dataset.src === url;
  if (same) { saveDockPrefs(); return; }
  if (sp) sp.classList.remove('hide');
  f.dataset.src = url;
  f.src = url;
  saveDockPrefs();
  requestAnimationFrame(function () { drawAll(); });
}
function closeDock() {
  var d = $('dock3d'), f = $('dockFrame');
  dockPostMsg({ ucf: 'fly-stop' });
  ST.dockOpen = false;
  ST.dockHover = false;
  if (d) { d.classList.remove('on'); d.setAttribute('aria-hidden', 'true'); }
  var app = document.querySelector('.app');
  if (app) app.classList.remove('docked');
  $('nav3d').classList.remove('on');
  $('btnOpen3d').classList.remove('on');
  var bd = $('dockBadge');
  if (bd) { bd.textContent = '关'; bd.classList.remove('on'); }
  if (f) { f.src = 'about:blank'; f.dataset.src = ''; }
  saveDockPrefs();
  requestAnimationFrame(function () { drawAll(); });
}
function toggleDock() { if (ST.dockOpen) closeDock(); else openDock(); }

/* 3D 侧栏的键盘：iframe 里的 navview 报「鼠标进了/离开了 3D 画面」（fly-hover），
 * 本页据此把 W/A/S/D/Q/E/空格/Shift 的按下与抬起 postMessage 进去（fly-key）。
 * 点过 3D 画面之后焦点就在 iframe 里，那一路由 navview 自己的 keydown 处理，两边不重复。 */
var DOCK_FLY_KEYS = { w: 1, a: 1, s: 1, d: 1, q: 1, e: 1, ' ': 1, shift: 1 };
function dockPostMsg(msg) {
  var f = $('dockFrame');
  if (!ST.dockOpen || !f || !f.contentWindow) return;
  try { f.contentWindow.postMessage(msg, '*'); } catch (e) {}
}
function dockFlyKey(e, down) {
  if (!ST.dockOpen || !ST.dockHover) return false;
  var t = (e.target && e.target.tagName) || '';
  if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT') return false;
  var k = (e.key === ' ' || e.key === 'Spacebar') ? ' ' : String(e.key || '').toLowerCase();
  if (!DOCK_FLY_KEYS[k]) return false;
  dockPostMsg({ ucf: 'fly-key', k: k, down: !!down });
  return true;
}

/* 3D 侧栏的罗盘和工作台「方向」开关是同一个状态：发消息，不重载 iframe */
function syncCompassToDock() {
  var f = $('dockFrame');
  if (!ST.dockOpen || !f || !f.contentWindow) return;
  try { f.contentWindow.postMessage({ ucf: 'compass', on: !!ST.show.compass }, '*'); } catch (e) {}
}

/* 拖左边框调宽度；双击回到默认 */
function bindDockGrip() {
  var grip = $('dockGrip'), dock = $('dock3d');
  if (!grip || !dock) return;
  var drag = null;
  grip.addEventListener('pointerdown', function (e) {
    if (!ST.dockOpen) return;
    drag = { x: e.clientX, w: dock.getBoundingClientRect().width };
    dock.classList.add('resizing');
    try { grip.setPointerCapture(e.pointerId); } catch (x) {}
    e.preventDefault();
  });
  grip.addEventListener('pointermove', function (e) {
    if (!drag) return;
    setDockWidth(drag.w - (e.clientX - drag.x));
    drawAll();
  });
  grip.addEventListener('pointerup', function () {
    if (!drag) return;
    drag = null;
    dock.classList.remove('resizing');
    saveDockPrefs();
    requestAnimationFrame(function () { drawAll(); });
  });
  grip.addEventListener('dblclick', function () { setDockWidth(DOCK_DEF); saveDockPrefs(); drawAll(); });
}

/* ---- 画布平移 / 缩放 / 悬停 ---- */
function bindCanvas(cv, kind) {
  if (!cv) return;
  var drag = null;
  cv.addEventListener('contextmenu', function (e) { e.preventDefault(); });
  cv.addEventListener('mousedown', function (e) {
    if (!ST.doc) return;
    if (e.button !== 0 && e.button !== 1 && e.button !== 2) return;
    var r = cv.getBoundingClientRect();
    drag = { px: e.clientX - r.left, py: e.clientY - r.top, moved: false };
    cv.parentNode.classList.add('dragging');
    e.preventDefault();
  });
  cv.addEventListener('mousemove', function (e) {
    if (!ST.doc) return;
    var r = cv.getBoundingClientRect();
    var px = e.clientX - r.left, py = e.clientY - r.top;
    if (drag) {
      var v = viewOf(cv);
      ST.cam.cx -= (px - drag.px) / v.s;
      ST.cam.cz -= (py - drag.py) / v.s;
      if (Math.abs(px - drag.px) + Math.abs(py - drag.py) > 2) drag.moved = true;
      drag.px = px; drag.py = py;
      drawAll();
      return;
    }
    if (kind === 'main') {
      var tip = $('mapTip');
      var w = s2w(px, py, viewOf(cv));
      if (tip) {
        tip.style.display = 'block';
        tip.style.left = Math.round(px) + 'px';
        tip.style.top = Math.round(py) + 'px';
        tip.textContent = 'x ' + w[0].toFixed(2) + '  z ' + w[1].toFixed(2);
      }
    }
  });
  function end(e) {
    if (!drag) return;
    var wasDrag = drag.moved;
    drag = null;
    cv.parentNode.classList.remove('dragging');
    if (!wasDrag && e && e.button === 0) {
      var r = cv.getBoundingClientRect();
      if (kind === 'route') pickRouteAt(e.clientX - r.left, e.clientY - r.top, cv);
      if (kind === 'zone') pickZoneAt(e.clientX - r.left, e.clientY - r.top, cv);
    }
  }
  cv.addEventListener('mouseup', end);
  cv.addEventListener('mouseleave', function () {
    drag = null;
    cv.parentNode.classList.remove('dragging');
    var tip = $('mapTip');
    if (tip) tip.style.display = 'none';
  });
  cv.addEventListener('wheel', function (e) {
    if (!ST.doc) return;
    e.preventDefault();
    var r = cv.getBoundingClientRect();
    var px = e.clientX - r.left, py = e.clientY - r.top;
    var before = s2w(px, py, viewOf(cv));
    var f = e.deltaY < 0 ? 1.12 : 1 / 1.12;
    ST.cam.zoom = Math.max(0.08, Math.min(40, ST.cam.zoom * f));
    var after = s2w(px, py, viewOf(cv));
    ST.cam.cx += before[0] - after[0];
    ST.cam.cz += before[1] - after[1];
    drawAll();
    var tip = $('mapTip');
    if (tip) tip.style.display = 'none';
  }, { passive: false });
}

function pickRouteAt(px, py, cv) {
  var v = viewOf(cv);
  var items = routeItems();
  var best = null, bd = 10 * 10;
  items.forEach(function (it) {
    if (it.type === 'jump') {
      var j = ST.jumpLinks[it.index];
      var a = w2s(j.a[0], j.a[2], v), b = w2s(j.b[0], j.b[2], v);
      var d = segDist2(px, py, a[0], a[1], b[0], b[1]);
      if (d < bd) { bd = d; best = it; }
    } else if (it.type === 'orphan') {
      ST.jumpOrphans.forEach(function (f) {
        var q = w2s(f.x, f.z, v);
        var d = (q[0] - px) * (q[0] - px) + (q[1] - py) * (q[1] - py);
        if (d < bd) { bd = d; best = it; }
      });
    } else if (it.type === 'route') {
      var r = ST.routes[it.index];
      for (var i = 1; i < r.pts.length; i++) {
        var p1 = w2s(r.pts[i - 1][0], r.pts[i - 1][2], v);
        var p2 = w2s(r.pts[i][0], r.pts[i][2], v);
        var d2 = segDist2(px, py, p1[0], p1[1], p2[0], p2[1]);
        if (d2 < bd) { bd = d2; best = it; }
      }
    }
  });
  if (best) {
    ST.selRoute = { type: best.type, index: best.index };
    renderRoutes();
    drawAll();
  }
}
function segDist2(px, py, x1, y1, x2, y2) {
  var dx = x2 - x1, dy = y2 - y1;
  if (!dx && !dy) return (px - x1) * (px - x1) + (py - y1) * (py - y1);
  var t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy);
  t = Math.max(0, Math.min(1, t));
  var qx = x1 + t * dx, qy = y1 + t * dy;
  return (px - qx) * (px - qx) + (py - qy) * (py - qy);
}
function pickZoneAt(px, py, cv) {
  var v = viewOf(cv);
  var items = zoneItems();
  var best = null, bd = 14 * 14;
  items.forEach(function (it) {
    if (it.type === 'area' || it.type === 'loose') {
      var g = zoneGroups()[it.index];
      var pts = g.pts.length ? g.pts : [{ x: g.x, z: g.z }];
      pts.forEach(function (f) {
        var q = w2s(f.x, f.z, v);
        var d = (q[0] - px) * (q[0] - px) + (q[1] - py) * (q[1] - py);
        if (d < bd) { bd = d; best = it; }
      });
    } else {
      var z = ST.zones[it.index];
      var c = centroid(z.pts);
      var q2 = w2s(c[0], c[2], v);
      var d2 = (q2[0] - px) * (q2[0] - px) + (q2[1] - py) * (q2[1] - py);
      if (d2 < bd) { bd = d2; best = it; }
    }
  });
  if (best) {
    ST.selZone = { type: best.type, index: best.index };
    renderZones();
    drawAll();
  }
}
function centroid(pts) {
  var x = 0, y = 0, z = 0;
  pts.forEach(function (p) { x += p[0]; y += p[1]; z += p[2]; });
  return [x / pts.length, y / pts.length, z / pts.length];
}

/* ---- 启动 ---- */
function boot() {
  setConn(false, '连接 navserver…');
  try {
    var sp = new URLSearchParams(location.search);
    var pg = sp.get('page');
    if (pg && PAGE_TITLE[pg]) ST.startPage = pg;
    ST.startMap = sp.get('map') || '';
    ST.startPack = sp.get('pack') || '';
    ST.autoDock = sp.get('viewer') === '1';
    /* 新参数 ?view=final|pack|native；旧的 ?profile=dev|deploy|test 交给 server 别名兼容 */
    ST.startView = sp.get('view') || sp.get('profile') || '';
    ST.packByFolder = lsJSON(STORAGE_PACKS, {});
    if (!ST.startView) {
      var savedView = lsGet(STORAGE_VIEW, '');
      if (savedView) ST.startView = savedView;
    }
  } catch (e) {}
  initDockPrefs();
  bindTop();
  bindLayerList();
  bindRouteList();
  bindZoneList();
  bindMapTable();
  bindLogs();
  bindCanvas($('cvMain'), 'main');
  bindCanvas($('cvRoute'), 'route');
  bindCanvas($('cvZone'), 'zone');
  window.addEventListener('resize', function () {
    if (ST.dockOpen) setDockWidth(ST.dockW);
    requestAnimationFrame(function () { drawAll(); });
  });
  showPage(ST.startPage);
  var pre = ST.startView
    ? api('/api/profile?set=' + encodeURIComponent(ST.startView)).then(function (j) {
        if (j && j.profile && j.profile.note) ST.bootNote = j.profile.note;
        return j;
      }).catch(function () { return null; })
    : Promise.resolve(null);
  pre.then(function () { return api('/api/workbench'); }).then(function (wb) {
    if (!wb || !wb.ok) throw new Error((wb && wb.error) || '接口失败');
    ST.wb = wb;
    ST.maps = wb.maps || [];
    applyView(wb);
    setConn(true, '本地只读服务 · ' + (wb.profile ? wb.profile.cn : ''));
    ST.wb.log && parseLogs();
    pickDefaultMap();
    if (ST.dockWantOpen) { openDock(); ST.dockWantOpen = false; }
    if (ST.bootNote) {
      var note = ST.bootNote;
      ST.bootNote = '';
      /* 等地图载入的 toast 先说完，再把旧链接的迁移提示补上，别被盖掉 */
      setTimeout(function () { toast(note, 'ok'); }, 1400);
    }
    /* 没带 ?map= 直接进「地图数据 / 日志 / 总览」时也要有内容（原来只 updateHeader，表格会空着） */
    renderAll();
  }).catch(function (e) {
    setConn(false, 'navserver 未连接');
    splash(true, '先开控制台 → 路点工作台（查看）');
    var s = $('mapSplash');
    if (s) {
      s.classList.add('on');
      s.innerHTML = '<div style="font-size:20px">⚠</div><h2>连不上本地服务</h2><p>' +
        '请从 <b>UCF 控制台 → 路点工作台（查看）</b> 打开；它会先启动 navserver（127.0.0.1），再打开本页。</p>' +
        '<p>' + esc(e.message) + '</p>';
    }
    toast('连接失败：' + e.message, 'err');
  });
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();

})();
