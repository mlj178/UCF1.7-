'use strict';

// 运行时烟测（不连游戏）：验证「托管调用只在游戏主线程发生」这条护栏。
//
// 背景：2026-11-10 实测崩溃 —— Unity 的 Boehm GC 在 Frida JS 线程上被触发回收，
// 直接 abort（"Fatal error in GC: Collecting from unknown thread"）。
// 只要 setInterval / rpc.exports 里调了会分配托管内存的函数（LayerToName /
// Object.get_name / OverlapSphere / IgnoreCollision 等），这个崩溃就可能复现。
//
// 本文件把 script.js 装进 vm，用桩记录「每一次 NativeFunction 调用」，
// 然后断言：
//   1. layerName() 是纯 JS（0 次原生调用）
//   2. 心跳（setInterval 回调）里 0 次原生调用，只登记 sweepPending
//   3. 启用（RPC）里 0 次原生调用
//   4. 关闭（RPC）里 0 次原生调用
//   5. 真正的原生调用全部发生在 pumpMainThreadWork()（ModeBase.Update 钩子）
//
// 跑法：node test_thread_safety_runtime.js

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const scriptPath = path.join(__dirname, 'script.js');
let source = fs.readFileSync(scriptPath, 'utf8').replace(/^\uFEFF/, '');

const exportPattern = '    rpc.exports = {';
assert(source.includes(exportPattern), 'rpc.exports block not found');
source = source.replace(exportPattern, `    rpc.exports = {
        __test: {
            getRuntime: function () { return Runtime; },
            layerName: layerName,
            learnLayerName: learnLayerName,
            learnLayerNamesStep: learnLayerNamesStep,
            pumpMainThreadWork: pumpMainThreadWork,
            sweepMissileStates: sweepMissileStates,
            processSweepQueue: processSweepQueue,
            enableFeature: enableFeature,
            disableFeature: disableFeature,
            queueReleaseAll: queueReleaseAll
        },`);

// ---- 桩 ---------------------------------------------------------------
let nativeCalls = 0;
const nativeTargets = [];
const attachedHooks = [];
const intervals = new Map();
let nextTimerId = 1;
const sentMessages = [];

function fakePtr(addr) {
    const value = {
        addr: addr === undefined ? 0 : addr,
        isNull: function () { return value.addr === 0; },
        add: function (off) { return fakePtr(value.addr + (off | 0)); },
        sub: function (off) { return fakePtr(value.addr - (off | 0)); },
        readPointer: function () { return fakePtr(0); },
        readS32: function () { return 0; },
        readU32: function () { return 0; },
        readU16: function () { return 0; },
        readU8: function () { return 0; },
        readFloat: function () { return 0; },
        writeS32: function () {},
        writeU32: function () {},
        writeU8: function () {},
        writeFloat: function () {},
        writePointer: function () {},
        equals: function (other) { return !!other && other.addr === value.addr; },
        toString: function () { return '0x' + value.addr.toString(16); }
    };
    return value;
}

function NativeFunction(target, retType) {
    const fn = function () {
        nativeCalls += 1;
        nativeTargets.push(String(target));
        if (retType === 'void') return undefined;
        if (retType === 'bool') return 0;
        if (retType === 'int32' || retType === 'uint32') return 0;
        return fakePtr(0x1000);
    };
    return fn;
}

const context = {
    console: console,
    Date: Date,
    Math: Math,
    JSON: JSON,
    String: String,
    Number: Number,
    Object: Object,
    Array: Array,
    Error: Error,
    isFinite: isFinite,
    parseInt: parseInt,
    parseFloat: parseFloat,
    Process: {
        arch: 'ia32',
        pointerSize: 4,
        findModuleByName: function () { return { name: 'GameAssembly.dll', base: fakePtr(0x10000000) }; },
        findRangeByAddress: function () { return { base: fakePtr(0x10000000), size: 0x1000000, protection: 'r-x' }; }
    },
    Memory: { alloc: function (n) { return fakePtr(0x20000000 + (n | 0)); } },
    NativeFunction: NativeFunction,
    Interceptor: {
        attach: function (addr, callbacks) {
            const hook = { addr: addr, callbacks: callbacks, detach: function () {} };
            attachedHooks.push(hook);
            return hook;
        },
        replace: function () { throw new Error('Interceptor.replace must not be used'); },
        revert: function () {}
    },
    ptr: function (v) { return fakePtr(v === undefined ? 0 : v); },
    NULL: fakePtr(0),
    rpc: { exports: {} },
    send: function (msg) { sentMessages.push(msg); },
    setInterval: function (fn) { const id = nextTimerId++; intervals.set(id, fn); return id; },
    clearInterval: function (id) { intervals.delete(id); },
    setTimeout: function (fn) { return 0; },
    clearTimeout: function () {}
};
vm.createContext(context);
vm.runInContext(source, context, { filename: scriptPath });

const test = context.rpc.exports.__test;
assert(test, '__test exports missing');
const Runtime = test.getRuntime();

function resetNativeCounter() {
    nativeCalls = 0;
    nativeTargets.length = 0;
}

// ---- 1. layerName(): 纯 JS -------------------------------------------
resetNativeCounter();
assert.strictEqual(test.layerName(7), '7');
assert.strictEqual(test.layerName(-1), '-1');
assert.strictEqual(test.layerName(32), '32');
assert.strictEqual(nativeCalls, 0, 'layerName() 不许调用任何游戏函数');

// ---- 2. 启用：RPC 线程 0 次原生调用（同时把 native.* 初始化出来）----
resetNativeCounter();
const enabledResult = test.enableFeature();
assert.strictEqual(enabledResult.ok, true, 'enableFeature 应成功');
assert.strictEqual(nativeCalls, 0, '启用路径（RPC 线程）不许调用任何游戏函数');
assert.strictEqual(Runtime.enabled, true);
assert.ok(attachedHooks.some(function (h) { return h.callbacks && h.callbacks.onEnter; }), '应装上钩子');

// ---- 3. learnLayerName(): 只在主线程调用，且每个层只学一次 ------------
resetNativeCounter();
test.learnLayerName(7);
assert.strictEqual(nativeCalls, 1, 'learnLayerName() 应该只调一次 LayerToName');
assert.strictEqual(Runtime.layerNames[7], '7');
test.learnLayerName(7);
assert.strictEqual(nativeCalls, 1, '已缓存的层名不许重复调用');

// ---- 4. 心跳：0 次原生调用，只登记待清理 ------------------------------
resetNativeCounter();
Runtime.missiles = {
    '0xaa11': { at: Date.now() - 120000, ignores: [], ghost: false },
    '0xbb22': { at: Date.now(), ignores: [], ghost: false }
};
test.sweepMissileStates();
assert.strictEqual(nativeCalls, 0, '心跳清理不许调用任何游戏函数');
assert.strictEqual(JSON.stringify(Runtime.sweepPending), JSON.stringify(['0xaa11']),
    '过期弹体应只登记、不立即还原');

// ---- 5. 主线程泵：真的执行还原 ---------------------------------------
resetNativeCounter();
test.processSweepQueue();
assert.strictEqual(Runtime.missiles['0xaa11'], undefined, '主线程泵应删掉过期弹体状态');
assert.strictEqual(Runtime.stats.projectileSweepRemoved, 1);
assert.strictEqual(Runtime.sweepPending.length, 0, '主线程泵消费完应清空登记队列');

// ---- 6. 关闭：RPC 线程 0 次原生调用 ----------------------------------
resetNativeCounter();
test.disableFeature();
assert.strictEqual(nativeCalls, 0, '关闭路径（RPC 线程）不许调用任何游戏函数');
assert.strictEqual(Runtime.enabled, false);

// ---- 7. 主线程泵：分帧补齐层名，且每次 ≤ budget -----------------------
resetNativeCounter();
Runtime.layerNames = {};
Runtime.layerNamesLogged = false;
let pumps = 0;
while (!Runtime.layerNamesLogged && pumps < 20) {
    const before = nativeCalls;
    test.pumpMainThreadWork();
    assert.ok(nativeCalls - before <= 6, '单帧补层名不许超过 6 次托管调用');
    pumps += 1;
}
assert.ok(Runtime.layerNamesLogged, '32 个层名应在若干帧内补齐并打印一次');
for (let id = 0; id <= 31; id++) {
    assert.ok(Runtime.layerNames[id] !== undefined, '层 ' + id + ' 应有名字或数字兜底');
}

console.log('PASS 29_bullet_wall_penetration thread-safety runtime smoke');
console.log('  native calls: enable=0 disable=0 heartbeat=0 layerName=0');
console.log('  layer-name table pumped in ' + pumps + ' frames, logged once');
