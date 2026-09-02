// feature_id: fast_stock_hit_stun_bypass
// 临时验证：仅跳过本地枪托命中后的动画硬直，其他角色保持游戏原逻辑。
// 已知边界：该函数也会触发本地命中镜头震动；本验证版本会一并跳过，正式方案再拆分保留。

"use strict";

const Runtime = {
  feature_id: "fast_stock_hit_stun_bypass",
  enabled: false,
  initialized: false,
  target: null,
  replacement: null,
  stats: {
    bypassedLocalHitStun: 0,
    passedThroughOtherHitStun: 0,
    errorCount: 0,
    lastError: ""
  }
};

const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  CFAnimator_PlayKnifeHitStunAnim: 0xB34CC0
};

let isMyWeapon = null;
let originalPlayKnifeHitStun = null;

function log(level, event, data) {
  try {
    send({
      type: "log",
      level: level,
      module: "极速枪托验证",
      audience: "dev",
      message: JSON.stringify({ feature_id: Runtime.feature_id, event: event, at_ms: Date.now(), data: data || {} })
    });
  } catch (_) {}
}

function pointerText(value) {
  try { return value && !value.isNull() ? value.toString() : "0x0"; } catch (_) { return "unavailable"; }
}

function isLocalWeapon(self) {
  try {
    return Boolean(self && !self.isNull() && isMyWeapon && isMyWeapon(self, ptr(0)));
  } catch (_) {
    return false;
  }
}

function resetReplacement() {
  if (Runtime.target) {
    try {
      Interceptor.revert(Runtime.target);
      Interceptor.flush();
    } catch (_) {}
  }
  Runtime.target = null;
  Runtime.replacement = null;
  originalPlayKnifeHitStun = null;
  isMyWeapon = null;
}

function enable() {
  if (Runtime.enabled) return status();
  const module = Process.findModuleByName("GameAssembly.dll");
  if (!module) return { ok: false, reason: "gameassembly_not_loaded" };

  try {
    isMyWeapon = new NativeFunction(
      module.base.add(RVA.Weapon_get_isMyWeapon),
      "bool",
      ["pointer", "pointer"],
      "mscdecl"
    );
    Runtime.target = module.base.add(RVA.CFAnimator_PlayKnifeHitStunAnim);
    originalPlayKnifeHitStun = new NativeFunction(
      Runtime.target,
      "void",
      ["pointer", "bool", "pointer"],
      "mscdecl"
    );

    Runtime.replacement = new NativeCallback(function (self, isBigshot, method) {
      if (isLocalWeapon(self)) {
        Runtime.stats.bypassedLocalHitStun += 1;
        log("info", "local_hit_stun_bypassed", { self: pointerText(self), is_bigshot: Boolean(isBigshot) });
        return;
      }

      Runtime.stats.passedThroughOtherHitStun += 1;
      originalPlayKnifeHitStun(self, isBigshot, method);
    }, "void", ["pointer", "bool", "pointer"], "mscdecl");

    Interceptor.replace(Runtime.target, Runtime.replacement);
    Interceptor.flush();
    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "bypass_enabled", { target: Runtime.target.toString(), local_only: true });
    return status();
  } catch (error) {
    Runtime.stats.errorCount += 1;
    Runtime.stats.lastError = error.message;
    resetReplacement();
    return { ok: false, reason: "enable_failed", error: error.message };
  }
}

function disable() {
  resetReplacement();
  Runtime.enabled = false;
  log("info", "bypass_disabled", {});
  return status();
}

function status() {
  return {
    ok: true,
    feature_id: Runtime.feature_id,
    enabled: Runtime.enabled,
    initialized: Runtime.initialized,
    target: Runtime.target ? Runtime.target.toString() : null,
    stats: Runtime.stats
  };
}

function cleanup() {
  return disable();
}

function setConfig() {
  return { ok: true, local_only: true, note: "Temporary validation script has no configurable values." };
}

rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
