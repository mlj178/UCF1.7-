(function () {
    'use strict';

    function sendLog(level, category, message) {
        send({ type: 'log', level: level, category: category, message: message });
    }

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch (e) { return null; }
    }

    function readFloat(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readFloat();
        } catch (e) { return null; }
    }

    function readInt(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readInt();
        } catch (e) { return null; }
    }

    function readBool(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readU8() !== 0;
        } catch (e) { return null; }
    }

    function getArrayLength(arrAddr) {
        try {
            if (!arrAddr || arrAddr.isNull()) return 0;
            return arrAddr.add(0x10).readInt();
        } catch (e) { return 0; }
    }

    function getArrayElement(arrAddr, index, elementSize) {
        try {
            if (!arrAddr || arrAddr.isNull()) return null;
            return arrAddr.add(0x18 + index * elementSize);
        } catch (e) { return null; }
    }

    function dumpPostureFloat(addr, name) {
        try {
            if (!addr || addr.isNull()) return;
            var standIdle = readFloat(addr.add(0x0));
            var crouchIdle = readFloat(addr.add(0x4));
            var standRun = readFloat(addr.add(0x8));
            var crouchRun = readFloat(addr.add(0xC));
            var floating = readFloat(addr.add(0x10));
            sendLog('info', 'Struct', name + ': standIdle=' + standIdle + ', crouchIdle=' + crouchIdle + ', standRun=' + standRun + ', crouchRun=' + crouchRun + ', floating=' + floating);
        } catch (e) {}
    }

    function dumpZoomAction(addr, name) {
        try {
            if (!addr || addr.isNull()) return;
            var openTime = readFloat(addr.add(0x0));
            var closeTime = readFloat(addr.add(0x4));
            var closeZoomWhenShoot = readBool(addr.add(0xC));
            sendLog('info', 'Struct', name + ': openTime=' + openTime + ', closeTime=' + closeTime + ', closeZoomWhenShoot=' + closeZoomWhenShoot);
        } catch (e) {}
    }

    function dumpChangeMovingRealSize(addr, name) {
        try {
            if (!addr || addr.isNull()) return;
            var DecreaseSpeed = readFloat(addr.add(0x0));
            var Increase_Repeat = readFloat(addr.add(0x4));
            var Increase_Oneshot = readFloat(addr.add(0x8));
            var Min = readFloat(addr.add(0x10));
            sendLog('info', 'Struct', name + ': DecreaseSpeed=' + DecreaseSpeed + ', Increase_Repeat=' + Increase_Repeat + ', Increase_Oneshot=' + Increase_Oneshot + ', Min=' + Min);
        } catch (e) {}
    }

    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    if (!gameAssembly) {
        sendLog('error', '系统', '未找到 GameAssembly.dll');
        return;
    }

    sendLog('info', '系统', 'GameAssembly.dll base: ' + gameAssembly.base);
    var base = gameAssembly.base;

    var staticFieldRVA = {
        'GameManager': 0xE22684,
        'CameraManager': 0xE22588,
        'EffectManager': 0xE225F4,
        'SoundManager': 0xE233FC,
        'MapManager': 0xE23228,
        'AssetManager': 0xE22498,
        'PlayerController': 0xE23324,
        'SentryGunSystem': 0xE23390,
        'ModeBase': 0xE232B8,
        'HUD_Bag': 0xE226EC,
        'HUD_ChatBox': 0xE227A0,
        'HUD_Cheat': 0xE22854,
        'HUD_Role': 0xE23190
    };

    function getRootInstance(className) {
        try {
            var fieldRVA = staticFieldRVA[className];
            if (!fieldRVA) return null;
            var fieldAddr = base.add(fieldRVA);
            return readPtr(fieldAddr);
        } catch (e) { return null; }
    }

    var results = {};

    sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
    sendLog('info', '分类', '【根节点实例地址】');

    var gameManager = getRootInstance('GameManager');
    if (gameManager) {
        results.GameManager = gameManager;
        sendLog('success', '根节点', 'GameManager (游戏管理器) → ' + gameManager);
    }

    var modeBase = getRootInstance('ModeBase');
    if (modeBase) {
        results.ModeBase = modeBase;
        sendLog('success', '根节点', 'ModeBase (模式基类) → ' + modeBase);
    }

    var rootNodes = [
        ['CameraManager', '相机管理器'],
        ['EffectManager', '特效管理器'],
        ['SoundManager', '音效管理器'],
        ['MapManager', '地图管理器'],
        ['AssetManager', '资源管理器'],
        ['PlayerController', '玩家控制器'],
        ['SentryGunSystem', '哨戒炮系统']
    ];
    rootNodes.forEach(function(item) {
        var name = item[0];
        var cnName = item[1];
        var inst = getRootInstance(name);
        if (inst) {
            results[name] = inst;
            sendLog('success', '根节点', name + ' (' + cnName + ') → ' + inst);
        }
    });

    var hudNodes = [
        ['HUD_Bag', '武器背包UI'],
        ['HUD_ChatBox', '聊天框UI'],
        ['HUD_Cheat', '作弊菜单UI'],
        ['HUD_Role', '角色UI']
    ];
    hudNodes.forEach(function(item) {
        var name = item[0];
        var cnName = item[1];
        var inst = getRootInstance(name);
        if (inst) {
            results[name] = inst;
            sendLog('success', '根节点', name + ' (' + cnName + ') → ' + inst);
        }
    });

    sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
    sendLog('info', '分类', '【GameManager.DamageEvent】(伤害事件委托类)');
    
    var damageEventClass = null;
    var damageEventInvalidCheck = readPtr(base.add(0xE226A8));
    if (damageEventInvalidCheck) {
        var vtable = readPtr(damageEventInvalidCheck);
        if (vtable) {
            damageEventClass = readPtr(vtable);
            sendLog('success', 'DamageEvent', '  GameManager.DamageEvent (类地址) → ' + damageEventClass);
            sendLog('info', 'DamageEvent', '    vtable=' + vtable + ', TypeDefIndex=5361');
        }
    }
    if (!damageEventClass) {
        sendLog('warning', 'DamageEvent', '  GameManager.DamageEvent (类地址) → 无法获取');
    }
    
    sendLog('info', 'DamageEvent', '  ─────────────────────────────────────────────────────');
    
    if (damageEventInvalidCheck) {
        sendLog('success', 'DamageEvent', '  DamageEvent_InvalidCheck_Observers (无效检查) → ' + damageEventInvalidCheck);
        var target = readPtr(damageEventInvalidCheck.add(0x4));
        var methodPtr = readPtr(damageEventInvalidCheck.add(0x8));
        var invocationList = readPtr(damageEventInvalidCheck.add(0xC));
        sendLog('info', 'DamageEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var damageEventPreCal = readPtr(base.add(0xE226AC));
    if (damageEventPreCal) {
        sendLog('success', 'DamageEvent', '  DamageEvent_PreCal_Observers (预计算) → ' + damageEventPreCal);
        var target = readPtr(damageEventPreCal.add(0x4));
        var methodPtr = readPtr(damageEventPreCal.add(0x8));
        var invocationList = readPtr(damageEventPreCal.add(0xC));
        sendLog('info', 'DamageEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var damageEventPostCal = readPtr(base.add(0xE226B0));
    if (damageEventPostCal) {
        sendLog('success', 'DamageEvent', '  DamageEvent_PostCal_Observers (后计算) → ' + damageEventPostCal);
        var target = readPtr(damageEventPostCal.add(0x4));
        var methodPtr = readPtr(damageEventPostCal.add(0x8));
        var invocationList = readPtr(damageEventPostCal.add(0xC));
        sendLog('info', 'DamageEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var damageEventPost = readPtr(base.add(0xE226B4));
    if (damageEventPost) {
        sendLog('success', 'DamageEvent', '  DamageEvent_Post_Observers (后处理) → ' + damageEventPost);
        var target = readPtr(damageEventPost.add(0x4));
        var methodPtr = readPtr(damageEventPost.add(0x8));
        var invocationList = readPtr(damageEventPost.add(0xC));
        sendLog('info', 'DamageEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var myPlayerCasueDamageEvent = readPtr(base.add(0xE226D4));
    if (myPlayerCasueDamageEvent) {
        sendLog('success', 'DamageEvent', '  MyPlayerCasueDamageEvent_Observers (我的玩家造成伤害) → ' + myPlayerCasueDamageEvent);
        var target = readPtr(myPlayerCasueDamageEvent.add(0x4));
        var methodPtr = readPtr(myPlayerCasueDamageEvent.add(0x8));
        var invocationList = readPtr(myPlayerCasueDamageEvent.add(0xC));
        sendLog('info', 'DamageEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var myPlayerGetDamageEvent = readPtr(base.add(0xE226D8));
    if (myPlayerGetDamageEvent) {
        sendLog('success', 'DamageEvent', '  MyPlayerGetDamageEvent_Observers (我的玩家受到伤害) → ' + myPlayerGetDamageEvent);
        var target = readPtr(myPlayerGetDamageEvent.add(0x4));
        var methodPtr = readPtr(myPlayerGetDamageEvent.add(0x8));
        var invocationList = readPtr(myPlayerGetDamageEvent.add(0xC));
        sendLog('info', 'DamageEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }

    sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
    sendLog('info', '分类', '【GameManager.DeathEvent】(死亡事件委托类)');
    
    var deathEventClass = null;
    var deathEvent = readPtr(base.add(0xE226B8));
    if (deathEvent) {
        var vtable = readPtr(deathEvent);
        if (vtable) {
            deathEventClass = readPtr(vtable);
            sendLog('success', 'DeathEvent', '  GameManager.DeathEvent (类地址) → ' + deathEventClass);
            sendLog('info', 'DeathEvent', '    vtable=' + vtable + ', TypeDefIndex=5362');
        }
    }
    if (!deathEventClass) {
        sendLog('warning', 'DeathEvent', '  GameManager.DeathEvent (类地址) → 无法获取');
    }
    
    sendLog('info', 'DeathEvent', '  ─────────────────────────────────────────────────────');
    
    if (deathEvent) {
        sendLog('success', 'DeathEvent', '  DeathEvent_Observers (死亡事件) → ' + deathEvent);
        var target = readPtr(deathEvent.add(0x4));
        var methodPtr = readPtr(deathEvent.add(0x8));
        var invocationList = readPtr(deathEvent.add(0xC));
        sendLog('info', 'DeathEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var deathEventForGameRule = readPtr(base.add(0xE226BC));
    if (deathEventForGameRule) {
        sendLog('success', 'DeathEvent', '  DeathEvent_ForGameRule (游戏规则) → ' + deathEventForGameRule);
        var target = readPtr(deathEventForGameRule.add(0x4));
        var methodPtr = readPtr(deathEventForGameRule.add(0x8));
        var invocationList = readPtr(deathEventForGameRule.add(0xC));
        sendLog('info', 'DeathEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var myPlayerKillEvent = readPtr(base.add(0xE226DC));
    if (myPlayerKillEvent) {
        sendLog('success', 'DeathEvent', '  MyPlayerKillEvent_Observers (我的玩家击杀) → ' + myPlayerKillEvent);
        var target = readPtr(myPlayerKillEvent.add(0x4));
        var methodPtr = readPtr(myPlayerKillEvent.add(0x8));
        var invocationList = readPtr(myPlayerKillEvent.add(0xC));
        sendLog('info', 'DeathEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }
    
    var myPlayerDeathEvent = readPtr(base.add(0xE226E0));
    if (myPlayerDeathEvent) {
        sendLog('success', 'DeathEvent', '  MyPlayerDeathEvent_Observers (我的玩家死亡) → ' + myPlayerDeathEvent);
        var target = readPtr(myPlayerDeathEvent.add(0x4));
        var methodPtr = readPtr(myPlayerDeathEvent.add(0x8));
        var invocationList = readPtr(myPlayerDeathEvent.add(0xC));
        sendLog('info', 'DeathEvent', '    target=' + (target ? target : 'null') + ', methodPtr=' + (methodPtr ? methodPtr : 'null') + ', invocationList=' + (invocationList ? invocationList : 'null'));
    }

    sendLog('info', '系统', '根节点实例地址获取完成');
})();
