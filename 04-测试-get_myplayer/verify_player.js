// verify_player.js - 验证 Player 实例是否是你
// 用法：修改 PLAYER_ADDRESS 为你在CE中找到的地址

(function () {
    'use strict';

    function sendLog(level, module, message) {
        send({ type: 'log', level: level, module: module, message: message });
    }

    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    if (!gameAssembly) {
        sendLog('error', '系统', '未找到 GameAssembly.dll');
        return;
    }

    var base = gameAssembly.base;
    var ADDR_PLAYER_IS_MY = base.add(0xB55FD0);
    var isMyPlayer = new NativeFunction(ADDR_PLAYER_IS_MY, 'bool', ['pointer', 'pointer']);

    // ⬇️ 在这里修改你在CE中找到的Player实例地址 ⬇️
    var PLAYER_ADDRESS = "0x12345678";  // ← 修改这个地址

    sendLog('info', '验证', 'Player地址: ' + PLAYER_ADDRESS);

    try {
        var playerPtr = ptr(PLAYER_ADDRESS);
        
        // 调用 isMyPlayer
        var result = isMyPlayer(playerPtr, NULL);
        
        if (result) {
            sendLog('success', '验证', '✅ 这是你的Player实例!');
        } else {
            sendLog('warn', '验证', '❌ 这是Bot或其他玩家的实例');
        }

        // 尝试读取 clientData.nickName
        try {
            // Player → clientData (偏移需要根据实际情况)
            // 从 Player_Fields 结构计算偏移
            // clientData 在 Player_Fields 中，需要先计算 Entity_Fields 大小
            
            // 简单方法：直接读取几个可能的偏移
            var offsets = [0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88, 0x90, 0x98];
            
            for (var i = 0; i < offsets.length; i++) {
                try {
                    var clientDataPtr = playerPtr.add(offsets[i]).readPointer();
                    if (clientDataPtr && !clientDataPtr.isNull()) {
                        // 尝试读取 nickName (ClientData_Fields 偏移 0x18)
                        var nickNamePtr = clientDataPtr.add(0x18).readPointer();
                        if (nickNamePtr && !nickNamePtr.isNull()) {
                            var nickName = nickNamePtr.readCString();
                            if (nickName && nickName.length > 0 && nickName.length < 50) {
                                sendLog('info', '验证', '偏移 0x' + offsets[i].toString(16) + ' - 昵称: ' + nickName);
                            }
                        }
                    }
                } catch (e) {}
            }
        } catch (e) {
            sendLog('warn', '验证', '读取昵称失败: ' + e);
        }

    } catch (e) {
        sendLog('error', '验证', '验证失败: ' + e);
    }

    // 提供手动验证函数
    globalThis.verifyPlayer = function(address) {
        try {
            var playerPtr = ptr(address);
            var result = isMyPlayer(playerPtr, NULL);
            sendLog('info', '验证', address + ' isMyPlayer = ' + result);
            return result;
        } catch (e) {
            sendLog('error', '验证', '错误: ' + e);
            return false;
        }
    };

    sendLog('success', '系统', '✅ 脚本已加载');
    sendLog('info', '系统', '用法: verifyPlayer("0x12345678")');
})();
