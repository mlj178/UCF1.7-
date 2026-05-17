(function () {
    'use strict';

    function L(l, m) {
        var p = '[测试] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    function sendLog(level, message) {
        send({ type: 'log', level: level, message: message });
        L(level === 'error' ? 'e' : (level === 'warning' ? 'w' : 'i'), message);
    }

    function rp(a, o) { 
        try { return a.add(o).readPointer(); } 
        catch(e) { return null; } 
    }

    function isValid(pp) {
        if (!pp || pp.isNull()) return false;
        try { 
            var vt = pp.readPointer(); 
            return vt && !vt.isNull(); 
        } catch(e) { return false; }
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { 
        sendLog('error', 'GameAssembly.dll not found'); 
        return; 
    }
    var B = mod.base;

    sendLog('info', 'GameAssembly.dll base: ' + B);

    var R = {
        GM_AddP:   0xAF9A90,
        P_isMy:    0xB55FD0,
        E_isDead:  0xB400E0,
        Bot_Update: 0xB33370,
        SingGetInst: 0x4A8170,
    };

    var SING = {
        GM: 0xE1CE64,
    };

    var O = {
        GM_allPlayers: 0x1C,
        P_clientData: 0x94,
        CD_isBot: 0x1C,
        Bot_thisPlayer: 0x24,
    };

    var gm = null;
    var trackedPlayers = {};
    var trackedBots = {};
    var botUpdateSeen = {};

    var isMy = new NativeFunction(B.add(R.P_isMy), 'bool', ['pointer', 'pointer']);
    var isDead = new NativeFunction(B.add(R.E_isDead), 'bool', ['pointer', 'pointer']);
    var singletonGetter = new NativeFunction(B.add(R.SingGetInst), 'pointer', ['pointer']);

    function getGM() {
        if (gm) return gm;
        try {
            var methodInfo = B.add(SING.GM).readPointer();
            gm = singletonGetter(methodInfo);
        } catch(e) {}
        if (gm && !gm.isNull()) { 
            sendLog('success', '✅ GM (方式1): ' + gm); 
            return gm; 
        }
        try {
            var classPtr = B.add(SING.GM).readPointer();
            if (classPtr && !classPtr.isNull()) {
                gm = classPtr.add(0xC).readPointer();
            }
        } catch(e) {}
        if (gm && !gm.isNull()) {
            sendLog('success', '✅ GM (方式2): ' + gm);
        }
        return gm;
    }

    function trackFromBot(botPtr) {
        var key = botPtr.toString();
        if (botUpdateSeen[key]) return;
        botUpdateSeen[key] = true;
        
        var player = rp(botPtr, O.Bot_thisPlayer);
        var pValid = player && !player.isNull() && isValid(player);
        
        trackedBots[key] = { 
            bot: botPtr, 
            player: pValid ? player : null, 
            hasPlayer: pValid 
        };
        
        if (pValid) {
            var pk = player.toString();
            if (!trackedPlayers[pk]) {
                trackedPlayers[pk] = player;
                sendLog('info', '  [Bot.Update] 发现 Player → ' + player);
            }
        }
    }

    sendLog('info', '安装 Bot.Update Hook...');
    try {
        Interceptor.attach(B.add(R.Bot_Update), {
            onEnter: function(args) { 
                trackFromBot(args[0]); 
            }
        });
        sendLog('success', '✅ Bot.Update Hook OK');
    } catch(e) { 
        sendLog('error', 'Bot.Update Hook 失败: ' + e.message); 
    }

    sendLog('info', '安装 AddPlayer Hook...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), { 
            onEnter: function(a) { 
                if (!gm) { 
                    gm = a[0]; 
                    sendLog('success', '✅ GM (AddPlayer): ' + gm); 
                } 
            } 
        });
        sendLog('success', '✅ AddPlayer Hook OK');
    } catch(e) { 
        sendLog('error', 'AddPlayer Hook 失败: ' + e.message); 
    }

    function scanAllPlayers() {
        sendLog('info', '');
        sendLog('info', '═══════════════════════════════════════════════════════════');
        sendLog('info', '【扫描 allPlayers 数组】');
        sendLog('info', '═══════════════════════════════════════════════════════════');

        if (!gm) {
            sendLog('warning', 'GM 未就绪，尝试获取...');
            getGM();
        }

        if (!gm || gm.isNull()) {
            sendLog('error', 'GM 仍然为空');
            return;
        }

        sendLog('success', 'GameManager → ' + gm);

        var ap;
        try { 
            ap = gm.add(O.GM_allPlayers).readPointer(); 
        } catch(e) {
            sendLog('error', '读取 allPlayers 失败: ' + e.message);
            return;
        }

        if (!ap || ap.isNull()) {
            sendLog('error', 'allPlayers 数组为空');
            return;
        }

        sendLog('info', 'allPlayers 数组地址 → ' + ap);

        var total;
        try { 
            total = ap.add(0xC).readU32(); 
        } catch(e) { 
            sendLog('error', '读取数组长度失败');
            return; 
        }

        sendLog('info', '数组长度 (偏移0xC) → ' + total);

        sendLog('info', '');
        sendLog('info', '--- 调试：扫描数组前32字节 ---');
        for (var offset = 0x0; offset <= 0x20; offset += 4) {
            try {
                var val = ap.add(offset).readU32();
                var ptr = ap.add(offset).readPointer();
                sendLog('info', '  偏移 0x' + offset.toString(16).padStart(2, '0') + ' → U32=' + val + ' Ptr=' + ptr);
            } catch(e) {}
        }

        sendLog('info', '');
        sendLog('info', '--- 遍历 Player (元素大小=8字节) ---');

        var myPlayerCount = 0;
        var botCount = 0;
        var nullCount = 0;

        for (var i = 0; i < total; i++) {
            var pp;
            try { 
                pp = ap.add(0x10 + i * 8).readPointer(); 
            } catch(e) { 
                pp = null; 
            }

            if (!pp || pp.isNull() || !isValid(pp)) {
                nullCount++;
                sendLog('warning', '  #' + i + ': [空或无效]');
                continue;
            }

            var tag = '';
            var isMyResult = false;
            try { 
                isMyResult = isMy(pp, ptr(0)); 
                if (isMyResult) { 
                    tag = '★玩家'; 
                } 
            } catch(e) {}

            var cd = rp(pp, O.P_clientData);
            var isB = '?';
            if (cd && !cd.isNull()) {
                try { 
                    isB = cd.add(O.CD_isBot).readU8(); 
                } catch(e) {}
            }
            var d = false;
            try { 
                d = isDead(pp, ptr(0)); 
            } catch(e) {}

            if (!tag) {
                if (isB === 1) {
                    tag = d ? 'Bot(死)' : 'Bot(活)';
                    botCount++;
                } else if (isB === 0) {
                    tag = '真人';
                } else {
                    tag = '?' + isB;
                    botCount++;
                }
            } else {
                myPlayerCount++;
            }

            var pk = pp.toString();
            if (!trackedPlayers[pk]) {
                trackedPlayers[pk] = pp;
            }

            sendLog(isMyResult ? 'success' : 'info', 
                '  #' + i + ': ' + tag + ' @' + pp + ' (isMyPlayer=' + isMyResult + ', isBot=' + isB + ')');
        }

        sendLog('info', '');
        sendLog('info', '═══════════════════════════════════════════════════════════');
        sendLog('info', '【统计结果】');
        sendLog('success', '  玩家数量: ' + myPlayerCount);
        sendLog('info', '  BOT数量: ' + botCount);
        sendLog('warning', '  空数量: ' + nullCount);
        sendLog('info', '  数组总数: ' + total);
        sendLog('info', '═══════════════════════════════════════════════════════════');

        sendLog('info', '');
        sendLog('info', '【Bot.Update 追踪统计】');
        sendLog('info', '  Bot组件数量: ' + Object.keys(trackedBots).length);
        sendLog('info', '  追踪Player数量: ' + Object.keys(trackedPlayers).length);
        sendLog('info', '═══════════════════════════════════════════════════════════');
    }

    setTimeout(function() {
        if (!gm) { 
            sendLog('info', '⏳ 3秒后尝试获取 GM...');
            getGM(); 
        }
        scanAllPlayers();
    }, 3000);

    rpc.exports = {
        scan: function() {
            scanAllPlayers();
            return 'OK';
        },
        status: function() {
            return {
                gm: gm ? gm.toString() : 'null',
                players: Object.keys(trackedPlayers).length,
                bots: Object.keys(trackedBots).length
            };
        }
    };

    sendLog('info', '');
    sendLog('info', '╔══════════════════════════════════╗');
    sendLog('info', '║  测试脚本就绪                    ║');
    sendLog('info', '║  scan()   → 扫描 allPlayers      ║');
    sendLog('info', '║  status() → 状态                 ║');
    sendLog('info', '╚══════════════════════════════════╝');
    sendLog('info', '');
    sendLog('info', '等待3秒后自动扫描...');

})();
