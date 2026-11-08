// ============================================================
// test_lifesteal_runtime.js —— 伤害吸血运行时逻辑测试（不连接游戏）
//
// 目的：用最小 Frida 桩 + 可读写内存模型，把 script.js 真实跑起来，
//       验证「OnEntityHurt 上下文 -> HealthData.Hurt 结算 -> Heal」整条链路。
//
// 不验证真实游戏偏移（那由实机测试负责），只验证：
//   - 事件上下文压栈/出栈与匹配
//   - 本地玩家识别、自己/队友过滤
//   - 7 种来源分类与开关
//   - 吸血比例、封顶、死亡保护、累积取整
//   - 同一事件多层上下文不重复吸血
//
// 运行：node "05-正式功能/41-伤害吸血/test_lifesteal_runtime.js"
// ============================================================

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// ---------------- 内存模型 ----------------
const BASE = 0x10000000;
const mem = new Map();

function w8(a, v) { mem.set(a >>> 0, v & 0xff); }
function r8(a) { return mem.has(a >>> 0) ? mem.get(a >>> 0) : 0; }
function w32(a, v) {
  v = v >>> 0;
  for (let i = 0; i < 4; i += 1) w8(a + i, (v >>> (i * 8)) & 0xff);
}
function r32(a) {
  let v = 0;
  for (let i = 0; i < 4; i += 1) v += r8(a + i) * Math.pow(256, i);
  return v >>> 0;
}
function wf32(a, v) {
  const buf = new ArrayBuffer(4);
  new DataView(buf).setFloat32(0, v, true);
  w32(a, new DataView(buf).getUint32(0, true));
}
function rf32(a) {
  const buf = new ArrayBuffer(4);
  new DataView(buf).setUint32(0, r32(a), true);
  return new DataView(buf).getFloat32(0, true);
}

class Ptr {
  constructor(v) { this.v = v >>> 0; }
  isNull() { return this.v === 0; }
  equals(other) { return !!other && this.v === (other.v >>> 0); }
  add(n) { return new Ptr(this.v + (n | 0)); }
  sub(n) { return new Ptr(this.v - (n | 0)); }
  readPointer() { return new Ptr(r32(this.v)); }
  readS32() { return r32(this.v) | 0; }
  readU32() { return r32(this.v); }
  readU8() { return r8(this.v); }
  readFloat() { return rf32(this.v); }
  readUtf16String(len) {
    let out = '';
    for (let i = 0; i < len; i += 1) out += String.fromCharCode(r32(this.v + i * 2) & 0xffff);
    return out;
  }
  toInt32() { return this.v | 0; } // Frida 的 NativePointer.toInt32 是取指针值本身
  toString() { return '0x' + this.v.toString(16); }
}

function wp(a, p) { w32(a, p instanceof Ptr ? p.v : p); }
function rp(a) { return new Ptr(r32(a)); }

// ---------------- 地址表 ----------------
const ADDR = {
  gm: 0x40000000,
  localPlayer: 0x40001000,
  victimPlayer: 0x40002000,
  localHealth: 0x40003000,
  victimHealth: 0x40004000,
  playerWeapons: 0x40005000,
  allList: 0x40006000,
  itemsArray: 0x40007000,
  weapon: 0x40008000,
  weaponData: 0x40009000,
  weaponName: 0x4000A000,
  playersBL: 0x4000B000,
  playersGR: 0x4000C000,
  stack: 0x4000D000,
  gmTypeInfo: 0x4000E000,
  gmStaticFields: 0x4000E400,
  missile: 0x4000F000,
};
const EVENT = ADDR.stack + 8;

// ---------------- 游戏状态（测试可改） ----------------
const state = {
  localHp: 50,
  localMaxHp: 100,
  victimHp: 100,
  localTeam: 1,
  victimTeam: 0,
  wpnIndex: 42,
  wpnClass: 5, // Pistol
  wpnName: 'M9',
  dead: false,
  healCalls: [],
};

function writeObscured(a, value) {
  const key = 0x1234;
  w32(a, key);
  w32(a + 4, (value ^ key) >>> 0);
  w8(a + 8, 1);
}
function readObscured(a) {
  const key = r32(a);
  const hidden = r32(a + 4);
  return (hidden ^ key) | 0;
}

function setupMemory() {
  mem.clear();

  // GameManager：allPlayers 数组 = [local, victim]
  wp(ADDR.gm + 0x1C, ADDR.itemsArray + 0x100);
  w32(ADDR.itemsArray + 0x10C, 2);
  wp(ADDR.itemsArray + 0x110, ADDR.localPlayer);
  wp(ADDR.itemsArray + 0x114, ADDR.victimPlayer);

  // 空的队伍 List，避免读越界
  [ADDR.playersBL, ADDR.playersGR].forEach((list) => {
    wp(list + 0x08, ADDR.itemsArray + 0x200);
    w32(list + 0x0C, 0);
  });

  // 本地玩家 / 敌人
  wp(ADDR.localPlayer + 0x1C, ADDR.localHealth);
  w32(ADDR.localPlayer + 0x20, state.localTeam);
  wp(ADDR.localPlayer + 0xA0, ADDR.playerWeapons);

  wp(ADDR.victimPlayer + 0x1C, ADDR.victimHealth);
  w32(ADDR.victimPlayer + 0x20, state.victimTeam);

  writeObscured(ADDR.localHealth + 0x08, state.localHp);
  writeObscured(ADDR.localHealth + 0x1C, state.localMaxHp);
  writeObscured(ADDR.victimHealth + 0x08, state.victimHp);
  writeObscured(ADDR.victimHealth + 0x1C, 100);

  // PlayerWeapons.all -> [weapon]
  wp(ADDR.playerWeapons + 0x0C, ADDR.allList);
  wp(ADDR.allList + 0x08, ADDR.itemsArray);
  w32(ADDR.allList + 0x0C, 1);
  wp(ADDR.itemsArray + 0x10, ADDR.weapon);

  // Weapon.data -> WeaponData
  wp(ADDR.weapon + 0x68, ADDR.weaponData);
  w32(ADDR.weaponData + 0x0C, state.wpnIndex);
  w32(ADDR.weaponData + 0x10, state.wpnClass);
  wp(ADDR.weaponData + 0x14, ADDR.weaponName);

  // Il2CppString：length @ +8，chars @ +0xC
  const name = state.wpnName;
  w32(ADDR.weaponName + 0x08, name.length);
  for (let i = 0; i < name.length; i += 1) w32(ADDR.weaponName + 0x0C + i * 2, name.charCodeAt(i));

  // 本地玩家来源：GameManager.myPlayer 静态字段
  //   [0x00E2933C] -> Il2CppClass* -> +0x5C static_fields -> +0x00 myPlayer
  wp(BASE + 0x00E2933C, ADDR.gmTypeInfo);
  wp(ADDR.gmTypeInfo + 0x5C, ADDR.gmStaticFields);
  wp(ADDR.gmStaticFields + 0x00, ADDR.localPlayer);
}

function writeDamageEvent(attacker, victim, type, wpnIndex) {
  wp(EVENT + 0x00, attacker);
  wp(EVENT + 0x04, victim);
  w32(EVENT + 0x34, type);
  w32(EVENT + 0x38, 0);
  w32(EVENT + 0x3C, wpnIndex);
}

// ---------------- Frida 桩 ----------------
const hooksByRva = new Map();

global.ptr = (v) => new Ptr(v === undefined ? 0 : v);
global.Process = {
  arch: 'ia32',
  pointerSize: 4,
  findModuleByName(name) {
    if (name !== 'GameAssembly.dll') return null;
    return { base: new Ptr(BASE), name };
  },
};
global.Interceptor = {
  attach(addr, callbacks) {
    const rva = (addr.v - BASE) >>> 0;
    hooksByRva.set(rva, callbacks);
    return { detach() { hooksByRva.delete(rva); } };
  },
};
global.NativeFunction = function (addr) {
  const rva = (addr.v - BASE) >>> 0;
  return function () {
    const args = Array.prototype.slice.call(arguments);
    if (rva === 0x00AE4830) { // HealthData.get_isDead
      return state.dead;
    }
    if (rva === 0x00AE44F0) { // HealthData.Heal
      const healthData = args[0].v;
      const amount = typeof args[1] === 'number' ? args[1] : args[1].v;
      const current = readObscured(healthData + 0x08);
      const maxHp = readObscured(healthData + 0x1C);
      const next = Math.min(current + amount, maxHp);
      writeObscured(healthData + 0x08, next);
      state.healCalls.push({ healthData, amount, before: current, after: next });
      return undefined;
    }
    return new Ptr(0);
  };
};
global.rpc = { exports: {} };
const logs = [];
global.send = function (payload) { logs.push(payload); };

const realLog = console.log;
console.log = function () {}; // 屏蔽 script.js 日志
const realWarn = console.warn;
const realError = console.error;
console.error = function () {};

// ---------------- 加载 script.js ----------------
setupMemory();
const scriptPath = path.join(__dirname, 'script.js');
vm.runInThisContext(fs.readFileSync(scriptPath, 'utf8'), { filename: 'script.js' });
const api = global.rpc.exports;

const FULL_CONFIG = {
  lifesteal_percent: 10,
  src_gun_primary_enabled: true,
  src_gun_secondary_enabled: true,
  src_gun_stock_enabled: true,
  src_knife_enabled: true,
  src_grenade_enabled: true,
  src_special_enabled: true,
  src_infect_enabled: false,
  only_enemy_victim: true,
  diagnostic_log: false,
};
function enableWith(overrides) {
  return global.rpc.exports.enable(Object.assign({}, FULL_CONFIG, overrides || {}));
}

// ---------------- 触发工具 ----------------
function onHurtEnter(which) {
  const callbacks = hooksByRva.get(which);
  if (!callbacks || !callbacks.onEnter) throw new Error('hook not installed: ' + which);
  const invocation = { context: { esp: new Ptr(ADDR.stack) } };
  callbacks.onEnter.call(invocation);
  return invocation;
}
function onHurtLeave(which, invocation) {
  const callbacks = hooksByRva.get(which);
  if (callbacks && callbacks.onLeave) callbacks.onLeave.call(invocation);
}
function fireHurt(healthData, damage) {
  const callbacks = hooksByRva.get(0x00AE45B0);
  if (!callbacks) throw new Error('HealthData.Hurt hook not installed');
  callbacks.onEnter.call({}, [new Ptr(healthData), new Ptr(damage)]);
}
function damage(attacker, victim, type, wpnIndex, amount, healthData) {
  writeDamageEvent(attacker, victim, type, wpnIndex);
  const invocation = onHurtEnter(0x00B3F470);
  fireHurt(healthData || (victim === ADDR.localPlayer ? ADDR.localHealth : ADDR.victimHealth), amount);
  onHurtLeave(0x00B3F470, invocation);
}

// ---------------- 断言 ----------------
let passed = 0;
let failed = 0;
function check(name, condition, detail) {
  if (condition) {
    passed += 1;
    realLog('  ok  ' + name);
  } else {
    failed += 1;
    realLog('  FAIL ' + name + (detail === undefined ? '' : ' -> ' + JSON.stringify(detail)));
  }
}

function resetGame(overrides) {
  state.localHp = 50;
  state.localMaxHp = 100;
  state.victimHp = 100;
  state.localTeam = 1;
  state.victimTeam = 0;
  state.wpnIndex = 42;
  state.wpnClass = 5;
  state.wpnName = 'M9';
  state.dead = false;
  state.healCalls = [];
  Object.assign(state, overrides || {});
  setupMemory();
  api.reset('test_reset');
}

// ---------------- 测试 ----------------
realLog('== lifesteal runtime test ==');

// 1. 开启 + 副武器 10% 吸血
resetGame();
enableWith({
  lifesteal_percent: 10,
  src_gun_primary_enabled: true,
  src_gun_secondary_enabled: true,
  src_gun_stock_enabled: true,
  src_knife_enabled: true,
  src_grenade_enabled: true,
  src_special_enabled: true,
  only_enemy_victim: true,
});
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
let status = api.status();
if (state.healCalls.length !== 1) {
  realLog('DEBUG status: ' + JSON.stringify(status, null, 1));
  realLog('DEBUG logs: ' + JSON.stringify(logs.slice(-15), null, 1));
}
check('副武器 100 伤害 10% 回 10 血', state.healCalls.length === 1 && state.healCalls[0].amount === 10, state.healCalls);
check('回血后本地血量 50 -> 60', readObscured(ADDR.localHealth + 0x08) === 60, readObscured(ADDR.localHealth + 0x08));
check('分类为 gun_secondary', status.last_category === 'gun_secondary', status.last_category);
check('累计回血 10', status.healed_total === 10, status.healed_total);

// 2. 同一事件 Player + Entity 双层上下文只结算一次
resetGame();
enableWith({ lifesteal_percent: 10 });
writeDamageEvent(ADDR.localPlayer, ADDR.victimPlayer, 1, 42);
const playerInv = onHurtEnter(0x00B516B0);
const entityInv = onHurtEnter(0x00B3F470);
fireHurt(ADDR.victimHealth, 100);
fireHurt(ADDR.victimHealth, 100); // 同一上下文第二次 Hurt（模拟重复调用）
onHurtLeave(0x00B3F470, entityInv);
onHurtLeave(0x00B516B0, playerInv);
status = api.status();
check('双层上下文只回一次血', state.healCalls.length === 1, state.healCalls);
check('重复 Hurt 被 consumed 拦截', status.skipped_duplicate === 1, status.skipped_duplicate);

// 3. 自己打自己不吸血
resetGame();
enableWith({ lifesteal_percent: 10 });
damage(ADDR.localPlayer, ADDR.localPlayer, 1, 42, 100, ADDR.localHealth);
status = api.status();
check('自伤不回血', state.healCalls.length === 0, state.healCalls);
check('自伤计入 skipped_self_victim', status.skipped_self_victim === 1, status.skipped_self_victim);

// 4. 打队友默认不吸血
resetGame({ victimTeam: 1 });
enableWith({ lifesteal_percent: 10 });
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
status = api.status();
check('队友不回血（默认）', state.healCalls.length === 0, state.healCalls);
check('计入 skipped_mate_victim', status.skipped_mate_victim === 1, status.skipped_mate_victim);

// 5. 关掉副武器分类 -> 不吸血
resetGame();
enableWith({ lifesteal_percent: 10, src_gun_secondary_enabled: false });
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
status = api.status();
check('关闭副武器分类后不吸血', state.healCalls.length === 0, state.healCalls);
check('计入分类关闭跳过', status.skipped_category_disabled >= 1, status.skipped_category_disabled);

// 6. 枪托重击 / 近战 / 投掷 / 特殊 分类
function classifyCase(wpnClass, type, expected) {
  resetGame({ wpnClass: wpnClass });
  enableWith({ lifesteal_percent: 10 });
  damage(ADDR.localPlayer, ADDR.victimPlayer, type, 42, 100);
  const st = api.status();
  return { category: st.last_category, healed: state.healCalls.length, expected: expected };
}
let c = classifyCase(0, 2, 'gun_stock');
check('枪械类 + type=Knife -> 枪托重击', c.category === 'gun_stock' && c.healed === 1, c);
c = classifyCase(6, 2, 'knife');
check('Knife 类 + type=Knife -> 近战武器', c.category === 'knife' && c.healed === 1, c);
c = classifyCase(7, 3, 'grenade');
check('type=Grenade -> 投掷/爆炸', c.category === 'grenade' && c.healed === 1, c);
c = classifyCase(9, 5, 'special');
check('type=Other -> 特殊/技能', c.category === 'special' && c.healed === 1, c);
c = classifyCase(5, 1, 'gun_secondary');
check('Pistol + type=Gun -> 副武器', c.category === 'gun_secondary' && c.healed === 1, c);

// 6.5 attacker 是 missile 实体时，结算时读 [missile+0x30] owner 还原（零 Hook 兜底）
resetGame();
enableWith({ lifesteal_percent: 10 });
wp(ADDR.missile + 0x30, ADDR.localPlayer);
damage(ADDR.missile, ADDR.victimPlayer, 3, 42, 100);
status = api.status();
check('missile owner 还原后正常吸血', state.healCalls.length === 1 && state.healCalls[0].amount === 10, state.healCalls);
check('计入 attacker_missile_resolved', status.attacker_missile_resolved === 1, status.attacker_missile_resolved);
check('分类仍为投掷/爆炸', status.last_category === 'grenade', status.last_category);

// 7. 累积取整：10% 打两下 5 点 -> 第一次不回，第二次回 1
resetGame();
enableWith({ lifesteal_percent: 10 });
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 5);
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 5);
status = api.status();
check('小额伤害累积后回 1 点', state.healCalls.length === 1 && state.healCalls[0].amount === 1, state.healCalls);

// 8. 满血时不涨血（Heal 封顶）
resetGame({ localHp: 100 });
enableWith({ lifesteal_percent: 10 });
const totalBefore = api.status().healed_total;
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
status = api.status();
check('满血时实际回血为 0', status.healed_total === totalBefore && state.healCalls.length === 1,
  { before: totalBefore, after: status.healed_total });

// 9. 死亡状态不回血
resetGame({ dead: true });
enableWith({ lifesteal_percent: 10 });
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
status = api.status();
check('死亡状态不回血', state.healCalls.length === 0 && status.skipped_dead >= 1, status.skipped_dead);

// 10. 只有敌人开关关闭后，打队友也能吸
resetGame({ victimTeam: 1 });
enableWith({ lifesteal_percent: 10, only_enemy_victim: false });
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
check('关闭只吸敌人后队友也能吸', state.healCalls.length === 1, state.healCalls);

// 11. percent=0 不回血
resetGame();
enableWith({ lifesteal_percent: 0 });
damage(ADDR.localPlayer, ADDR.victimPlayer, 1, 42, 100);
status = api.status();
check('比例 0% 不回血', state.healCalls.length === 0, state.healCalls);

// 12. 清理后 Hook 全部 detach
api.cleanup();
check('cleanup 后 Hook 全部卸载', hooksByRva.size === 0, hooksByRva.size);

realLog('== result: ' + passed + ' passed, ' + failed + ' failed ==');
if (failed > 0) process.exit(1);
