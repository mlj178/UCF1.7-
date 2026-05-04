// ============================================================
// 诊断: allPlayers[30] 逐槽详细输出
// 每槽输出: 指针, ClientData, isBot, team, camera, playerData
//            characterContainer, 血量状态等
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[Diag-AP] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;

    L('i', '╔════════════════════════════════════════╗');
    L('i', '║  allPlayers[30] 逐槽详细诊断          ║');
    L('i', '╚════════════════════════════════════════╝');

    var R = { GM_AddP: 0xAF9A90, P_isMy: 0xB55FD0, E_isDead: 0xB400E0 };
    var O = {
        GM_allPlayers: 0x1C,  // Player[30]
        P_cameraManager:      0x48,
        P_characterContainer: 0x58,
        P_recoil:             0x54,
        P_clientData:         0x94,
        P_playerData:         0x98,
        P_input:              0x9C,
        P_weapons:            0xA0,
        P_skills:             0xB0,
        E_team:               0x20,
        E_healthData:         0x1C,
        E_characterController: 0x2C,
        CD_isBot:             0x1C,
        CD_joinTeam:          0x18,
        CD_nickName:          0x10,
        CD_level:             0x14,
    };

    var gm = null;
    var isMy = new NativeFunction(B.add(R.P_isMy), 'bool', ['pointer', 'pointer']);
    var isDead = new NativeFunction(B.add(R.E_isDead), 'bool', ['pointer', 'pointer']);

    function rp(a, o) { try { return a.add(o).readPointer(); } catch(e) { return null; } }

    function inRange(p) {
        try { var o = p.sub(B); return o.compare(0) >= 0 && o.compare(mod.size) < 0; } catch(e) { return false; }
    }

    function readStr(p) {
        if (!p || p.isNull()) return 'null';
        try {
            // IL2CPP string: +0x0 = length, +0xC = chars
            var len = p.add(0x8).readU32();
            if (len <= 0 || len > 50) return '(len=' + len + ')';
            return p.add(0xC).readUtf16String(len);
        } catch(e) { return '(read err)'; }
    }

    function describeSlot(idx, pp) {
        if (!pp || pp.isNull()) {
            L('i', '  ─────────────────────────────────────────');
            L('i', '  #' + idx + ': [NULL]');
            return;
        }

        // VTable check
        var vt = null, vtOff = '?', isValid = false;
        try { vt = pp.readPointer(); vtOff = vt.sub(B).toString(16); isValid = inRange(vt) && vtOff.compare(0) >= 0; } catch(e) {}

        // isMyPlayer
        var self = false;
        try { self = isMy(pp, ptr(0)); } catch(e) {}

        // isDead
        var dead = false;
        try { dead = isDead(pp, ptr(0)); } catch(e) {}

        // ClientData
        var cd = rp(pp, O.P_clientData);
        var hasCD = cd && !cd.isNull() && inRange(cd);
        var isBot = '?', team = '?', nick = '?', level = '?';
        if (hasCD) {
            try { isBot = cd.add(O.CD_isBot).readU8(); } catch(e) {}
            try { team = cd.add(O.CD_joinTeam).readU8(); } catch(e) {}
            try { level = cd.add(O.CD_level).readU32(); } catch(e) {}
            try { nick = readStr(rp(cd, 0x10)); } catch(e) { nick = '(err)'; }
        }

        // cameraManager
        var cam = rp(pp, O.P_cameraManager);
        var hasCam = cam && !cam.isNull();

        // characterContainer
        var cc = rp(pp, O.P_characterContainer);
        var hasCC = cc && !cc.isNull();

        // playerData
        var pd = rp(pp, O.P_playerData);
        var hasPD = pd && !pd.isNull();

        // Entity fields
        var eTeam = '?';
        try { eTeam = pp.add(O.E_team).readU8(); } catch(e) {}
        var health = rp(pp, O.E_healthData);
        var hasHealth = health && !health.isNull();
        var charCtrl = rp(pp, O.E_characterController);
        var hasCharCtrl = charCtrl && !charCtrl.isNull();

        // Player extras
        var inp = rp(pp, O.P_input);
        var wpn = rp(pp, O.P_weapons);
        var sk = rp(pp, O.P_skills);
        var recoil = rp(pp, O.P_recoil);

        // Type classification
        var type = '';
        if (self) type = '★ 自己';
        else if (hasCD && isBot === 0) type = '真人';
        else if (hasCD && isBot === 1) type = dead ? 'Bot(已死)' : 'Bot';
        else if (!hasCD && hasCam) type = '? noCD+cam';
        else if (!hasCD && !hasCam) type = '? noCD-nocam';
        else type = '? isBot=' + isBot;

        L('i', '  ─────────────────────────────────────────');
        L('i', '  #' + idx + ': ' + type);
        L('i', '    地址=' + pp + ' vtable=0x' + vtOff + (isValid ? '' : '(越界!)'));
        L('i', '    isMy=' + (self?'1':'0') + ' isDead=' + (dead?'1':'0') + ' Entity.team=' + eTeam);
        L('i', '    ClientData@' + cd + (hasCD ? ' isBot='+isBot+' team='+team+' lv='+level+' nick='+nick : ' [null]'));
        L('i', '    cameraManager@' + (hasCam ? cam : 'null') + ' | characterContainer@' + (hasCC ? cc : 'null'));
        L('i', '    playerData@' + (hasPD ? pd : 'null') + ' | healthData@' + (hasHealth ? health : 'null'));
        L('i', '    charController@' + (hasCharCtrl ? charCtrl : 'null') + ' | recoil@' + (recoil ? recoil : 'null'));
        L('i', '    input@' + (inp ? inp : 'null') + ' weapons@' + (wpn ? wpn : 'null') + ' skills@' + (sk ? sk : 'null'));
    }

    // Hook AddPlayer to get GM
    try {
        Interceptor.attach(B.add(R.GM_AddP), {
            onEnter: function(a) { if (!gm) { gm = a[0]; L('i', '✅ GM: ' + gm); } }
        });
        L('i', 'AddPlayer Hook installed');
    } catch(e) {
        L('e', 'Hook failed: ' + e.message);
    }

    rpc.exports = {
        dump: function() {
            var waited = 0;
            while (!gm && waited < 5000) { Thread.sleep(0.1); waited += 100; }
            if (!gm) { L('w', 'GM 未就绪'); return; }

            var ap; try { ap = gm.add(O.GM_allPlayers).readPointer(); } catch(e) {}
            if (!ap || ap.isNull()) { L('e', 'allPlayers null'); return; }
            var total; try { total = ap.add(0xC).readU32(); } catch(e) { L('e', 'read len err'); return; }

            L('i', '');
            L('i', '═══════════════════════════════════════════');
            L('i', ' allPlayers[30] @ ' + ap + '  (len=' + total + ')');
            L('i', '═══════════════════════════════════════════');
            L('i', '');

            for (var i = 0; i < total; i++) {
                var pp; try { pp = ap.add(0x10 + i * 8).readPointer(); } catch(e) { pp = null; }
                describeSlot(i, pp);
            }

            L('i', '');
            L('i', '═══════════════════════════════════════════');
            L('i', '  诊断完成');
            L('i', '═══════════════════════════════════════════');

            return { total: total };
        }
    };

    L('i', '');
    L('i', '已加载。进入房间后调用:');
    L('i', '  rpc.exports.dump()  → 输出 allPlayers 详表');
})();
