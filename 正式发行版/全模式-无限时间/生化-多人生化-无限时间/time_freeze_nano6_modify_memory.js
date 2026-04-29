// time_freeze_nano6_modify_memory.js - 多人生化模式修改内存实现无限时间

console.log("[*] === Nano6 Mode Modify Memory (Infinite Time) ===\n");

var gameAssembly = Process.findModuleByName("GameAssembly.dll");
var logFile = null;
var modeBaseInstance = null;
var lastModifyTime = 0;
var modifyCount = 0;

// 打开日志文件
function openLogFile() {
    try {
        logFile = new File("D:\\trae_project\\time_freeze_nano6_modify_memory_log.txt", "w");
        logFile.write("=== Nano6 Mode Modify Memory (Infinite Time) Log ===\n");
        logFile.write("Start Time: " + new Date().toISOString() + "\n\n");
        logFile.flush();
        console.log("[+] Log file created");
    } catch (e) {
        console.log("[-] Log file error: " + e);
    }
}

// 写入日志
function writeLog(message) {
    if (logFile) {
        try {
            logFile.write(message + "\n");
            logFile.flush();
        } catch (e) {}
    }
}

// 安全修改时间
function safeModifyTime(instance, minute, second) {
    try {
        // 检查实例地址是否有效
        if (!instance || instance.equals(ptr(0))) {
            return false;
        }
        
        // 检查地址是否在合理范围内（应该在堆内存区域）
        var gameBase = gameAssembly.base;
        var gameEnd = gameBase.add(gameAssembly.size);
        
        // 实例地址应该在堆内存，不在GameAssembly.dll范围内
        // 但我们仍然可以检查地址是否有效
        if (instance.compare(ptr(0x10000)) < 0) {
            return false; // 地址太小，可能是无效地址
        }
        
        // 修改时间
        instance.add(0x34).writeS32(minute);
        instance.add(0x38).writeS32(second);
        return true;
    } catch (e) {
        return false;
    }
}

// 读取当前时间
function readCurrentTime(instance) {
    try {
        if (!instance || instance.equals(ptr(0))) {
            return null;
        }
        
        var minute = instance.add(0x34).readS32();
        var second = instance.add(0x38).readS32();
        
        // 检查数值是否合理
        if (minute < 0 || minute > 200 || second < 0 || second > 59) {
            return null; // 数值不合理，可能是错误的实例
        }
        
        return { minute: minute, second: second };
    } catch (e) {
        return null;
    }
}

function main() {
    console.log("\n========================================");
    console.log("  Nano6 Mode Modify Memory (Infinite Time)");
    console.log("========================================\n");
    
    if (!gameAssembly) {
        console.log("[-] No GameAssembly.dll");
        return;
    }
    
    openLogFile();
    writeLog("[*] GameAssembly.dll Base: " + gameAssembly.base);
    
    var base = gameAssembly.base;
    
    // ============================================
    // 1. Hook ModeBase_Nano.CheckRoundOver - 获取实例地址并修改内存
    // ============================================
    console.log("[*] Hooking ModeBase_Nano.CheckRoundOver...\n");
    writeLog("[*] Hooking ModeBase_Nano.CheckRoundOver...");
    
    var checkRoundOver = base.add(0xAEF8A0);
    var checkRoundOverCount = 0;
    
    Interceptor.attach(checkRoundOver, {
        onEnter: function(args) {
            checkRoundOverCount++;
            var newInstance = args[0];
            
            // 检查是否是新实例（新回合）
            if (!modeBaseInstance || !newInstance.equals(modeBaseInstance)) {
                modeBaseInstance = newInstance;
                var msg = "[NEW INSTANCE #" + checkRoundOverCount + "] New ModeBase instance: " + modeBaseInstance;
                console.log(msg);
                writeLog(msg);
            }
            
            // 读取当前时间
            var currentTime = readCurrentTime(modeBaseInstance);
            if (currentTime) {
                // 只在时间小于90分钟时修改
                if (currentTime.minute < 90) {
                    // 修改为99分钟59秒
                    if (safeModifyTime(modeBaseInstance, 99, 59)) {
                        modifyCount++;
                        var modifyMsg = "[CALL #" + checkRoundOverCount + "] Modified restGameTime from " + currentTime.minute + ":" + currentTime.second + " to 99:59 (total: " + modifyCount + ")";
                        console.log(modifyMsg);
                        writeLog(modifyMsg);
                    }
                } else {
                    var skipMsg = "[CALL #" + checkRoundOverCount + "] Skip modify (time=" + currentTime.minute + ":" + currentTime.second + " >= 90)";
                    console.log(skipMsg);
                    writeLog(skipMsg);
                }
            } else {
                var errorMsg = "[CALL #" + checkRoundOverCount + "] Cannot read time, resetting instance";
                console.log(errorMsg);
                writeLog(errorMsg);
                // 重置实例，下次重新获取
                modeBaseInstance = null;
            }
        },
        onLeave: function(retval) {
            // 不阻止
        }
    });
    
    console.log("[+] ModeBase_Nano.CheckRoundOver hooked!\n");
    writeLog("[+] ModeBase_Nano.CheckRoundOver hooked!");
    
    // ============================================
    // 2. Hook ModeBase.UpdateTimeUI - 修改显示的时间
    // ============================================
    console.log("[*] Hooking ModeBase.UpdateTimeUI...\n");
    writeLog("[*] Hooking ModeBase.UpdateTimeUI...");
    
    var updateTimeUI = base.add(0xAF6930);
    var updateTimeUICount = 0;
    
    try {
        Interceptor.attach(updateTimeUI, {
            onEnter: function(args) {
                updateTimeUICount++;
                
                // 修改实例的restGameTime
                if (modeBaseInstance) {
                    var currentTime = readCurrentTime(modeBaseInstance);
                    if (currentTime && currentTime.minute < 90) {
                        if (safeModifyTime(modeBaseInstance, 99, 59)) {
                            modifyCount++;
                            if (updateTimeUICount <= 20 || modifyCount % 10 === 0) {
                                var msg = "[CALL #" + updateTimeUICount + "] UpdateTimeUI - modified restGameTime from " + currentTime.minute + ":" + currentTime.second + " to 99:59 (total: " + modifyCount + ")";
                                console.log(msg);
                                writeLog(msg);
                            }
                        }
                    }
                }
            },
            onLeave: function(retval) {
                // 不阻止
            }
        });
        
        console.log("[+] ModeBase.UpdateTimeUI hooked!\n");
        writeLog("[+] ModeBase.UpdateTimeUI hooked!");
    } catch (e) {
        console.log("[-] Failed: " + e);
        writeLog("[-] Failed: " + e);
    }
    
    // ============================================
    // 3. Hook ModeBase_Nano.OnTimeOut - 监控
    // ============================================
    console.log("[*] Hooking ModeBase_Nano.OnTimeOut (monitor)...\n");
    writeLog("[*] Hooking ModeBase_Nano.OnTimeOut (monitor)...");
    
    var onTimeOut = base.add(0xAF1920);
    var onTimeOutCount = 0;
    
    try {
        Interceptor.attach(onTimeOut, {
            onEnter: function(args) {
                onTimeOutCount++;
                var msg = "[MONITOR #" + onTimeOutCount + "] OnTimeOut - resetting instance";
                console.log(msg);
                writeLog(msg);
                
                // 时间结束时重置实例
                modeBaseInstance = null;
            },
            onLeave: function(retval) {
                // 不阻止
            }
        });
        
        console.log("[+] ModeBase_Nano.OnTimeOut hooked!\n");
        writeLog("[+] ModeBase_Nano.OnTimeOut hooked!");
    } catch (e) {
        console.log("[-] Failed: " + e);
        writeLog("[-] Failed: " + e);
    }
    
    // ============================================
    // 4. Hook GameManager.GameRoundEnd - 回合结束时重置实例
    // ============================================
    console.log("[*] Hooking GameManager.GameRoundEnd (reset instance)...\n");
    writeLog("[*] Hooking GameManager.GameRoundEnd (reset instance)...");
    
    var gameRoundEnd = base.add(0xAFAA40);
    var gameRoundEndCount = 0;
    
    try {
        Interceptor.attach(gameRoundEnd, {
            onEnter: function(args) {
                gameRoundEndCount++;
                var msg = "[CALL #" + gameRoundEndCount + "] GameRoundEnd - resetting instance";
                console.log(msg);
                writeLog(msg);
                
                // 回合结束时重置实例
                modeBaseInstance = null;
            },
            onLeave: function(retval) {
                // 不阻止
            }
        });
        
        console.log("[+] GameManager.GameRoundEnd hooked!\n");
        writeLog("[+] GameManager.GameRoundEnd hooked!");
    } catch (e) {
        console.log("[-] Failed: " + e);
        writeLog("[-] Failed: " + e);
    }
    
    // ============================================
    // 5. 定期修改内存的定时器（带安全检查）
    // ============================================
    console.log("[*] Starting memory modification timer (with safety checks)...\n");
    writeLog("[*] Starting memory modification timer (with safety checks)...");
    
    setInterval(function() {
        if (modeBaseInstance) {
            var currentTime = readCurrentTime(modeBaseInstance);
            if (currentTime) {
                // 如果时间小于90分钟，修改为99:59
                if (currentTime.minute < 90) {
                    if (safeModifyTime(modeBaseInstance, 99, 59)) {
                        modifyCount++;
                        var now = Date.now();
                        // 每秒最多输出一次日志
                        if (now - lastModifyTime > 1000) {
                            var msg = "[TIMER] Modified restGameTime from " + currentTime.minute + ":" + currentTime.second + " to 99:59 (total: " + modifyCount + ")";
                            console.log(msg);
                            writeLog(msg);
                            lastModifyTime = now;
                        }
                    }
                }
            } else {
                // 读取失败，重置实例
                var errorMsg = "[TIMER] Cannot read time, resetting instance";
                console.log(errorMsg);
                writeLog(errorMsg);
                modeBaseInstance = null;
            }
        }
    }, 1000); // 每秒检查一次
    
    console.log("[+] Memory modification timer started!\n");
    writeLog("[+] Memory modification timer started!");
    
    writeLog("\n[*] === Nano6 Mode Modify Memory Script Running ===\n");
    console.log("\n[*] === Nano6 Mode Modify Memory Script Running ===");
    console.log("[*] Modifying restGameTime to 99:59 on every CheckRoundOver call");
    console.log("[*] Modifying restGameTime to 99:59 on every UpdateTimeUI call");
    console.log("[*] Timer checks and modifies restGameTime every second");
    console.log("[*] Safety checks: validates instance address before modifying");
    console.log("[*] Auto-reset instance on round end");
    console.log("[*] This should achieve INFINITE TIME in Nano6 mode!\n");
}

main();
