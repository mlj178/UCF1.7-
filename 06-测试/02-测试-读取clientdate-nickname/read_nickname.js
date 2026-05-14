(function () {
    'use strict';

    function log(level, module, message) {
        console.log('[' + level + '][' + module + '] ' + message);
        try { send({ type: 'log', level: level, module: module, message: message }); } catch (e) {}
    }

    var gameAssembly = null;
    var tryCount = 0;
    var base = null;

    var waitTimer = setInterval(function () {
        gameAssembly = Process.findModuleByName('GameAssembly.dll');
        if (gameAssembly) {
            clearInterval(waitTimer);
            base = gameAssembly.base;
            log('info', '系统', 'GameAssembly.dll: base=' + base);
            onReady();
        } else if (++tryCount > 30) {
            clearInterval(waitTimer);
            log('error', '系统', '等待超时 30 秒，未找到 GameAssembly.dll');
        }
    }, 1000);

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch (e) { return null; }
    }

    function onReady() {
        var RVA_PLAYER_IS_MY = 0xB55FD0;
        var myPlayerPtr = null;
        var inst = {};

        log('info', '系统', '正在 Hook Player$$get_isMyPlayer ...');

        try {
            var addrIsMy = base.add(RVA_PLAYER_IS_MY);
            var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

            Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
                try {
                    var result = origIsMy(playerPtr, methodInfo);
                    if (playerPtr && !playerPtr.isNull() && result && !myPlayerPtr) {
                        myPlayerPtr = playerPtr;
                        inst.player = playerPtr;
                        setTimeout(function () { runAllMethods(inst); }, 2000);
                    }
                    return result;
                } catch (e) { return false; }
            }, 'bool', ['pointer', 'pointer']));

            log('success', '系统', 'Player$$get_isMyPlayer Hook 成功，等待玩家出现...');
        } catch (e) {
            log('error', '系统', 'Player$$get_isMyPlayer Hook 失败: ' + e);
        }

        function getClientData(inst) {
            if (!inst.player) return null;
            var cd = readPtr(inst.player.add(0x94));
            if (cd) inst.clientData = cd;
            return cd;
        }

        function method1_directMemory(inst) {
            var cd = getClientData(inst);
            if (!cd) return { ok: false, msg: 'ClientData 实例为空' };
            try {
                var strObj = readPtr(cd.add(0x10));
                if (!strObj) return { ok: false, msg: 'nickName 字段为空' };
                var len = strObj.add(0x08).readS32();
                if (len < 0 || len > 500) return { ok: false, msg: '长度异常: ' + len };
                var text = strObj.add(0x0C).readUtf16String(len * 2);
                return { ok: true, value: text, detail: { strObj: strObj, len: len } };
            } catch (e) {
                return { ok: false, msg: e.toString() };
            }
        }

        function method2_il2cppBridge(inst) {
            try {
                if (typeof Il2Cpp === 'undefined') {
                    return { ok: false, msg: 'Il2Cpp Bridge 插件不可用' };
                }
                var clientDataClass = Il2Cpp.Domain.assembly('Assembly-CSharp').image.class('ClientData');
                var mine = clientDataClass.field('mine').value;
                if (mine && !mine.isNull()) {
                    var nickname = mine.field('nickName').value;
                    return { ok: true, value: nickname.toString(), via: 'mine' };
                }
                var cd = inst.clientData;
                if (cd) {
                    var obj = new Il2Cpp.Object(cd);
                    var nickname = obj.field('nickName').value;
                    return { ok: true, value: nickname.toString(), via: 'directWrap' };
                }
                return { ok: false, msg: 'ClientData.mine 为空，且 inst.clientData 未捕获' };
            } catch (e) {
                return { ok: false, msg: e.toString() };
            }
        }

        var RVA_GET_NICKNAME = 0xB50810;
        var hookInstalled = false;
        var myNicknameCache = null;

        function method3_hookGetter(inst) {
            if (hookInstalled) return { ok: true, msg: 'Hook 已安装，无需重复安装' };
            try {
                var addr = base.add(RVA_GET_NICKNAME);
                Interceptor.attach(addr, {
                    onEnter: function (args) {
                        this.self = inst.clientData && args[0].equals(inst.clientData);
                    },
                    onLeave: function (retval) {
                        if (!this.self) return;
                        if (!retval || retval.isNull()) return;
                        try {
                            var len = retval.add(0x08).readS32();
                            if (len < 0 || len > 500) return;
                            var text = retval.add(0x0C).readUtf16String(len * 2);
                            if (text !== myNicknameCache) {
                                myNicknameCache = text;
                                log('success', '方案三(Hook·已筛选)', '【你自己】nickname = "' + text + '"');
                            }
                        } catch (e) {}
                    }
                });
                hookInstalled = true;

                // 安装后立即用方案一的方式读一次，确保马上能看到结果
                var nickname = method1_directMemory(inst);
                if (nickname.ok) {
                    myNicknameCache = nickname.value;
                    log('success', '方案三(Hook)', '首次读取 nickname = "' + nickname.value + '"');
                }

                return { ok: true, msg: 'get_nickName Hook 安装成功（已输出当前昵称，后续变更自动监控）' };
            } catch (e) {
                return { ok: false, msg: e.toString() };
            }
        }

        function runAllMethods(inst) {
            var cd = getClientData(inst);
            if (!cd) {
                log('error', '系统', '无法获取 ClientData 实例地址');
                return;
            }

            log('info', '', '');
            log('success', '╔════════════════════════════════════════════════════════════════╗', '');
            log('success', '║          ClientData.nickname  三种读取方案对比               ║', '');
            log('success', '╚════════════════════════════════════════════════════════════════╝', '');
            log('info', '系统', 'ClientData 实例地址: ' + cd);
            log('info', '系统', 'nickName 字段地址:   ' + cd.add(0x10) + ' (cd+0x10)');
            log('info', '', '');

            log('info', '━━━', '方案一：直接读内存（推荐 ★★★★★）');
            var r1 = method1_directMemory(inst);
            if (r1.ok) {
                log('success', '方案一', 'nickname = "' + r1.value + '"');
                log('info', '方案一', '  String对象@' + r1.detail.strObj + ', 字符长度=' + r1.detail.len);
            } else {
                log('error', '方案一', '失败: ' + r1.msg);
            }

            log('info', '━━━', '方案二：Il2Cpp Bridge 字段访问');
            var r2 = method2_il2cppBridge(inst);
            if (r2.ok) {
                log('success', '方案二', 'nickname = "' + r2.value + '" (途径: ' + r2.via + ')');
            } else {
                log('error', '方案二', '失败: ' + r2.msg);
            }

            log('info', '━━━', '方案三：Hook get_nickName() 返回值（已筛选）');
            var r3 = method3_hookGetter(inst);
            if (r3.ok) {
                log('success', '方案三', r3.msg);
            } else {
                log('error', '方案三', '失败: ' + r3.msg);
            }

            log('info', '', '');
            log('success', '┌────────────────────────────────────────────────────────────────┐', '');
            log('success', '│  方案对比总结                                                 │', '');
            log('success', '├────────────────────────────────────────────────────────────────┤', '');
            log('info',    '│  ★ 方案一(直接读内存) → ' +
                (r1.ok ? '✅ 成功 "' + r1.value + '"' : '❌ ' + r1.msg), '');
            log('info',    '│  ☆ 方案二(Bridge)     → ' +
                (r2.ok ? '✅ 成功 "' + r2.value + '"' : '❌ ' + r2.msg), '');
            log('info',    '│  ☆ 方案三(Hook)       → ' +
                (r3.ok ? '✅ 已安装，等待调用' : '❌ ' + r3.msg), '');
            log('success', '└────────────────────────────────────────────────────────────────┘', '');
            log('info', '', '');
            log('info', '系统', '命令: readNow() - 重新读取 nickname');
        }

        globalThis.readNow = function () {
            if (!inst.clientData) {
                log('warn', '系统', '尚未获取到 ClientData 实例');
                return;
            }
            var r1 = method1_directMemory(inst);
            if (r1.ok) {
                log('success', '刷新', 'nickname = "' + r1.value + '"');
            } else {
                log('error', '刷新', '读取失败: ' + r1.msg);
            }
        };

        globalThis.getInst = function () {
            log('info', '系统', 'Player:     ' + (inst.player || 'null'));
            log('info', '系统', 'ClientData: ' + (inst.clientData || 'null'));
            log('info', '系统', '方法三Hook: ' + (hookInstalled ? '已安装' : '未安装'));
        };

        log('success', '系统', '✅ read_nickname.js 已加载');
        log('info', '系统', '进入游戏后自动运行三种方案并输出结果');
        log('info', '系统', '命令: readNow() - 重新读取 nickname（方案一）');
        log('info', '系统', '命令: getInst() - 查看当前实例地址');
    }

    setInterval(function () {}, 10000);
})();
