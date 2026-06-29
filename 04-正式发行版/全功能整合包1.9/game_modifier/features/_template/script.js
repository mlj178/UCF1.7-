var templateState = {
  enabled: false,
  config: {}
};

rpc.exports = {
  enable: function() {
    templateState.enabled = true;
    return { ok: true, enabled: true };
  },
  disable: function() {
    templateState.enabled = false;
    return { ok: true, enabled: false };
  },
  setConfig: function(config) {
    templateState.config = config || {};
    return { ok: true, config: templateState.config };
  },
  status: function() {
    return {
      enabled: templateState.enabled,
      config: templateState.config
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

