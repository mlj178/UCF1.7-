var moduleBase = null;
var module = Process.findModuleByName("GameAssembly.dll");
if (module) {
    moduleBase = module.base;
    send({type: "log", level: "success", category: "初始化", message: "GameAssembly.dll 基址: " + moduleBase});
} else {
    send({type: "log", level: "error", category: "初始化", message: "未找到 GameAssembly.dll"});
}

var GameManager_TypeInfo_RVA = 0x0E2933C;

function rp(addr, off) {
    try { return addr.add(off).readPointer(); }
    catch (e) { return null; }
}

if (!moduleBase) {
    send({type: "log", level: "error", category: "完成", message: "中止"});
} else {
    var typeInfoSlot = moduleBase.add(GameManager_TypeInfo_RVA);
    var klass = rp(typeInfoSlot, 0);

    send({type: "log", level: "success", category: "TypeInfo", message: "槽地址: " + typeInfoSlot + " → klass: " + klass});

    if (!klass || klass.isNull()) {
        send({type: "log", level: "error", category: "验证", message: "klass 为空"});
    } else {
        send({type: "log", level: "info", category: "分类", message: "Il2CppClass_1 (基于 klass)"});

        var image = klass.add(0x00).readU32();
        send({type: "log", level: "info", category: "Field", message: "image: 0x" + image.toString(16)});

        var name_ptr = rp(klass, 0x08);
        if (name_ptr && !name_ptr.isNull()) {
            try {
                send({type: "log", level: "success", category: "验证", message: "类名: " + name_ptr.readCString()});
            } catch (e) {
                send({type: "log", level: "error", category: "验证", message: "读取类名失败"});
            }
        }

        var namespaze_ptr = rp(klass, 0x0C);
        if (namespaze_ptr && !namespaze_ptr.isNull()) {
            try {
                send({type: "log", level: "success", category: "验证", message: "命名空间: " + namespaze_ptr.readCString()});
            } catch (e) {
                send({type: "log", level: "error", category: "验证", message: "读取命名空间失败"});
            }
        }

        var sf = rp(klass, 0x5C);
        var rgctx = rp(klass, 0x60);
        send({type: "log", level: "info", category: "Field", message: "static_fields: " + sf});
        send({type: "log", level: "info", category: "Field", message: "rgctx_data: " + rgctx});

        var Il2CppClass_2_base = klass.add(0x64);
        var cctor_finished = Il2CppClass_2_base.add(0x10).readU32();
        var static_fields_size = Il2CppClass_2_base.add(0x2C).readU32();
        var bitflags2 = Il2CppClass_2_base.add(0x57).readU8();

        send({type: "log", level: "info", category: "Field", message: "cctor_finished: " + cctor_finished});
        send({type: "log", level: "success", category: "Field", message: "static_fields_size: 0x" + static_fields_size.toString(16)});
        send({type: "log", level: "info", category: "Field", message: "bitflags2: " + bitflags2});

        send({type: "log", level: "info", category: "分类", message: "扫描 klass 上 static_fields 偏移 0x50~0x70"});

        for (var offset = 0x50; offset <= 0x70; offset += 4) {
            try {
                var value = klass.add(offset).readU32();
                var mark = (offset === 0x5C) ? " ← static_fields" : "";
                send({type: "log", level: offset === 0x5C ? "success" : "info", category: "Scan",
                    message: "klass+0x" + offset.toString(16) + ": 0x" + value.toString(16) + mark});
            } catch (e) {
                send({type: "log", level: "error", category: "Scan", message: "klass+0x" + offset.toString(16) + ": 读取失败"});
            }
        }

        if (sf && !sf.isNull()) {
            send({type: "log", level: "info", category: "分类", message: "═══════════════════════════════════════"});
            send({type: "log", level: "info", category: "分类", message: "【GameManager 所有静态字段 (共27个)】"});

            function readField(offset, type, name) {
                var addr = sf.add(offset);
                var value;
                if (type === 'ptr') value = rp(sf, offset);
                else if (type === 'int') value = addr.readS32();
                else if (type === 'bool') value = addr.readU8();
                else if (type === 'float') value = addr.readFloat();
                send({type: "log", level: "success", category: "Field",
                    message: name + " (0x" + offset.toString(16).toUpperCase() + ") 地址: " + addr + ". 数值: " + value});
            }

            readField(0x00, 'ptr', 'myPlayer');
            readField(0x04, 'int', 'gameMode');
            readField(0x08, 'int', 'weaponLimited');
            readField(0x0C, 'bool', 'revengeEnable');
            readField(0x10, 'ptr', 'gameModePrefab');
            readField(0x14, 'ptr', 'ace');
            readField(0x18, 'ptr', 'WpnDictionary');
            readField(0x1C, 'ptr', 'WpnDataDictionary');
            readField(0x20, 'bool', 'gameRoundOver');
            readField(0x24, 'ptr', 'DamageEvent_InvalidCheck');
            readField(0x28, 'ptr', 'DamageEvent_PreCal');
            readField(0x2C, 'ptr', 'DamageEvent_PostCal');
            readField(0x30, 'ptr', 'DamageEvent_Post');
            readField(0x34, 'ptr', 'DeathEvent_Observers');
            readField(0x38, 'ptr', 'DeathEvent_ForGameRule');
            readField(0x3C, 'ptr', 'firstAndLastKillChecker');
            readField(0x40, 'ptr', 'NewPlayerJoinEvent');
            readField(0x44, 'ptr', 'PlayerSpawnEvent');
            readField(0x48, 'ptr', 'MyPlayerJoinEvent');
            readField(0x4C, 'ptr', 'MyPlayerSpawnEvent');
            readField(0x50, 'ptr', 'MyPlayerCasueDamageEvent');
            readField(0x54, 'ptr', 'MyPlayerGetDamageEvent');
            readField(0x58, 'ptr', 'MyPlayerKillEvent');
            readField(0x5C, 'ptr', 'MyPlayerDeathEvent');
            readField(0x60, 'ptr', 'NewGameRoundStart');
            readField(0x64, 'ptr', 'GetGrenadeFromBag');
            readField(0x68, 'float', 'dropWpnRecycleTime');
        }

        send({type: "log", level: "info", category: "分类", message: "═══════════════════════════════════════"});
        send({type: "log", level: "info", category: "分类", message: "【ModeBase 静态字段 (共4个)】"});

        var mbTypeInfoRVA = 0xE2CC54;
        var mbTypeInfoSlot = moduleBase.add(mbTypeInfoRVA);
        var mbKlass = rp(mbTypeInfoSlot, 0);
        send({type: "log", level: "info", category: "MB验证", message: "TypeInfo: " + mbTypeInfoSlot + " → klass: " + mbKlass});

        var name_ptr_mb = rp(mbKlass, 0x08);
        if (name_ptr_mb && !name_ptr_mb.isNull()) {
            try {
                send({type: "log", level: "success", category: "MB验证", message: "类名: " + name_ptr_mb.readCString()});
            } catch (e) {}
        }

        var mbIl2CppClass_2_base = mbKlass.add(0x64);
        var mb_cctor_finished = mbIl2CppClass_2_base.add(0x10).readU32();
        var mb_bitflags2 = mbIl2CppClass_2_base.add(0x57).readU8();
        var mb_needInit = (mb_bitflags2 & 4) !== 0 && mb_cctor_finished === 0;
        send({type: "log", level: "info", category: "MB验证", message: "cctor_finished=" + mb_cctor_finished + " bitflags2=" + mb_bitflags2 + " needInit=" + mb_needInit});

        var mbSf = rp(mbKlass, 0x5C);
        send({type: "log", level: "info", category: "MB验证", message: "static_fields(初始化前): " + mbSf});

        if (mb_needInit) {
            try {
                var initFn = new NativeFunction(moduleBase.add(0x108970), 'void', ['pointer']);
                initFn(mbKlass);
                send({type: "log", level: "success", category: "MB验证", message: "il2cpp_runtime_class_init 完成"});
                mbSf = rp(mbKlass, 0x5C);
                send({type: "log", level: "success", category: "MB验证", message: "static_fields(初始化后): " + mbSf});
            } catch (e) {
                send({type: "log", level: "error", category: "MB验证", message: "class_init 失败: " + e.message});
            }
        }

        if (mbSf && !mbSf.isNull()) {
            function readMBField(offset, type, name) {
                var addr = mbSf.add(offset);
                var value;
                if (type === 'ptr') value = rp(mbSf, offset);
                else if (type === 'int') value = addr.readS32();
                else if (type === 'bool') value = addr.readU8();
                else if (type === 'float') value = addr.readFloat();
                send({type: "log", level: "success", category: "MBField",
                    message: name + " (0x" + offset.toString(16).toUpperCase() + ") 地址: " + addr + ". 数值: " + value});
            }

            readMBField(0x00, 'int', 'targetRound');
            readMBField(0x04, 'int', 'targetScore');
            readMBField(0x08, 'int', 'gameTime.x');
            readMBField(0x0C, 'int', 'gameTime.y');
            readMBField(0x10, 'float', 'respawnTime');
        } else {
            send({type: "log", level: "error", category: "MB验证", message: "static_fields 仍为 null，初始化后仍未分配"});
        }

        send({type: "log", level: "info", category: "分类", message: "═══════════════════════════════════════"});
        send({type: "log", level: "info", category: "分类", message: "【ModeBase_Nano 静态字段 (共9个)】"});

        var mbnTypeInfoRVA = 0xE2CC74;
        var mbnTypeInfoSlot = moduleBase.add(mbnTypeInfoRVA);
        var mbnKlass = rp(mbnTypeInfoSlot, 0);
        send({type: "log", level: "info", category: "MBN验证", message: "TypeInfo: " + mbnTypeInfoSlot + " → klass: " + mbnKlass});

        var name_ptr_mbn = rp(mbnKlass, 0x08);
        if (name_ptr_mbn && !name_ptr_mbn.isNull()) {
            try {
                send({type: "log", level: "success", category: "MBN验证", message: "类名: " + name_ptr_mbn.readCString()});
            } catch (e) {}
        }

        var mbnIl2CppClass_2_base = mbnKlass.add(0x64);
        var mbn_cctor_finished = mbnIl2CppClass_2_base.add(0x10).readU32();
        var mbn_bitflags2 = mbnIl2CppClass_2_base.add(0x57).readU8();
        var mbn_needInit = (mbn_bitflags2 & 4) !== 0 && mbn_cctor_finished === 0;
        send({type: "log", level: "info", category: "MBN验证", message: "cctor_finished=" + mbn_cctor_finished + " bitflags2=" + mbn_bitflags2 + " needInit=" + mbn_needInit});

        var mbnSf = rp(mbnKlass, 0x5C);
        send({type: "log", level: "info", category: "MBN验证", message: "static_fields(初始化前): " + mbnSf});

        if (mbn_needInit) {
            try {
                var initFn2 = new NativeFunction(moduleBase.add(0x108970), 'void', ['pointer']);
                initFn2(mbnKlass);
                send({type: "log", level: "success", category: "MBN验证", message: "il2cpp_runtime_class_init 完成"});
                mbnSf = rp(mbnKlass, 0x5C);
                send({type: "log", level: "success", category: "MBN验证", message: "static_fields(初始化后): " + mbnSf});
            } catch (e) {
                send({type: "log", level: "error", category: "MBN验证", message: "class_init 失败: " + e.message});
            }
        }

        if (mbnSf && !mbnSf.isNull()) {
            function readMBNField(offset, type, name) {
                var addr = mbnSf.add(offset);
                var value;
                if (type === 'ptr') value = rp(mbnSf, offset);
                else if (type === 'int') value = addr.readS32();
                else if (type === 'bool') value = addr.readU8();
                else if (type === 'float') value = addr.readFloat();
                send({type: "log", level: "success", category: "MBNField",
                    message: name + " (0x" + offset.toString(16).toUpperCase() + ") 地址: " + addr + ". 数值: " + value});
            }

            readMBNField(0x00, 'int', 'soldierAttackPower');
            readMBNField(0x04, 'bool', 'nanoRespawn_Melee');
            readMBNField(0x05, 'bool', 'nanoRespawn_Headshot');
            readMBNField(0x08, 'ptr', 'nanoLevelUpNeedExp');
            readMBNField(0x0C, 'int', 'BornNanoGhostHP');
            readMBNField(0x10, 'float', 'AbsorbNeedTime');
            readMBNField(0x14, 'int', 'AbsorbCheckCount');
            readMBNField(0x18, 'ptr', 'Text_GetSkill');
            readMBNField(0x1C, 'ptr', 'Tip_Infect');
        } else {
            send({type: "log", level: "error", category: "MBN验证", message: "static_fields 为 null"});
        }

        send({type: "log", level: "success", category: "完成", message: "所有字段读取完成"});
    }
}
