/* eslint-disable */
// ==========================================================================
// 40_direct_damage / death_diag 离线冒烟测试
// --------------------------------------------------------------------------
// 用一套最小 Frida stub 把 features/40_direct_damage/script.js 跑起来，然后
// 手动驱动钩子，验证死亡→复活链上的全部修复：
//   1) DeathEventBroadcast onEnter -> 全字段 dump + 字典 key 实查 (dict: ...)
//   2) 上一次广播"进了没出" -> [deathDiag:abort]（异常现场的完整字段）
//   3) Il2Cpp_Exception_Raise -> [deathDiag:raise]（异常类名 + 调用栈 RVA，默认关）
//   4) ★2026-10-15 GameManager.TakeDamage 抛异常 -> 死亡广播没跑 ->
//      death_fix_broadcast 用同一份字段补发游戏自己的 DeathEventBroadcast
//      （验证 14 个 dword 与 DeathEventData 偏移一一对应，且补发后游戏能自己排复活）
//   5) ★2026-10-15 death_fix_respawn 新闸门：只要"宽限期过了还是死的"就兜底
//      （不再要求 bcDone=false / scheduled=false），且目标必须通过
//      isPlausibleVictim（含"必须在当前玩家列表里"）
// 用法：
//   node 06-测试/_crash18_26/run_smoke.js <script.js 路径>
//   node 06-测试/_crash18_26/run_smoke2.js 06-测试/_crash18_26/smoke_no_raise.js <script.js 路径>
// 退出码 0 = 全部断言通过。
// --------------------------------------------------------------------------
//   ★NativeFunction 桩故意不吞异常：Frida 里被调用的游戏函数抛托管异常时会变成
//     JS 异常（message = "system error"），脚本的 try/catch 才看得到 —— 这正是
//     2026-10-15 那条 [fail:applyDamage:gun@takeDamage] 的现场。
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
        findRangeByAddress: function (a) {
            const addr = num(a);
            if (addr >= MODULE_BASE && addr < MODULE_BASE + MODULE_SIZE) {
                return { base: new NP(MODULE_BASE), size: new NP(MODULE_SIZE), protection: 'r-x' };
            }
            return null;   // 模块外一律"不可执行"，用来验证跳过手势的安全阀
        },
        findModuleByAddress: function (a) { const n = num(a); return (n >= MODULE_BASE && n < MODULE_BASE + MODULE_SIZE) ? moduleObj : null; },
        getModuleByAddress: function () { return moduleObj; },
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
        // ★不吞异常：实现里 throw 就是"游戏函数抛托管异常"（Frida 会报 system error）
        const f = function () {
            const a = Array.prototype.slice.call(arguments);
            if (impl) return impl.apply(null, a);
            return defaultRet(ret);
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

    function setNative(addr, fn) {
        const e = natives.get(num(addr));
        if (!e) return false;
        e.set(fn);
        return true;
    }

    return {
        BYTES: BYTES, NP: NP, ptr: ptr, alloc: alloc, wStr: wStr, num: num, rd: rd, wr: wr,
        attaches: attaches, replaces: replaces, sent: sent, consoles: consoles, natives: natives,
        ProcessStub: ProcessStub, ModuleStub: ModuleStub, InterceptorStub: InterceptorStub, MemoryStub: MemoryStub,
        NativeFunction: NativeFunction, NativeCallback: NativeCallback, ThreadStub: ThreadStub, BacktracerStub: BacktracerStub,
        send: send, setIntervalStub: setIntervalStub, clearIntervalStub: clearIntervalStub, consoleStub: consoleStub,
        moduleObj: moduleObj, setNative: setNative
    };
}

function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
// 统一用 Reflect.apply 驱动钩子（等价于 Frida 的 hook.onEnter(args, state)）
function fire(fn, thisArg, args) { return Reflect.apply(fn, thisArg, args); }

async function runSmoke(scriptPath, opts) {
    opts = opts || {};
    const withRaise = opts.raiseProbe !== false;      // 默认：装上异常漏斗探针（正面用例）
    const withSkipGesture = opts.skipGesture !== false;

    const W = createWorld();
    const heartbeatFns = [];
    const setIntervalCapture = function (fn, ms) { heartbeatFns.push(fn); return W.setIntervalStub(fn, ms); };
    const src = fs.readFileSync(scriptPath, 'utf8');
    const rpcObj = {};
    const factory = new Function(
        'Process', 'Module', 'Interceptor', 'Memory', 'NativeFunction', 'NativeCallback',
        'Thread', 'Backtracer', 'ptr', 'Ptr', 'send', 'setInterval', 'clearInterval', 'console', 'rpc',
        src);
    factory(W.ProcessStub, W.ModuleStub, W.InterceptorStub, W.MemoryStub, W.NativeFunction, W.NativeCallback,
        W.ThreadStub, W.BacktracerStub, W.ptr, W.ptr, W.send, setIntervalCapture, W.clearIntervalStub, W.consoleStub, rpcObj);
    const out = [];
    const log = function (s) { out.push(s); };

    const RVA = {
        GameManager_TypeInfo: 0x00E2933C,
        GameManager_DeathEventBroadcast: 0x00AFA400,
        GameManager_TakeDamage: 0x00AFC1C0,
        GameManager_GetWpnData: 0x00AFB130,
        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_MethodInfo: 0x00E1CE64,
        ModeBase_Nano_RespawnPlayer: 0x00AF2670,
        ModeBase_Nano_DeathEvent: 0x00AEF9E0,
        Player_Respawn: 0x00B527A0,
        Il2Cpp_Exception_Raise: 0x0013FF10,
        WPN_Gun_Damage: 0x00B613D0,
        Entity_get_isDead: 0x00B400E0,
        Entity_get_team: 0x001E0070,
        Weapon_get_isMyWeapon: 0x00B6E1D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Player_get_nanoRole: 0x00B56200,
        Component_get_transform: 0x0032CF40,
        Transform_get_position_Injected: 0x003F4280,
        HealthData_get_rate: 0x00AE4950,
        HealthData_get_isDead: 0x00AE4830
    };

    // ---- 假 WpnDataDictionary：keys {100,200,300}（验证字典读取 + 存在性判定）----
    const klass = W.alloc(64), sf = W.alloc(256), dict = W.alloc(64), entries = W.alloc(64);
    W.wr(MODULE_BASE + RVA.GameManager_TypeInfo, 4, W.num(klass));
    W.wr(W.num(klass) + 0x5C, 4, W.num(sf));
    W.wr(W.num(sf) + 0x1C, 4, W.num(dict));
    W.wr(W.num(dict) + 0x0C, 4, W.num(entries));
    W.wr(W.num(dict) + 0x10, 4, 3);
    W.wr(W.num(dict) + 0x14, 4, 1);
    [100, 200, 300].forEach(function (k, i) { W.wr(W.num(entries) + 0x10 + i * 16 + 8, 4, k); });

    // ---- GameManager 单例 + 玩家列表 ----
    const gm = W.alloc(0x100);
    W.wr(MODULE_BASE + RVA.SingletonGameManager_MethodInfo, 4, W.num(W.alloc(8)) || 1);
    const health = new Map();     // healthPtr -> { rate, dead }
    const deadSet = new Set();    // "现在是死的" 的实体指针
    const roleOf = new Map();     // playerPtr -> nanoRole
    const positions = new Map();  // transformAddr -> {x,y,z}
    const mode = W.alloc(64);

    function mkPlayer(tag, team, pos) {
        const p = W.alloc(0x400);
        W.wr(W.num(p) + 0x20, 4, team);                       // Entity_team
        const hp = W.alloc(0x80);
        W.wr(W.num(p) + 0x1C, 4, W.num(hp));                  // Entity_healthData
        W.wr(W.num(p) + 0x08, 4, tag);
        health.set(W.num(hp), { rate: 1, dead: 0 });
        positions.set(W.num(p) + 0x100, pos || { x: 0, y: 0, z: 0 });
        return p;
    }

    const myPlayer = mkPlayer(0x11, 1, { x: 0, y: 0, z: 0 });
    const enemy = mkPlayer(0x12, 0, { x: 5, y: 0, z: 0 });
    const deadA = mkPlayer(0xA1, 1, { x: -100, y: 0, z: 0 });
    const deadB = mkPlayer(0xB1, 1, { x: -100, y: 0, z: 0 });
    const deadC = mkPlayer(0xC1, 1, { x: -100, y: 0, z: 0 });
    const deadD = mkPlayer(0xD1, 1, { x: -100, y: 0, z: 0 });
    const deadH = mkPlayer(0x71, 1, { x: -100, y: 0, z: 0 });
    const deadI = mkPlayer(0x72, 1, { x: -100, y: 0, z: 0 });
    const bogusVictim = mkPlayer(0xB0B, 1, { x: -100, y: 0, z: 0 });
    const ghostVictim = mkPlayer(0x601, 1, { x: -100, y: 0, z: 0 });   // ★故意不进玩家列表
    roleOf.set(W.num(bogusVictim), 126398040);                          // 22:25 闪退的字段指纹

    // 玩家列表：除 ghostVictim 之外全部在列表里
    const listed = [myPlayer, enemy, deadA, deadB, deadC, deadD, deadH, deadI, bogusVictim];
    const arr = W.alloc(0x10 + listed.length * 4 + 16);
    W.wr(W.num(arr) + 0x0C, 4, listed.length);
    listed.forEach(function (p, i) { W.wr(W.num(arr) + 0x10 + i * 4, 4, W.num(p)); });
    W.wr(W.num(gm) + 0x1C, 4, W.num(arr));

    // 全部"死亡观察对象"一开始就是死的（活着的只有 myPlayer / enemy）
    [deadA, deadB, deadC, deadD, deadH, deadI, bogusVictim, ghostVictim].forEach(function (p) {
        deadSet.add(W.num(p));
        const e = health.get(W.rd(W.num(p) + 0x1C, 4));
        if (e) { e.dead = 1; e.rate = 0; }
    });

    // ---- enable ----
    const st0 = rpcObj.exports.enable({
        death_diag: true, death_diag_detail: true,
        death_diag_raise: withRaise,
        death_fix_respawn: true, death_respawn_grace_ms: 1000,
        death_fix_broadcast: true,
        verbose_probe: true, log_to_file: false, log_file: ''
    });
    log('enable -> enabled=' + st0.enabled + ' init=' + st0.initialized + ' attaches=' + st0.attach_hooks);
    log('  attaches recorded=' + W.attaches.length + ' replaces=' + W.replaces.length);

    // ---- 原生桩（必须在 enable 之后：ensureNative 那时才建 NativeFunction）----
    W.setNative(MODULE_BASE + RVA.Singleton_GameManager_get_instance, function () { return gm; });
    W.setNative(MODULE_BASE + RVA.Player_get_isMyPlayer, function (p) { return W.num(p) === W.num(myPlayer) ? 1 : 0; });
    W.setNative(MODULE_BASE + RVA.Entity_get_team, function (p) { return W.rd(W.num(p) + 0x20, 4) | 0; });
    W.setNative(MODULE_BASE + RVA.Entity_get_isDead, function (p) { return deadSet.has(W.num(p)) ? 1 : 0; });
    W.setNative(MODULE_BASE + RVA.Component_get_transform, function (p) { return new W.NP(W.num(p) + 0x100); });
    W.setNative(MODULE_BASE + RVA.Transform_get_position_Injected, function (t, buf) {
        const v = positions.get(W.num(t)) || { x: 0, y: 0, z: 0 };
        const b = Buffer.alloc(12);
        b.writeFloatLE(v.x, 0); b.writeFloatLE(v.y, 4); b.writeFloatLE(v.z, 8);
        for (let i = 0; i < 12; i += 1) W.BYTES.set((W.num(buf) + i) >>> 0, b[i]);
        return 0;
    });
    W.setNative(MODULE_BASE + RVA.HealthData_get_rate, function (h) { const e = health.get(W.num(h)); return e ? e.rate : 1; });
    W.setNative(MODULE_BASE + RVA.HealthData_get_isDead, function (h) { const e = health.get(W.num(h)); return e && e.dead ? 1 : 0; });
    W.setNative(MODULE_BASE + RVA.Player_get_nanoRole, function (p) { return roleOf.get(W.num(p)) || 0; });
    W.setNative(MODULE_BASE + RVA.Weapon_get_isMyWeapon, function () { return 1; });
    W.setNative(MODULE_BASE + RVA.GameManager_GetWpnData, function (idx, outPtr) {
        if (idx === 100 || idx === 200 || idx === 300) { W.wr(W.num(outPtr), 4, 0x1234); return 1; }
        return 0;
    });

    const findA = function (rva) { return W.attaches.filter(function (a) { return W.num(a.addr) === MODULE_BASE + rva; })[0]; };
    const broadcast = findA(RVA.GameManager_DeathEventBroadcast);
    const respawn = findA(RVA.ModeBase_Nano_RespawnPlayer);
    const raiseHook = findA(RVA.Il2Cpp_Exception_Raise);
    const deathEvent = findA(RVA.ModeBase_Nano_DeathEvent);
    const gun = findA(RVA.WPN_Gun_Damage);
    const gunReplaced = W.replaces.filter(function (r) { return W.num(r.addr) === MODULE_BASE + RVA.WPN_Gun_Damage; })[0];
    log('hooks: broadcast=' + !!broadcast + ' respawn=' + !!respawn + ' raise=' + !!raiseHook + ' deathEvent=' + !!deathEvent +
        ' gun=' + !!gun + ' gunReplaced=' + !!gunReplaced);
    if (!broadcast || !respawn || !deathEvent || !gun || gunReplaced) {
        return { ok: false, out: out, reason: 'hook layout unexpected: broadcast=' + !!broadcast + ' respawn=' + !!respawn +
            ' deathEvent=' + !!deathEvent + ' gun=' + !!gun + ' gunReplaced=' + !!gunReplaced };
    }
    if (withRaise && !raiseHook) return { ok: false, out: out, reason: 'raise probe hook missing (death_diag_raise=true)' };
    if (!withRaise && raiseHook) return { ok: false, out: out, reason: 'raise probe installed although death_diag_raise=false' };

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
    function evEsp(ev) { return { context: { esp: new W.NP(W.num(ev) - 4) } }; }
    function fireDeath(killer, dead, wpnIndex, complete, dmgType) {
        const ev = mkEvent(killer, dead, wpnIndex, 0, 0, 0, dmgType || 1);
        fire(broadcast.callbacks.onEnter, evEsp(ev), []);
        if (complete !== false) fire(broadcast.callbacks.onLeave, evEsp(ev), []);
        return ev;
    }

    // ---- 抓 mode 实例（复活兜底要用它当 this）----
    const modeSp = W.alloc(64);
    W.wr(W.num(modeSp) + 4, 4, W.num(mode));
    W.wr(W.num(modeSp) + 8, 4, W.num(deadA));
    W.wr(W.num(modeSp) + 12, 4, 1);
    W.wr(W.num(modeSp) + 16, 1, 1);
    W.wr(W.num(modeSp) + 20, 1, 0);
    fire(respawn.callbacks.onEnter, { context: { esp: new W.NP(W.num(modeSp)) } }, []);

    const killer = myPlayer;

    // ---- 1) 正常死亡（广播完整返回）----
    fireDeath(killer, deadA, 100, true, 1);

    // ---- 2) 被打断的死亡（只 onEnter，不 onLeave）----
    fireDeath(killer, deadB, 341, false, 1);

    // ---- 3) 下一次死亡 -> [deathDiag:abort]（内容是上一次 341）----
    fireDeath(killer, deadC, 200, true, 3);

    // ---- 4) 托管异常漏斗探针（拉到 onEnter 即可）----
    const evD = fireDeath(killer, deadD, 300, false, 3);
    const exc = W.alloc(16), excKlass = W.alloc(64), excName = W.alloc(64);
    W.wr(W.num(exc), 4, W.num(excKlass));
    W.wr(W.num(excKlass) + 8, 4, W.num(excName));
    W.wStr(excName, 'KeyNotFoundException');
    if (raiseHook) fire(raiseHook.callbacks.onEnter, { context: { esp: new W.NP(0) } }, [[new W.NP(W.num(exc)), new W.NP(0)]]);
    fire(broadcast.callbacks.onLeave, evEsp(evD), []);

    // ------------------------------------------------------------------
    // 5) ★2026-10-15：GameManager.TakeDamage 抛异常 -> 补发死亡广播
    // ------------------------------------------------------------------
    //   走真实链路：本地武器开火 -> WPN_Gun.Damage(attach) -> directDamage ->
    //   selectTarget -> applyDamage -> GameManager.TakeDamage 抛 "system error"。
    //   异常落在死亡广播之前（游戏那一次死亡流程一步都没跑）-> 脚本必须：
    //     a) 把这一笔死亡登记进观察窗口（note=exception@takeDamage）
    //     b) 用同一份字段补发游戏自己的 DeathEventBroadcast
    //   桩里把 deathBroadcast 实现成"游戏自己跑一遍广播"（onEnter + 模拟 mode 观察者
    //   调 RespawnPlayer + onLeave），于是可以验证：
    //     · 14 个 dword 与 DeathEventData 偏移一一对应（onEnter 读回来的字段必须一致）
    //     · 游戏自己的复活调度被排上（scheduled=true）
    const rebroadcasts = [];
    W.setNative(MODULE_BASE + RVA.GameManager_DeathEventBroadcast, function () {
        const args = Array.prototype.slice.call(arguments);
        rebroadcasts.push(args);
        const buf = W.alloc(0x40);
        for (let k = 0; k < 14; k += 1) W.wr(W.num(buf) + k * 4, 4, W.num(args[k]));
        fire(broadcast.callbacks.onEnter, { context: { esp: new W.NP(W.num(buf) - 4) } }, []);
        // mode 的 DeathEvent 观察者（真实游戏在广播内部就调 RespawnPlayer）
        const sp = W.alloc(64);
        W.wr(W.num(sp) + 4, 4, W.num(mode));
        W.wr(W.num(sp) + 8, 4, W.num(args[1]));
        W.wr(W.num(sp) + 12, 4, 2);
        W.wr(W.num(sp) + 16, 1, 1);
        W.wr(W.num(sp) + 20, 1, 0);
        fire(respawn.callbacks.onEnter, { context: { esp: new W.NP(W.num(sp)) } }, []);
        fire(broadcast.callbacks.onLeave, { context: { esp: new W.NP(W.num(buf) - 4) } }, []);
        return 0;
    });
    // TakeDamage：先把目标打死（血量/死亡位），再抛托管异常（= 日志里的 system error）
    W.setNative(MODULE_BASE + RVA.GameManager_TakeDamage, function () {
        deadSet.add(W.num(enemy));
        const e = health.get(W.rd(W.num(enemy) + 0x1C, 4));
        if (e) { e.dead = 1; e.rate = 0; }
        throw new Error('system error');
    });

    const weapon = W.alloc(0x200);
    const wdata = W.alloc(0x200);
    W.wr(W.num(weapon) + 0x68, 4, W.num(wdata));           // Weapon_data
    W.wr(W.num(wdata) + 0x0C, 4, 100);                      // WeaponData.wpnIndex = 100（字典里）
    W.wr(W.num(wdata) + 0xA8, 4, W.num(W.alloc(32)));       // hitEffectName（常驻资源名）
    rpcObj.exports.setConfig({
        damage_entry: 'gamemanager',
        damage_override: 40,
        target_mode: 'nearest',
        target_cache_ms: 0,
        fallback_to_original: false,
        death_fix_broadcast: true,
        death_fix_respawn: true,
        death_respawn_grace_ms: 1000
    });
    const retAddr = new W.NP(MODULE_BASE + 0x1234);
    const retSp = W.alloc(16);
    W.wr(W.num(retSp), 4, W.num(retAddr));
    const fireCtx = { context: { esp: new W.NP(W.num(retSp)), pc: new W.NP(MODULE_BASE) }, returnAddress: retAddr };
    fire(gun.callbacks.onEnter, fireCtx, [[new W.NP(W.num(weapon)), 0, 0, 0, 0, 0, 0, new W.NP(0)]]);
    const stFire = rpcObj.exports.status();

    // ------------------------------------------------------------------
    // 6) 复活兜底新闸门
    // ------------------------------------------------------------------
    //   deadA 先"活过来"（isDead=0）-> 一条都不能兜；
    //   deadB(bcDone=false) / deadC(bcDone=true) / deadD(bcDone=true) 都还死着
    //   -> 必须全部兜底（证明闸门不再要求"广播被打断"）；
    //   enemy 虽然也还死着，但游戏已经排了复活（scheduled + respawnTime=2s）
    //   -> 让开路，不在 1 秒宽限期里抢先。
    deadSet.delete(W.num(deadA));
    const eA = health.get(W.rd(W.num(deadA) + 0x1C, 4));
    if (eA) { eA.dead = 0; eA.rate = 1; }
    await sleep(1300);
    fireDeath(killer, deadH, 100, true, 1);           // 这一下触发 deathRescueTick
    const stRescue = rpcObj.exports.status();

    // ------------------------------------------------------------------
    // 7) 硬闸门：role 离谱 / 不在玩家列表 -> 绝不下手
    // ------------------------------------------------------------------
    await sleep(1300);
    fireDeath(killer, bogusVictim, 100, false, 1);    // 只 onEnter（顺便再触发一次 abort 记录）
    fireDeath(killer, ghostVictim, 100, false, 1);
    await sleep(1300);
    fireDeath(killer, deadI, 100, true, 1);           // 触发 tick
    const stGate = rpcObj.exports.status();

    // ------------------------------------------------------------------
    // 8/9) attach 模式"跳过原函数"手势（返回地址校验的正面 + 反向用例）
    // ------------------------------------------------------------------
    let stSkip = null, stNoSkip = null, skipCtx = null, noSkipCtx = null;
    let skipRet = null, skipSp0 = 0;
    if (withSkipGesture) {
        rpcObj.exports.setConfig({ fallback_to_original: false });
        const fakeRet = new W.NP(MODULE_BASE + 0x1234);
        skipRet = fakeRet;
        const fakeSp = W.alloc(16);
        skipSp0 = W.num(fakeSp);
        W.wr(W.num(fakeSp), 4, W.num(fakeRet));
        skipCtx = { context: { esp: new W.NP(W.num(fakeSp)), pc: new W.NP(MODULE_BASE) }, returnAddress: fakeRet };
        fire(gun.callbacks.onEnter, skipCtx, [[new W.NP(W.num(weapon)), 0, 0, 0, 0, 0, 0, new W.NP(0)]]);
        stSkip = rpcObj.exports.status();

        const bogusRet = new W.NP(0x7f000000);
        const fakeSp2 = W.alloc(16);
        W.wr(W.num(fakeSp2), 4, W.num(bogusRet));
        noSkipCtx = { context: { esp: new W.NP(W.num(fakeSp2)), pc: new W.NP(0) }, returnAddress: bogusRet };
        fire(gun.callbacks.onEnter, noSkipCtx, [[new W.NP(W.num(weapon)), 0, 0, 0, 0, 0, 0, new W.NP(0)]]);
        stNoSkip = rpcObj.exports.status();
    }

    const st1 = rpcObj.exports.status();

    // ------------------------------------------------------------------
    // 6b) ★2026-10-15：兜底必须"isDead 真的变 false"才算成功（旧版调用成功就收工）
    // ------------------------------------------------------------------
    //   装上"真的会把人复活"的 RespawnPlayer 实现，然后让一个还死着的目标进观察窗口：
    //     · 兜底调用后 isDead=false -> death_rescued 必须 +1
    //     · 同一个目标不能再补第二次（entry.rescued）
    const deadJ = mkPlayer(0xE1, 1, { x: -100, y: 0, z: 0 });
    listed.push(deadJ);
    W.wr(W.num(arr) + 0x0C, 4, listed.length);
    W.wr(W.num(arr) + 0x10 + (listed.length - 1) * 4, 4, W.num(deadJ));
    deadSet.add(W.num(deadJ));
    { const eJ = health.get(W.rd(W.num(deadJ) + 0x1C, 4)); if (eJ) { eJ.dead = 1; eJ.rate = 0; } }
    W.setNative(MODULE_BASE + RVA.ModeBase_Nano_RespawnPlayer, function (m, dead, rt, isNormal, clearExp) {
        // 先按真实链路触发钩子（登记 scheduled / 抓 mode 实例），再真的把人复活
        const sp = W.alloc(64);
        W.wr(W.num(sp) + 4, 4, W.num(m));
        W.wr(W.num(sp) + 8, 4, W.num(dead));
        W.wr(W.num(sp) + 12, 4, W.num(rt));
        W.wr(W.num(sp) + 16, 1, W.num(isNormal));
        W.wr(W.num(sp) + 20, 1, W.num(clearExp));
        fire(respawn.callbacks.onEnter, { context: { esp: new W.NP(W.num(sp)) } }, []);
        deadSet.delete(W.num(dead));
        const e = health.get(W.rd(W.num(dead) + 0x1C, 4));
        if (e) { e.dead = 0; e.rate = 1; }
        return 0;
    });
    await sleep(1300);
    fireDeath(killer, deadJ, 100, true, 1);       // 登记这笔死亡
    await sleep(1300);
    fireDeath(killer, deadI, 100, true, 1);       // 触发 tick -> 兜底 -> 桩里真的复活
    // 心跳里会跑 checkDeathWatch：救活的目标必须结案（half_dead_recovered +1）
    if (heartbeatFns.length) { try { heartbeatFns[0](); } catch (_) {} }
    const stRevive = rpcObj.exports.status();

    // ------------------------------------------------------------------
    // 10) ★2026-10-15：原生射线接管（gun_ray_redirect）
    // ------------------------------------------------------------------
    //   构造一条"像射线"的栈（weapon + origin + 单位方向），然后：
    //     · onEnter 必须把方向参数改写成"指向目标"
    //     · 原函数不能被跳过（gun_skipped 不变）-> 游戏自己的伤害/死亡流程照跑
    //     · onLeave 核对血量：掉了 = ray_redirect_hits；没掉 = ray_redirect_miss + 退回注入
    rpcObj.exports.setConfig({ gun_ray_redirect: true, fallback_to_original: false, target_mode: 'nearest', target_cache_ms: 0 });
    deadSet.delete(W.num(enemy));
    { const eE = health.get(W.rd(W.num(enemy) + 0x1C, 4)); if (eE) { eE.dead = 0; eE.rate = 1; } }
    // 注入兜底用：把 TakeDamage 换成"正常扣血且不抛异常"的实现（miss 用例要用）
    W.setNative(MODULE_BASE + RVA.GameManager_TakeDamage, function () {
        const eE = health.get(W.rd(W.num(enemy) + 0x1C, 4));
        if (eE) { eE.rate = 0.25; }
        return 0;
    });
    function mkRayCtx() {
        const sp = W.alloc(64);
        W.wr(W.num(sp), 4, W.num(new W.NP(MODULE_BASE + 0x3000)));      // 返回地址
        W.wr(W.num(sp) + 4, 4, W.num(weapon));                           // arg0 = weapon
        new W.NP(W.num(sp) + 8).writeFloat(0);                           // origin
        new W.NP(W.num(sp) + 12).writeFloat(0);
        new W.NP(W.num(sp) + 16).writeFloat(0);
        new W.NP(W.num(sp) + 20).writeFloat(1);                          // dir = (1,0,0)
        new W.NP(W.num(sp) + 24).writeFloat(0);
        new W.NP(W.num(sp) + 28).writeFloat(0);
        return { sp: sp, ctx: { context: { esp: new W.NP(W.num(sp)), pc: new W.NP(MODULE_BASE) },
            returnAddress: new W.NP(MODULE_BASE + 0x3000), dd_target: null } };
    }
    const rayHit = mkRayCtx();
    const raySkippedBefore = rpcObj.exports.status().gun_skipped;
    fire(gun.callbacks.onEnter, rayHit.ctx, [[new W.NP(W.num(weapon)), 0, 0, 0, 0, 0, 0, new W.NP(0)]]);
    const rayDirAfter = { x: new W.NP(W.num(rayHit.sp) + 20).readFloat(), y: new W.NP(W.num(rayHit.sp) + 24).readFloat(), z: new W.NP(W.num(rayHit.sp) + 28).readFloat() };
    // 模拟"原版这一发真的打掉了血"
    { const eE = health.get(W.rd(W.num(enemy) + 0x1C, 4)); if (eE) { eE.rate = 0.5; } }
    fire(gun.callbacks.onLeave, rayHit.ctx, []);
    const stRayHit = rpcObj.exports.status();
    // miss 用例：原版没打掉血 -> 必须退回注入
    const rayMiss = mkRayCtx();
    { const eE = health.get(W.rd(W.num(enemy) + 0x1C, 4)); if (eE) { eE.rate = 1; eE.dead = 0; } }
    fire(gun.callbacks.onEnter, rayMiss.ctx, [[new W.NP(W.num(weapon)), 0, 0, 0, 0, 0, 0, new W.NP(0)]]);
    fire(gun.callbacks.onLeave, rayMiss.ctx, []);
    const stRayMiss = rpcObj.exports.status();
    const allLogs = W.sent.map(function (s) {
        try { const o = JSON.parse(s); return String(o.message || s); } catch (e) { return String(s); }
    }).concat(W.consoles.map(String));
    const logs = [];
    const seenLog = {};
    allLogs.forEach(function (l) {
        const key = l.replace(/^(\[[^\]]*\]\s*)+/, '');
        if (!seenLog[key]) { seenLog[key] = 1; logs.push(l); }
    });
    const pick = function (needle) { return logs.filter(function (l) { return String(l).indexOf(needle) >= 0; }); };

    const checks = [];
    function check(name, cond, detail) { checks.push({ name: name, ok: !!cond, detail: detail || '' }); }

    // ---- 基础诊断 ----
    const inLines = pick('[deathDiag:deathIn]');
    check('deathIn 打全 12 个字段', inLines[0] && ['killer', 'dead', 'headShot', 'wallThrough', 'dmgType', 'origin', 'specialKill', 'nanoKill', 'revenge', 'dmgTag', 'wpn', 'wpnSpr'].every(function (k) { return inLines[0].indexOf(k + '=') >= 0; }), inLines[0]);
    check('字典实查: wpn=100 -> :OK', inLines[0] && inLines[0].indexOf('wpn=100:OK') >= 0, inLines[0]);
    const aborts = pick('[deathDiag:abort]');
    check('abort 检测到"上一次进了没出"', aborts.length >= 1 && aborts[0].indexOf('wpn=341') >= 0 && aborts[0].indexOf(deadB.toString()) >= 0, 'got ' + aborts.length + ' :: ' + (aborts[0] || '').slice(0, 120));
    if (withRaise) {
        const raises = pick('[deathDiag:raise]');
        check('异常探针抓到 KeyNotFoundException', raises.length === 1 && raises[0].indexOf('KeyNotFoundException') >= 0, raises[0]);
        check('异常探针标出 inBroadcast=YES', raises[0] && raises[0].indexOf('inBroadcast=YES') >= 0, raises[0]);
    } else {
        check('默认不装异常漏斗探针 -> 0 条 [deathDiag:raise]', pick('[deathDiag:raise]').length === 0, 'got ' + pick('[deathDiag:raise]').length);
        check('安装日志标注探针已禁用', pick('托管异常探针已禁用').length >= 1, '');
    }

    // ---- 5) 补发死亡广播 ----
    const rebroadcastLogs = pick('已补发游戏自己的 DeathEventBroadcast');
    check('TakeDamage 抛异常 -> 补发失败日志为空', pick('[fail:deathFix:broadcast]').length === 0, pick('[fail:deathFix:broadcast]').join(' | '));
    check('TakeDamage 抛异常 -> 补发 1 次 DeathEventBroadcast', rebroadcasts.length === 1 && rebroadcastLogs.length >= 1, 'rebroadcasts=' + rebroadcasts.length + ' logs=' + rebroadcastLogs.length);
    const rb = rebroadcasts[0] || [];
    check('补发数据 killer/dead 正确（dword0/dword1）', W.num(rb[0]) === W.num(myPlayer) && W.num(rb[1]) === W.num(enemy), JSON.stringify([String(rb[0]), String(rb[1])]));
    check('补发数据 offset 映射正确（+0x10 dmgType / +0x30 wpnIndex）', W.num(rb[4]) === 1 && W.num(rb[12]) === 100 && W.num(rb[13]) === 0, 'dmgType=' + W.num(rb[4]) + ' wpn=' + W.num(rb[12]) + ' wpnSpr=' + W.num(rb[13]));
    check('补发参数 15 个（14 dword + method）', rb.length === 15, 'args=' + rb.length);
    check('status.death_rebroadcast=1', st1.death_rebroadcast === 1, String(st1.death_rebroadcast));
    check('补发后游戏自己排上了复活（scheduled）', st1.respawn_scheduled >= 1, String(st1.respawn_scheduled));
    check('补发的广播走的是我们的 onEnter（death_in 增加）', st1.death_in >= 4, 'death_in=' + st1.death_in);
    check('补发那一笔先按 exception@takeDamage 登记（广播没跑的证据）',
        pick('(gun exception@takeDamage)').length >= 1, pick('死亡登记').join(' | ').slice(0, 200));
    check('异常那一发仍然压掉原版（gun_skipped=1，不会双倍伤害）', stFire.gun_skipped === 1, String(stFire.gun_skipped));

    // ---- 6) 复活兜底新闸门 ----
    const rescues = pick('[deathFix] 复活兜底');
    const rescuedKeys = rescues.map(function (l) { return String(l); });
    check('兜底 >=3 次（deadB/C/D 都还死着）', rescues.length >= 3, 'got ' + rescues.length + ' :: ' + rescuedKeys.map(function (l) { return l.slice(0, 80); }).join(' | '));
    check('bcDone=true 的目标也会兜底（deadC / deadD）',
        rescuedKeys.some(function (l) { return l.indexOf(deadC.toString()) >= 0; }) && rescuedKeys.some(function (l) { return l.indexOf(deadD.toString()) >= 0; }),
        rescuedKeys.join(' | ').slice(0, 220));
    check('广播被打断的目标照样兜底（deadB）', rescuedKeys.some(function (l) { return l.indexOf(deadB.toString()) >= 0; }), rescuedKeys.join(' | ').slice(0, 220));
    check('已经活过来的目标绝不兜底（deadA）', !rescuedKeys.some(function (l) { return l.indexOf(deadA.toString()) >= 0; }), rescuedKeys.join(' | ').slice(0, 220));
    check('游戏已排复活的目标让开（enemy 不在本次兜底里）', !rescuedKeys.some(function (l) { return l.indexOf(enemy.toString()) >= 0; }), rescuedKeys.join(' | ').slice(0, 220));
    check('兜底走 ModeBase_Nano.RespawnPlayer', rescues[0] && rescues[0].indexOf('ModeBase_Nano.RespawnPlayer') >= 0, rescues[0]);
    check('兜底日志标出"复活调度=已命中但没生效 / 未命中"', /复活调度=(已命中但没生效|未命中)/.test(rescues[0] || ''), rescues[0]);
    // ★2026-10-15：调用成功 ≠ 救活。桩里的 RespawnPlayer 不会真的复活 -> 只能算尝试，
    //   目标还是死的就该继续补（旧版这里就收工了，正是"兜底也没效果"的根因）。
    check('兜底重试：尝试>=3 次且没救活不算成功', stRescue.death_rescue_attempts >= 3 && stRescue.death_rescued === 0,
        'attempts=' + stRescue.death_rescue_attempts + ' rescued=' + stRescue.death_rescued);
    check('兜底日志标出"目标仍是死的，稍后重试"', /目标仍是死的/.test(rescues[0] || ''), rescues[0]);
    check('兜底真的救活 -> death_rescued>=1', stRevive.death_rescued >= 1, String(stRevive.death_rescued));
    check('救活的日志标出"-> 目标已活"',
        pick('[deathFix] 复活兜底').some(function (l) { return l.indexOf('-> 目标已活') >= 0; }),
        pick('[deathFix] 复活兜底').join(' | ').slice(0, 220));
    check('同一个目标救活后不再补第二次',
        pick('[deathFix] 复活兜底').filter(function (l) { return l.indexOf(deadJ.toString()) >= 0; }).length === 1,
        pick('[deathFix] 复活兜底').filter(function (l) { return l.indexOf(deadJ.toString()) >= 0; }).join(' | ').slice(0, 220));
    check('已经复活的目标从观察窗口移除（isDead=false）',
        pick('目标已复活').some(function (l) { return l.indexOf(deadJ.toString()) >= 0; }) || stRevive.half_dead_recovered >= 1,
        'recovered=' + stRevive.half_dead_recovered);

    // ---- 10) 原生射线接管 ----
    check('射线参数不像射线 -> 自动退回注入（不写栈）', stRayMiss.ray_redirect_bad_args >= 1, String(stRayMiss.ray_redirect_bad_args));
    check('原生射线接管：方向被改写成指向目标',
        stRayHit.ray_redirect_shots >= 1 &&
        (Math.abs(rayDirAfter.y) > 1e-3 || Math.abs(rayDirAfter.z) > 1e-3) &&
        Math.abs(Math.sqrt(rayDirAfter.x * rayDirAfter.x + rayDirAfter.y * rayDirAfter.y + rayDirAfter.z * rayDirAfter.z) - 1) < 1e-3,
        JSON.stringify(rayDirAfter));
    check('原生射线接管：不跳过原函数（游戏自己的伤害/死亡流程照跑）',
        stRayHit.gun_skipped === raySkippedBefore, 'skipped=' + stRayHit.gun_skipped + ' before=' + raySkippedBefore);
    check('原生射线接管：原版打掉了血 -> ray_redirect_hits>=1', stRayHit.ray_redirect_hits >= 1, String(stRayHit.ray_redirect_hits));
    check('原生射线接管：原版没打掉血 -> 退回注入（miss>=1）',
        stRayMiss.ray_redirect_miss >= 1 && stRayMiss.ray_redirect_shots >= 2,
        'miss=' + stRayMiss.ray_redirect_miss + ' shots=' + stRayMiss.ray_redirect_shots);

    // ---- 7) 硬闸门 ----
    const rejects = pick('[deathDiag] 放弃兜底');
    check('role 离谱的目标被硬闸门拦下', rejects.some(function (l) { return l.indexOf(bogusVictim.toString()) >= 0; }), rejects.map(function (l) { return l.slice(0, 120); }).join(' | '));
    check('不在玩家列表里的目标被拦下（防指针回收）', rejects.some(function (l) { return l.indexOf(ghostVictim.toString()) >= 0; }), rejects.map(function (l) { return l.slice(0, 120); }).join(' | '));
    check('status.death_rescue_rejected>=2', stGate.death_rescue_rejected >= 2, String(stGate.death_rescue_rejected));

    // ---- 8/9) 跳过原函数 ----
    check('WPN_Gun.Damage 走 attach（replace 数=0）', !!gun && W.replaces.length === 0, 'replaces=' + W.replaces.length);
    check('attach 模式下 gunSkipped/gunSkipFailed 已计数', st1.gun_skipped !== undefined && st1.gun_skip_failed !== undefined, JSON.stringify({ skipped: st1.gun_skipped, failed: st1.gun_skip_failed }));
    if (withSkipGesture) {
        check('跳过原函数：pc 指回调用方 + esp 前进 4（模拟 ret）',
            W.num(skipCtx.context.pc) === W.num(skipRet) && W.num(skipCtx.context.esp) === (skipSp0 + 4),
            JSON.stringify({ pc: String(skipCtx.context.pc), wantPc: String(skipRet), esp: String(skipCtx.context.esp), wantEsp: '0x' + (skipSp0 + 4).toString(16) }));
        check('跳过原函数：gun_skipped 再 +1', stSkip.gun_skipped === stFire.gun_skipped + 1, String(stSkip.gun_skipped) + ' (was ' + stFire.gun_skipped + ')');
        check('返回地址不在模块内 -> 拒绝跳过（pc 不变 / gun_skip_failed=1）',
            W.num(noSkipCtx.context.pc) === 0 && stNoSkip.gun_skip_failed === 1,
            JSON.stringify({ pc: String(noSkipCtx.context.pc), failed: stNoSkip.gun_skip_failed }));
    }

    out.push('');
    out.push('=== 命中日志 ===');
    ['[deathDiag:deathIn]', '[deathDiag:abort]', '[deathDiag:raise]', '[deathFix]', '[deathDiag] 死亡登记', '[deathDiag:deathOut]', '[probe:hp]'].forEach(function (n) {
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
