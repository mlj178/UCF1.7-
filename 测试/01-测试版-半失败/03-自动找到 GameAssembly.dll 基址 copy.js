// ============================================================
// 全自动获取 camMgr 并验证 Pitch 偏移 0x1C0
// ============================================================

var camMgr = null;
var isScanning = false;

// 1. 自动获取 GameAssembly.dll 基址
var module = Process.getModuleByName("GameAssembly.dll");
console.log("[*] GameAssembly.dll base: " + module.base);

// 2. 计算 AddCameraRotation 绝对地址
var addCamRotAddr = module.base.add(0xB4F790);
console.log("[*] AddCameraRotation address: " + addCamRotAddr);

// 3. Hook 该函数，首次调用时提取 camMgr
Interceptor.attach(addCamRotAddr, {
    onEnter: function(args) {
        if (camMgr != null) return;  // 已经拿到 camMgr 就不再处理

        // IL2CPP 成员函数，this 通常是 args[0]
        var player = ptr(args[0]);
        console.log("[*] Player instance: " + player);

        // 尝试从 Player+0x48 读取 cameraManager 字段
        try {
            camMgr = player.add(0x48).readPointer();
            console.log("[*] camMgr (from Player+0x48): " + camMgr);

            // 验证 camMgr 是否有效（简单检查：能读一个值）
            var testYaw = camMgr.add(0x1BC).readFloat();
            console.log("[*] 测试读取 camMgr+0x1BC Yaw: " + testYaw.toFixed(4));

            // 若 camMgr 为空指针则回退尝试 Player+0xA0
            if (camMgr.isNull()) {
                console.log("[!] Player+0x48 为空，尝试 Player+0xA0...");
                camMgr = player.add(0xA0).readPointer();
                console.log("[*] camMgr (from Player+0xA0): " + camMgr);
                testYaw = camMgr.add(0x1BC).readFloat();
                console.log("[*] 测试读取 camMgr+0x1BC Yaw: " + testYaw.toFixed(4));
            }

            if (!camMgr.isNull()) {
                console.log("[*] camMgr 获取成功，开始扫描 Pitch...");
                startScanning();
            } else {
                console.log("[!] 两种偏移的 camMgr 均为空，请检查偏移是否正确。");
            }
        } catch(e) {
            console.log("[!] 提取 camMgr 时出错: " + e.message);
        }
    }
});

// 4. Pitch 扫描函数
function startScanning() {
    isScanning = true;
    const YAW_OFFSET   = 0x1BC;
    const PITCH_OFFSET = 0x1C0;   // 主候选，若不符可改：0x1B8, 0x1C4, 0x1C8, 0x1D0

    console.log("[*] 开始监控视角数据...");
    console.log("[*] Yaw  偏移: 0x" + YAW_OFFSET.toString(16));
    console.log("[*] Pitch 偏移: 0x" + PITCH_OFFSET.toString(16));
    console.log("===========================================");

    var lastYaw = 0, lastPitch = 0;

    setInterval(function() {
        if (!camMgr || camMgr.isNull()) return;
        try {
            var rawYaw   = camMgr.add(YAW_OFFSET).readFloat();
            var rawPitch = camMgr.add(PITCH_OFFSET).readFloat();

            var yawDeg   = rawYaw * 180.0 / Math.PI;
            var pitchDeg = rawPitch * 180.0 / Math.PI;

            var deltaYaw   = rawYaw - lastYaw;
            var deltaPitch = rawPitch - lastPitch;
            lastYaw   = rawYaw;
            lastPitch = rawPitch;

            console.log(
                "[Yaw] raw:" + rawYaw.toFixed(4) +
                " deg:" + yawDeg.toFixed(2) + "°" +
                " Δ:" + deltaYaw.toFixed(4) +
                " | [Pitch] raw:" + rawPitch.toFixed(4) +
                " deg:" + pitchDeg.toFixed(2) + "°" +
                " Δ:" + deltaPitch.toFixed(4)
            );
        } catch(e) {
            console.log("[!] 读取内存出错: " + e.message);
        }
    }, 200);
}

console.log("[*] 等待 AddCameraRotation 被调用（移动鼠标即可触发）...");