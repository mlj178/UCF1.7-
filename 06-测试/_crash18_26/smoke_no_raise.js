/* eslint-disable */
// ==========================================================================
// 40_direct_damage / death_diag 离线冒烟测试
// --------------------------------------------------------------------------
// 用一套最小 Frida stub 把 features/40_direct_damage/script.js 跑起来，然后
// 手动驱动三个钩子，验证 20261014 新增的诊断与兜底代码：
//   1) DeathEventBroadcast onEnter -> 全字段 dump + 字典 key 实查 (dict: ...)
//   2) 上一次广播"进了没出" -> [deathDiag:abort]（异常现场的完整字段）
//   3) Il2Cpp_Exception_Raise -> [deathDiag:raise]（异常类名 + 调用栈 RVA）
//   4) death_fix_respawn -> [deathFix] 复活兜底（超过 grace 还 isDead 就补 RespawnPlayer）
// 用法：
//   node 06-测试/death-diag-stub/smoke_death_diag.js [script.js 路径]
// 退出码 0 = 全部断言通过。
'use strict';
const fs = require('fs');
const path = require('path');

const MODULE_BASE = 0x6d060000;
const MODULE_SIZE = 0x00f00000;
const ALLOC_BASE = 0x20000000;
const MODULE_NAME = 'GameAssembly.dll';

function createWorld() {
    const BYTES = new Map();
    let allocNext = ALLOC_BASE;
    const attaches = [];
    const replaces = [];
    const sent = [];
    const consoles = [];
    const natives = new Map();

    function num(x) { return x instanceof NP ? x.addr : (Number(x) | 0); }
    function rd(addr, size) {
        let v = 0;
        for (let i = 0; i < size; i += 1) v += (BYTES.get((addr + i) >>> 0) || 0) * Math.pow(2, 8 * i);
        return v >>> 0;
    }
    function wr(addr, size, value) {
        let v = Number(value) >>> 0;
        for (let i = 0; i < size; i += 1) { BYTES.set((addr + i) >>> 0, v & 0xff); v = v >>> 8; }
    }
    class NP {
        constructor(a) { this.addr = (typeof a === 'number' ? a : num(a)) >>> 0; }
        isNull() { return this.addr === 0; }
        toString(radix) { return '0x' + this.addr.toString(radix || 16); }
        toInt32() { return this.addr | 0; }
        toUInt32() { return this.addr >>> 0; }
        add(n) { return new NP(this.addr + num(n)); }
        sub(n) { return new NP(this.addr - num(n)); }
        equals(o) { return !!o && o.addr === this.addr; }
        compare(o) { return this.addr - num(o); }
        readU8() { return rd(this.addr, 1); }
        readS32() { return rd(this.addr, 4) | 0; }
        readU32() { return rd(this.addr, 4) >>> 0; }
        readFloat() { const b = Buffer.alloc(4); b.writeUInt32LE(rd(this.addr, 4) >>> 0, 0); return b.readFloatLE(0); }
        readPointer() { return new NP(rd(this.addr, 4)); }
        writeU8(v) { wr(this.addr, 1, v); return this; }
        writeS32(v) { wr(this.addr, 4, v); return this; }
        writeU32(v) { wr(this.addr, 4, v); return this; }
        writeFloat(v) { const b = Buffer.alloc(4); b.writeFloatLE(Number(v) || 0, 0); wr(this.addr, 4, b.readUInt32LE(0)); return this; }
        writePointer(v) { wr(this.addr, 4, v instanceof NP ? v.addr : Number(v)); return this; }
        readUtf8String(n) {
            let s = '';
            for (let i = 0; i < (n || 64); i += 1) { const c = BYTES.get((this.addr + i) >>> 0) || 0; if (!c) break; s += String.fromCharCode(c); }
            return s;
        }
    }
    function ptr(v) { return v instanceof NP ? v : new NP(v === undefined || v === null ? 0 : v); }
    function alloc(size) { const p = new NP(allocNext); allocNext += Math.max(16, Number(size) | 0) + 16; return p; }
    function wStr(addr, s) { for (let i = 0; i < s.length; i += 1) BYTES.set((num(addr) + i) >>> 0, s.charCodeAt(i) & 0xff); BYTES.set(num(addr) + s.length, 0); }

    const moduleObj = { name: MODULE_NAME, base: new NP(MODULE_BASE), size: new NP(MODULE_SIZE), path: 'C:/game/GameAssembly.dll' };
    const ProcessStub = {
        arch: 'ia32', pointerSize: 4,
        findModuleByName: function () { return moduleObj; },
        findRangeByAddress: function () { return { base: new NP(MODULE_BASE), size: new NP(MODULE_SIZE), protection: 'r-x' }; },
        enumerateModules: function () { return [moduleObj]; },
        getModuleByName: function () { return moduleObj; }
    };
    const ModuleStub = { findExportByName: function () { return null; }, getExportByName: function () { return null; }, findBaseAddress: function () { return new NP(MODULE_BASE); } };
    const InterceptorStub = {
        attach: function (addr, callbacks) { const h = { addr: addr, callbacks: callbacks, detach: function () {} }; attaches.push(h); return h; },
        replace: function (addr, cb) { replaces.push({ addr: addr, cb: cb }); return { revert: function () {} }; },
        revert: function () { return true; },
        detachAll: function () {}
    };
    const MemoryStub = { alloc: function (size) { return alloc(size); }, readByteArray: function () { return []; } };
    function defaultRet(ret) { return ret === 'float' ? 0 : 0; }
    function NativeFunction(addr, ret, argTypes, conv) {
        let impl = null;
        const f = function () {
            const a = Array.prototype.slice.call(arguments);
            try { return impl ? impl.apply(null, a) : defaultRet(ret); } catch (e) { return defaultRet(ret); }
        };
        natives.set(num(addr), { fn: f, set: function (g) { impl = g; }, ret: ret, addr: num(addr) });
        return f;
    }
    function NativeCallback(fn) { return fn; }
    const ThreadStub = { backtrace: function () { return []; } };
    const BacktracerStub = { FUZZY: 'fuzzy', ACCURATE: 'accurate' };
    function send(msg) { sent.push(typeof msg === 'string' ? msg : JSON.stringify(msg)); }
    const timers = [];
    function setIntervalStub(fn, ms) { timers.push({ fn: fn, ms: ms }); return timers.length; }
    function clearIntervalStub() {}
    const consoleStub = { log: function () { consoles.push(Array.prototype.join.call(arguments, ' ')); }, error: function () {}, warn: function () {} };

    return {
        BYTES: BYTES, NP: NP, ptr: ptr, alloc: alloc, wStr: wStr, num: num, rd: rd, wr: wr,
        attaches: attaches, replaces: replaces, sent: sent, consoles: consoles, natives: natives,
        ProcessStub: ProcessStub, ModuleStub: ModuleStub, InterceptorStub: InterceptorStub, MemoryStub: MemoryStub,
        NativeFunction: NativeFunction, NativeCallback: NativeCallback, ThreadStub: ThreadStub, BacktracerStub: BacktracerStub,
        send: send, setIntervalStub: setIntervalStub, clearIntervalStub: clearIntervalStub, consoleStub: consoleStub,
        moduleObj: moduleObj
    };
}

function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
// 统一用 Reflect.apply 驱动钩子（等价于 Frida 的 hook.onEnter(args, state)）
function fire(fn, thisArg, args) { return Reflect.apply(fn, thisArg, args); }

async function runSmoke(scriptPath) {
    const W = createWorld();
    const src = fs.readFileSync(scriptPath, 'utf8');
    const rpcObj = {};
    const factory = new Function(
        'Process', 'Module', 'Interceptor', 'Memory', 'NativeFunction', 'NativeCallback',
        'Thread', 'Backtracer', 'ptr', 'Ptr', 'send', 'setInterval', 'clearInterval', 'console', 'rpc',
        src);
    factory(W.ProcessStub, W.ModuleStub, W.InterceptorStub, W.MemoryStub, W.NativeFunction, W.NativeCallback,
        W.ThreadStub, W.BacktracerStub, W.ptr, W.ptr, W.send, W.setIntervalStub, W.clearIntervalStub, W.consoleStub, rpcObj);
    const out = [];
    const log = function (s) { out.push(s); };

    const RVA = {
        GameManager_TypeInfo: 0x00E2933C,
        GameManager_DeathEventBroadcast: 0x00AFA400,
        ModeBase_Nano_RespawnPlayer: 0x00AF2670,
        ModeBase_Nano_DeathEvent: 0x00AEF9E0,
        Il2Cpp_Exception_Raise: 0x0013FF10,
        WPN_Gun_Damage: 0x00B613D0,
        Entity_get_isDead: 0x00B400E0
    };

    // ---- 假 WpnDataDictionary：keys {100,200,300}（验证字典读取 + 存在性判定）----
    const klass = W.alloc(64), sf = W.alloc(256), dict = W.alloc(64), entries = W.alloc(64), items = W.alloc(128);
    W.wr(MODULE_BASE + RVA.GameManager_TypeInfo, 4, W.num(klass));
    W.wr(W.num(klass) + 0x5C, 4, W.num(sf));
    W.wr(W.num(sf) + 0x1C, 4, W.num(dict));
    W.wr(W.num(dict) + 0x0C, 4, W.num(entries));
    W.wr(W.num(dict) + 0x10, 4, 3);
    W.wr(W.num(dict) + 0x14, 4, 1);
    // Il2CppArray 的数据区内联在 +0x10（Entry 16 字节，key 在 +0x08）
    [100, 200, 300].forEach(function (k, i) { W.wr(W.num(entries) + 0x10 + i * 16 + 8, 4, k); });

    function mkPlayer(tag) {
        const p = W.alloc(0x200);
        W.wr(W.num(p) + 0x20, 4, 1);   // Entity_team = 1 -> isValidPlayer 通过
        W.wr(W.num(p) + 0x08, 4, tag);
        return p;
    }
    function mkEvent(killer, dead, wpnIndex, dmgTag, specialKill, nanoKill, dmgType) {
        const ev = W.alloc(0x48);
        W.wr(W.num(ev) + 0x00, 4, W.num(killer));
        W.wr(W.num(ev) + 0x04, 4, W.num(dead));
        W.wr(W.num(ev) + 0x08, 4, 0);
        W.wr(W.num(ev) + 0x0C, 1, 0);
        W.wr(W.num(ev) + 0x10, 4, dmgType || 1);
        W.wr(W.num(ev) + 0x14, 4, 0);
        W.wr(W.num(ev) + 0x20, 4, specialKill || 0);
        W.wr(W.num(ev) + 0x24, 4, nanoKill || 0);
        W.wr(W.num(ev) + 0x28, 1, 0);
        W.wr(W.num(ev) + 0x2C, 4, dmgTag || 0);
        W.wr(W.num(ev) + 0x30, 4, wpnIndex === undefined ? -1 : wpnIndex);
        W.wr(W.num(ev) + 0x34, 4, 0);
        return ev;
    }

    // ---- enable ----
    const st0 = rpcObj.exports.enable({
        death_diag: true, death_diag_detail: true,
        death_fix_respawn: true, death_respawn_grace_ms: 1000,
        verbose_probe: true, log_to_file: false, log_file: ''
    });
    log('enable -> enabled=' + st0.enabled + ' init=' + st0.initialized + ' attaches=' + st0.attach_hooks + ' replaced=' + (st0.attach_hooks && 0));
    log('  attaches recorded=' + W.attaches.length + ' replaces=' + W.replaces.length);

    const findA = function (rva) { return W.attaches.filter(function (a) { return W.num(a.addr) === MODULE_BASE + rva; })[0]; };
    const broadcast = findA(RVA.GameManager_DeathEventBroadcast);
    const respawn = findA(RVA.ModeBase_Nano_RespawnPlayer);
    const raiseHook = findA(RVA.Il2Cpp_Exception_Raise);
    const deathEvent = findA(RVA.ModeBase_Nano_DeathEvent);
    const gun = W.replaces.filter(function (r) { return W.num(r.addr) === MODULE_BASE + RVA.WPN_Gun_Damage; })[0];
    log('hooks: broadcast=' + !!broadcast + ' respawn=' + !!respawn + ' raise=' + !!raiseHook + ' deathEvent=' + !!deathEvent + ' gun=' + !!gun);
    if (!broadcast || !respawn || raiseHook || !gun) return { ok: false, out: out, reason: 'raise hook installed although death_diag_raise was absent: ' + !!raiseHook };

    // ---- 抓 mode 实例 ----
    const mode = W.alloc(64), modeDead = mkPlayer(0x1000);
    const sp = W.alloc(64);
    W.wr(W.num(sp) + 4, 4, W.num(mode));
    W.wr(W.num(sp) + 8, 4, W.num(modeDead));
    W.wr(W.num(sp) + 12, 4, 1);
    W.wr(W.num(sp) + 16, 1, 1);
    W.wr(W.num(sp) + 20, 1, 0);
    fire(respawn.callbacks.onEnter, { context: { esp: new W.NP(W.num(sp)) } }, []);

    // ---- 1) 正常死亡（wpn=100 合法）----
    const killer = mkPlayer(0x2000);
    const deadA = mkPlayer(0xA1);
    const evA = mkEvent(killer, deadA, 100, 0x40, 0, 0, 1);
    fire(broadcast.callbacks.onEnter, { context: { esp: new W.NP(W.num(evA) - 4) } }, []);
    fire(broadcast.callbacks.onLeave, { context: { esp: new W.NP(W.num(evA) - 4) } }, []);

    // ---- 2) 被打断的死亡（wpn=341 不在字典里，故意不调 onLeave）----
    const deadB = mkPlayer(0xB1);
    const evB = mkEvent(killer, deadB, 341, 0x40, 0, 0, 1);
    fire(broadcast.callbacks.onEnter, { context: { esp: new W.NP(W.num(evB) - 4) } }, []);

    // ---- 3) 下一次死亡 -> 应该报 [deathDiag:abort]，内容是上一次(341) ----
    const deadC = mkPlayer(0xC1);
    const evC = mkEvent(killer, deadC, 200, 0, 0, 0, 3);
    fire(broadcast.callbacks.onEnter, { context: { esp: new W.NP(W.num(evC) - 4) } }, []);
    fire(broadcast.callbacks.onLeave, { context: { esp: new W.NP(W.num(evC) - 4) } }, []);

    // ---- 4) 托管异常（死亡广播正在飞的时候）----
    const deadD = mkPlayer(0xD1);
    const evD = mkEvent(killer, deadD, 300, 0, 0, 0, 3);
    fire(broadcast.callbacks.onEnter, { context: { esp: new W.NP(W.num(evD) - 4) } }, []);
    const exc = W.alloc(16), excKlass = W.alloc(64), excName = W.alloc(64);
    W.wr(W.num(exc), 4, W.num(excKlass));
    W.wr(W.num(excKlass) + 8, 4, W.num(excName));
    W.wStr(excName, 'KeyNotFoundException');
    // Frida 的 onEnter(args, state)：第 1 个参数就是 [ex, method]
    if (raiseHook) fire(raiseHook.callbacks.onEnter, { context: { esp: new W.NP(0) } }, [[new W.NP(W.num(exc)), new W.NP(0)]]);
    fire(broadcast.callbacks.onLeave, { context: { esp: new W.NP(W.num(evD) - 4) } }, []);

    // ---- 5) 复活兜底：IS_DEAD 返回 true，超过 grace 后从开火钩子触发 ----
    const isDeadEntry = W.natives.get(MODULE_BASE + RVA.Entity_get_isDead);
    if (isDeadEntry) isDeadEntry.set(function () { return 1; });
    await sleep(1200);
    const weapon = W.alloc(64);
    gun.cb(new W.NP(W.num(weapon)), 0, 0, 0, 0, 0, 0, new W.NP(0));

    const st1 = rpcObj.exports.status();
    const allLogs = W.sent.map(function (s) {
        try { const o = JSON.parse(s); return String(o.message || s); } catch (e) { return String(s); }
    }).concat(W.consoles.map(String));
    // 同一条日志会被 send 两次（结构化 message + 渲染后的整行），这里按"去掉前缀后的正文"去重
    const logs = [];
    const seenLog = {};
    allLogs.forEach(function (l) {
        const key = l.replace(/^(\[[^\]]*\]\s*)+/, '');
        if (!seenLog[key]) { seenLog[key] = 1; logs.push(l); }
    });
    const pick = function (needle) { return logs.filter(function (l) { return String(l).indexOf(needle) >= 0; }); };

    const checks = [];
    function check(name, cond, detail) { checks.push({ name: name, ok: !!cond, detail: detail || '' }); }

    const inLines = pick('[deathDiag:deathIn]');
    check('deathIn 逐条打印(4 条)', inLines.length === 4, 'got ' + inLines.length);
    check('deathIn 打全 12 个字段', inLines[0] && ['killer', 'dead', 'headShot', 'wallThrough', 'dmgType', 'origin', 'specialKill', 'nanoKill', 'revenge', 'dmgTag', 'wpn', 'wpnSpr'].every(function (k) { return inLines[0].indexOf(k + '=') >= 0; }), inLines[0]);
    check('字典实查: wpn=100 -> :OK', inLines[0] && inLines[0].indexOf('wpn=100:OK') >= 0, inLines[0]);
    check('字典实查: wpn=341 -> :MISS', inLines[1] && inLines[1].indexOf('wpn=341:MISS') >= 0, inLines[1]);
    const aborts = pick('[deathDiag:abort]');
    check('abort 检测 1 次', aborts.length === 1, 'got ' + aborts.length);
    check('abort 内容是上一次(341)', aborts[0] && aborts[0].indexOf('wpn=341') >= 0 && aborts[0].indexOf(deadB.toString()) >= 0, aborts[0]);
    const raises = pick('[deathDiag:raise]');
    check('默认不装异常漏斗探针 -> 0 条 [deathDiag:raise]', raises.length === 0, 'got ' + raises.length);
    check('安装日志标注探针已禁用', pick('托管异常探针已禁用').length >= 1, '');
    const rescues = pick('[deathFix] 复活兜底');
    check('复活兜底 >=1 次', rescues.length >= 1, 'got ' + rescues.length);
    check('兜底走 ModeBase_Nano.RespawnPlayer', rescues[0] && rescues[0].indexOf('ModeBase_Nano.RespawnPlayer') >= 0, rescues[0]);
    check('status.death_aborted=1', st1.death_aborted === 1, String(st1.death_aborted));
    check('status.death_rescued>=1', st1.death_rescued >= 1, String(st1.death_rescued));
    check('status.death_in=4 / death_out=3', st1.death_in === 4 && st1.death_out === 3, st1.death_in + '/' + st1.death_out);

    out.push('');
    out.push('=== 命中日志 ===');
    ['[deathDiag:deathIn]', '[deathDiag:abort]', '[deathDiag:raise]', '[deathFix]', '[deathDiag] 死亡登记', '[deathDiag:deathOut]'].forEach(function (n) {
        pick(n).forEach(function (l) { out.push('  | ' + String(l).slice(0, 260)); });
    });
    out.push('');
    out.push('=== 检查项 ===');
    checks.forEach(function (c) { out.push((c.ok ? '  PASS ' : '  FAIL ') + c.name + (c.ok ? '' : '  <<< ' + c.detail)); });
    const failed = checks.filter(function (c) { return !c.ok; });
    out.push('');
    out.push(failed.length ? ('RESULT: ' + failed.length + ' / ' + checks.length + ' FAILED') : ('RESULT: ALL ' + checks.length + ' CHECKS PASSED'));
    return { ok: failed.length === 0, out: out };
}

module.exports = { runSmoke: runSmoke };
