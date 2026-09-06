// feature_id: fast_stock_damage_unlock
// 验证：原始 KnifeAttackEvent 完整返回（原伤害已发起）后，调用游戏自己的 OnKnifeAttackExit 提前解除枪托锁。

"use strict";

const Runtime = {
  feature_id: "fast_stock_damage_unlock",
  enabled: false,
  initialized: false,
  hooks: [],
  lastUnlockAt: new Map(),
  calculations: new Map(),
  nextCalculationId: 1,
  stats: { localDamageEvents: 0, unlockedAfterDamage: 0, damageCalculations: 0, targetChecksPassed: 0, targetChecksRejected: 0, damageDispatches: 0, skippedDebounce: 0, errors: 0, lastError: "" }
};

const CONFIG = { MIN_UNLOCK_INTERVAL_MS: 30 };
const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  WPN_Gun_KnifeAttackEvent: 0xB62730,
  WPN_Gun_OnKnifeAttackExit: 0xB62990,
  Weapon_CallKnifeAttack: 0xB6B380,
  Weapon_ShouldDamage: 0xB6D950,
  Weapon_TriggerDmgEventAndClear: 0xB6DB60
};

let isMyWeapon = null;
let originalOnKnifeAttackExit = null;

function log(level, event, data) {
  try { send({ type: "log", level: level, module: "极速枪托伤害后解锁验证", audience: "dev", message: JSON.stringify({ feature_id: Runtime.feature_id, event: event, at_ms: Date.now(), data: data || {} }) }); } catch (_) {}
}

function pointerText(value) { try { return value && !value.isNull() ? value.toString() : "0x0"; } catch (_) { return "unavailable"; } }
function isLocalWeapon(weapon) { try { return Boolean(weapon && !weapon.isNull() && isMyWeapon && isMyWeapon(weapon, ptr(0))); } catch (_) { return false; } }
function knifeAttackAnim(weapon) { try { return weapon.add(0x11C).readS32(); } catch (_) { return null; } }

function shouldUnlock(weapon) {
  const key = pointerText(weapon);
  const now = Date.now();
  const last = Runtime.lastUnlockAt.get(key) || 0;
  if (now - last < CONFIG.MIN_UNLOCK_INTERVAL_MS) {
    Runtime.stats.skippedDebounce += 1;
    return false;
  }
  Runtime.lastUnlockAt.set(key, now);
  return true;
}

function calculationFor(weapon) { return Runtime.calculations.get(pointerText(weapon)) || null; }

function attach(module, rva, callbacks) { Runtime.hooks.push(Interceptor.attach(module.base.add(rva), callbacks)); }

function enable() {
  if (Runtime.enabled) return status();
  const module = Process.findModuleByName("GameAssembly.dll");
  if (!module) return { ok: false, reason: "gameassembly_not_loaded" };
  try {
    isMyWeapon = new NativeFunction(module.base.add(RVA.Weapon_get_isMyWeapon), "bool", ["pointer", "pointer"], "mscdecl");
    originalOnKnifeAttackExit = new NativeFunction(module.base.add(RVA.WPN_Gun_OnKnifeAttackExit), "void", ["pointer", "pointer"], "mscdecl");
    attach(module, RVA.WPN_Gun_KnifeAttackEvent, {
      onEnter(args) {
        this.weapon = args[0];
        this.local = isLocalWeapon(this.weapon);
        this.attackIndex = args[1].toInt32();
      },
      onLeave() {
        if (!this.local) return;
        try {
          Runtime.stats.localDamageEvents += 1;
          if (knifeAttackAnim(this.weapon) !== 1 || !shouldUnlock(this.weapon)) return;
          const before = knifeAttackAnim(this.weapon);
          originalOnKnifeAttackExit(this.weapon, ptr(0));
          const after = knifeAttackAnim(this.weapon);
          Runtime.stats.unlockedAfterDamage += 1;
          log("info", "local_stock_unlocked_after_damage", {
            weapon: pointerText(this.weapon),
            attack_index: this.attackIndex,
            knife_attack_anim_before: before,
            knife_attack_anim_after: after,
            min_unlock_interval_ms: CONFIG.MIN_UNLOCK_INTERVAL_MS,
            damage_flow: "original_KnifeAttackEvent_completed"
          });
        } catch (error) {
          Runtime.stats.errors += 1;
          Runtime.stats.lastError = error.message;
          log("error", "local_stock_unlock_failed", { error: error.message });
        }
      }
    });
    attach(module, RVA.Weapon_CallKnifeAttack, {
      onEnter(args) {
        this.weapon = args[0];
        this.local = isLocalWeapon(this.weapon);
        if (!this.local) return;
        const calculation = { id: Runtime.nextCalculationId++, attackIndex: args[1].toInt32(), startedAt: Date.now(), shouldPass: 0, shouldReject: 0, dispatches: 0 };
        Runtime.calculations.set(pointerText(this.weapon), calculation);
        Runtime.stats.damageCalculations += 1;
        log("info", "stock_damage_calculation_started", { calculation_id: calculation.id, weapon: pointerText(this.weapon), attack_index: calculation.attackIndex });
      },
      onLeave() {
        if (!this.local) return;
        const calculation = calculationFor(this.weapon);
        if (!calculation) return;
        log("info", "stock_damage_calculation_finished", { calculation_id: calculation.id, attack_index: calculation.attackIndex, elapsed_ms: Date.now() - calculation.startedAt, should_damage_pass: calculation.shouldPass, should_damage_reject: calculation.shouldReject, damage_dispatches: calculation.dispatches });
        Runtime.calculations.delete(pointerText(this.weapon));
      }
    });
    attach(module, RVA.Weapon_ShouldDamage, {
      onEnter(args) { this.weapon = args[0]; this.local = isLocalWeapon(this.weapon); },
      onLeave(retval) {
        if (!this.local) return;
        const calculation = calculationFor(this.weapon);
        if (!calculation) return;
        if (retval.toInt32() !== 0) { calculation.shouldPass += 1; Runtime.stats.targetChecksPassed += 1; }
        else { calculation.shouldReject += 1; Runtime.stats.targetChecksRejected += 1; }
      }
    });
    attach(module, RVA.Weapon_TriggerDmgEventAndClear, {
      onEnter(args) {
        this.weapon = args[0];
        this.local = isLocalWeapon(this.weapon);
        if (!this.local) return;
        const calculation = calculationFor(this.weapon);
        if (calculation) { calculation.dispatches += 1; Runtime.stats.damageDispatches += 1; }
      }
    });
    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "damage_unlock_enabled", { local_only: true, unlock_point: "after_original_KnifeAttackEvent" });
    return status();
  } catch (error) {
    Runtime.stats.errors += 1;
    Runtime.stats.lastError = error.message;
    disable();
    return { ok: false, reason: "enable_failed", error: error.message };
  }
}

function disable() {
  Runtime.hooks.forEach(function (hook) { try { hook.detach(); } catch (_) {} });
  Runtime.hooks = [];
  Runtime.lastUnlockAt.clear();
  Runtime.calculations.clear();
  Runtime.enabled = false;
  isMyWeapon = null;
  originalOnKnifeAttackExit = null;
  log("info", "damage_unlock_disabled", {});
  return status();
}

function status() { return { ok: true, feature_id: Runtime.feature_id, enabled: Runtime.enabled, initialized: Runtime.initialized, stats: Runtime.stats }; }
function cleanup() { return disable(); }
function setConfig() { return { ok: true, local_only: true, min_unlock_interval_ms: CONFIG.MIN_UNLOCK_INTERVAL_MS }; }
rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
