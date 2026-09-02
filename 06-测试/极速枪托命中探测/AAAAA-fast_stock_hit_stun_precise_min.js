// feature_id: fast_stock_hit_stun_precise
// 精确验证：原命中协程完整执行（包括镜头震动），仅在本地协程将两套 Animator 置零后立即复原为 1。
// 依据：GameAssembly 0xB73050 的 state=1 分支先写 speed=0、再调用 PlayKnifeHitStunShake、最后 yield WaitForSeconds。

"use strict";

const Runtime = {
  feature_id: "fast_stock_hit_stun_precise",
  enabled: false,
  initialized: false,
  listener: null,
  stats: {
    restoredLocalHitStun: 0,
    restoredAnimatorWrites: 0,
    errorCount: 0,
    lastError: ""
  }
};

const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  KnifeHitStunCoroutine_MoveNext: 0xB73050,
  CFAnimator_get_characterAnimator: 0xB35310,
  CFAnimator_get_handAnimator: 0xB35330,
  Animator_set_speed: 0xAA8C30
};

let isMyWeapon = null;
let getCharacterAnimator = null;
let getHandAnimator = null;
let setAnimatorSpeed = null;

function log(level, event, data) {
  try {
    send({
      type: "log",
      level: level,
      module: "极速枪托精确验证",
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

function restoreAnimatorSpeed(animator) {
  if (!animator || animator.isNull()) return false;
  setAnimatorSpeed(animator, 1.0, ptr(0));
  Runtime.stats.restoredAnimatorWrites += 1;
  return true;
}

function restoreLocalAnimatorSpeeds(cfAnimator) {
  const characterAnimator = getCharacterAnimator(cfAnimator, ptr(0));
  const handAnimator = getHandAnimator(cfAnimator, ptr(0));
  const characterRestored = restoreAnimatorSpeed(characterAnimator);
  const handRestored = restoreAnimatorSpeed(handAnimator);
  return { characterRestored: characterRestored, handRestored: handRestored };
}

function reset() {
  if (Runtime.listener) {
    try { Runtime.listener.detach(); } catch (_) {}
  }
  try { Interceptor.detachAll(); } catch (_) {}
  Runtime.listener = null;
  isMyWeapon = null;
  getCharacterAnimator = null;
  getHandAnimator = null;
  setAnimatorSpeed = null;
}

function enable() {
  if (Runtime.enabled) return status();
  const module = Process.findModuleByName("GameAssembly.dll");
  if (!module) return { ok: false, reason: "gameassembly_not_loaded" };

  try {
    isMyWeapon = new NativeFunction(module.base.add(RVA.Weapon_get_isMyWeapon), "bool", ["pointer", "pointer"], "mscdecl");
    getCharacterAnimator = new NativeFunction(module.base.add(RVA.CFAnimator_get_characterAnimator), "pointer", ["pointer", "pointer"], "mscdecl");
    getHandAnimator = new NativeFunction(module.base.add(RVA.CFAnimator_get_handAnimator), "pointer", ["pointer", "pointer"], "mscdecl");
    setAnimatorSpeed = new NativeFunction(module.base.add(RVA.Animator_set_speed), "void", ["pointer", "float", "pointer"], "mscdecl");

    Runtime.listener = Interceptor.attach(module.base.add(RVA.KnifeHitStunCoroutine_MoveNext), {
      onEnter(args) {
        this.shouldRestore = false;
        try {
          const coroutine = args[0];
          const state = coroutine.add(0x8).readS32();
          const isPauseStage = state === 1;
          if (!isPauseStage) return;

          const displayClass = coroutine.add(0x10).readPointer();
          if (!displayClass || displayClass.isNull()) return;
          const cfAnimator = displayClass.add(0x8).readPointer();
          if (!isLocalAnimator(cfAnimator)) return;

          this.shouldRestore = true;
          this.cfAnimator = cfAnimator;
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
        }
      },
      onLeave() {
        if (!this.shouldRestore) return;
        try {
          const restored = restoreLocalAnimatorSpeeds(this.cfAnimator);
          Runtime.stats.restoredLocalHitStun += 1;
          log("info", "local_hit_stun_speed_restored", {
            animator_owner: pointerText(this.cfAnimator),
            character_restored: restored.characterRestored,
            hand_restored: restored.handRestored,
            camera_shake_kept: true
          });
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
          log("error", "local_hit_stun_restore_failed", { error: error.message });
        }
      }
    });

    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "precise_restore_enabled", { target: module.base.add(RVA.KnifeHitStunCoroutine_MoveNext).toString(), local_only: true });
    return status();
  } catch (error) {
    Runtime.stats.errorCount += 1;
    Runtime.stats.lastError = error.message;
    reset();
    return { ok: false, reason: "enable_failed", error: error.message };
  }
}

function disable() {
  reset();
  Runtime.enabled = false;
  log("info", "precise_restore_disabled", {});
  return status();
}

function status() {
  return { ok: true, feature_id: Runtime.feature_id, enabled: Runtime.enabled, initialized: Runtime.initialized, stats: Runtime.stats };
}

function cleanup() { return disable(); }
function setConfig() { return { ok: true, local_only: true, camera_shake_kept: true }; }

rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
