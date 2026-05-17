var moduleBase = null;
var module = Process.findModuleByName("GameAssembly.dll");
if (module) {
    moduleBase = module.base;
    send({type: "log", level: "success", category: "初始化", message: "GameAssembly.dll 基址: " + moduleBase});
} else {
    send({type: "log", level: "error", category: "初始化", message: "未找到 GameAssembly.dll"});
}

var GameManager_TypeInfo_RVA = 0x0E2933C;
var il2cpp_runtime_class_init_RVA = 0x108970;
var Singleton_GM_MethodInfo_RVA = 0xE1CE64;
var Singleton_GetInstance_RVA = 0x4A8170;

function rp(addr, off) {
    try { return addr.add(off).readPointer(); }
    catch (e) { return null; }
}

if (!moduleBase) {
    send({type: "log", level: "error", category: "完成", message: "中止"});
} else {
    var typeInfoSlot = moduleBase.add(GameManager_TypeInfo_RVA);
    var klass = rp(typeInfoSlot, 0);

    send({type: "log", level: "info", category: "步骤1", message: "TypeInfo槽: " + typeInfoSlot + " → klass: " + klass});

    if (!klass || klass.isNull()) {
        send({type: "log", level: "error", category: "步骤1", message: "klass 为空，无法继续"});
    } else {
        var Il2CppClass_2_base = klass.add(0x64);
        var cctor_finished = Il2CppClass_2_base.add(0x10).readU32();
        var bitflags2 = Il2CppClass_2_base.add(0x57).readU8();
        var needInit = (bitflags2 & 4) !== 0 && cctor_finished === 0;

        send({type: "log", level: "info", category: "步骤2", message: "cctor_finished=" + cctor_finished + " bitflags2=" + bitflags2});

        var sfBefore = rp(klass, 0x5C);
        send({type: "log", level: "info", category: "步骤3", message: "static_fields(初始化前): " + sfBefore});

        if (needInit) {
            try {
                var init = new NativeFunction(moduleBase.add(il2cpp_runtime_class_init_RVA), 'void', ['pointer']);
                init(klass);
                send({type: "log", level: "success", category: "步骤4", message: "il2cpp_runtime_class_init 完成"});
            } catch (e) {
                send({type: "log", level: "error", category: "步骤4", message: "class_init 失败: " + e.message});
            }
        }

        var sf = rp(klass, 0x5C);
        send({type: "log", level: "success", category: "步骤5", message: "static_fields(初始化后): " + sf});

        if (sf && !sf.isNull()) {
            var myPlayer = rp(sf, 0x00);
            var gameMode = sf.add(0x04).readS32();
            var weaponLimited = sf.add(0x08).readS32();
            var revengeEnable = sf.add(0x0C).readU8();
            var ace = rp(sf, 0x14);

            send({type: "log", level: "info", category: "静态字段", message: "myPlayer: " + myPlayer});
            send({type: "log", level: "info", category: "静态字段", message: "gameMode: " + gameMode + " weaponLimited: " + weaponLimited});
            send({type: "log", level: "info", category: "静态字段", message: "revengeEnable: " + revengeEnable + " ace: " + ace});
        }

        try {
            var mi = rp(moduleBase, Singleton_GM_MethodInfo_RVA);
            var getInst = new NativeFunction(moduleBase.add(Singleton_GetInstance_RVA), 'pointer', ['pointer']);
            var gmInstance = getInst(mi);
            send({type: "log", level: "info", category: "单例对比", message: "Singleton.get_instance → GameManager对象: " + gmInstance});
            if (sf && !sf.isNull()) {
                send({type: "log", level: "info", category: "单例对比", message: "static_fields.myPlayer → Player对象: " + rp(sf, 0x00)});
            }
        } catch (e) {
            send({type: "log", level: "warning", category: "单例对比", message: "get_instance 失败: " + e.message});
        }

        send({type: "log", level: "success", category: "完成", message: "验证完成"});
    }
}
