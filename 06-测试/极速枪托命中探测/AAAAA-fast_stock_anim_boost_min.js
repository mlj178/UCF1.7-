// feature_id: fast_stock_anim_boost
// 验证目标：只加速本地枪托动画；伤害仍由原有 KnifeAttackEvent / CallKnifeAttack 动画事件产生。
// 命中硬直会把 Animator.speed 写为 0；本脚本在该写入完成后把它恢复为枪托倍率，而非 1。

"use strict";

const Runtime = {
  feature_id: "fast_stock_anim_boost",
  enabled: false,
  initialized: false,
  listeners: [],
  activeStockWeapons: new Map(),
  stats: {
    stockStarts: 0,
    hitStunBoostReapplied: 0,
    stockEnds: 0,
    animatorWrites: 0,
    errorCount: 0,
    lastError: ""
  }
};

const CONFIG = { BOOST_SPEED: 10.0 };
const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  CFAnimator_get_isSelecting: 0xB353D0,
  CFAnimator_get_characterAnimator: 0xB35310,
  CFAnimator_get_handAnimator: 0xB35330,
  Animator_set_speed: 0xAA8C30,
  WPN_Gun_OnSpecialBtnDown: 0xB629F0,
  WPN_Gun_OnAnimationExit: 0xB62800,
  KnifeHitStunCoroutine_MoveNext: 0xB73050
};

let isMyWeapon = null;
let getIsSelecting = null;
let getCharacterAnimator = null;
let getHandAnimator = null;
let setAnimatorSpeed = null;

function log(level, event, data) {
  try {
    send({
      type: "log",
      level: level,
      module: "极速枪托动画验证",
      audience: "dev",
      message: JSON.stringify({ feature_id: Runtime.feature_id, event: event, at_ms: Date.now(), data: data || {} })
    });
  } catch (_) {}
}

function pointerText(value) {
  try { return value && !value.isNull() ? value.toString() : "0x0"; } catch (_) { return "unavailable"; }
}

function managedString(value) {
  try {
    if (!value || value.isNull()) return "";
    const length = value.add(0x8).readS32();
    return length >= 0 && length <= 256 ? value.add(0xC).readUtf16String(length) : "";
  } catch (_) { return ""; }
}

function isLocalWeapon(weapon) {
  try { return Boolean(weapon && !weapon.isNull() && isMyWeapon && isMyWeapon(weapon, ptr(0))); } catch (_) { return false; }
}

function setSpeedIfValid(animator, speed) {
  if (!animator || animator.isNull()) return false;
  setAnimatorSpeed(animator, speed, ptr(0));
  Runtime.stats.animatorWrites += 1;
  return true;
}

function applyStockSpeed(weapon, speed) {
  const characterAnimator = getCharacterAnimator(weapon, ptr(0));
  const handAnimator = getHandAnimator(weapon, ptr(0));
  return {
    character: setSpeedIfValid(characterAnimator, speed),
    hand: setSpeedIfValid(handAnimator, speed)
  };
}

function isActiveStockWeapon(weapon) {
  return Runtime.activeStockWeapons.has(pointerText(weapon));
}

function detachAll() {
  for (const weapon of Runtime.activeStockWeapons.values()) {
    try { applyStockSpeed(weapon, 1.0); } catch (_) {}
  }
  Runtime.activeStockWeapons.clear();
  for (const listener of Runtime.listeners) {
    try { listener.detach(); } catch (_) {}
  }
  try { Interceptor.detachAll(); } catch (_) {}
  Runtime.listeners = [];
  isMyWeapon = null;
  getIsSelecting = null;
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
    getIsSelecting = new NativeFunction(module.base.add(RVA.CFAnimator_get_isSelecting), "bool", ["pointer", "pointer"], "mscdecl");
    getCharacterAnimator = new NativeFunction(module.base.add(RVA.CFAnimator_get_characterAnimator), "pointer", ["pointer", "pointer"], "mscdecl");
    getHandAnimator = new NativeFunction(module.base.add(RVA.CFAnimator_get_handAnimator), "pointer", ["pointer", "pointer"], "mscdecl");
    setAnimatorSpeed = new NativeFunction(module.base.add(RVA.Animator_set_speed), "void", ["pointer", "float", "pointer"], "mscdecl");

    Runtime.listeners.push(Interceptor.attach(module.base.add(RVA.WPN_Gun_OnSpecialBtnDown), {
      onEnter(args) {
        this.weapon = args[0];
        this.shouldBoost = false;
        try {
          if (!isLocalWeapon(this.weapon)) return;
          if (this.weapon.add(0x118).readS32() <= 0) return;
          if (this.weapon.add(0x11C).readS32() !== 0) return;
          if (getIsSelecting(this.weapon, ptr(0))) return;
          this.shouldBoost = true;
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
        }
      },
      onLeave() {
        if (!this.shouldBoost) return;
        try {
          const applied = applyStockSpeed(this.weapon, CONFIG.BOOST_SPEED);
          Runtime.activeStockWeapons.set(pointerText(this.weapon), this.weapon);
          Runtime.stats.stockStarts += 1;
          log("info", "stock_anim_boost_applied", { weapon: pointerText(this.weapon), speed: CONFIG.BOOST_SPEED, character: applied.character, hand: applied.hand });
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
          log("error", "stock_anim_boost_failed", { error: error.message });
        }
      }
    }));

    Runtime.listeners.push(Interceptor.attach(module.base.add(RVA.KnifeHitStunCoroutine_MoveNext), {
      onEnter(args) {
        this.weapon = null;
        try {
          const coroutine = args[0];
          if (coroutine.add(0x8).readS32() !== 1) return;
          const displayClass = coroutine.add(0x10).readPointer();
          if (!displayClass || displayClass.isNull()) return;
          const weapon = displayClass.add(0x8).readPointer();
          if (isLocalWeapon(weapon) && isActiveStockWeapon(weapon)) this.weapon = weapon;
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
        }
      },
      onLeave() {
        if (!this.weapon) return;
        try {
          const applied = applyStockSpeed(this.weapon, CONFIG.BOOST_SPEED);
          Runtime.stats.hitStunBoostReapplied += 1;
          log("info", "stock_hit_stun_boost_reapplied", { weapon: pointerText(this.weapon), speed: CONFIG.BOOST_SPEED, character: applied.character, hand: applied.hand });
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
        }
      }
    }));

    Runtime.listeners.push(Interceptor.attach(module.base.add(RVA.WPN_Gun_OnAnimationExit), {
      onEnter(args) {
        this.weapon = args[0];
        this.shouldRestore = isLocalWeapon(this.weapon) && isActiveStockWeapon(this.weapon) && managedString(args[1]) === "knife-attack";
      },
      onLeave() {
        if (!this.shouldRestore) return;
        try {
          const applied = applyStockSpeed(this.weapon, 1.0);
          Runtime.activeStockWeapons.delete(pointerText(this.weapon));
          Runtime.stats.stockEnds += 1;
          log("info", "stock_anim_speed_restored", { weapon: pointerText(this.weapon), character: applied.character, hand: applied.hand });
        } catch (error) {
          Runtime.stats.errorCount += 1;
          Runtime.stats.lastError = error.message;
        }
      }
    }));

    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "stock_anim_boost_enabled", { local_only: true, speed: CONFIG.BOOST_SPEED, damage_flow: "original_animation_event" });
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
  log("info", "stock_anim_boost_disabled", {});
  return status();
}

function status() { return { ok: true, feature_id: Runtime.feature_id, enabled: Runtime.enabled, initialized: Runtime.initialized, stats: Runtime.stats }; }
function cleanup() { return disable(); }
function setConfig() { return { ok: true, local_only: true, speed: CONFIG.BOOST_SPEED, damage_flow: "original_animation_event" }; }

rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
