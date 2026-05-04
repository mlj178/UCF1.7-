// ============================================================
// Bot 出生点集合器 v23 — 直扫 allPlayers
//
// 所有诊断结论:
//   allPlayers[30] (GM+0x1C) = 唯一容器，持有所有 Player
//   队伍列表 playersBL/GR 在死亡时被清空 → 不可靠
//   事件追踪在晚加载时不会触发 → 不可靠
//
// 策略: 传送时直扫 allPlayers[30] × 安全遍历
//   - 跳过自己 (isMyPlayer)
//   - 跳过真人 (isBot==0 || cameraManager!=null)
//   - 跳过死亡 (isDead)
//   - 其余传送
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[v23] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;

    L('i', '╔══════════════════════════════════╗');
    L('i', '║  Bot 集合器 v23 — 直扫 allPlayers');
    L('i', '║  GameAssembly @ ' + B);
    L('i', '╚══════════════════════════════════╝');

    // RVA
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
    };

    var gm = null;
    var mm = null;
    var spawn = null;
    var ntp = false;
    var tn = 0;

    var isMy   = new NativeFunction(B.add(R.P_isMy),  'bool',   ['pointer','pointer']);
    var isDead = new NativeFunction(B.add(R.E_isDead), 'bool',   ['pointer','pointer']);
    var getCC  = new NativeFunction(B.add(R.E_getCC), 'pointer', ['pointer','pointer']);
    var cSE    = new NativeFunction(B.add(R.C_setEn), 'void',    ['pointer','int','pointer']);
    var gt     = new NativeFunction(B.add(R.getTrans), 'pointer', ['pointer','pointer']);
    var spi    = new NativeFunction(B.add(R.setPosInj),'void',   ['pointer','pointer','pointer']);
    var posBuf = Memory.alloc(16);

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
                if (b === 1) return false;  // 明确标记为 Bot
                if (b === 0) return true;   // 明确标记为真人
            } catch(e) {}
        }
        // 没有 ClientData → 用 cameraManager 辅助判断
        if (rp(pp, O.P_cameraManager)) return true;
        return false;
    }

    function teleport(pp) {
        try {
            var tr = rp(pp, O.P_charContainer);
            if (!tr || tr.isNull()) { tr = gt(pp, ptr(0)); if (!tr || tr.isNull()) return 'T=null'; }
            var cc = getCC(pp, ptr(0));
            if (cc && !cc.isNull()) cSE(cc, 0, ptr(0));
            spi(tr, posBuf, ptr(0));
            try { var np = tr.add(0x10).readPointer(); if (np) { np.add(0x38).writeFloat(spawn.x); np.add(0x3C).writeFloat(spawn.y); np.add(0x40).writeFloat(spawn.z); } } catch(e) {}
            if (cc && !cc.isNull()) cSE(cc, 1, ptr(0));
            return 'OK';
        } catch(e) { return 'ERR:' + e.message; }
    }

    // Hook: 捕获 GM 实例
    L('i', '安装 AddPlayer Hook...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), { onEnter: function(a) { if (!gm) { gm = a[0]; L('i', '✅ GM: ' + gm); } } });
        L('i', 'OK');
    } catch(e) { L('e', 'AddPlayer Hook failed'); }

    L('i', '安装 MapGunInit Hook...');
    try {
        Interceptor.attach(B.add(R.MM_MapGun), { onEnter: function(a) {
            if (mm) return;
            mm = a[0]; L('i', '✅ MM: ' + mm);
            try {
                var arr = mm.add(O.MM_SP_GR).readPointer();
                var len = (arr && !arr.isNull()) ? arr.add(0xC).readU32() : 0;
                if (len > 0) { var p = arr.add(0x10); spawn = { x: p.readFloat(), y: p.add(4).readFloat(), z: p.add(8).readFloat() }; }
                if (!spawn) { arr = mm.add(O.MM_SP_BL).readPointer(); len = (arr && !arr.isNull()) ? arr.add(0xC).readU32() : 0;
                    if (len > 0) { var p = arr.add(0x10); spawn = { x: p.readFloat(), y: p.add(4).readFloat(), z: p.add(8).readFloat() }; } }
                L('i', '  出生点: ' + (spawn ? '(' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ')' : '无'));
            } catch(e) { L('w', '读取出生点失败: ' + e.message); }
        }});
        L('i', 'OK');
    } catch(e) { L('e', 'MapGunInit failed'); }

    L('i', '安装 Player.Update Hook...');
    try {
        Interceptor.attach(B.add(R.P_Update), { onEnter: function(a) {
            if (!ntp) return; ntp = false;
            if (!gm || !mm || !spawn) { L('w', '未就绪'); return; }
            tn++;
            L('i', '╔══ 传送 #' + tn + ' ══╗');
            L('i', '目标: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ')');
            posBuf.writeFloat(spawn.x); posBuf.add(4).writeFloat(spawn.y); posBuf.add(8).writeFloat(spawn.z);

            var ap; try { ap = gm.add(O.GM_allPlayers).readPointer(); } catch(e) {}
            if (!ap || ap.isNull()) { L('e', 'allPlayers null'); return; }
            var total; try { total = ap.add(0xC).readU32(); } catch(e) { return; }
            L('i', 'allPlayers.len=' + total);

            var self = 0, real = 0, dead = 0, bot = 0, ok = 0, fail = 0, nullSlots = 0, invSlots = 0;
            var log = [];

            for (var i = 0; i < total; i++) {
                var pp; try { pp = ap.add(0x10 + i * 8).readPointer(); } catch(e) { pp = null; }
                if (!pp || pp.isNull()) { nullSlots++; continue; }
                if (!isValid(pp)) { invSlots++; continue; }

                try {
                    // 自己
                    if (isMy(pp, ptr(0))) { self++; log.push('#' + i + ': ★自己'); continue; }
                    // 真人
                    if (isHuman(pp)) { real++; log.push('#' + i + ': 真人'); continue; }
                    // 死亡
                    if (isDead(pp, ptr(0))) { dead++; log.push('#' + i + ': Bot(已死)'); continue; }
                    // ←存活 Bot
                    bot++;
                    var r = teleport(pp);
                    if (r === 'OK') { ok++; log.push('#' + i + ': Bot→OK'); }
                    else { fail++; log.push('#' + i + ': Bot→' + r); }
                } catch(e) { fail++; log.push('#' + i + ': ★' + e.message); }
            }

            for (var j = 0; j < log.length; j++) L('i', '  ' + log[j]);
            L('i', '');
            L('i', '┌─ ' + total + '槽 ─────────────────┐');
            L('i', '│ 空=' + nullSlots + ' 无效=' + invSlots + ' 自己=' + self + ' 真人=' + real + ' Bot死=' + dead + ' Bot活=' + bot + ' ✓=' + ok);
            if (fail > 0) L('i', '│ 失败=' + fail);
            L('i', '└──────────────────────────────────┘');
            L('i', '╚══════╝');
            send(JSON.stringify({t:'done',n:tn,total:total,bots:bot,ok:ok,fail:fail}));
        }});
        L('i', 'OK');
    } catch(e) { L('e', 'Player.Update failed'); }

    rpc.exports = {
        teleport: function() {
            if (!gm || !mm || !spawn) { L('w', '未就绪: GM=' + (!!gm) + ' MM=' + (!!mm) + ' SP=' + (!!spawn)); return 'ERR'; }
            ntp = true; L('i', '★ ★ ★ 传送 ★ ★ ★'); return 'OK';
        },
        status: function() { return { gm: !!gm, mm: !!mm, spawn: !!spawn }; },
        diag: function() {
            if (!gm) { L('w', 'GM null'); return; }
            var ap; try { ap = gm.add(O.GM_allPlayers).readPointer(); } catch(e) { L('e', 'read err'); return; }
            var total = (ap && !ap.isNull()) ? ap.add(0xC).readU32() : 0;
            var valid = 0, nullP = 0;
            for (var i = 0; i < total; i++) {
                var pp; try { pp = ap.add(0x10 + i * 8).readPointer(); } catch(e) { pp = null; }
                if (!pp || pp.isNull()) { nullP++; continue; }
                if (isValid(pp)) valid++;
            }
            L('i', 'allPlayers: ' + total + ' 槽, 有效=' + valid + ' null=' + nullP + ' 无效=' + (total - valid - nullP));
        }
    };

    L('i', '');
    L('i', '╔════════════════════════╗');
    L('i', '║  v23 就绪              ║');
    L('i', '║  teleport() 传送       ║');
    L('i', '║  diag()    诊断        ║');
    L('i', '╚════════════════════════╝');
})();
