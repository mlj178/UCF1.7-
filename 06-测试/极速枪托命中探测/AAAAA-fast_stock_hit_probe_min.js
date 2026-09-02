// feature_id: fast_stock_hit_probe
// 目标：只读记录枪托开始、伤害判定、受伤事件、命中硬直和动画退出的时序。
// 禁止事项：本脚本不写游戏内存、不替换函数、不修改 Animator 速度。

"use strict";

const Runtime = {
  feature_id: "fast_stock_hit_probe",
  enabled: false,
  initialized: false,
  generation: 0,
  hooks: [],
  sessions: [],
  stats: {
    hookHits: 0,
    specialStarts: 0,
    knifeEvents: 0,
    damageCalls: 0,
    hurtEvents: 0,
    stunStarts: 0,
    stunCoroutineSteps: 0,
    animationExits: 0,
    errorCount: 0,
    lastError: "",
    lastResetReason: ""
  }
};

const RVA = {
  Weapon_get_isMyWeapon: 0xB6E1D0,
  WPN_Gun_OnSpecialBtnDown: 0xB629F0,
  WPN_Gun_KnifeAttackEvent: 0xB62730,
  Weapon_CallKnifeAttack: 0xB6B380,
  Entity_OnEntityHurt: 0xB3F470,
  CFAnimator_PlayKnifeHitStunAnim: 0xB34CC0,
  KnifeHitStunCoroutine_MoveNext: 0xB73050,
  WPN_Gun_OnAnimationExit: 0xB62800
};

let isMyWeapon = null;

function nowMs() {
  return Date.now();
}

function log(level, event, data) {
  const payload = {
    feature_id: Runtime.feature_id,
    generation: Runtime.generation,
    at_ms: nowMs(),
    event: event,
    data: data || {}
  };
  try {
    send({ type: "log", level: level, module: "极速枪托探测", message: JSON.stringify(payload), audience: "dev" });
  } catch (_) {
    console.log("[fast_stock_hit_probe] " + JSON.stringify(payload));
  }
}

function reportError(stage, error) {
  Runtime.stats.errorCount += 1;
  Runtime.stats.lastError = stage + ": " + error.message;
  log("warn", "probe_error", { stage: stage, error: error.message });
}

function pointerText(value) {
  try {
    return value && !value.isNull() ? value.toString() : "0x0";
  } catch (_) {
    return "unavailable";
  }
}

function isLocalWeapon(weapon) {
  try {
    return Boolean(weapon && !weapon.isNull() && isMyWeapon && isMyWeapon(weapon, ptr(0)));
  } catch (_) {
    return false;
  }
}

function pruneSessions() {
  const cutoff = nowMs() - 5000;
  Runtime.sessions = Runtime.sessions.filter(function (session) {
    return session.startedAt >= cutoff;
  });
}

function findSession(weapon) {
  for (let index = Runtime.sessions.length - 1; index >= 0; index -= 1) {
    const session = Runtime.sessions[index];
    if (session.weapon.equals(weapon)) return session;
  }
  return null;
}

function recordSessionEvent(weapon, event, extra) {
  const session = findSession(weapon);
  const at = nowMs();
  const payload = Object.assign({ weapon: pointerText(weapon) }, extra || {});
  if (session) {
    payload.session_id = session.id;
    payload.since_special_ms = at - session.startedAt;
    session.events.push({ name: event, at: at, extra: extra || {} });
  }
  log("info", event, payload);
}

function resetRuntime(reason) {
  Runtime.generation += 1;
  Runtime.sessions = [];
  Runtime.stats.lastResetReason = reason || "reset";
}

function detachHooks() {
  Runtime.hooks.forEach(function (hook) {
    try { hook.detach(); } catch (_) {}
  });
  Runtime.hooks = [];
}

function attachProbe(address, callbacks, label) {
  try {
    Runtime.hooks.push(Interceptor.attach(address, callbacks));
    log("info", "hook_installed", { label: label, address: address.toString() });
  } catch (error) {
    reportError("attach " + label, error);
  }
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

    attachProbe(module.base.add(RVA.WPN_Gun_OnSpecialBtnDown), {
      onEnter(args) {
        try {
          const weapon = args[0];
          if (!isLocalWeapon(weapon)) return;
          pruneSessions();
          const session = { id: Runtime.stats.specialStarts + 1, weapon: weapon, startedAt: nowMs(), events: [] };
          Runtime.sessions.push(session);
          Runtime.stats.hookHits += 1;
          Runtime.stats.specialStarts += 1;
          recordSessionEvent(weapon, "special_button_down");
        } catch (error) { reportError("special_button_down", error); }
      }
    }, "WPN_Gun.OnSpecialBtnDown");

    attachProbe(module.base.add(RVA.WPN_Gun_KnifeAttackEvent), {
      onEnter(args) {
        try {
          if (!isLocalWeapon(args[0])) return;
          Runtime.stats.hookHits += 1;
          Runtime.stats.knifeEvents += 1;
          recordSessionEvent(args[0], "knife_attack_event", { attack_index: args[1].toInt32() });
        } catch (error) { reportError("knife_attack_event", error); }
      }
    }, "WPN_Gun.KnifeAttackEvent");

    attachProbe(module.base.add(RVA.Weapon_CallKnifeAttack), {
      onEnter(args) {
        try {
          if (!isLocalWeapon(args[0])) return;
          Runtime.stats.hookHits += 1;
          Runtime.stats.damageCalls += 1;
          recordSessionEvent(args[0], "call_knife_attack", { attack_index: args[1].toInt32() });
        } catch (error) { reportError("call_knife_attack", error); }
      }
    }, "Weapon.CallKnifeAttack");

    attachProbe(module.base.add(RVA.Entity_OnEntityHurt), {
      onEnter(args) {
        try {
          Runtime.stats.hookHits += 1;
          Runtime.stats.hurtEvents += 1;
          log("info", "entity_hurt", {
            victim_this: pointerText(args[0]),
            attacker_from_damage_event: pointerText(args[1]),
            victim_from_damage_event: pointerText(args[2]),
            recent_local_stock_sessions: Runtime.sessions.length
          });
        } catch (error) { reportError("entity_hurt", error); }
      }
    }, "Entity.OnEntityHurt");

    attachProbe(module.base.add(RVA.CFAnimator_PlayKnifeHitStunAnim), {
      onEnter(args) {
        try {
          Runtime.stats.hookHits += 1;
          Runtime.stats.stunStarts += 1;
          log("info", "knife_hit_stun_start", {
            animator_owner: pointerText(args[0]),
            is_bigshot: args[1].toInt32() !== 0,
            recent_local_stock_sessions: Runtime.sessions.length
          });
        } catch (error) { reportError("knife_hit_stun_start", error); }
      }
    }, "CFAnimator.PlayKnifeHitStunAnim");

    attachProbe(module.base.add(RVA.KnifeHitStunCoroutine_MoveNext), {
      onEnter(args) {
        try {
          Runtime.stats.hookHits += 1;
          Runtime.stats.stunCoroutineSteps += 1;
          log("info", "knife_hit_stun_coroutine_step", { coroutine: pointerText(args[0]) });
        } catch (error) { reportError("knife_hit_stun_coroutine_step", error); }
      }
    }, "KnifeHitStunCoroutine.MoveNext");

    attachProbe(module.base.add(RVA.WPN_Gun_OnAnimationExit), {
      onEnter(args) {
        try {
          if (!isLocalWeapon(args[0])) return;
          Runtime.stats.hookHits += 1;
          Runtime.stats.animationExits += 1;
          recordSessionEvent(args[0], "weapon_animation_exit", {
            anim_name: pointerText(args[1]),
            anim_tag: pointerText(args[2])
          });
        } catch (error) { reportError("weapon_animation_exit", error); }
      }
    }, "WPN_Gun.OnAnimationExit");

    Runtime.enabled = true;
    Runtime.initialized = true;
    log("info", "probe_enabled", { hooks: Runtime.hooks.length, read_only: true });
    return status();
  } catch (error) {
    detachHooks();
    isMyWeapon = null;
    reportError("enable", error);
    return { ok: false, reason: "enable_failed", error: error.message };
  }
}

function disable() {
  detachHooks();
  Runtime.enabled = false;
  isMyWeapon = null;
  resetRuntime("disable");
  log("info", "probe_disabled", { read_only: true });
  return status();
}

function status() {
  return {
    ok: true,
    feature_id: Runtime.feature_id,
    enabled: Runtime.enabled,
    initialized: Runtime.initialized,
    generation: Runtime.generation,
    active_sessions: Runtime.sessions.length,
    hook_count: Runtime.hooks.length,
    stats: Runtime.stats
  };
}

function cleanup() {
  return disable();
}

function setConfig() {
  return { ok: true, read_only: true, message: "This probe has no writable configuration." };
}

rpc.exports = { enable, disable, status, cleanup, setConfig };
rpc.exports.setconfig = setConfig;
