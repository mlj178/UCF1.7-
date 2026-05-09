// getCamMgr.js
var moduleBase = Module.findBaseAddress("GameAssembly.dll"); // 注意用 Module，不是 Process
var addCamRotAddr = moduleBase.add(0xB4F790);
console.log("[*] AddCameraRotation address: " + addCamRotAddr);

var camMgr = null;

Interceptor.attach(addCamRotAddr, {
    onEnter: function(args) {
        if (camMgr != null) return;

        var player = ptr(args[0]);
        console.log("[*] Player instance: " + player);

        var mgr = player.add(0x48).readPointer();
        if (mgr.isNull()) {
            mgr = player.add(0xA0).readPointer();
        }

        if (!mgr.isNull()) {
            camMgr = mgr;
            console.log("[+] camMgr = " + camMgr);
            console.log("[*] camMgr+0x1BC test: " + camMgr.add(0x1BC).readFloat().toFixed(4));
        } else {
            console.log("[!] Failed to get camMgr");
        }
    }
});

console.log("[*] Move your mouse in game to trigger AddCameraRotation...");