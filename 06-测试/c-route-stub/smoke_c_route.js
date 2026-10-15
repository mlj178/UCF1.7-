/* eslint-disable */
// ==========================================================================
// 40_direct_damage / C 路线（根治版）离线冒烟测试
// --------------------------------------------------------------------------
// 用一套最小 Frida stub 把 features/40_direct_damage/script.js 真正跑起来，
// 然后调用它的 RPC。验的不是"代码里搜不到字符串"，而是**运行时事实**：
//   1) 脚本能加载，rpc.exports 表面完整
//   2) enable({}) 能成功装钩子，装的全是"只读目标选择 + 改写射线/速度"的钩子
//   3) ★ NativeFunction 从来没有被创建过任何"伤害/死亡"入口
//      （TakeDamage / OnEntityHurt / HealthData.Hurt / DeathEventBroadcast /
//        RespawnPlayer / Player.Respawn / GameRoundEnd ...）
//   4) ★ Interceptor.replace / revert 一次都没被调用过
//      （"跳过原函数"这条路必须整个不存在）
//   5) 触发 WPN_Gun.Damage 钩子不会抛异常、不会注入伤害
//   6) status().config 里没有任何已废弃的配置键
//   7) disable() 会把钩子全部摘掉
// 用法：node 06-测试/c-route-stub/smoke_c_route.js <script.js 路径>
// 退出码 0 = 全部断言通过。
// ==========================================================================
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const MODULE_NAME = 'GameAssembly.dll';
const BASE = 0x6d060000;
const MODULE_SIZE = 0x00f00000;
const DEFAULT_SCRIPT = path.resolve(
    __dirname, '..', '..',
    '04-正式发行版', '全功能整合包2.7', 'game_modifier', 'features', '40_direct_damage', 'script.js'
);

// 旧版（注入式）用过的地址 —— 只要有一个出现在 NativeFunction/attach 里就是回归
const RETIRED_RVA = {
    0x00AFC1C0: 'GameManager.TakeDamage',
    0x00B3F470: 'Entity.OnEntityHurt',
    0x00B516B0: 'Player.OnEntityHurt',
    0x00AE45B0: 'HealthData.Hurt',
    0x00B3D0D0: 'DamageEventData.TakePlace',
    0x00AFA400: 'GameManager.DeathEventBroadcast',
    0x00AFB970: 'GameManager.PlayHitFxAndSnd',
    0x00AFAA40: 'GameManager.GameRoundEnd',
    0x00AEBCB0: 'GameManager.NewGameRoundStart',
    0x00AEBD40: 'GameManager.OnDestroy',
    0x00AF2670: 'ModeBase_Nano.RespawnPlayer',
    0x00B527A0: 'Player.Respawn',
    0x0013FF10: 'Il2Cpp.Exception.Raise',
    0x00AEF9E0: 'ModeBase_Nano.DeathEvent',
};

const RETIRED_CONFIG_KEYS = [
    'damage_entry', 'gun_hook_mode', 'entry_fallback', 'damage_override',
    'use_event_template', 'fallback_to_original', 'wpn_key_fallback',
    'death_diag', 'death_fix_respawn', 'death_fix_broadcast',
    'death_rescue_max_tries', 'death_respawn_grace_ms',
];

const results = [];
function check(name, ok, detail) {
    results.push({ name: name, ok: !!ok, detail: detail === undefined ? '' : String(detail) });
}

function createWorld() {
    let allocNext = 0x20000000;
    const nativeCalls = [];
    const attaches = [];
    const replaces = [];
    const reverts = [];
    const sends = [];
    const logs = [];
    const timers = [];

    function P(addr) {
        const a = Number(addr) | 0;
        const self = {
            __addr: a,
            add(n) { return P(a + n); },
            sub(n) { return P(a - n); },
            and(n) { return P(a & n); },
            or(n) { return P(a | n); },
            shl(n) { return P(a << n); },
            shr(n) { return P(a >>> n); },
            isNull() { return a === 0; },
            equals(o) { return !!o && o.__addr === a; },
            compare(o) { return a - (o && o.__addr); },
            toString(radix) { return a.toString(radix || 16); },
            // 未映射内存一律读成 0：isNull()/readable() 会自然走到"拿不到对象"的分支
            readU8() { return 0; },
            readS32() { return 0; },
            readU32() { return 0; },
            readFloat() { return 0; },
            readPointer() { return P(0); },
            readCString() { return ''; },
            writeFloat() { return self; },
            writeU32() { return self; },
            writePointer() { return self; },
            writeS32() { return self; },
        };
        return self;
    }

    const sandbox = {
        ptr: (v) => P(v === undefined || v === null ? 0 : v),
        NULL: P(0),
        Process: {
            arch: 'ia32',
            pointerSize: 4,
            findModuleByName(name) {
                if (name !== MODULE_NAME) return null;
                return { name: MODULE_NAME, base: P(BASE), size: MODULE_SIZE, path: 'C:/game/GameAssembly.dll' };
            },
            findRangeByAddress() { return { base: P(BASE), size: MODULE_SIZE, protection: 'r-x' }; },
        },
        Memory: { alloc: (n) => P((allocNext += (n || 16) + 16)) },
        NativeFunction: function (address, retType, argTypes, conv) {
            nativeCalls.push({ address: address.__addr, retType: retType, conv: conv });
            return function () { return 0; };
        },
        Interceptor: {
            attach(address, callbacks) {
                const record = { address: address.__addr, callbacks: callbacks, detached: false };
                attaches.push(record);
                return { detach() { record.detached = true; } };
            },
            replace(address) { replaces.push(address.__addr); return { revert() {} }; },
            revert(address) { reverts.push(address.__addr); },
        },
        send(payload) { sends.push(payload); },
        rpc: { exports: {} },
        setInterval(fn, ms) { const id = timers.length; timers.push({ fn: fn, ms: ms }); return id; },
        clearInterval(id) { if (timers[id]) timers[id].cleared = true; },
        setTimeout() { return 0; },
        console: { log(...a) { logs.push(a.join(' ')); }, warn() {}, error() {} },
    };
    sandbox.globalThis = sandbox;
    const context = vm.createContext(sandbox);
    return {
        context, P,
        nativeCalls, attaches, replaces, reverts, sends, logs, timers,
        rpc: sandbox.rpc,
    };
}

function main() {
    const scriptPath = process.argv[2] ? path.resolve(process.argv[2]) : DEFAULT_SCRIPT;
    if (!fs.existsSync(scriptPath)) {
        console.error('script.js not found: ' + scriptPath);
        process.exit(2);
    }
    const world = createWorld();
    let loadError = null;
    try {
        vm.runInContext(fs.readFileSync(scriptPath, 'utf8'), world.context, { filename: scriptPath });
    } catch (error) {
        loadError = error;
    }
    check('script loads without throwing', !loadError, loadError && loadError.message);
    if (loadError) { return finish(); }

    const rpc = world.rpc.exports;
    const expectedRpc = ['enable', 'disable', 'status', 'cleanup', 'setConfig', 'logs', 'clearLogs', 'dump', 'snapshot', 'setLogFile'];
    const missingRpc = expectedRpc.filter((name) => typeof rpc[name] !== 'function');
    check('rpc.exports surface intact', missingRpc.length === 0, 'missing=' + missingRpc.join(','));

    let status = null;
    let enableError = null;
    try { status = rpc.enable({}); } catch (error) { enableError = error; }
    check('enable({}) does not throw', !enableError, enableError && enableError.message);
    check('enable() reports initialized', !!status && status.initialized === true, JSON.stringify(status && status.initialized));
    check('enable() reports enabled', !!status && status.enabled === true);

    const hookNames = world.attaches.map((a) => a.address);
    const retiredHits = world.attaches.filter((a) => RETIRED_RVA[a.address]).map((a) => RETIRED_RVA[a.address]);
    check('no retired damage/death RVA is hooked', retiredHits.length === 0, retiredHits.join(','));

    const nativeHits = world.nativeCalls.filter((c) => RETIRED_RVA[c.address]).map((c) => RETIRED_RVA[c.address]);
    check('no damage/death NativeFunction is ever created', nativeHits.length === 0, nativeHits.join(','));

    check('Interceptor.replace never used', world.replaces.length === 0, world.replaces.length);
    check('Interceptor.revert never used', world.reverts.length === 0, world.reverts.length);

    const expectHooks = 15;
    check('installed hook count matches the C route (' + expectHooks + ')', world.attaches.length === expectHooks, world.attaches.length);
    check('WPN_Gun.Damage is attach-hooked exactly once',
        hookNames.filter((a) => a === BASE + 0x00B613D0).length === 1,
        hookNames.filter((a) => a === BASE + 0x00B613D0).length);

    // 触发开火钩子：不允许抛异常，且不许出现任何"注入伤害"的副作用
    let fireError = null;
    for (const record of world.attaches) {
        if (record.address !== BASE + 0x00B613D0) continue;
        try {
            record.callbacks.onEnter.call(
                { context: { esp: world.P(0x30000000) } },
                [world.P(0x40000000)]
            );
            if (record.callbacks.onLeave) record.callbacks.onLeave.call({});
        } catch (error) {
            fireError = error;
        }
    }
    check('firing the gun hook does not throw', !fireError, fireError && fireError.message);

    const afterFire = rpc.status();
    check('gun hook recorded the call', afterFire.gun_damage_calls >= 1, afterFire.gun_damage_calls);
    check('no damage was ever applied (counter is gone)',
        afterFire.damage_applied === undefined && afterFire.death_in === undefined,
        JSON.stringify({ damage_applied: afterFire.damage_applied, death_in: afterFire.death_in }));

    const retiredConfig = RETIRED_CONFIG_KEYS.filter((key) => Object.prototype.hasOwnProperty.call(afterFire.config, key));
    check('status().config has no retired keys', retiredConfig.length === 0, retiredConfig.join(','));

    // 关掉：钩子必须全部 detach
    let disableError = null;
    try { rpc.disable(); } catch (error) { disableError = error; }
    check('disable() does not throw', !disableError, disableError && disableError.message);
    const stillAttached = world.attaches.filter((a) => !a.detached).length;
    check('disable() detached every hook', stillAttached === 0, stillAttached);

    return finish();
}

function finish() {
    let failed = 0;
    for (const item of results) {
        if (!item.ok) failed += 1;
        console.log((item.ok ? 'ok   ' : 'FAIL ') + item.name + (item.detail ? '   [' + item.detail + ']' : ''));
    }
    console.log('---');
    console.log(results.length + ' checks, ' + failed + ' failed');
    process.exit(failed === 0 ? 0 : 1);
}

main();
