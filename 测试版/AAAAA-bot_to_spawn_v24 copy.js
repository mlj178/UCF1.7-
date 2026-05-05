// ============================================================
// Bot 出生点集合器 v24 — 双路径扫描 + v14传送模式
//
// 路径A: 扫描 allPlayers[30] → 找到已注册的 Player
// 路径B: Hook Bot.Update → 捕获所有 Bot 组件实例
//         → 读 Bot.thisPlayer(0x24) 拿到 Player 指针
//
// 传送: CC.disable → Transform.set_position → CC.enable (v14模式)
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[v24] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;

    L('i', '╔════════════════════════════════════════╗');
    L('i', '║  Bot 集合器 v24 — 双路径扫描          ║');
    L('i', '║  GameAssembly @ ' + B);
    L('i', '╚════════════════════════════════════════╝');

    var R = {
        GM_AddP:   0xAF9A90,
        MM_MapGun: 0xAEBB70,
        P_Update:  0xB551D0,
        P_isMy:    0xB55FD0,
        E_isDead:  0xB400E0,
        E_getCC:   0x1CF180,
        C_setEn:   0xAB86B0,
        getTrans:  0x32CF40,
        setPosInj: 0x3F4810,
        Bot_Update: 0xB33370,
        SingGetInst: 0x4A8170,
    };

    var SING = {
        GM: 0xE1CE64,
        MM: 0xE1D9E8,
    };

    var O = {
        GM_allPlayers: 0x1C,
        MM_SP_GR: 0x14,
        MM_SP_BL: 0x10,
        P_cameraManager: 0x48,
        P_charContainer: 0x58,
        P_clientData: 0x94,
        CD_isBot: 0x1C,
        CD_team:  0x18,
        Bot_thisPlayer: 0x24,
    };

    var gm = null;
    var mm = null;
    // 硬编码 SP_GR(潜伏者/佣兵)出生点坐标 — 不依赖 MM 读取
    var spawn = { x: 13.6, y: 14.1, z: 0.1 };
    var ntp = false;
    var tn = 0;

    var trackedPlayers = {};
    var trackedBots = {};
    var botUpdateSeen = {};

    var isMy   = new NativeFunction(B.add(R.P_isMy),  'bool',   ['pointer','pointer']);
    var isDead = new NativeFunction(B.add(R.E_isDead), 'bool',   ['pointer','pointer']);
    var getCC  = new NativeFunction(B.add(R.E_getCC), 'pointer', ['pointer','pointer']);
    var cSE    = new NativeFunction(B.add(R.C_setEn), 'void',    ['pointer','int','pointer']);
    var gt     = new NativeFunction(B.add(R.getTrans), 'pointer', ['pointer','pointer']);
    var spi    = new NativeFunction(B.add(R.setPosInj),'void',   ['pointer','pointer','pointer']);
    var posBuf = Memory.alloc(16);

    var singletonGetter = new NativeFunction(B.add(R.SingGetInst), 'pointer', ['pointer']);

    function getGM() {
        if (gm) return gm;
        try {
            var methodInfo = B.add(SING.GM).readPointer();
            gm = singletonGetter(methodInfo);
        } catch(e) {}
        if (gm && !gm.isNull()) { L('i', '✅ GM: ' + gm); return gm; }
        try {
            var classPtr = B.add(SING.GM).readPointer();
            if (classPtr && !classPtr.isNull()) {
                gm = classPtr.add(0xC).readPointer();
            }
        } catch(e) {}
        if (gm && !gm.isNull()) L('i', '✅ GM: ' + gm);
        return gm;
    }

    function getMM() {
        if (mm) return mm;
        try {
            var methodInfo = B.add(SING.MM).readPointer();
            mm = singletonGetter(methodInfo);
        } catch(e) {}
        if (mm && !mm.isNull()) L('i', '✅ MM: ' + mm);
        return mm;
    }

    function rp(a, o) { try { return a.add(o).readPointer(); } catch(e) { return null; } }

    function isValid(pp) {
        if (!pp || pp.isNull()) return false;
        try { var vt = pp.readPointer(); return vt && !vt.isNull(); } catch(e) { return false; }
    }

    function isHuman(pp) {
        var cd = rp(pp, O.P_clientData);
        if (cd && !cd.isNull()) {
            try {
                var b = cd.add(O.CD_isBot).readU8();
                if (b === 1) return false;
                if (b === 0) return true;
            } catch(e) {}
        }
        if (rp(pp, O.P_cameraManager)) return true;
        return false;
    }

    function trackFromBot(botPtr) {
        var key = botPtr.toString();
        if (botUpdateSeen[key]) return;
        botUpdateSeen[key] = true;
        var player = rp(botPtr, O.Bot_thisPlayer);
        var pValid = player && !player.isNull() && isValid(player);
        trackedBots[key] = { bot: botPtr, player: pValid ? player : null, hasPlayer: pValid };
        if (pValid) {
            var pk = player.toString();
            if (!trackedPlayers[pk]) trackedPlayers[pk] = player;
        }
    }

    function teleportEntity(ppOrBot, isBot) {
        try {
            var tr = gt(ppOrBot, ptr(0));
            if (!tr || tr.isNull()) {
                if (!isBot) tr = rp(ppOrBot, O.P_charContainer);
                else tr = null;
            }
            if (!tr || tr.isNull()) return 'T=null';

            var cc = getCC(ppOrBot, ptr(0));
            if (cc && !cc.isNull()) cSE(cc, 0, ptr(0));

            spi(tr, posBuf, ptr(0));
            try {
                var np = tr.add(0x10).readPointer();
                if (np) {
                    np.add(0x38).writeFloat(spawn.x);
                    np.add(0x3C).writeFloat(spawn.y);
                    np.add(0x40).writeFloat(spawn.z);
                }
            } catch(e) {}

            if (cc && !cc.isNull()) cSE(cc, 1, ptr(0));

            return 'OK';
        } catch(e) { return 'ERR:' + e.message; }
    }

    L('i', '安装 Bot.Update Hook...');
    try {
        Interceptor.attach(B.add(R.Bot_Update), {
            onEnter: function(args) { trackFromBot(args[0]); }
        });
        L('i', '✅ Bot.Update OK');
    } catch(e) { L('e', 'Bot.Update failed'); }

    function executeTeleport() {
        tn++;
        L('i', '');
        L('i', '╔══ 传送 #' + tn + ' ══╗');
        getGM(); getMM();
        if (!gm || !mm) { L('e', 'GM/MM 未就绪'); return; }

        L('i', '出生点: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ')');
        posBuf.writeFloat(spawn.x); posBuf.add(4).writeFloat(spawn.y); posBuf.add(8).writeFloat(spawn.z);

        try {
            var ap = gm.add(O.GM_allPlayers).readPointer();
            if (ap && !ap.isNull()) {
                var t = ap.add(0xC).readU32();
                for (var i = 0; i < t; i++) {
                    try {
                        var pp = ap.add(0x10 + i * 8).readPointer();
                        if (isValid(pp)) {
                            var pk = pp.toString();
                            if (!trackedPlayers[pk]) trackedPlayers[pk] = pp;
                        }
                    } catch(e) {}
                }
            }
        } catch(e) {}

        var bKeys = Object.keys(trackedBots);
        for (var bi = 0; bi < bKeys.length; bi++) {
            var e = trackedBots[bKeys[bi]];
            if (e.hasPlayer && e.player) {
                var pk = e.player.toString();
                if (!trackedPlayers[pk]) trackedPlayers[pk] = e.player;
            }
        }

        L('i', '追踪: ' + Object.keys(trackedPlayers).length + ' Player | ' + bKeys.length + ' Bot组件');

        var self = 0, real = 0, dead = 0, botOk = 0, botFail = 0;
        var pKeys = Object.keys(trackedPlayers);
        var log = [];

        for (var pi = 0; pi < pKeys.length; pi++) {
            var pp = trackedPlayers[pKeys[pi]];
            try {
                if (isMy(pp, ptr(0))) { self++; continue; }
                if (isHuman(pp)) { real++; continue; }
                if (isDead(pp, ptr(0))) { dead++; continue; }
                var r = teleportEntity(pp, false);
                if (r === 'OK') botOk++;
                else botFail++;
                log.push('#' + pi + ': Bot→' + r);
            } catch(e) { botFail++; }
        }

        for (var j = 0; j < log.length; j++) L('i', '  ' + log[j]);

        L('i', '');
        L('i', '┌─ ' + pKeys.length + '人 ──────────────────┐');
        L('i', '│  自己=' + self + ' 真人=' + real + '  Bot死=' + dead + ' Bot活=' + botOk);
        if (botFail > 0) L('i', '│  失败=' + botFail);
        L('i', '└──────────────────────────────────────────┘');
        L('i', '╚══════╝');
        send(JSON.stringify({t:'done',n:tn,bots:botOk,fail:botFail}));
    }

    L('i', '安装 AddPlayer...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), { onEnter: function(a) { if (!gm) { gm = a[0]; L('i', '✅ GM: ' + gm); } } });
        L('i', 'OK');
    } catch(e) { L('e', 'AddPlayer failed'); }

    setTimeout(function() {
        if (!gm) { L('i', '⏳ 尝试获取 GM...'); getGM(); }
        if (!mm) { getMM(); }
    }, 3000);

    L('i', '安装 MapGunInit...');
    try {
        Interceptor.attach(B.add(R.MM_MapGun), { onEnter: function(a) {
            if (mm) return;
            mm = a[0]; L('i', '✅ MM: ' + mm);
            L('i', '  出生点坐标: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ') - 硬编码 SP_GR');
        }});
        L('i', 'OK');
    } catch(e) { L('e', 'MapGunInit failed'); }

    L('i', '安装 Player.Update...');
    try {
        Interceptor.attach(B.add(R.P_Update), { onEnter: function(a) {
            if (!ntp) return; ntp = false;
            if (!gm || !mm) { L('w', '未就绪'); return; }
            executeTeleport();
        }});
        L('i', 'OK');
    } catch(e) { L('e', 'Player.Update failed'); }

    function teleportSinglePlayer(pp, label) {
        try {
            if (isMy(pp, ptr(0))) { L('i', label + ' → 自己, 跳过'); return; }
            if (isHuman(pp)) { L('i', label + ' → 真人, 跳过'); return; }
            if (isDead(pp, ptr(0))) { L('i', label + ' → 已死, 跳过'); return; }

            posBuf.writeFloat(spawn.x); posBuf.add(4).writeFloat(spawn.y); posBuf.add(8).writeFloat(spawn.z);
            var tr = gt(pp, ptr(0));
            if (!tr || tr.isNull()) tr = rp(pp, O.P_charContainer);
            if (!tr || tr.isNull()) { L('i', label + ' → T=null'); return; }

            var cc = getCC(pp, ptr(0));
            if (cc && !cc.isNull()) cSE(cc, 0, ptr(0));
            spi(tr, posBuf, ptr(0));
            try { var np = tr.add(0x10).readPointer(); if (np) { np.add(0x38).writeFloat(spawn.x); np.add(0x3C).writeFloat(spawn.y); np.add(0x40).writeFloat(spawn.z); } } catch(e) {}
            if (cc && !cc.isNull()) cSE(cc, 1, ptr(0));

            L('i', '✅ ' + label + ' → OK');
        } catch(e) { L('i', label + ' → ' + e.message); }
    }

    rpc.exports = {
        teleport: function() {
            getGM(); getMM();
            if (!gm || !mm) { L('w', 'GM/MM 未就绪'); return 'ERR'; }
            ntp = true; L('i', '★ ★ ★ 传送 ★ ★ ★'); return 'OK';
        },
        status: function() {
            return {
                gm: !!gm, mm: !!mm, spawn: !!spawn,
                players: Object.keys(trackedPlayers).length,
                bots: Object.keys(trackedBots).length
            };
        },
        list: function() {
            getGM();
            if (!gm) { L('w', 'GM 未就绪'); return; }
            var ap; try { ap = gm.add(O.GM_allPlayers).readPointer(); } catch(e) {}
            if (!ap || ap.isNull()) { L('e', 'allPlayers null'); return; }
            var total; try { total = ap.add(0xC).readU32(); } catch(e) { return; }
            L('i', '');
            for (var i = 0; i < total; i++) {
                var pp; try { pp = ap.add(0x10 + i * 8).readPointer(); } catch(e) { pp = null; }
                if (!pp || pp.isNull() || !isValid(pp)) { L('i', '  #' + i + ': [空]'); continue; }
                var tag = '';
                try { if (isMy(pp, ptr(0))) { tag = '★自己'; } } catch(e) {}
                if (!tag) {
                    var cd = rp(pp, O.P_clientData);
                    var isB = '?';
                    if (cd && !cd.isNull()) try { isB = cd.add(O.CD_isBot).readU8(); } catch(e) {}
                    var d = false; try { d = isDead(pp, ptr(0)); } catch(e) {}
                    if (isB === 1) tag = d ? 'Bot死' : 'Bot';
                    else if (isB === 0) tag = '真人';
                    else tag = '?' + isB;
                }
                L('i', '  #' + i + ': ' + tag + ' @' + pp);
            }
        },
    };

    L('i', '');
    L('i', '╔══════════════════════════════════╗');
    L('i', '║  v24 就绪                        ║');
    L('i', '║  teleport() → 传送              ║');
    L('i', '║  status()  → 状态               ║');
    L('i', '╚══════════════════════════════════╝');
})();
