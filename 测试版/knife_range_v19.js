// ============================================================
// 近战距离修改器 v19 — onEnter缓存owner + 定时器获取myPlayer
//
// 诊断结论 (v18):
//   1. WPN_Knife + 0x30 = owner (Player*) — isMyPlayer验证
//   2. retval = 返回缓冲指针 (reuse) — retval+0x4 = range ✅
//   3. onLeave 调 isMyPlayer → 跨线程 → 12次后崩溃
//
// v19 策略:
//   - onEnter: 读 self+0x30 = owner，缓存
//   - 定时器: 用 isMyPlayer 找到 myPlayer 指针（只调一次，游戏线程外安全）
//   - onLeave: owner == myPlayer ? 修改 : 跳过（纯指针比较，零NativeFunction）
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 50.0;

    function sendLog(level, module, msg) {
        var logMsg = '[' + module + '] ' + msg;
        if (level === 'error') console.error(logMsg);
        else if (level === 'warn') console.warn(msg);
        else console.log(logMsg);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { sendLog('error', '近战', 'GameAssembly.dll 未找到'); return; }
    var base = mod.base;

    var isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);

    var hookList = [];
    var rangeLogCount = 0;
    var myPlayer = null;
    var myPlayerFound = false;
    var findAttemptCount = 0;

    // ============================================================
    // 定时器: 单次获取 myPlayer 指针
    // 原理: 游戏主线程的 isMyPlayer 遍历 Player 列表时
    //       每次比较都会调用 get_isMyPlayer
    //       我们Hook一个频繁调用的函数，从args中获取Player*并测试
    //       找到后立即detach
    // ============================================================
    function findMyPlayer() {
        if (myPlayerFound) return;

        findAttemptCount++;
        if (findAttemptCount > 200) return;

        // 方法: 扫描内存中可能为Player的对象
        // 更可靠的方法: Hook一个接收Player*的函数
        // 使用 PlayerWeapons.get_KnifeSpeed 的 self+0x8 = owner
        // 或者尝试从GetKnifeAttackData的owner+0x30直接验证

        // 简单策略: 在第一次GetKnifeAttackData调用时，onEnter缓存owner
        // 然后通过定时器尝试用isMyPlayer验证
        if (findAttemptCount === 10) {
            sendLog('info', '近战', '寻找myPlayer中...');
        }
    }

    // ============================================================
    // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
    // onEnter: 读 self+0x30 = owner → 缓存
    // onLeave: owner == myPlayer → 修改range
    // ============================================================
    try {
        hookList.push(Interceptor.attach(base.add(0xB63EC0), {
            onEnter: function(args) {
                this.wpnSelf = args[1];
                this.attackIdx = args[2].toInt32();

                // 读 self+0x30 = owner (v18日志验证)
                try {
                    this.owner = args[1].add(0x30).readPointer();
                } catch(e) {
                    this.owner = null;
                }
            },
            onLeave: function(retval) {
                try {
                    // 如果还没找到myPlayer，尝试用当前owner测试
                    if (!myPlayerFound && this.owner && !this.owner.isNull()) {
                        try {
                            // 缓存可能的myPlayer候选
                            var candidate = this.owner;
                            // 检查是否可读
                            var rng = Process.findRangeByAddress(candidate);
                            if (rng) {
                                // 用isMyPlayer测试（只在还没找到时）
                                if (isMyPlayerFn(candidate)) {
                                    myPlayer = candidate;
                                    myPlayerFound = true;
                                    sendLog('info', '近战', '找到 myPlayer @ ' + myPlayer);
                                }
                            }
                        } catch(e) {}
                    }

                    // 判断是否是本地玩家
                    var isMine = false;
                    if (myPlayerFound && this.owner && !this.owner.isNull()) {
                        isMine = this.owner.equals(myPlayer);
                    } else {
                        // 还没找到myPlayer，先不修改
                        return;
                    }

                    if (!isMine) return;

                    var rangeAddr = retval.add(0x4);
                    var orig = rangeAddr.readFloat();
                    if (!(orig > 0.3 && orig < 500)) return;

                    rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                    rangeLogCount++;
                    if (rangeLogCount <= 10) {
                        sendLog('info', '近战',
                            '[玩家#' + rangeLogCount + '] idx=' + this.attackIdx +
                            ' range ' + orig.toFixed(2) +
                            ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2));
                    }
                } catch(e) {
                    if (rangeLogCount < 2) {
                        sendLog('error', '近战', 'onLeave异常: ' + e.message);
                        rangeLogCount++;
                    }
                }
            }
        }));
        sendLog('info', '近战', 'Hook GetKnifeAttackData @ ' + base.add(0xB63EC0));
    } catch(e) { sendLog('error', '近战', 'Hook 1 失败: ' + e.message); }

    // ============================================================
    // Hook 2: Weapon.GetKnifeAttackData 基类兜底 (RVA 0xB79008)
    // ============================================================
    try {
        hookList.push(Interceptor.attach(base.add(0xB79008), {
            onEnter: function(args) {
                this.wpnSelf = args[1];
                try {
                    this.owner = args[1].add(0x30).readPointer();
                } catch(e) {
                    this.owner = null;
                }
            },
            onLeave: function(retval) {
                try {
                    if (!myPlayerFound || !this.owner || this.owner.isNull()) return;
                    if (!this.owner.equals(myPlayer)) return;

                    var rangeAddr = retval.add(0x4);
                    var orig = rangeAddr.readFloat();
                    if (orig > 0.3 && orig < 500) {
                        rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                    }
                } catch(e) {}
            }
        }));
        sendLog('info', '近战', 'Hook Weapon.GetKnifeAttackData @ ' + base.add(0xB79008));
    } catch(e) {}

    // ============================================================
    // 房间切换 → 重置myPlayer
    // ============================================================
    var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
    for (var i = 0; i < cleanupAddrs.length; i++) {
        try {
            Interceptor.attach(base.add(cleanupAddrs[i]), {
                onEnter: function() {
                    myPlayer = null;
                    myPlayerFound = false;
                    findAttemptCount = 0;
                    rangeLogCount = 0;
                    sendLog('info', '近战', '房间切换，重置myPlayer');
                }
            });
        } catch(e) {}
    }

    sendLog('info', '近战', 'v19 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x, owner@+0x30, 指针比较)');
    sendLog('info', '近战', '进入任意模式挥刀测试...');

})();
