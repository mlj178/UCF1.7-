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
            send({type: "log", level: "info", category: "Test", message: "static_fields[0x00] myPlayer: " + rp(sf, 0x00)});
            send({type: "log", level: "info", category: "Test", message: "static_fields[0x04] gameMode: " + sf.add(0x04).readS32()});
        }

        send({type: "log", level: "success", category: "完成", message: "验证完成"});
    }
}
