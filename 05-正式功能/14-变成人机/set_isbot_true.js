(function() {
    'use strict';

    const RVA_IS_MY_PLAYER  = 0xB55FD0;
    const OFF_CLIENT        = 0x94;
    const OFF_ISBOT         = 0x1C;
    const OFF_NICK          = 0x10;

    let localPlayer = null;
    let clientData = null;
    let dumped = false;
    let logCount = 0;
    const MAX_LOG = 15;

    function log(level, msg) {
        if (logCount >= MAX_LOG && level !== 'error') return;
        logCount++;
        send({ type: 'log', level: level, module: 'isBot', message: msg });
    }

    function readStr(ptr) {
        try {
            let obj = ptr.readPointer();
            if (!obj || obj.isNull()) return '?';
            let len = obj.add(-4).readS32();
            if (len < 0 || len > 64) return '?';
            return obj.readUtf8String(len);
        } catch(e) { return '?'; }
    }

    function dump() {
        if (!clientData) return;
        let bot = clientData.add(OFF_ISBOT).readU8();
        let nick = readStr(clientData.add(OFF_NICK));
        log('info', localPlayer + '|' + clientData + '|0x1C:' + bot + '|nick:' + nick);
    }

    function writeBot(val) {
        if (!clientData) return false;
        try {
            clientData.add(OFF_ISBOT).writeU8(val);
            let after = clientData.add(OFF_ISBOT).readU8();
            log('info', 'isBot=' + after + ' (写入' + val + ')');
            return true;
        } catch(e) { return false; }
    }

    let mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { log('error', 'GameAssembly.dll not found'); return; }

    let addrIsMy = mod.base.add(RVA_IS_MY_PLAYER);
    let origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

    Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
        let result = origIsMy(playerPtr, methodInfo);
        if (result && !localPlayer) {
            localPlayer = playerPtr;
            let cd = playerPtr.add(OFF_CLIENT).readPointer();
            if (cd) {
                clientData = cd;
                dumped = true;
                setTimeout(dump, 2000);
            }
        }
        return result;
    }, 'bool', ['pointer', 'pointer']));

    function modify() {
        if (writeBot(1)) return JSON.stringify({ success: true, bot: 1 });
        return JSON.stringify({ success: false });
    }

    function restore() {
        if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
        return JSON.stringify({ success: false });
    }

    function stop() {
        if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
        return JSON.stringify({ success: false });
    }

    function status() {
        return JSON.stringify({
            player: localPlayer ? localPlayer.toString() : null,
            cd: clientData ? clientData.toString() : null,
            bot: clientData ? clientData.add(OFF_ISBOT).readU8() : null
        });
    }

    rpc.exports = { modify, restore, stop, status };
    log('info', '已加载');
})();
