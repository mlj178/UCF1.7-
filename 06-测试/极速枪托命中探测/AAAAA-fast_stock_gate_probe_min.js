// feature_id: fast_stock_gate_probe
// 只读：定位“枪托开始 → 伤害动画事件 → 伤害 → 动画退出 → knifeAttackAnim 解锁”的真实时序。

"use strict";

const Runtime = {
  feature_id: "fast_stock_gate_probe",
  enabled: false,
  initialized: false,
  hooks: [],
  stats: { input: 0, accepted: 0, damageEvents: 0, damageCalls: 0, hurts: 0, animationEnds: 0, animationExits: 0, unlocks: 0, errors: 0 }
};

const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  WPN_Gun_OnSpecialBtnDown: 0xB629F0,
  WPN_Gun_KnifeAttackEvent: 0xB62730,
  Weapon_CallKnifeAttack: 0xB6B380,
  Entity_OnEntityHurt: 0xB3F470,
  WPN_Gun_OnAnimationEnd: 0xB627A0,
  WPN_Gun_OnAnimationExit: 0xB62800,
  WPN_Gun_OnKnifeAttackExit: 0xB62990
};

let isMyWeapon = null;

function log(level, event, data) {
  try { send({ type: "log", level: level, module: "极速枪托解锁探测", audience: "dev", message: JSON.stringify({ feature_id: Runtime.feature_id, event: event, at_ms: Date.now(), data: data || {} }) }); } catch (_) {}
}

function pointerText(value) { try { return value && !value.isNull() ? value.toString() : "0x0"; } catch (_) { return "unavailable"; } }
function readI32(object, offset) { try { return object && !object.isNull() ? object.add(offset).readS32() : null; } catch (_) { return null; } }
function managedString(value) {
  try { const length = value.add(0x8).readS32(); return length >= 0 && length <= 256 ? value.add(0xC).readUtf16String(length) : ""; } catch (_) { return ""; }
}
function isLocalWeapon(weapon) { try { return Boolean(weapon && !weapon.isNull() && isMyWeapon && isMyWeapon(weapon, ptr(0))); } catch (_) { return false; } }
function snapshot(weapon) { return { weapon: pointerText(weapon), knife_attack_count: readI32(weapon, 0x118), knife_attack_anim: readI32(weapon, 0x11C), fire_anim: readI32(weapon, 0x10C) }; }
function recordError(where, error) { Runtime.stats.errors += 1; log("error", "probe_error", { where: where, error: error.message }); }

function attach(address, callbacks, label) {
  Runtime.hooks.push(Interceptor.attach(address, callbacks));
  log("info", "hook_installed", { label: label, address: address.toString() });
}

function enable() {
  if (Runtime.enabled) return status();
  const module = Process.findModuleByName("GameAssembly.dll");
  if (!module) return { ok: false, reason: "gameassembly_not_loaded" };
  try {
    isMyWeapon = new NativeFunction(module.base.add(RVA.Weapon_get_isMyWeapon), "bool", ["pointer", "pointer"], "mscdecl");
    attach(module.base.add(RVA.WPN_Gun_OnSpecialBtnDown), {
      onEnter(args) {
        try { this.weapon = args[0]; this.local = isLocalWeapon(this.weapon); if (!this.local) return; Runtime.stats.input += 1; log("info", "stock_input_gate", Object.assign({ phase: "before" }, snapshot(this.weapon))); } catch (error) { recordError("input enter", error); }
      },
      onLeave() {
        try { if (!this.local) return; const data = snapshot(this.weapon); if (data.knife_attack_anim === 1) Runtime.stats.accepted += 1; log("info", "stock_input_gate", Object.assign({ phase: "after", accepted: data.knife_attack_anim === 1 }, data)); } catch (error) { recordError("input leave", error); }
      }
    }, "WPN_Gun.OnSpecialBtnDown");
    attach(module.base.add(RVA.WPN_Gun_KnifeAttackEvent), { onEnter(args) { try { if (!isLocalWeapon(args[0])) return; Runtime.stats.damageEvents += 1; log("info", "stock_damage_animation_event", Object.assign({ attack_index: args[1].toInt32() }, snapshot(args[0]))); } catch (error) { recordError("damage event", error); } } }, "WPN_Gun.KnifeAttackEvent");
    attach(module.base.add(RVA.Weapon_CallKnifeAttack), { onEnter(args) { try { if (!isLocalWeapon(args[0])) return; Runtime.stats.damageCalls += 1; log("info", "stock_damage_call", Object.assign({ attack_index: args[1].toInt32() }, snapshot(args[0]))); } catch (error) { recordError("damage call", error); } } }, "Weapon.CallKnifeAttack");
    attach(module.base.add(RVA.Entity_OnEntityHurt), { onEnter(args) { try { Runtime.stats.hurts += 1; log("info", "stock_damage_received", { victim: pointerText(args[0]), damage_event: pointerText(args[1]) }); } catch (error) { recordError("hurt", error); } } }, "Entity.OnEntityHurt");
    attach(module.base.add(RVA.WPN_Gun_OnAnimationEnd), { onEnter(args) { try { if (!isLocalWeapon(args[0])) return; Runtime.stats.animationEnds += 1; log("info", "stock_animation_end", Object.assign({ anim_name: managedString(args[1]), anim_tag: managedString(args[2]) }, snapshot(args[0]))); } catch (error) { recordError("animation end", error); } } }, "WPN_Gun.OnAnimationEnd");
    attach(module.base.add(RVA.WPN_Gun_OnAnimationExit), { onEnter(args) { try { if (!isLocalWeapon(args[0])) return; Runtime.stats.animationExits += 1; log("info", "stock_animation_exit", Object.assign({ anim_name: managedString(args[1]), anim_tag: managedString(args[2]) }, snapshot(args[0]))); } catch (error) { recordError("animation exit", error); } } }, "WPN_Gun.OnAnimationExit");
    attach(module.base.add(RVA.WPN_Gun_OnKnifeAttackExit), {
      onEnter(args) { try { this.weapon = args[0]; this.local = isLocalWeapon(this.weapon); if (this.local) log("info", "stock_gate_unlocked", Object.assign({ phase: "before" }, snapshot(this.weapon))); } catch (error) { recordError("unlock enter", error); } },
      onLeave() { try { if (!this.local) return; Runtime.stats.unlocks += 1; log("info", "stock_gate_unlocked", Object.assign({ phase: "after" }, snapshot(this.weapon))); } catch (error) { recordError("unlock leave", error); } }
    }, "WPN_Gun.OnKnifeAttackExit");
    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "gate_probe_enabled", { hooks: Runtime.hooks.length, read_only: true });
    return status();
  } catch (error) {
    disable();
    return { ok: false, reason: "enable_failed", error: error.message };
  }
}

function disable() {
  for (const hook of Runtime.hooks) { try { hook.detach(); } catch (_) {} }
  Runtime.hooks = [];
  Runtime.enabled = false;
  isMyWeapon = null;
  log("info", "gate_probe_disabled", {});
  return status();
}

function status() { return { ok: true, feature_id: Runtime.feature_id, enabled: Runtime.enabled, initialized: Runtime.initialized, stats: Runtime.stats }; }
function cleanup() { return disable(); }
function setConfig() { return { ok: true, read_only: true }; }
rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
