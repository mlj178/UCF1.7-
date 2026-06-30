var templateState = {
  enabled: false,
  config: {}
};

function sendStatus(enabled) {
  try {
    send({ type: "status", feature: "template_feature", enabled: enabled });
  } catch (_) {}
}

rpc.exports = {
  enable: function(config) {
    templateState.enabled = true;
    templateState.config = config || templateState.config;
    sendStatus(true);
    return { ok: true, enabled: true, config: templateState.config };
  },

  disable: function() {
    templateState.enabled = false;
    sendStatus(false);
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
