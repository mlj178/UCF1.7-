'use strict';
// ==========================================================================
// 40_direct_damage / 突破复活无敌（pierce_respawn_invincible）离线运行时测试
// --------------------------------------------------------------------------
// 用一块真实可读写的内存 + 最小 Frida stub 把 script.js 跑起来，直接调
// readDefenseState() / clearDefenseBeforeShot()，验的是**运行时事实**：
//   1) 目标处于复活无敌时：只写 Entity.damageRate / Entity.isInvincible /
//      HealthData.invinsibleEndTime 三个字段，字节级 diff 不允许有第四处
//   2) 目标是"干净的"（没有无敌/减伤）：一个字节都不写
//   3) 部分减伤/护盾（0 < damageRate < 1）：一个字节都不写；只有完全免疫（≈0）才复位
//   4) 指针不可读 / healthData 为空 / victim 为空：不抛异常、一个字节都不写，
//      只累加 invincibleUnreadable（这条保证"读不到就绝不动手"）
//   5) readDefenseState() 是纯只读的
// 用法：node 05-正式功能/40-开火直伤/test_defense_runtime.js
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
    '        __defenseTest: {\n' +
    '            getRuntime: function () { return Runtime; },\n' +
    '            readDefenseState: readDefenseState,\n' +
    '            clearDefenseBeforeShot: clearDefenseBeforeShot,\n' +
    '            explosionTouchesTarget: explosionTouchesTarget,\n' +
    '            readTakeDamageArgs: readTakeDamageArgs,\n' +
    '            readExplosionArgs: readExplosionArgs\n' +
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

const context = {
    console: console,
    Date: Date,
    Process: {
        arch: 'ia32',
        pointerSize: 4,
        findModuleByName: function () { return null; },
        findRangeByAddress: function () { return null; }
    },
    Memory: { alloc: function (n) { return P(MEM_BASE); } },
    NativeFunction: function NativeFunction() { throw new Error('NativeFunction must not be created'); },
    Interceptor: {
        attach: function () { throw new Error('Interceptor must not be used'); },
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

const test = context.rpc.exports.__defenseTest;
assert(test && typeof test.clearDefenseBeforeShot === 'function', 'defense test exports missing');
const Runtime = test.getRuntime();

// ---- 场景准备 -------------------------------------------------------------
const VICTIM = 0x11000;
const HEALTH = 0x12000;
const HEALTH_HP = 0x8;             // HealthData.currentHealth（本测试只放哨兵值）
const OFF_DAMAGE_RATE = 0x14;      // Entity.<damageRate>k__BackingField
const OFF_IS_INVINCIBLE = 0x18;    // Entity.<isInvincible>k__BackingField
const OFF_HEALTH_DATA = 0x1c;      // Entity.<healthData>k__BackingField
const OFF_INV_END = 0x44;          // HealthData.invinsibleEndTime
mapRange(VICTIM, 0x100);
mapRange(HEALTH, 0x100);
view.setUint32(VICTIM + OFF_HEALTH_DATA - MEM_BASE, HEALTH, true);
view.setInt32(HEALTH + HEALTH_HP - MEM_BASE, 77, true);      // 血量哨兵：任何写入都会被发现

function snapshot() { return new Uint8Array(buffer.slice(0)); }
function diff(before, after) {
    const out = [];
    for (let i = 0; i < after.length; i++) if (before[i] !== after[i]) out.push(MEM_BASE + i);
    return out;
}
function allowedAddrs() {
    return new Set([HEALTH + OFF_INV_END, HEALTH + OFF_INV_END + 1, HEALTH + OFF_INV_END + 2, HEALTH + OFF_INV_END + 3,
        VICTIM + OFF_DAMAGE_RATE, VICTIM + OFF_DAMAGE_RATE + 1, VICTIM + OFF_DAMAGE_RATE + 2, VICTIM + OFF_DAMAGE_RATE + 3,
        VICTIM + OFF_IS_INVINCIBLE]);
}
const r32 = (a) => view.getFloat32(a - MEM_BASE, true);
const w32 = (a, v) => view.setFloat32(a - MEM_BASE, v, true);
const r8 = (a) => view.getUint8(a - MEM_BASE);
const w8 = (a, v) => view.setUint8(a - MEM_BASE, v);

// ---- 1) 复活无敌全开：只写三个防御字段 ------------------------------------
w32(VICTIM + OFF_DAMAGE_RATE, 0.0);
w8(VICTIM + OFF_IS_INVINCIBLE, 1);
w32(HEALTH + OFF_INV_END, 12.5);

let before = snapshot();
let result = test.clearDefenseBeforeShot(P(VICTIM));
let changed = diff(before, snapshot());
assert.strictEqual(result.ok, true, 'defense state must be readable: ' + JSON.stringify(result));
assert.strictEqual(result.active, true, 'active defense must be detected');
assert.strictEqual(r32(HEALTH + OFF_INV_END), 0, 'invinsibleEndTime must be reset to 0');
assert.strictEqual(r32(VICTIM + OFF_DAMAGE_RATE), 1, 'damageRate must be reset to 1.0');
assert.strictEqual(r8(VICTIM + OFF_IS_INVINCIBLE), 0, 'isInvincible must be reset to 0');
assert.ok(changed.length > 0, 'an active defense must be written');
assert.deepStrictEqual(changed.filter((addr) => !allowedAddrs().has(addr)), [], 'only the three defense fields may be written');
assert.strictEqual(view.getInt32(HEALTH + HEALTH_HP - MEM_BASE, true), 77, 'HP must never be touched');
assert.strictEqual(Runtime.stats.invincibleCleared, 1);

// ---- 2) 目标干净：一个字节都不写 ------------------------------------------
w32(VICTIM + OFF_DAMAGE_RATE, 1.0);
w8(VICTIM + OFF_IS_INVINCIBLE, 0);
w32(HEALTH + OFF_INV_END, 0);
before = snapshot();
result = test.clearDefenseBeforeShot(P(VICTIM));
changed = diff(before, snapshot());
assert.strictEqual(result.active, false, 'clean target is not active');
assert.deepStrictEqual(changed, [], 'clean target must not be written');
assert.strictEqual(Runtime.stats.invincibleCleared, 1);

// ---- 3a) 部分减伤（终结者护盾 0.03 / 补给箱 0.88）：一个字节都不写 --------
w32(VICTIM + OFF_DAMAGE_RATE, 0.88);
w8(VICTIM + OFF_IS_INVINCIBLE, 0);
w32(HEALTH + OFF_INV_END, 0);
before = snapshot();
result = test.clearDefenseBeforeShot(P(VICTIM));
changed = diff(before, snapshot());
assert.strictEqual(result.active, false, 'partial reduction is not respawn invincibility');
assert.ok(Math.abs(r32(VICTIM + OFF_DAMAGE_RATE) - 0.88) < 1e-5, 'shield must be preserved');
assert.deepStrictEqual(changed, [], 'partial damage reduction must never be wiped');
assert.strictEqual(Runtime.stats.invincibleCleared, 1);

// ---- 3b) 完全免疫（复活保护 damageRate=0）：只复位 damageRate --------------
w32(VICTIM + OFF_DAMAGE_RATE, 0.0);
w8(VICTIM + OFF_IS_INVINCIBLE, 0);
w32(HEALTH + OFF_INV_END, 0);
before = snapshot();
result = test.clearDefenseBeforeShot(P(VICTIM));
changed = diff(before, snapshot());
assert.strictEqual(result.active, true);
assert.strictEqual(r32(VICTIM + OFF_DAMAGE_RATE), 1);
assert.ok(changed.length > 0, 'full immunity must be written');
assert.deepStrictEqual(
    changed.filter((addr) => addr < VICTIM + OFF_DAMAGE_RATE || addr > VICTIM + OFF_DAMAGE_RATE + 3),
    [],
    'only damageRate may be written when only full immunity is active'
);
assert.strictEqual(Runtime.stats.invincibleCleared, 2);

// ---- 4) victim 指针不可读：不抛异常、不写、只记账 --------------------------
before = snapshot();
const unreadableBefore = Runtime.stats.invincibleUnreadable;
assert.doesNotThrow(() => test.clearDefenseBeforeShot(P(0x900000)));
assert.deepStrictEqual(diff(before, snapshot()), [], 'unreadable victim must not be written');
assert.strictEqual(Runtime.stats.invincibleUnreadable, unreadableBefore + 1);

// ---- 5) healthData 为空：同样绝不动手 -------------------------------------
view.setUint32(VICTIM + OFF_HEALTH_DATA - MEM_BASE, 0, true);
before = snapshot();
assert.doesNotThrow(() => test.clearDefenseBeforeShot(P(VICTIM)));
assert.deepStrictEqual(diff(before, snapshot()), [], 'victim without HealthData must not be written');
assert.strictEqual(Runtime.stats.invincibleUnreadable, unreadableBefore + 2);
view.setUint32(VICTIM + OFF_HEALTH_DATA - MEM_BASE, HEALTH, true);

// ---- 6) 数值不合理（指针被回收/复用）：不写、只记账 ----------------------
w32(VICTIM + OFF_DAMAGE_RATE, 99.0);
w8(VICTIM + OFF_IS_INVINCIBLE, 1);
w32(HEALTH + OFF_INV_END, 12.5);
before = snapshot();
const rejectedBefore = Runtime.stats.invincibleUnreadable;
assert.doesNotThrow(() => test.clearDefenseBeforeShot(P(VICTIM)));
assert.deepStrictEqual(diff(before, snapshot()), [], 'implausible state must not be written');
assert.strictEqual(Runtime.stats.invincibleUnreadable, rejectedBefore + 1);
w32(VICTIM + OFF_DAMAGE_RATE, 1.0);
w8(VICTIM + OFF_IS_INVINCIBLE, 0);
w32(HEALTH + OFF_INV_END, 0);

// ---- 7) 空指针：不抛异常、不写 --------------------------------------------
before = snapshot();
assert.doesNotThrow(() => test.clearDefenseBeforeShot(P(0)));
assert.deepStrictEqual(diff(before, snapshot()), [], 'null victim must not be written');

// ---- 8) readDefenseState 必须只读 -----------------------------------------
w32(VICTIM + OFF_DAMAGE_RATE, 0.0);
w8(VICTIM + OFF_IS_INVINCIBLE, 1);
w32(HEALTH + OFF_INV_END, 9.0);
before = snapshot();
const info = test.readDefenseState(P(VICTIM));
assert.strictEqual(info.ok, true);
assert.strictEqual(info.invEnd, 9);
assert.strictEqual(info.damageRate, 0);
assert.strictEqual(info.isInvincible, 1);
assert.deepStrictEqual(diff(before, snapshot()), [], 'readDefenseState must be read-only');

// ---- 9) 爆炸半径判定（explosionTouchesTarget）------------------------------
const origin = { x: 0, y: 0, z: 0 };
assert.strictEqual(test.explosionTouchesTarget(origin, { x: 2.0, y: 0, z: 0 }, 3.0), true, 'inside range');
assert.strictEqual(test.explosionTouchesTarget(origin, { x: 3.4, y: 0, z: 0 }, 3.0), true, 'range + 0.5 margin');
assert.strictEqual(test.explosionTouchesTarget(origin, { x: 3.6, y: 0, z: 0 }, 3.0), false, 'outside range + margin');
assert.strictEqual(test.explosionTouchesTarget(origin, { x: 0, y: 5.0, z: 0 }, 3.0), false, 'vertical distance counts');
assert.strictEqual(test.explosionTouchesTarget(origin, { x: 0, y: 0, z: 2.9 }, 3.0), true, 'z axis inside');
assert.strictEqual(test.explosionTouchesTarget(origin, { x: NaN, y: 0, z: 0 }, 3.0), false, 'NaN never matches');

// ---- 10) 入口 ABI：esp 指向返回地址，参数从 +4 开始 ------------------------
// 2026-10-20 的线上 bug：TakeDamage 的 attacker 读成了 esp+0（返回地址），
// 于是永远认不出我们的伤害，RPG 打不死人。这里把偏移钉死。
const STACK = 0x13000;
mapRange(STACK, 0x100);
view.setUint32(STACK + 4 - MEM_BASE, VICTIM, true);        // attacker
view.setUint32(STACK + 8 - MEM_BASE, 0x11100, true);       // victim
view.setInt32(STACK + 0x38 - MEM_BASE, 3, true);           // type = Grenade
const tdArgs = test.readTakeDamageArgs(P(STACK));
assert.strictEqual(tdArgs.attacker.__addr, VICTIM, 'attacker must be at esp+4');
assert.strictEqual(tdArgs.victim.__addr, 0x11100, 'victim must be at esp+8');
assert.strictEqual(tdArgs.type, 3, 'type must be at esp+0x38');
assert.notStrictEqual(tdArgs.attacker.__addr, P(STACK).readPointer().__addr, 'never treat the return address as attacker');

const ESTACK = 0x13100;
mapRange(ESTACK, 0x100);
w32(ESTACK + 4, 1.5);
w32(ESTACK + 8, 2.5);
w32(ESTACK + 12, -3.5);
w32(ESTACK + 0x14, 6.0);
view.setUint32(ESTACK + 0x20 - MEM_BASE, 0x11200, true);
const exArgs = test.readExplosionArgs(P(ESTACK));
assert.strictEqual(exArgs.worldPos.x, 1.5);
assert.strictEqual(exArgs.worldPos.y, 2.5);
assert.strictEqual(exArgs.worldPos.z, -3.5);
assert.strictEqual(exArgs.range, 6);
assert.strictEqual(exArgs.eventPtr.__addr, 0x11200, 'DamageEventData must be at esp+0x20');

console.log('direct damage defense runtime tests passed');
