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

    var hudBag = getRootInstance('HUD_Bag');
    if (hudBag) {
        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【HUD_Bag 子节点】(武器背包UI)');

        var buttons = readPtr(hudBag.add(0xC));
        if (buttons) {
            var buttonsLen = getArrayLength(buttons);
            sendLog('success', 'HUD_Bag', '  buttons[] (按钮数组) 长度=' + buttonsLen + ' → ' + buttons);
            
            for (var b = 0; b < Math.min(buttonsLen, 10); b++) {
                var btn = readPtr(getArrayElement(buttons, b, 4));
                if (btn) {
                    sendLog('success', 'HUD_BagButton', '    buttons[' + b + '] (武器背包按钮) → ' + btn);
                }
            }
        }
    }

    var hudCheat = getRootInstance('HUD_Cheat');
    if (hudCheat) {
        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【HUD_Cheat 子节点】(作弊菜单UI)');

        var curChoiceList = readPtr(hudCheat.add(0x18));
        if (curChoiceList) {
            sendLog('success', 'HUD_Cheat', '  curChoiceList (当前选项列表) → ' + curChoiceList);
        }
    }

    if (gameManager) {
        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【GameManager 子节点】(游戏管理器)');

        var gm = gameManager;

        var entityBL_Alive = readPtr(gm.add(0x14));
        if (entityBL_Alive) sendLog('success', 'GameManager', 'entityBL_Alive (黑名单存活实体) → ' + entityBL_Alive);

        var entityGR_Alive = readPtr(gm.add(0x18));
        if (entityGR_Alive) sendLog('success', 'GameManager', 'entityGR_Alive (全球风险存活实体) → ' + entityGR_Alive);

        var allPlayers = readPtr(gm.add(0x1C));
        if (allPlayers) {
            var playerCount = getArrayLength(allPlayers);
            sendLog('success', 'GameManager', 'allPlayers[] (所有玩家数组) 长度=' + playerCount + ' → ' + allPlayers);
            
            sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
            sendLog('info', '分类', '【Player 实例列表】(遍历 allPlayers[])');
            
            for (var p = 0; p < Math.min(playerCount, 16); p++) {
                var playerInst = readPtr(getArrayElement(allPlayers, p, 4));
                if (playerInst) {
                    sendLog('success', 'Player', '  allPlayers[' + p + '] → ' + playerInst);
                }
            }
        }

        var playersBL = readPtr(gm.add(0x20));
        if (playersBL) sendLog('success', 'GameManager', 'playersBL (黑名单玩家) → ' + playersBL);

        var playersBL_Alive = readPtr(gm.add(0x24));
        if (playersBL_Alive) sendLog('success', 'GameManager', 'playersBL_Alive (黑名单存活玩家) → ' + playersBL_Alive);

        var playersGR = readPtr(gm.add(0x28));
        if (playersGR) sendLog('success', 'GameManager', 'playersGR (全球风险玩家) → ' + playersGR);

        var playersGR_Alive = readPtr(gm.add(0x2C));
        if (playersGR_Alive) sendLog('success', 'GameManager', 'playersGR_Alive (全球风险存活玩家) → ' + playersGR_Alive);

        var weaponAsset = readPtr(gm.add(0x30));
        if (weaponAsset) {
            sendLog('success', 'GameManager', 'weaponAsset (武器资产) → ' + weaponAsset);
            
            var weaponList = readPtr(weaponAsset.add(0x10));
            if (weaponList) {
                var weaponListLen = getArrayLength(weaponList);
                sendLog('success', 'WeaponAsset', '  weaponList[] (武器列表) 长度=' + weaponListLen + ' → ' + weaponList);
            }
        }

        var characterAsset = readPtr(gm.add(0x34));
        if (characterAsset) sendLog('success', 'GameManager', 'characterAsset (角色资产) → ' + characterAsset);
    }

    if (gameManager) {
        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【Player 子节点】(从 GameManager.myPlayer)');

        var myPlayerStaticAddr = base.add(0xE22694);
        var myPlayer = readPtr(myPlayerStaticAddr);
        
        sendLog('info', '调试', 'myPlayer 静态字段地址: ' + myPlayerStaticAddr);
        sendLog('info', '调试', 'myPlayer 指针值: ' + (myPlayer ? myPlayer : 'null'));
        
        if (myPlayer) {
            sendLog('success', 'Player', 'myPlayer (我的玩家) → ' + myPlayer);

            sendLog('info', '调试', '读取 healthData (偏移 0x1C): ' + myPlayer.add(0x1C));
            var healthData = readPtr(myPlayer.add(0x1C));
            if (healthData) sendLog('success', 'Player', '  healthData (生命数据) → ' + healthData);
            else sendLog('warning', 'Player', '  healthData (生命数据) = null');

            sendLog('info', '调试', '读取 clientData (偏移 0x94): ' + myPlayer.add(0x94));
            var clientData = readPtr(myPlayer.add(0x94));
            if (clientData) sendLog('success', 'Player', '  clientData (客户端数据) → ' + clientData);
            else sendLog('warning', 'Player', '  clientData (客户端数据) = null');
            
            sendLog('info', '调试', '--- 扫描 Player 字段 (32位游戏，指针4字节) ---');
            var offsets = [0x88, 0x8C, 0x90, 0x94, 0x98, 0x9C, 0xA0, 0xA4, 0xA8, 0xAC, 0xB0, 0xB4, 0xB8, 0xC0, 0xC8];
            for (var i = 0; i < offsets.length; i++) {
                var off = offsets[i];
                var val = readPtr(myPlayer.add(off));
                if (val && !val.isNull()) {
                    var valNum = parseInt(val);
                    if (valNum > 0x100000 && valNum < 0xFFFFFFFF) {
                        sendLog('info', '扫描', '  偏移 0x' + off.toString(16) + ' → ' + val + ' (可能是有效指针)');
                    }
                }
            }

            sendLog('info', '调试', '读取 playerData (偏移 0x98): ' + myPlayer.add(0x98));
            var playerData = readPtr(myPlayer.add(0x98));
            if (playerData) sendLog('success', 'Player', '  playerData (玩家数据) → ' + playerData);
            else sendLog('warning', 'Player', '  playerData (玩家数据) = null');

            sendLog('info', '调试', '读取 wpns (偏移 0xA0): ' + myPlayer.add(0xA0));
            var wpns = readPtr(myPlayer.add(0xA0));
            if (wpns) sendLog('success', 'Player', '  wpns (武器系统) → ' + wpns);
            else sendLog('warning', 'Player', '  wpns (武器系统) = null');

            sendLog('info', '调试', '读取 weaponBag (偏移 0xA4): ' + myPlayer.add(0xA4));
            var weaponBag = readPtr(myPlayer.add(0xA4));
            if (weaponBag) sendLog('success', 'Player', '  weaponBag (武器背包) → ' + weaponBag);
            else sendLog('warning', 'Player', '  weaponBag (武器背包) = null');

            var cameraManager = readPtr(myPlayer.add(0x48));
            if (cameraManager) sendLog('success', 'Player', '  cameraManager (相机管理器) → ' + cameraManager);

            var recoil = readPtr(myPlayer.add(0x54));
            if (recoil) sendLog('success', 'Player', '  recoil (后坐力) → ' + recoil);

            var characterContainer = readPtr(myPlayer.add(0x58));
            if (characterContainer) sendLog('success', 'Player', '  characterContainer (角色容器) → ' + characterContainer);

            var currentCharacter = readPtr(myPlayer.add(0x5C));
            if (currentCharacter) sendLog('success', 'Player', '  currentCharacter (当前角色模型) → ' + currentCharacter);

            var velData = readPtr(myPlayer.add(0x90));
            if (velData) sendLog('success', 'Player', '  velData (速度数据) → ' + velData);

            var input = readPtr(myPlayer.add(0x9C));
            if (input) sendLog('success', 'Player', '  input (输入) → ' + input);

            var nanoRoleSelect = readPtr(myPlayer.add(0xA8));
            if (nanoRoleSelect) {
                sendLog('success', 'Player', '  nanoRoleSelect (纳米角色选择) → ' + nanoRoleSelect);
                
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【NanoRoleSelect 子节点】(纳米角色选择)');
                
                var owner = readPtr(nanoRoleSelect.add(0x8));
                if (owner) sendLog('success', 'NanoRoleSelect', '  owner (所有者Player) → ' + owner);
                
                var selection = readInt(nanoRoleSelect.add(0x14));
                sendLog('info', 'Struct', '  selection (选择)=' + selection);
            }

            var nano4TData = readPtr(myPlayer.add(0xAC));
            if (nano4TData) sendLog('success', 'Player', '  nano4TData (纳米4T数据) → ' + nano4TData);

            var skills = readPtr(myPlayer.add(0xB0));
            if (skills) sendLog('success', 'Player', '  skills (技能系统) → ' + skills);

            var modelInfo = readPtr(myPlayer.add(0xB4));
            if (modelInfo) sendLog('success', 'Player', '  modelInfo (模型信息) → ' + modelInfo);

            if (weaponBag) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【WeaponBag 子节点】(武器背包)');

                var available = readPtr(weaponBag.add(0x20));
                if (available) sendLog('success', 'WeaponBag', '  available[] (可用槽位) → ' + available);

                var weaponID = readPtr(weaponBag.add(0x24));
                if (weaponID) sendLog('success', 'WeaponBag', '  weaponID[][] (武器ID) → ' + weaponID);
            }

            if (healthData) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【HealthData 子节点】(生命数据)');

                var currentHealth = readPtr(healthData.add(0x8));
                if (currentHealth) sendLog('success', 'HealthData', '  currentHealth (当前生命) → ' + currentHealth);

                var maxHealth = readPtr(healthData.add(0x1C));
                if (maxHealth) sendLog('success', 'HealthData', '  maxHealth (最大生命) → ' + maxHealth);

                var tempHealth = readPtr(healthData.add(0x30));
                if (tempHealth) sendLog('success', 'HealthData', '  tempHealth (临时生命) → ' + tempHealth);
            }

            if (clientData) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【ClientData 子节点】(客户端数据)');

                var wpnBags = readPtr(clientData.add(0xC));
                if (wpnBags) sendLog('success', 'ClientData', '  wpnBags (武器背包数组) → ' + wpnBags);

                var itemList = readPtr(clientData.add(0x28));
                if (itemList) sendLog('success', 'ClientData', '  itemList (物品列表) → ' + itemList);
            }

            if (playerData) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【PlayerData 子节点】(玩家数据)');

                var multiKillTimer = readPtr(playerData.add(0x10));
                if (multiKillTimer) sendLog('success', 'PlayerData', '  multiKillTimer (连杀计时器) → ' + multiKillTimer);

                var zoomSprite = readPtr(playerData.add(0x2C));
                if (zoomSprite) sendLog('success', 'PlayerData', '  zoomSprite (缩放精灵) → ' + zoomSprite);

                var kill = readPtr(playerData.add(0x4C));
                if (kill) sendLog('success', 'PlayerData', '  kill (击杀数) → ' + kill);

                var death = readPtr(playerData.add(0x50));
                if (death) sendLog('success', 'PlayerData', '  death (死亡数) → ' + death);

                var survival = readPtr(playerData.add(0x54));
                if (survival) sendLog('success', 'PlayerData', '  survival (存活数) → ' + survival);

                var score = readPtr(playerData.add(0x58));
                if (score) sendLog('success', 'PlayerData', '  score (分数) → ' + score);

                var aceSign = readPtr(playerData.add(0x5C));
                if (aceSign) sendLog('success', 'PlayerData', '  aceSign (王牌标志) → ' + aceSign);

                var nanoRole = readPtr(playerData.add(0x60));
                if (nanoRole) sendLog('success', 'PlayerData', '  nanoRole (纳米角色) → ' + nanoRole);
            }

            if (skills) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【PlayerSkills 子节点】(技能系统)');

                var allSkills = readPtr(skills.add(0x8));
                if (allSkills) sendLog('success', 'PlayerSkills', '  all[] (所有技能数组) → ' + allSkills);
            }

            if (nano4TData) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【Nano4T_Data 子节点】(纳米4T数据)');

                var humanLayer = readPtr(nano4TData.add(0x8));
                if (humanLayer) sendLog('success', 'Nano4T_Data', '  humanLayer (人类层数) → ' + humanLayer);

                var nanoLayer = readPtr(nano4TData.add(0xC));
                if (nanoLayer) sendLog('success', 'Nano4T_Data', '  nanoLayer (纳米层数) → ' + nanoLayer);

                var pickUpBoxCount = readPtr(nano4TData.add(0x10));
                if (pickUpBoxCount) sendLog('success', 'Nano4T_Data', '  pickUpBoxCount (拾取箱子计数) → ' + pickUpBoxCount);
            }

            if (wpns) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【PlayerWeapons 子节点】(武器系统)');

                var all = readPtr(wpns.add(0xC));
                if (all) {
                    var allLen = getArrayLength(all);
                    sendLog('success', 'PlayerWeapons', '  all[] (所有武器列表) 长度=' + allLen + ' → ' + all);
                    
                    sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                    sendLog('info', '分类', '【WPN_* 武器实例子类】(遍历 PlayerWeapons.all[])');
                    
                    for (var w = 0; w < Math.min(allLen, 10); w++) {
                        var weaponInst = readPtr(getArrayElement(all, w, 4));
                        if (weaponInst) {
                            sendLog('success', 'WPN_*', '  all[' + w + '] → ' + weaponInst);
                        }
                    }
                }

                var inUse = readPtr(wpns.add(0x18));
                if (inUse) sendLog('success', 'PlayerWeapons', '  inUse (当前武器) → ' + inUse);

                var current = readPtr(wpns.add(0x1C));
                if (current) sendLog('success', 'PlayerWeapons', '  current[] (当前武器槽) → ' + current);

                var normal = readPtr(wpns.add(0x20));
                if (normal) sendLog('success', 'PlayerWeapons', '  normal[] (常规武器) → ' + normal);

                var special = readPtr(wpns.add(0x24));
                if (special) sendLog('success', 'PlayerWeapons', '  special[] (特殊武器) → ' + special);

                var temporaryWpn = readPtr(wpns.add(0x28));
                if (temporaryWpn) sendLog('success', 'PlayerWeapons', '  temporaryWpn (临时武器) → ' + temporaryWpn);

                var F_KeyWpn = readPtr(wpns.add(0x2C));
                if (F_KeyWpn) sendLog('success', 'PlayerWeapons', '  F_KeyWpn (F键武器) → ' + F_KeyWpn);

                var mapWpn = readPtr(wpns.add(0x30));
                if (mapWpn) sendLog('success', 'PlayerWeapons', '  mapWpn (地图武器) → ' + mapWpn);

                var Modifier_ReloadSpeed = readPtr(wpns.add(0x3C));
                if (Modifier_ReloadSpeed) sendLog('success', 'PlayerWeapons', '  Modifier_ReloadSpeed (换弹速度修正) → ' + Modifier_ReloadSpeed);

                var Modifier_KnifeRange = readPtr(wpns.add(0x40));
                if (Modifier_KnifeRange) sendLog('success', 'PlayerWeapons', '  Modifier_KnifeRange (刀范围修正) → ' + Modifier_KnifeRange);

                var Modifier_KnifeSpeed = readPtr(wpns.add(0x44));
                if (Modifier_KnifeSpeed) sendLog('success', 'PlayerWeapons', '  Modifier_KnifeSpeed (刀速度修正) → ' + Modifier_KnifeSpeed);

                if (inUse) {
                    sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                    sendLog('info', '分类', '【Weapon 子节点】(当前武器 inUse)');

                    var weaponData = readPtr(inUse.add(0x68));
                    if (weaponData) sendLog('success', 'Weapon', '  data (武器数据) → ' + weaponData);

                    var shootHitTemp = readPtr(inUse.add(0x6C));
                    if (shootHitTemp) sendLog('success', 'Weapon', '  shootHitTemp (射击命中临时) → ' + shootHitTemp);

                    var damageEventTemp = readPtr(inUse.add(0x70));
                    if (damageEventTemp) sendLog('success', 'Weapon', '  damageEventTemp (伤害事件临时) → ' + damageEventTemp);

                    var knifeHitTemp = readPtr(inUse.add(0x74));
                    if (knifeHitTemp) sendLog('success', 'Weapon', '  knifeHitTemp (刀命中临时) → ' + knifeHitTemp);

                    var bindMapTrigger = readPtr(inUse.add(0xD0));
                    if (bindMapTrigger) sendLog('success', 'Weapon', '  bindMapTrigger (绑定地图触发器) → ' + bindMapTrigger);

                    if (weaponData) {
                        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                        sendLog('info', '分类', '【WeaponData_* 武器数据子类】(武器数据)');

                        var viewData = readPtr(weaponData.add(0x18));
                        if (viewData) sendLog('success', 'WeaponData_*', '  viewData (视角数据) → ' + viewData);

                        var spriteAsset = readPtr(weaponData.add(0x4C));
                        if (spriteAsset) sendLog('success', 'WeaponData_*', '  spriteAsset (精灵资产) → ' + spriteAsset);

                        var qvMdlPrefab = readPtr(weaponData.add(0xAC));
                        if (qvMdlPrefab) sendLog('success', 'WeaponData_*', '  qvMdlPrefab (武器模型预制体) → ' + qvMdlPrefab);

                        var botControlData = readPtr(weaponData.add(0xB0));
                        if (botControlData) sendLog('success', 'WeaponData_*', '  botControlData (机器人控制数据) → ' + botControlData);

                        var components = readPtr(weaponData.add(0xB4));
                        if (components) sendLog('success', 'WeaponData_*', '  components (组件数据) → ' + components);

                        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                        sendLog('info', '分类', '【WeaponData_Gun 结构体字段】(枪械数据)');

                        var clip = readInt(weaponData.add(0xB8));
                        var ammo = readInt(weaponData.add(0xBC));
                        sendLog('info', 'Struct', '  clip (弹夹)=' + clip + ', ammo (备弹)=' + ammo);

                        var shotsPerMinute = readFloat(weaponData.add(0xCC));
                        var reloadAnimRatio = readFloat(weaponData.add(0xD4));
                        sendLog('info', 'Struct', '  shotsPerMinute (射速)=' + shotsPerMinute + ', reloadAnimRatio (换弹动画比例)=' + reloadAnimRatio);

                        var range = readFloat(weaponData.add(0x148));
                        var ammoDamage = readFloat(weaponData.add(0x14C));
                        sendLog('info', 'Struct', '  range (射程)=' + range + ', ammoDamage (弹药伤害)=' + ammoDamage);

                        dumpChangeMovingRealSize(weaponData.add(0x100), '  changeMovingRealSize (移动准星变化)');
                        dumpZoomAction(weaponData.add(0x1B0), '  zoomAction (缩放动作)');

                        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                        sendLog('info', '分类', '【WeaponData_Gun 数组字段】(枪械数据数组)');

                        var perturbMin = readPtr(weaponData.add(0xF8));
                        if (perturbMin) {
                            var len = getArrayLength(perturbMin);
                            sendLog('success', 'Array', '  perturbMin[] (最小散布) 长度=' + len + ' → ' + perturbMin);
                            for (var i = 0; i < Math.min(len, 3); i++) {
                                var elem = getArrayElement(perturbMin, i, 0x14);
                                if (elem) dumpPostureFloat(elem, '    perturbMin[' + i + ']');
                            }
                        }

                        var perturbMax = readPtr(weaponData.add(0xFC));
                        if (perturbMax) {
                            var len = getArrayLength(perturbMax);
                            sendLog('success', 'Array', '  perturbMax[] (最大散布) 长度=' + len + ' → ' + perturbMax);
                        }

                        var fullReactYaw = readPtr(weaponData.add(0x134));
                        if (fullReactYaw) {
                            var len = getArrayLength(fullReactYaw);
                            sendLog('success', 'Array', '  fullReactYaw[] (完整后坐力偏航) 长度=' + len + ' → ' + fullReactYaw);
                        }
                    }
                }
            }

            if (currentCharacter) {
                sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
                sendLog('info', '分类', '【CharacterModel 子节点】(角色模型)');

                var characterAnimator = readPtr(currentCharacter.add(0x48));
                if (characterAnimator) sendLog('success', 'CharacterModel', '  characterAnimator (角色动画器) → ' + characterAnimator);

                var handAnimator = readPtr(currentCharacter.add(0x4C));
                if (handAnimator) sendLog('success', 'CharacterModel', '  handAnimator (手部动画器) → ' + handAnimator);

                var characterEffect = readPtr(currentCharacter.add(0x50));
                if (characterEffect) sendLog('success', 'CharacterModel', '  characterEffect (角色特效) → ' + characterEffect);

                var cvRenderers = readPtr(currentCharacter.add(0x54));
                if (cvRenderers) sendLog('success', 'CharacterModel', '  cvRenderers (渲染器数组) → ' + cvRenderers);

                var spine = readPtr(currentCharacter.add(0x5C));
                if (spine) sendLog('success', 'CharacterModel', '  spine (脊柱) → ' + spine);

                var spine1 = readPtr(currentCharacter.add(0x60));
                if (spine1) sendLog('success', 'CharacterModel', '  spine1 (脊柱1) → ' + spine1);

                var neck = readPtr(currentCharacter.add(0x64));
                if (neck) sendLog('success', 'CharacterModel', '  neck (颈部) → ' + neck);

                var helmet = readPtr(currentCharacter.add(0x6C));
                if (helmet) sendLog('success', 'CharacterModel', '  helmet (头盔) → ' + helmet);

                var hitboxes = readPtr(currentCharacter.add(0x74));
                if (hitboxes) sendLog('success', 'CharacterModel', '  hitboxes (受击盒) → ' + hitboxes);

                var voiceAsset = readPtr(currentCharacter.add(0x80));
                if (voiceAsset) sendLog('success', 'CharacterModel', '  voiceAsset (语音资产) → ' + voiceAsset);

                var roleAsset = readPtr(currentCharacter.add(0x84));
                if (roleAsset) sendLog('success', 'CharacterModel', '  roleAsset (角色UI资产) → ' + roleAsset);

                var animSetting = readPtr(currentCharacter.add(0xA0));
                if (animSetting) sendLog('success', 'CharacterModel', '  animSetting (动画设置) → ' + animSetting);

                var bindQvMdl = readPtr(currentCharacter.add(0xB4));
                if (bindQvMdl) sendLog('success', 'CharacterModel', '  bindQvMdl (绑定武器模型) → ' + bindQvMdl);
            }
        } else {
            sendLog('warning', 'Player', 'myPlayer (我的玩家) 未找到');
        }
    }

    if (modeBase) {
        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【ModeBase 子节点】(模式基类)');

        var mb = modeBase;

        var scoreBoardImage = readPtr(mb.add(0x1C));
        if (scoreBoardImage) sendLog('success', 'ModeBase', 'scoreBoardImage (计分板图像) → ' + scoreBoardImage);

        var scoreText_L = readPtr(mb.add(0x24));
        if (scoreText_L) sendLog('success', 'ModeBase', 'scoreText_L (左方分数文本) → ' + scoreText_L);

        var scoreText_R = readPtr(mb.add(0x28));
        if (scoreText_R) sendLog('success', 'ModeBase', 'scoreText_R (右方分数文本) → ' + scoreText_R);

        var roundText_T = readPtr(mb.add(0x2C));
        if (roundText_T) sendLog('success', 'ModeBase', 'roundText_T (回合文本T) → ' + roundText_T);

        var roundText_C = readPtr(mb.add(0x30));
        if (roundText_C) sendLog('success', 'ModeBase', 'roundText_C (回合文本C) → ' + roundText_C);

        var timeText_M = readPtr(mb.add(0x3C));
        if (timeText_M) sendLog('success', 'ModeBase', 'timeText_M (时间文本M) → ' + timeText_M);

        var timeText_S = readPtr(mb.add(0x40));
        if (timeText_S) sendLog('success', 'ModeBase', 'timeText_S (时间文本S) → ' + timeText_S);

        var rectContainer = readPtr(mb.add(0x58));
        if (rectContainer) sendLog('success', 'ModeBase', 'rectContainer (矩形容器) → ' + rectContainer);

        var playerRectPrefab = readPtr(mb.add(0x5C));
        if (playerRectPrefab) sendLog('success', 'ModeBase', 'playerRectPrefab (玩家矩形预制体) → ' + playerRectPrefab);

        var playerRectPool = readPtr(mb.add(0x60));
        if (playerRectPool) sendLog('success', 'ModeBase', 'playerRectPool (玩家矩形池) → ' + playerRectPool);

        var playerRect_BL = readPtr(mb.add(0x64));
        if (playerRect_BL) sendLog('success', 'ModeBase', 'playerRect_BL (黑名单玩家矩形) → ' + playerRect_BL);

        var playerRect_GR = readPtr(mb.add(0x68));
        if (playerRect_GR) sendLog('success', 'ModeBase', 'playerRect_GR (全球风险玩家矩形) → ' + playerRect_GR);

        var mb_myPlayer = readPtr(mb.add(0x6C));
        if (mb_myPlayer) sendLog('success', 'ModeBase', 'myPlayer (我的玩家) → ' + mb_myPlayer);

        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【ModeBase 子类字段】(纳米模式子类)');

        var terminatorMsg = readPtr(mb.add(0xB8));
        if (terminatorMsg) sendLog('success', 'Mode_Nano4', 'terminatorMsg (终结者消息) → ' + terminatorMsg);

        var characterMark = readPtr(mb.add(0xBC));
        if (characterMark) sendLog('success', 'Mode_Nano4', 'characterMark (角色标记) → ' + characterMark);

        var humanGauge = readPtr(mb.add(0xC0));
        if (humanGauge) sendLog('success', 'Mode_Nano4', 'humanGauge (人类计量条) → ' + humanGauge);

        var becomeHeroKeyTip = readPtr(mb.add(0xC4));
        if (becomeHeroKeyTip) sendLog('success', 'Mode_Nano4', 'becomeHeroKeyTip (成为英雄按键提示) → ' + becomeHeroKeyTip);

        var eventTip = readPtr(mb.add(0xBC));
        if (eventTip && !characterMark) sendLog('success', 'Mode_Nano6', 'eventTip (事件提示) → ' + eventTip);

        var levelUpTip = readPtr(mb.add(0xC0));
        if (levelUpTip && !humanGauge) sendLog('success', 'Mode_Nano6', 'levelUpTip (升级提示) → ' + levelUpTip);

        var thermalVisionIcon = readPtr(mb.add(0xCC));
        if (thermalVisionIcon) sendLog('success', 'Mode_Nano6', 'thermalVisionIcon (热视觉图标) → ' + thermalVisionIcon);

        var skillTip = readPtr(mb.add(0xD0));
        if (skillTip) sendLog('success', 'Mode_Nano6', 'skillTip (技能提示) → ' + skillTip);

        var nanoClothCountUI = readPtr(mb.add(0xD4));
        if (nanoClothCountUI) sendLog('success', 'Mode_Nano6', 'nanoClothCount (纳米布料计数) → ' + nanoClothCountUI);

        sendLog('info', '分类', '═══════════════════════════════════════════════════════════');
        sendLog('info', '分类', '【Mode_Nano4_Terminator 子类字段】(纳米4终结者模式)');

        var realAsset = readPtr(mb.add(0xCC));
        if (realAsset) sendLog('success', 'Mode_Nano4T', 'realAsset (真实资产) → ' + realAsset);

        var upgradeBoxTip = readPtr(mb.add(0xD0));
        if (upgradeBoxTip) sendLog('success', 'Mode_Nano4T', 'upgradeBoxTip (升级箱提示) → ' + upgradeBoxTip);

        var nanoItemTip = readPtr(mb.add(0xD4));
        if (nanoItemTip) sendLog('success', 'Mode_Nano4T', 'nanoItemTip (纳米物品提示) → ' + nanoItemTip);

        var attributeAsset = readPtr(mb.add(0xD8));
        if (attributeAsset) sendLog('success', 'Mode_Nano4T', 'attributeAsset (属性资产) → ' + attributeAsset);

        var hud_Attribute = readPtr(mb.add(0xDC));
        if (hud_Attribute) sendLog('success', 'Mode_Nano4T', 'hud_Attribute (属性HUD) → ' + hud_Attribute);

        var attribute_Nano = readPtr(mb.add(0xE0));
        if (attribute_Nano) sendLog('success', 'Mode_Nano4T', 'attribute_Nano (纳米属性) → ' + attribute_Nano);

        var attribute_Human = readPtr(mb.add(0xE4));
        if (attribute_Human) sendLog('success', 'Mode_Nano4T', 'attribute_Human (人类属性) → ' + attribute_Human);

        var tombstonePool = readPtr(mb.add(0xE8));
        if (tombstonePool) sendLog('success', 'Mode_Nano4T', 'tombstonePool (墓碑池) → ' + tombstonePool);
    }

    sendLog('info', '系统', '实例地址获取完成');
})();
