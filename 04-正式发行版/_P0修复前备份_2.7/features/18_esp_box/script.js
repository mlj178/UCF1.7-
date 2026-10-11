// ESP box is implemented by the existing Universal-ImGui-Hook.dll pipeline.
// Source assets kept intact:
// - plugins/universal_hook/Universal-ImGui-Hook.dll
// - plugins/universal_hook/universal_hook.json
// - core/universal_hook_manager.py
// This plugin script is only the standard RPC adapter for plugin discovery.
var __espBoxState = false;
var __espBoxConfig = {};

function sendStatus(feature, enabled) {
    try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
}

rpc.exports = {
  enable: function(config) {
    __espBoxConfig = config || __espBoxConfig;
    __espBoxState = true;
    sendStatus('esp_box', true);
    return { ok: true, enabled: true, backend: 'Universal-ImGui-Hook.dll' };
  },
  disable: function() {
    __espBoxState = false;
    sendStatus('esp_box', false);
    return { ok: true, enabled: false, backend: 'Universal-ImGui-Hook.dll' };
  },
  setConfig: function(config) {
    __espBoxConfig = config || {};
    return { ok: true, config: __espBoxConfig, backend: 'Universal-ImGui-Hook.dll' };
  },
  status: function() {
    return { enabled: __espBoxState, config: __espBoxConfig, stats: { backend: 'Universal-ImGui-Hook.dll' } };
  },
  cleanup: function(payload) {
    __espBoxState = false;
    return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup', backend: 'Universal-ImGui-Hook.dll' };
  }
};

