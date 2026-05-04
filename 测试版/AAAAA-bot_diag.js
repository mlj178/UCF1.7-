// ============================================================
// 诊断工具: 追踪 Bot 创建流程
// Hook Bot.Awake, GenerateNanoGhost, OnNewPlayerJoin
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[BotDiag] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;

    L('i', '╔════════════════════════════════════════╗');
    L('i', '║  Bot 创建流程追踪                      ║');
    L('i', '║  GameAssembly.dll @ ' + B);
    L('i', '╚════════════════════════════════════════╝');

    var R = {
        Bot_Awake:          0xB2CEF0,  // Bot.Awake(this)
        GM_GenerateNano:    0xAF0280,  // ModeBase_Nano.GenerateNanoGhost(this)
        M4_GenerateNano:    0xB41BF0,  // Mode_Nano4.GenerateNanoGhost(this)
        M4_OnNewPlayer:     0xB42140,  // Mode_Nano4.OnNewPlayerJoin(this, Player)
        M4_OnDestroy:       0xB42080,  // Mode_Nano4.OnDestroy(this)
        GM_isNano:          0xAFDA80,  // GameManager.get_isNanoMode
        GM_AddP:            0xAF9A90,  // GameManager.AddPlayer
    };

    var O = {
        // Player fields
        P_cameraManager: 0x48,
        P_clientData:    0x94,
        P_playerData:    0x98,
        // Bot->Player relationship: Bot has 'thisPlayer' at offset
        Bot_thisPlayer:  0x24,  // Bot.thisPlayer (Property, backing field)
        // Entity team
        E_team:          0x20,
        // ClientData
        CD_isBot:        0x1C,
        CD_joinTeam:     0x18,
        // Gm allPlayers
        GM_allPlayers:   0x1C,
    };

    var gm = null;
    var modeNano = null;
    var isMy = new NativeFunction(B.add(0xB55FD0), 'bool', ['pointer', 'pointer']);
    var totalBots = 0;
    var trackedPlayers = {};
    var botAwakeCount = 0;

    function rp(addr, off) {
        try { return addr.add(off).readPointer(); } catch (e) { return null; }
    }

    function isValidPtr(p) {
        try { return p && !p.isNull() && p.readPointer() && !p.readPointer().isNull(); } catch (e) { return false; }
    }

    function describePlayer(pp, label) {
        if (!isValidPtr(pp)) return label + ': null/invalid';
        try {
            var isSelf = false;
            try { isSelf = isMy(pp, ptr(0)); } catch (e) {}
            if (isSelf) return label + ': ★ 自己';

            var cd = rp(pp, O.P_clientData);
            var hasCD = cd && !cd.isNull();
            var isBot = '?';
            var team = '?';
            if (hasCD) {
                try { isBot = cd.add(O.CD_isBot).readU8(); } catch (e) {}
                try { team = cd.add(O.CD_joinTeam).readU8(); } catch (e) {}
            }
            var cam = rp(pp, O.P_cameraManager);
            var hasCam = cam && !cam.isNull();

            var type = '?';
            if (isBot === 1) type = 'BOT';
            else if (isBot === 0) type = hasCam ? '真人' : '真人(无cam)';
            else if (!hasCD) type = 'noCD' + (hasCam ? '+cam' : '');
            else type = 'isBot=' + isBot;

            return label + ': ' + type + ' team=' + team + (hasCam ? ' cam=1' : '');
        } catch (e) {
            return label + ': ★ err: ' + e.message;
        }
    }

    // ──────────────────────────────────────────────────
    // ★ Hook: Bot.Awake
    // ──────────────────────────────────────────────────
    L('i', '安装 Bot.Awake Hook...');
    try {
        Interceptor.attach(B.add(R.Bot_Awake), {
            onEnter: function(args) {
                var botThis = args[0];
                botAwakeCount++;
                L('i', '──── Bot.Awake #' + botAwakeCount + ' ────');

                // 读取 Bot.thisPlayer (offset 0x24)
                var player = null;
                try { player = rp(botThis, O.Bot_thisPlayer); } catch (e) {}

                if (isValidPtr(player)) {
                    totalBots++;
                    var key = player.toString();
                    if (!trackedPlayers[key]) {
                        trackedPlayers[key] = { player: player, bot: botThis };
                    }

                    var desc = describePlayer(player, '  Bot #' + totalBots + ' → Player');
                    L('i', desc);

                    // 额外输出 Player 字段
                    var pd = rp(player, O.P_playerData);
                    L('i', '  Player@' + player + ' playerData@' + (pd ? pd : 'null'));
                    L('i', '  Bot对象@' + botThis + ' Bot.thisPlayer@' + player);
                } else {
                    L('i', '  Bot.Awake #' + botAwakeCount + ': thisPlayer=null');
                }
            }
        });
        L('i', '✅ Bot.Awake Hook OK');
    } catch (e) {
        L('e', 'Bot.Awake Hook 失败: ' + e.message);
    }

    // ──────────────────────────────────────────────────
    // ★ Hook: Mode_Nano4.OnNewPlayerJoin
    // ──────────────────────────────────────────────────
    L('i', '');
    L('i', '安装 Mode_Nano4.OnNewPlayerJoin Hook...');
    try {
        Interceptor.attach(B.add(R.M4_OnNewPlayer), {
            onEnter: function(args) {
                var modeThis = args[0];
                var player = args[1];
                if (!modeNano) modeNano = modeThis;

                var desc = describePlayer(player, 'OnNewPlayerJoin');
                L('i', desc);
            }
        });
        L('i', '✅ OnNewPlayerJoin Hook OK');
    } catch (e) {
        L('e', 'OnNewPlayerJoin Hook 失败: ' + e.message);
    }

    // ──────────────────────────────────────────────────
    // ★ Hook: Mode_Nano4.GenerateNanoGhost
    // ──────────────────────────────────────────────────
    L('i', '');
    L('i', '安装 Mode_Nano4.GenerateNanoGhost Hook...');
    try {
        Interceptor.attach(B.add(R.M4_GenerateNano), {
            onEnter: function(args) {
                var modeThis = args[0];
                if (!modeNano) modeNano = modeThis;
                L('i', '══★ GenerateNanoGhost 被调用 ★══');
            }
        });
        L('i', '✅ GenerateNanoGhost Hook OK');
    } catch (e) {
        L('e', 'GenerateNanoGhost Hook 失败: ' + e.message);
    }

    // ──────────────────────────────────────────────────
    // ★ Hook: GameManager.AddPlayer (跟踪创建的 Player)
    // ──────────────────────────────────────────────────
    L('i', '');
    L('i', '安装 AddPlayer Hook (跟踪创建)...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), {
            onEnter: function(args) {
                if (!gm) gm = args[0];
            },
            onLeave: function(retVal) {
                var pp = retVal;
                if (isValidPtr(pp)) {
                    var key = pp.toString();
                    if (!trackedPlayers[key]) {
                        trackedPlayers[key] = { player: pp, from: 'AddPlayer' };
                    }
                    L('i', describePlayer(pp, '  AddPlayer 创建'));
                } else {
                    L('w', '  AddPlayer → 返回 null (满了?)');
                }
            }
        });
        L('i', '✅ AddPlayer Hook OK');
    } catch (e) {
        L('e', 'AddPlayer Hook 失败: ' + e.message);
    }

    // ──────────────────────────────────────────────────
    // RPC: 输出所有跟踪到的 Player
    // ──────────────────────────────────────────────────
    rpc.exports = {
        report: function() {
            L('i', '');
            L('i', '═════════ 诊断报告 ═════════');
            L('i', 'Bot.Awake 触发次数: ' + botAwakeCount);
            L('i', 'Tracked Players: ' + Object.keys(trackedPlayers).length);
            L('i', '');

            var keys = Object.keys(trackedPlayers);
            for (var i = 0; i < keys.length; i++) {
                var entry = trackedPlayers[keys[i]];
                var desc = describePlayer(entry.player, '  [' + i + ']');
                L('i', desc + ' (from: ' + (entry.from || 'Bot.Awake') + ')');
            }

            L('i', '');
            L('i', '═════════ CSV 输出 ═════════');
            // CSV: index,addr,isBot,team,from
            for (var j = 0; j < keys.length; j++) {
                var pp = trackedPlayers[keys[j]].player;
                var cd = rp(pp, O.P_clientData);
                var isBot = '?';
                var team = '?';
                if (cd && !cd.isNull()) {
                    try { isBot = cd.add(O.CD_isBot).readU8(); } catch (e) {}
                    try { team = cd.add(O.CD_joinTeam).readU8(); } catch (e) {}
                }
                send(JSON.stringify({
                    t: 'player',
                    idx: j,
                    addr: pp.toString(),
                    isBot: isBot,
                    team: team,
                    from: trackedPlayers[keys[j]].from || 'BotAwake'
                }));
            }

            return { botAwake: botAwakeCount, tracked: Object.keys(trackedPlayers).length };
        }
    };

    L('i', '');
    L('i', '╔════════════════════════════════════════╗');
    L('i', '║  诊断就绪                               ║');
    L('i', '║  rpc.exports.report() → 输出报告        ║');
    L('i', '╚════════════════════════════════════════╝');
})();
