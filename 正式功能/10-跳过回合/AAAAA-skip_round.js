// skip_round.js - 全模式通用回合跳过脚本
// 原理：将 ModeBase.restGameTime 设为 0:00，所有模式时间耗尽都会触发原生结束流程
// 适用：生化模式 / 团队竞技 / 个人竞技 / 特殊战
// 不需要模式检测，所有模式共用同一策略

console.log("[*] === Skip Round Script ===\n");

var gameAssembly = Process.findModuleByName("GameAssembly.dll");
if (!gameAssembly) {
    console.log("[-] GameAssembly.dll not found!");
}

var base = gameAssembly ? gameAssembly.base : ptr(0);

var state = {
    modeBaseInstance: null,
    skipCount: 0,
    skipErrorCount: 0,
    roundActive: false,
    currentRound: 0,

    // 防重入：防止 Hook 回调自递归导致卡死
    inHook: false,
    skipGuard: false,

    hookCounts: {
        updateTimeUI: 0,
        checkRoundOver: 0,
        gameRoundEnd: 0,
        onTimeOut: 0
    },

    rpcReady: false,
    scriptLog: null
};

function pad2(n) { return n < 10 ? "0" + n : "" + n; }

function log(level, message) {
    var ts = new Date();
    var timestamp = ts.getFullYear() + "-" + pad2(ts.getMonth()+1) + "-" + pad2(ts.getDate()) +
        " " + pad2(ts.getHours()) + ":" + pad2(ts.getMinutes()) + ":" + pad2(ts.getSeconds());
    var prefixMap = {"INFO": "[+]", "WARN": "[!]", "ERROR": "[-]", "DEBUG": "[*]", "ACTION": "[>]"};
    var prefix = prefixMap[level] || "[*]";
    var line = timestamp + " " + prefix + " " + message;
    console.log(line);
    if (state.scriptLog) {
        try { state.scriptLog.write(line + "\n"); state.scriptLog.flush(); } catch (e) {}
    }
}

function openLogFile() {
    try {
        var logPath = "D:\\trae_project\\skip_round_log.txt";
        state.scriptLog = new File(logPath, "w");
        state.scriptLog.write("=== Skip Round Script Log ===\n");
        state.scriptLog.write("Start: " + new Date().toISOString() + "\n");
        state.scriptLog.write("Base: " + base + "\n\n");
        state.scriptLog.flush();
        log("INFO", "Log: " + logPath);
    } catch (e) {
        console.log("[-] Log file error: " + e);
    }
}

function sendToUI(type, data) {
    var payload = { type: type };
    for (var key in data) payload[key] = data[key];
    send(payload);
}

function isValidInstance(instance) {
    try {
        if (!instance || instance.equals(ptr(0))) return false;
        if (instance.compare(ptr(0x10000)) < 0) return false;
        instance.readU8();
        return true;
    } catch (e) {
        return false;
    }
}

// ============================================
// 核心：跳过当前回合
// 全模式通用策略：restGameTime = 0:00
// ============================================
function skipRound() {
    if (state.skipGuard) {
        log("WARN", "skipGuard active, skipping");
        return { ok: false, reason: "guard_active" };
    }

    var instance = state.modeBaseInstance;
    if (!isValidInstance(instance)) {
        state.skipErrorCount++;
        log("ERROR", "skipRound: no valid instance (err:" + state.skipErrorCount + ")");
        return { ok: false, reason: "no_instance" };
    }

    var minute = 0, second = 0;
    try {
        minute = instance.add(0x34).readS32();
        second = instance.add(0x38).readS32();
    } catch (e) {
        state.skipErrorCount++;
        log("ERROR", "skipRound: read failed (err:" + state.skipErrorCount + ")");
        return { ok: false, reason: "read_failed" };
    }

    if (minute === 0 && second === 0) {
        log("WARN", "skipRound: time already 0:00");
        return { ok: false, reason: "already_zero" };
    }

    try {
        state.skipGuard = true;
        instance.add(0x34).writeS32(0);
        instance.add(0x38).writeS32(0);
        state.skipCount++;
        state.roundActive = false;
        log("ACTION", "SKIP! " + minute + ":" + pad2(second) + " -> 0:00 (total:" + state.skipCount + ")");
        sendToUI("round_skipped", { from: minute + ":" + pad2(second), count: state.skipCount });
        state.skipGuard = false;
        return { ok: true };
    } catch (e) {
        state.skipGuard = false;
        state.skipErrorCount++;
        log("ERROR", "skipRound: write failed " + e + " (err:" + state.skipErrorCount + ")");
        return { ok: false, reason: "write_failed" };
    }
}

// ============================================
// Hook
// ============================================

function installHooks() {
    log("INFO", "Installing hooks...");
    log("INFO", "Base: " + base);
    sendToUI("status", { message: "Installing hooks..." });

    // Hook 1: ModeBase.UpdateTimeUI - 获取 ModeBase 实例
    // RVA: 0xAF6930
    log("DEBUG", "Hooking ModeBase.UpdateTimeUI at 0xAF6930...");
    try {
        Interceptor.attach(base.add(0xAF6930), {
            onEnter: function(args) {
                if (state.inHook) return;
                state.inHook = true;

                state.hookCounts.updateTimeUI++;
                var instance = args[0];
                if (!isValidInstance(instance)) { state.inHook = false; return; }

                var isNew = !state.modeBaseInstance || !instance.equals(state.modeBaseInstance);
                if (isNew) {
                    state.modeBaseInstance = instance;
                    try { state.currentRound = instance.add(0x14).readS32(); } catch(e) {}
                    state.roundActive = true;
                    log("DEBUG", "New instance, Round=" + state.currentRound);
                }

                state.inHook = false;
            },
            onLeave: function(retval) { state.inHook = false; }
        });
        log("INFO", "Hooked UpdateTimeUI (0xAF6930)");
    } catch (e) {
        log("ERROR", "Hook UpdateTimeUI failed: " + e);
    }

    // Hook 2: GameManager.GameRoundEnd - 回合结束清理
    // RVA: 0xAFAA40
    log("DEBUG", "Hooking GameManager.GameRoundEnd at 0xAFAA40...");
    try {
        Interceptor.attach(base.add(0xAFAA40), {
            onEnter: function(args) {
                state.hookCounts.gameRoundEnd++;
                log("INFO", "GameRoundEnd(#" + state.hookCounts.gameRoundEnd + ")");
                sendToUI("round_end", { count: state.hookCounts.gameRoundEnd });
                state.modeBaseInstance = null;
                state.roundActive = false;
            },
            onLeave: function(retval) {}
        });
        log("INFO", "Hooked GameRoundEnd (0xAFAA40)");
    } catch (e) {
        log("ERROR", "Hook GameRoundEnd failed: " + e);
    }

    // Hook 3: ModeBase.OnTimeOut - 监控超时
    // RVA: 0xAF1920
    log("DEBUG", "Hooking ModeBase.OnTimeOut at 0xAF1920...");
    try {
        Interceptor.attach(base.add(0xAF1920), {
            onEnter: function(args) {
                state.hookCounts.onTimeOut++;
                log("INFO", "OnTimeOut(#" + state.hookCounts.onTimeOut + ")");
                sendToUI("timeout", { count: state.hookCounts.onTimeOut });
                state.roundActive = false;
            },
            onLeave: function(retval) {}
        });
        log("INFO", "Hooked OnTimeOut (0xAF1920)");
    } catch (e) {
        log("ERROR", "Hook OnTimeOut failed: " + e);
    }

    state.rpcReady = true;
    log("INFO", "All hooks installed");
    sendToUI("ready", { message: "Hooks installed" });
}

// ============================================
// RPC
// ============================================

rpc.exports = {

    install: function() {
        log("INFO", "RPC: install()");
        if (!gameAssembly) return { ok: false, error: "GameAssembly.dll not found" };
        if (state.rpcReady) return { ok: true, message: "Already installed" };
        try { openLogFile(); installHooks(); return { ok: true, message: "Hooks installed" }; }
        catch (e) { log("ERROR", "install: " + e); return { ok: false, error: String(e) }; }
    },

    skipround: function() {
        log("INFO", "RPC: skipround()");
        var result = skipRound();
        return { ok: result.ok, reason: result.reason };
    },

    getstatus: function() {
        var timeStr = null;
        if (isValidInstance(state.modeBaseInstance)) {
            try {
                var m = state.modeBaseInstance.add(0x34).readS32();
                var s = state.modeBaseInstance.add(0x38).readS32();
                if (m >= 0 && m <= 200 && s >= 0 && s <= 59) timeStr = m + ":" + pad2(s);
            } catch(e) {}
        }
        return {
            ok: true,
            connected: !!gameAssembly,
            rpcReady: state.rpcReady,
            roundActive: state.roundActive,
            currentRound: state.currentRound,
            skipCount: state.skipCount,
            skipErrorCount: state.skipErrorCount,
            hasInstance: !!state.modeBaseInstance,
            restGameTime: timeStr
        };
    },

    reset: function() {
        log("INFO", "RPC: reset()");
        state.modeBaseInstance = null;
        state.roundActive = false;
        state.currentRound = 0;
        state.skipCount = 0;
        state.skipErrorCount = 0;
        state.skipGuard = false;
        state.inHook = false;
        for (var k in state.hookCounts) state.hookCounts[k] = 0;
        return { ok: true };
    }
};

console.log("\n========================================");
console.log("  Skip Round Script (全模式通用)");
console.log("  生化 / 团队 / 个人 / 特殊战 均可用");
console.log("========================================");
if (gameAssembly) {
    console.log("[+] Base: " + gameAssembly.base);
    console.log("[+] RPC: install, skipround, getstatus, reset");
} else {
    console.log("[-] GameAssembly.dll not found");
}
console.log("[*] Use Python UI to control this script\n");
