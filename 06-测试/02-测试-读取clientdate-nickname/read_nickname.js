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

    /** frida-il2cpp-bridge 的 Il2Cpp.perform 为异步；在 Frida 脚本里同步等待其完成 */
    function syncIl2CppPerform(block) {
        if (typeof Il2Cpp === 'undefined' || typeof Il2Cpp.perform !== 'function') {
            return block();
        }
        var st = { done: false, error: null, result: null };
        var finish = function () { st.done = true; };
        try {
            var p = Il2Cpp.perform(function () {
                st.result = block();
            });
            if (p && typeof p.then === 'function') {
                p.then(finish).catch(function (e) {
                    st.error = e;
                    finish();
                });
            } else {
                st.result = p;
                st.done = true;
            }
        } catch (e) {
            st.error = e;
            st.done = true;
        }
        for (var i = 0; i < 4000 && !st.done; i++) {
            Thread.sleep(0.01);
        }
        if (!st.done) {
            throw new Error('Il2Cpp.perform 超时(约40s)，IL2CPP 可能未初始化');
        }
        if (st.error) {
            throw st.error;
        }
        return st.result;
    }

    function il2cppValueToJs(v) {
        if (v === null || v === undefined) return '';
        if (typeof v === 'string') return v;
        try {
            if (v.content !== undefined && v.content !== null) return '' + v.content;
        } catch (e0) {}
        try { return '' + v; } catch (e1) { return ''; }
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

        function wrapClientDataInstance(klass, ptr) {
            if (!ptr) return null;
            if (typeof ptr.method === 'function' || typeof ptr.field === 'function') {
                return ptr;
            }
            var raw = ptr;
            try {
                if (ptr.isNull && ptr.isNull()) return null;
            } catch (eNull) {}
            if (ptr.handle !== undefined && ptr.handle) {
                raw = ptr.handle;
            }
            try {
                if (klass && typeof klass.from === 'function') {
                    return klass.from(raw);
                }
            } catch (e0) {}
            try {
                return new Il2Cpp.Object(raw);
            } catch (e1) {}
            return null;
        }

        function readNicknameFromBridgeObject(obj) {
            if (!obj) return { ok: false, msg: '对象为空' };
            try {
                var m = obj.method && obj.method('get_nickName');
                if (m && typeof m.invoke === 'function') {
                    var r = m.invoke();
                    return { ok: true, value: il2cppValueToJs(r), via: 'get_nickName()' };
                }
            } catch (e0) {}
            try {
                var f = obj.field && obj.field('nickName');
                if (f) {
                    return { ok: true, value: il2cppValueToJs(f.value), via: 'field.nickName' };
                }
            } catch (e1) {}
            try {
                var bf = obj.field && obj.field('<nickName>k__BackingField');
                if (bf) {
                    return { ok: true, value: il2cppValueToJs(bf.value), via: 'backingField' };
                }
            } catch (e2) {}
            return { ok: false, msg: 'get_nickName / nickName 字段均不可用' };
        }

        function method2_il2cppBridge(inst) {
            if (typeof Il2Cpp === 'undefined') {
                return { ok: false, msg: 'Il2Cpp Bridge 插件不可用' };
            }
            try {
                return syncIl2CppPerform(function () {
                    var domain = Il2Cpp.domain || Il2Cpp.Domain;
                    if (!domain || typeof domain.assembly !== 'function') {
                        return { ok: false, msg: 'Il2Cpp.domain 不可用（请确认 frida-il2cpp-bridge 版本与用法）' };
                    }
                    var asm = domain.assembly('Assembly-CSharp');
                    if (!asm || !asm.image) {
                        return { ok: false, msg: '找不到程序集 Assembly-CSharp' };
                    }
                    var clientDataClass = asm.image.class('ClientData');
                    if (!clientDataClass) {
                        return { ok: false, msg: '找不到类 ClientData' };
                    }

                    try {
                        var mineField = clientDataClass.field('mine');
                        if (mineField) {
                            var mineRaw = mineField.value;
                            var mineObj = wrapClientDataInstance(clientDataClass, mineRaw);
                            if (!mineObj && mineRaw && typeof mineRaw.field === 'function') {
                                mineObj = mineRaw;
                            }
                            if (mineObj) {
                                var rMine = readNicknameFromBridgeObject(mineObj);
                                if (rMine.ok) return rMine;
                            }
                        }
                    } catch (eMine) {}

                    var cd = inst.clientData;
                    if (!cd || cd.isNull()) {
                        return { ok: false, msg: 'ClientData.mine 无效且 inst.clientData 未捕获' };
                    }
                    var instObj = wrapClientDataInstance(clientDataClass, cd);
                    if (!instObj) {
                        return { ok: false, msg: '无法将 ClientData 指针包装为 Il2Cpp.Object' };
                    }
                    var rInst = readNicknameFromBridgeObject(instObj);
                    if (rInst.ok) return rInst;
                    return { ok: false, msg: rInst.msg || '实例读取失败' };
                });
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
                        var cd = inst.clientData;
                        if (inst.player && !inst.player.isNull()) {
                            var live = readPtr(inst.player.add(0x94));
                            if (live) cd = live;
                        }
                        this.filterCd = cd;
                        this.strAtField = cd ? readPtr(cd.add(0x10)) : null;
                        this.a0 = args[0];
                        this.a1 = args[1];
                        this.self = false;
                        if (!cd || cd.isNull()) return;
                        if (this.a0.equals(cd)) {
                            this.self = true;
                            return;
                        }
                        if (this.a1 && !this.a1.isNull() && this.a1.equals(cd)) {
                            this.self = true;
                        }
                    },
                    onLeave: function (retval) {
                        if (!retval || retval.isNull()) return;
                        var cd = this.filterCd;
                        var viaThis = this.self;
                        var viaStr = false;
                        try {
                            if (this.strAtField && !this.strAtField.isNull() && retval.equals(this.strAtField)) {
                                viaStr = true;
                            }
                        } catch (e0) {}
                        if (!viaThis && !viaStr) return;
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
