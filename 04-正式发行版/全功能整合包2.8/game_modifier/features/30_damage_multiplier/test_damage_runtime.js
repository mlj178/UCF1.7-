'use strict';
// ==========================================================================
// 30_damage_multiplier / 两段式伤害倍数 离线运行时测试
// --------------------------------------------------------------------------
// 用一块真实可读写的内存 + 最小 Frida stub 把 script.js 跑起来，直接调
// multiplyDamageEvent()，验证的是**运行时事实**：
//   1) 入口段（GameManager.TakeDamage）乘的是原始伤害，和受害者剩余血量无关：
//      100 伤害 × 0.1x = 10，哪怕受害者只剩 5 滴血。
//   2) 入口段不碰刀（type=2），刀留给 OnEntityHurt 收尾段。
//   3) 收尾段不再乘非刀伤害（避免入口段 + 收尾段乘两次）。
//   4) 刀的致死一击（damage >= 剩余血量）不削弱，避免血量几何级衰减。
//   5) 刀的普通一击仍按倍率；倍率 >=1 时不触发「致死一击跳过」。
//   6) 入口钩子安装失败时退回收尾段处理全部伤害。
//   7) 血量读不到时不抛异常、正常乘算，只累加 victimHpReadFailures。
//   8) 保底 1 点仍然有效（3 × 0.1 不是 0）。
// 用法：node 04-正式发行版/全功能整合包2.8/game_modifier/features/30_damage_multiplier/test_damage_runtime.js
// 退出码 0 = 全部断言通过。
// ==========================================================================
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const scriptPath = path.join(__dirname, 'script.js');
let source = fs.readFileSync(scriptPath, 'utf8').replace(/^\uFEFF/, '');
const exportPattern = '    rpc.exports = {';
assert(source.includes(exportPattern), 'rpc.exports block not found');
source = source.replace(exportPattern,
    '    rpc.exports = {\n' +
    '        __damageTest: {\n' +
    '            getRuntime: function () { return Runtime; },\n' +
    '            multiplyDamageEvent: multiplyDamageEvent,\n' +
    '            readVictimCurrentHealth: readVictimCurrentHealth,\n' +
    '            eventDataFromTakeDamageStack: eventDataFromTakeDamageStack,\n' +
    '            eventDataFromOnEntityHurtStack: eventDataFromOnEntityHurtStack,\n' +
    '            resetRuntimeStats: resetRuntimeStats\n' +
    '        },\n');

// ---- 一块真的能读写的内存 -------------------------------------------------
const MEM_BASE = 0x10000;
const MEM_SIZE = 0x20000;
const buffer = new ArrayBuffer(MEM_SIZE);
const view = new DataView(buffer);
const ranges = [];
function mapRange(addr, size) { ranges.push([addr >>> 0, (addr + size) >>> 0]); }
function ensure(addr, size) {
    const a = addr >>> 0;
    for (let i = 0; i < ranges.length; i++) {
        if (a >= ranges[i][0] && a + size <= ranges[i][1]) return;
    }
    throw new RangeError('access violation @0x' + a.toString(16));
}
const NULL_PTR = {
    __addr: 0,
    add() { return NULL_PTR; },
    sub() { return NULL_PTR; },
    isNull() { return true; },
    equals(o) { return !!o && o.__addr === 0; },
    compare(o) { return -(o && o.__addr || 0); },
    toString(radix) { return (0).toString(radix || 16); },
    readPointer() { throw new RangeError('null'); },
    readU8() { throw new RangeError('null'); },
    readU32() { throw new RangeError('null'); },
    readS32() { throw new RangeError('null'); },
    readFloat() { throw new RangeError('null'); },
    writeU8() { throw new RangeError('null'); },
    writeU32() { throw new RangeError('null'); },
    writeS32() { throw new RangeError('null'); },
    writeFloat() { throw new RangeError('null'); }
};
function P(addr) {
    const a = addr >>> 0;
    if (a === 0) return NULL_PTR;
    const self = {
        __addr: a,
        add(n) { return P((a + n) >>> 0); },
        sub(n) { return P((a - n) >>> 0); },
        isNull() { return a === 0; },
        equals(o) { return !!o && o.__addr === a; },
        compare(o) { return a - (o && o.__addr); },
        toString(radix) { return a.toString(radix || 16); },
        readPointer() { ensure(a, 4); return P(view.getUint32(a - MEM_BASE, true)); },
        readU32() { ensure(a, 4); return view.getUint32(a - MEM_BASE, true); },
        readS32() { ensure(a, 4); return view.getInt32(a - MEM_BASE, true); },
        readU8() { ensure(a, 1); return view.getUint8(a - MEM_BASE); },
        readFloat() { ensure(a, 4); return view.getFloat32(a - MEM_BASE, true); },
        writePointer(p) { ensure(a, 4); view.setUint32(a - MEM_BASE, p.__addr >>> 0, true); return self; },
        writeU32(v) { ensure(a, 4); view.setUint32(a - MEM_BASE, v >>> 0, true); return self; },
        writeS32(v) { ensure(a, 4); view.setInt32(a - MEM_BASE, v | 0, true); return self; },
        writeU8(v) { ensure(a, 1); view.setUint8(a - MEM_BASE, v & 0xff); return self; },
        writeFloat(v) { ensure(a, 4); view.setFloat32(a - MEM_BASE, v, true); return self; }
    };
    return self;
}

// 本地玩家地址：native.isMyPlayer 只认它。
const LOCAL_PLAYER = 0x12000;

const context = {
    console: console,
    Date: Date,
    Process: {
        arch: 'ia32',
        pointerSize: 4,
        findModuleByName: function () { return { base: P(0x1000), name: 'GameAssembly.dll' }; },
        findRangeByAddress: function () { return null; }
    },
    Memory: { alloc: function () { return P(MEM_BASE); } },
    NativeFunction: function NativeFunction() {
        return function (entityPtr) {
            return (entityPtr && entityPtr.__addr === LOCAL_PLAYER) ? 1 : 0;
        };
    },
    Interceptor: {
        attach: function () { return { detach: function () {} }; },
        replace: function () { throw new Error('Interceptor.replace must not be used'); },
        revert: function () { throw new Error('Interceptor.revert must not be used'); }
    },
    ptr: function (v) { return P(v === undefined || v === null ? 0 : v); },
    rpc: { exports: {} },
    send: function () {},
    setInterval: function () { return 1; },
    clearInterval: function () {},
    setTimeout: function () { return 0; }
};
vm.createContext(context);
vm.runInContext(source, context, { filename: scriptPath });

const test = context.rpc.exports.__damageTest;
assert(test && typeof test.multiplyDamageEvent === 'function', 'damage test exports missing');
const Runtime = test.getRuntime();

// ---- 场景准备 -------------------------------------------------------------
const EVENT = 0x11000;     // DamageEventData（按值）
const VICTIM = 0x13000;    // 受害者 Entity
const HEALTH = 0x14000;    // HealthData
const STACK = 0x15000;     // 伪造栈

const OFF_EVENT_ATTACKER = 0x00;
const OFF_EVENT_VICTIM = 0x04;
const OFF_EVENT_DAMAGE = 0x08;
const OFF_EVENT_TYPE = 0x34;
const OFF_ENTITY_HEALTH_DATA = 0x1C;
const OFF_HEALTH_KEY = 0x08;
const OFF_HEALTH_HIDDEN = 0x0C;
const HP_KEY = 0x1234;

mapRange(LOCAL_PLAYER, 0x100);
mapRange(EVENT, 0x100);
mapRange(VICTIM, 0x100);
mapRange(HEALTH, 0x100);
mapRange(STACK, 0x100);
view.setUint32(VICTIM + OFF_ENTITY_HEALTH_DATA - MEM_BASE, HEALTH, true);

function setHp(hp) {
    view.setInt32(HEALTH + OFF_HEALTH_KEY - MEM_BASE, HP_KEY, true);
    view.setInt32(HEALTH + OFF_HEALTH_HIDDEN - MEM_BASE, (hp ^ HP_KEY) | 0, true);
}
function setEvent(type, damage, attacker, victim) {
    view.setUint32(EVENT + OFF_EVENT_ATTACKER - MEM_BASE, (attacker === undefined ? LOCAL_PLAYER : attacker) >>> 0, true);
    view.setUint32(EVENT + OFF_EVENT_VICTIM - MEM_BASE, (victim === undefined ? VICTIM : victim) >>> 0, true);
    view.setFloat32(EVENT + OFF_EVENT_DAMAGE - MEM_BASE, damage, true);
    view.setInt32(EVENT + OFF_EVENT_TYPE - MEM_BASE, type, true);
    view.setInt32(EVENT + 0x38 - MEM_BASE, 0, true);
    view.setInt32(EVENT + 0x3C - MEM_BASE, 0, true);
    view.setInt32(EVENT + 0x40 - MEM_BASE, 0, true);
    view.setUint8(EVENT + 0x44 - MEM_BASE, 0);
}
const readDamage = () => view.getFloat32(EVENT + OFF_EVENT_DAMAGE - MEM_BASE, true);
const near = (a, b) => Math.abs(a - b) < 1e-4;

Runtime.enabled = true;
Runtime.preCapHookInstalled = true;
Runtime.config.diagnostic_log = false;
Runtime.config.self_multiplier = 0.1;
Runtime.config.self_enabled = true;
Runtime.config.skip_local_victim = true;

function reset() {
    test.resetRuntimeStats();
    Runtime.enabled = true;
    Runtime.preCapHookInstalled = true;
    Runtime.config.self_multiplier = 0.1;
    view.setUint32(VICTIM + OFF_ENTITY_HEALTH_DATA - MEM_BASE, HEALTH, true);
}

// ---- 1) 入口段：伤害和剩余血量无关 ---------------------------------------
reset();
setHp(5);
setEvent(1, 100);              // Gun, 原始 100，受害者只剩 5
let ret = test.multiplyDamageEvent(P(EVENT), 'test', 'pre_cap');
assert.strictEqual(ret, true, 'pre-cap damage must be written');
assert.strictEqual(near(readDamage(), 10), true, 'pre-cap 100 × 0.1 = 10, independent of 5 HP');
assert.strictEqual(Runtime.stats.preCapMultiplied, 1);
assert.strictEqual(Runtime.stats.skippedLethalCapped, 0);

// ---- 2) 入口段不碰刀 ------------------------------------------------------
reset();
setHp(5);
setEvent(2, 100);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'pre_cap');
assert.strictEqual(ret, false, 'knife must be skipped at pre-cap');
assert.strictEqual(near(readDamage(), 100), true, 'knife damage must stay raw at pre-cap');
assert.strictEqual(Runtime.stats.skippedKnifeAtPreCap, 1);

// ---- 3) 收尾段不碰非刀（避免乘两次） --------------------------------------
reset();
setHp(100);
setEvent(1, 10);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, false, 'non-knife must be skipped at post-cap when pre-cap hook is installed');
assert.strictEqual(near(readDamage(), 10), true, 'non-knife damage must not be multiplied twice');
assert.strictEqual(Runtime.stats.skippedNonKnifeAtPostCap, 1);

// ---- 4) 刀：普通一击仍按倍率 ----------------------------------------------
reset();
setHp(100);
setEvent(2, 20);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, true, 'non-lethal knife must be written');
assert.strictEqual(near(readDamage(), 2), true, 'knife 20 × 0.1 = 2');
assert.strictEqual(Runtime.stats.postCapMultiplied, 1);

// ---- 5) 刀：致死一击不削弱 ------------------------------------------------
reset();
setHp(5);
setEvent(2, 5);                // TakeDamage 已经把 100 伤害钳成剩余 5
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, false, 'lethal knife must not be weakened');
assert.strictEqual(near(readDamage(), 5), true, 'lethal knife keeps vanilla damage');
assert.strictEqual(Runtime.stats.skippedLethalCapped, 1);

// ---- 6) 刀：倍率 >=1 不触发致死跳过 ----------------------------------------
reset();
Runtime.config.self_multiplier = 2.0;
setHp(5);
setEvent(2, 5);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, true, 'boosted knife must be written');
assert.strictEqual(near(readDamage(), 10), true, 'knife 5 × 2 = 10');
assert.strictEqual(Runtime.stats.skippedLethalCapped, 0);

// ---- 7) 入口钩子安装失败：收尾段兜底处理非刀，并保留致死跳过 ----------------
reset();
Runtime.preCapHookInstalled = false;
setHp(100);
setEvent(1, 20);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, true, 'fallback post-cap non-knife must be written');
assert.strictEqual(near(readDamage(), 2), true, 'fallback 20 × 0.1 = 2');
setEvent(1, 5);
setHp(5);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, false, 'fallback must skip lethal capped damage');
assert.strictEqual(near(readDamage(), 5), true);

// ---- 8) 血量读不到：不抛异常、正常乘算、只记账 ----------------------------
reset();
view.setUint32(VICTIM + OFF_ENTITY_HEALTH_DATA - MEM_BASE, 0, true);
setEvent(2, 20);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'post_cap');
assert.strictEqual(ret, true, 'unreadable HP must fall back to normal scaling');
assert.strictEqual(near(readDamage(), 2), true);
assert.strictEqual(Runtime.stats.victimHpReadFailures, 1);
view.setUint32(VICTIM + OFF_ENTITY_HEALTH_DATA - MEM_BASE, HEALTH, true);

// ---- 9) 保底 1 点仍然有效 -------------------------------------------------
reset();
setHp(100);
setEvent(1, 3);
ret = test.multiplyDamageEvent(P(EVENT), 'test', 'pre_cap');
assert.strictEqual(ret, true);
assert.strictEqual(near(readDamage(), 1), true, '3 × 0.1 must floor to 1');
assert.strictEqual(Runtime.stats.flooredToMin, 1);

// ---- 10) 栈参数定位：TakeDamage 静态方法没有 this，data 在 esp+4 ----------
reset();
view.setUint32(STACK + 4 - MEM_BASE, LOCAL_PLAYER, true);
const td = test.eventDataFromTakeDamageStack({ esp: P(STACK) });
assert.strictEqual(td.__addr, STACK + 4, 'TakeDamage data must start at esp+4');
const oh = test.eventDataFromOnEntityHurtStack({ esp: P(STACK) });
assert.strictEqual(oh.__addr, STACK + 8, 'OnEntityHurt data must start at esp+8');

console.log('damage multiplier runtime tests passed');
