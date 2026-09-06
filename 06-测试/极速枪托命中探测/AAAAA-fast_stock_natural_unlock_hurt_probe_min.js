// feature_id: fast_stock_natural_unlock_hurt_probe
// 仅在原始伤害动画事件完成后解锁；记录随后实际进入 Entity.OnEntityHurt 的受击回调。

"use strict";

const Runtime = {
  feature_id: "fast_stock_natural_unlock_hurt_probe",
  enabled: false,
  hooks: [],
  lastNaturalDamage: null,
  stats: { naturalDamageEvents: 0, unlockedAfterNaturalDamage: 0, correlatedHurts: 0, uncorrelatedHurts: 0, errors: 0, lastError: "" }
};

const CONFIG = { MAX_HURT_CORRELATION_MS: 500, MIN_UNLOCK_INTERVAL_MS: 30 };
const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  WPN_Gun_KnifeAttackEvent: 0xB62730,
  WPN_Gun_OnKnifeAttackExit: 0xB62990,
  Entity_OnEntityHurt: 0xB3F470
};

let isMyWeapon = null;
let originalOnKnifeAttackExit = null;
let lastUnlockAt = new Map();

function log(level, event, data) {
  try { send({ type: "log", level: level, module: "极速枪托自然伤害受击探测", audience: "dev", message: JSON.stringify({ feature_id: Runtime.feature_id, event: event, at_ms: Date.now(), data: data || {} }) }); } catch (_) {}
}
function pointerText(value) { try { return value && !value.isNull() ? value.toString() : "0x0"; } catch (_) { return "unavailable"; } }
function isLocalWeapon(weapon) { try { return Boolean(weapon && !weapon.isNull() && isMyWeapon && isMyWeapon(weapon, ptr(0))); } catch (_) { return false; } }
function knifeAttackAnim(weapon) { try { return weapon.add(0x11C).readS32(); } catch (_) { return null; } }
function canUnlock(weapon) {
  const key = pointerText(weapon); const now = Date.now(); const previous = lastUnlockAt.get(key) || 0;
  if (now - previous < CONFIG.MIN_UNLOCK_INTERVAL_MS) return false;
  lastUnlockAt.set(key, now); return true;
}
function attach(module, rva, callbacks) { Runtime.hooks.push(Interceptor.attach(module.base.add(rva), callbacks)); }

function enable() {
  if (Runtime.enabled) return status();
  const module = Process.findModuleByName("GameAssembly.dll");
  if (!module) return { ok: false, reason: "gameassembly_not_loaded" };
  try {
    isMyWeapon = new NativeFunction(module.base.add(RVA.Weapon_get_isMyWeapon), "bool", ["pointer", "pointer"], "mscdecl");
    originalOnKnifeAttackExit = new NativeFunction(module.base.add(RVA.WPN_Gun_OnKnifeAttackExit), "void", ["pointer", "pointer"], "mscdecl");
    attach(module, RVA.WPN_Gun_KnifeAttackEvent, {
      onEnter(args) { this.weapon = args[0]; this.local = isLocalWeapon(this.weapon); this.attackIndex = args[1].toInt32(); },
      onLeave() {
        if (!this.local) return;
        try {
          const at = Date.now();
          Runtime.stats.naturalDamageEvents += 1;
          Runtime.lastNaturalDamage = { at: at, weapon: pointerText(this.weapon), attackIndex: this.attackIndex };
          log("info", "natural_stock_damage_event", Runtime.lastNaturalDamage);
          if (knifeAttackAnim(this.weapon) === 1 && canUnlock(this.weapon)) {
            originalOnKnifeAttackExit(this.weapon, ptr(0));
            Runtime.stats.unlockedAfterNaturalDamage += 1;
            log("info", "natural_stock_unlocked", { weapon: pointerText(this.weapon), attack_index: this.attackIndex, knife_attack_anim_after: knifeAttackAnim(this.weapon) });
          }
        } catch (error) { Runtime.stats.errors += 1; Runtime.stats.lastError = error.message; log("error", "natural_unlock_failed", { error: error.message }); }
      }
    });
    attach(module, RVA.Entity_OnEntityHurt, {
      onEnter(args) {
        const now = Date.now(); const natural = Runtime.lastNaturalDamage;
        const delta = natural ? now - natural.at : null;
        const correlated = delta !== null && delta >= 0 && delta <= CONFIG.MAX_HURT_CORRELATION_MS;
        if (correlated) Runtime.stats.correlatedHurts += 1; else Runtime.stats.uncorrelatedHurts += 1;
        log(correlated ? "info" : "debug", correlated ? "correlated_entity_hurt" : "uncorrelated_entity_hurt", { victim: pointerText(args[0]), damage_event: pointerText(args[1]), since_natural_damage_ms: delta, natural_event: natural });
      }
    });
    Runtime.enabled = true;
    log("info", "natural_unlock_hurt_probe_enabled", { local_only_unlock: true, max_hurt_correlation_ms: CONFIG.MAX_HURT_CORRELATION_MS });
    return status();
  } catch (error) { Runtime.stats.errors += 1; Runtime.stats.lastError = error.message; disable(); return { ok: false, reason: "enable_failed", error: error.message }; }
}

function disable() {
  Runtime.hooks.forEach(function (hook) { try { hook.detach(); } catch (_) {} }); Runtime.hooks = [];
  lastUnlockAt.clear(); Runtime.lastNaturalDamage = null; Runtime.enabled = false; isMyWeapon = null; originalOnKnifeAttackExit = null;
  log("info", "natural_unlock_hurt_probe_disabled", {}); return status();
}
function status() { return { ok: true, feature_id: Runtime.feature_id, enabled: Runtime.enabled, stats: Runtime.stats }; }
function cleanup() { return disable(); }
function setConfig() { return { ok: true, local_only_unlock: true, max_hurt_correlation_ms: CONFIG.MAX_HURT_CORRELATION_MS }; }
rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
