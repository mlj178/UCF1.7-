// feature_id: fast_stock_hit_stun_wait
// 第三版验证：保留原命中协程及镜头震动，仅把本地枪托命中暂停阶段创建的 WaitForSeconds 改为 0 秒。
// 作用范围由“同线程 + 本地 CFAnimator + MoveNext state=1”三项共同限定。

"use strict";

const Runtime = {
  feature_id: "fast_stock_hit_stun_wait",
  enabled: false,
  initialized: false,
  listeners: [],
  activeLocalPauseThreads: new Map(),
  stats: {
    shortenedLocalHitStunWait: 0,
    errorCount: 0,
    lastError: ""
  }
};

const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  KnifeHitStunCoroutine_MoveNext: 0xB73050,
  WaitForSeconds_ctor: 0xA59F50
};

let isMyWeapon = null;

function log(level, event, data) {
  try {
    send({
      type: "log",
      level: level,
      module: "极速枪托等待验证",
      audience: "dev",
      message: JSON.stringify({ feature_id: Runtime.feature_id, event: event, at_ms: Date.now(), data: data || {} })
    });
  } catch (_) {}
}

function pointerText(value) {
  try { return value && !value.isNull() ? value.toString() : "0x0"; } catch (_) { return "unavailable"; }
}

function isLocalAnimator(cfAnimator) {
  try {
    return Boolean(cfAnimator && !cfAnimator.isNull() && isMyWeapon && isMyWeapon(cfAnimator, ptr(0)));
  } catch (_) {
    return false;
  }
}

function detachAll() {
  for (const listener of Runtime.listeners) {
    try { listener.detach(); } catch (_) {}
  }
  try { Interceptor.detachAll(); } catch (_) {}
  Runtime.listeners = [];
  Runtime.activeLocalPauseThreads.clear();
  isMyWeapon = null;
}

function enable() {
  if (Runtime.enabled) return status();
  const module = Process.findModuleByName("GameAssembly.dll");
  if (!module) return { ok: false, reason: "gameassembly_not_loaded" };

  try {
    isMyWeapon = new NativeFunction(module.base.add(RVA.Weapon_get_isMyWeapon), "bool", ["pointer", "pointer"], "mscdecl");

    Runtime.listeners.push(Interceptor.attach(module.base.add(RVA.KnifeHitStunCoroutine_MoveNext), {
      onEnter(args) {
        this.armedThread = null;
        try {
          const coroutine = args[0];
          const state = coroutine.add(0x8).readS32();
          if (state !== 1) return;

          const displayClass = coroutine.add(0x10).readPointer();
          if (!displayClass || displayClass.isNull()) return;
          const cfAnimator = displayClass.add(0x8).readPointer();
          if (!isLocalAnimator(cfAnimator)) return;

          const threadId = Process.getCurrentThreadId();
          Runtime.activeLocalPauseThreads.set(threadId, cfAnimator);
          this.armedThread = threadId;
          this.cfAnimator = cfAnimator;
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
        }
      },
      onLeave() {
        if (this.armedThread !== null) Runtime.activeLocalPauseThreads.delete(this.armedThread);
      }
    }));

    Runtime.listeners.push(Interceptor.attach(module.base.add(RVA.WaitForSeconds_ctor), {
      onEnter(args) {
        try {
          const threadId = Process.getCurrentThreadId();
          if (!Runtime.activeLocalPauseThreads.has(threadId)) return;

          const originalSecondsBits = pointerText(args[1]);
          args[1] = ptr(0);
          Runtime.stats.shortenedLocalHitStunWait += 1;
          log("info", "local_hit_stun_wait_shortened", {
            animator_owner: pointerText(Runtime.activeLocalPauseThreads.get(threadId)),
            original_seconds_bits: originalSecondsBits,
            replacement_seconds: 0,
            camera_shake_kept: true
          });
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
          log("error", "local_hit_stun_wait_shorten_failed", { error: error.message });
        }
      }
    }));

    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "wait_shorten_enabled", { local_only: true, replacement_seconds: 0 });
    return status();
  } catch (error) {
    Runtime.stats.errorCount += 1;
    Runtime.stats.lastError = error.message;
    detachAll();
    return { ok: false, reason: "enable_failed", error: error.message };
  }
}

function disable() {
  detachAll();
  Runtime.enabled = false;
  log("info", "wait_shorten_disabled", {});
  return status();
}

function status() {
  return { ok: true, feature_id: Runtime.feature_id, enabled: Runtime.enabled, initialized: Runtime.initialized, stats: Runtime.stats };
}

function cleanup() { return disable(); }
function setConfig() { return { ok: true, local_only: true, replacement_seconds: 0, camera_shake_kept: true }; }

rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
