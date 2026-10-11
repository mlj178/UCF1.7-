var templateState = {
  enabled: false,
  config: {}
};

function sendStatus(enabled) {
  try {
    send({ type: "status", feature: "template_feature", enabled: enabled });
  } catch (_) {}
}

function sendPluginEvent(eventName, payload, audience) {
  try {
    send({
      type: "plugin_event",
      feature: "template_feature",
      event: eventName,
      payload: payload || {},
      audience: audience || "dev"
    });
  } catch (_) {}
}

rpc.exports = {
  enable: function(config) {
    templateState.enabled = true;
    templateState.config = config || templateState.config;
    sendStatus(true);
    sendPluginEvent("enabled", { config: templateState.config }, "dev");
    return { ok: true, enabled: true, config: templateState.config };
  },

  disable: function() {
    templateState.enabled = false;
    sendStatus(false);
    sendPluginEvent("disabled", {}, "dev");
    return { ok: true, enabled: false };
  },

  setConfig: function(config) {
    templateState.config = config || {};
    return { ok: true, config: templateState.config };
  },

  status: function() {
    return {
      enabled: templateState.enabled,
      config: templateState.config,
      stats: {}
    };
  },

  cleanup: function(payload) {
    templateState.enabled = false;
    return {
      ok: true,
      reason: payload && payload.reason ? payload.reason : "cleanup"
    };
  }
};
