// ============================================================
// 自动获取 camMgr 指针（只需要移动鼠标触发一次 AddCameraRotation）
// ============================================================

var moduleBase = Process.getModuleByName("GameAssembly.dll");
var addCamRotAddr = moduleBase.add(0xB4F790);
console.log("[*] AddCameraRotation 地址: " + addCamRotAddr);

var camMgr = null;

Interceptor.attach(addCamRotAddr, {
    onEnter: function(args) {
        if (camMgr != null) return; // 已经拿到了就不重复拿

        var player = ptr(args[0]); // this
        console.log("[*] Player 实例: " + player);

        // 尝试 Player+0x48
        var mgr = player.add(0x48).readPointer();
        if (mgr.isNull()) {
            console.log("[!] Player+0x48 为空，尝试 Player+0xA0...");
            mgr = player.add(0xA0).readPointer();
        }

        if (!mgr.isNull()) {
            camMgr = mgr;
            console.log("[+] camMgr = " + camMgr);
            console.log("[*] 现在你可以在任何地方使用这个 camMgr 了。");
            // 简单验证：读一下 +0x1BC 看看是否正常
            try {
                var testVal = camMgr.add(0x1BC).readFloat();
                console.log("[*] camMgr+0x1BC = " + testVal.toFixed(4));
            } catch(e) {
                console.log("[!] 读取 camMgr+0x1BC 失败: " + e.message);
            }
        } else {
            console.log("[!] 未能获取 camMgr（两个偏移均为空）");
        }
    }
});

console.log("[*] 请轻轻移动一下鼠标（转动视角）...");