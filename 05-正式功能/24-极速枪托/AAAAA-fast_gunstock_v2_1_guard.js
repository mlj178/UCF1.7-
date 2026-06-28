// ============================================================
// AAAAA-fast_gunstock_v2_1_guard.js
// 极速枪托 v2.1：防打断保护版
//
// 目标：
//   1. 不再修改角色/手部 Animator，避免手模动作错乱。
//   2. 使用 early_damage_unlock 思路，提高枪托伤害频率。
//   3. 新增“预约伤害保护窗口”：第一次伤害没出来前，吞掉第二次右键。
//   4. 第一次伤害完成并解锁后，才允许第二次枪托进入。
//   5. 所有用户可见日志改成中文。
//
// 重要说明：
//   这版会 replace WPN_Gun.OnSpecialBtnDown 和 WPN_Gun.KnifeAttackEvent。
//   attach 只能观察，不能阻止第二次右键；要防打断必须 replace 右键入口。
// ============================================================

(function() {
  'use strict';

  var 调用约定 = 'mscdecl';
  var 最大日志数 = 260;
  var 模块日志数 = {};

  var RVA = {
    枪_右键入口: 0xB629F0,          // WPN_Gun.OnSpecialBtnDown()
    枪_取枪托攻击数据: 0xB61F90,    // WPN_Gun.GetKnifeAttackData(int)
    枪_枪托伤害事件: 0xB62730,      // WPN_Gun.KnifeAttackEvent(int)
    枪_枪托退出: 0xB62990,          // WPN_Gun.OnKnifeAttackExit()
    武器_是否本地武器: 0xB6E1D0     // Weapon.get_isMyWeapon()
  };

  var 偏移 = {
    枪_realData: 0xEC,
    枪托_攻击数据数组: 0x180,
    枪_枪托数量: 0x118,
    枪_枪托动画锁: 0x11C
  };

  var 状态 = {
    已开启: false,
    已初始化: false,
    已安装: false,

    // 关键可调参数
    提前伤害延迟ms: 120,
    伤害后解锁延迟ms: 40,
    保护超时ms: 650,
    attackIndex: 0,

    // 运行统计
    右键进入次数: 0,
    右键放行次数: 0,
    右键吞掉次数: 0,
    右键非枪托跳过: 0,
    右键锁中跳过: 0,

    提前伤害次数: 0,
    自然伤害次数: 0,
    重复自然伤害吞掉次数: 0,
    解锁次数: 0,
    保护超时恢复次数: 0,

    最后错误: null,

    // 当前保护窗口
    当前攻击: null,
    序号: 0,
    正在手动调用伤害: false,

    // NativeFunction
    原始右键入口: null,
    原始枪托伤害事件: null,
    原始枪托退出: null,
    是否本地武器函数: null
  };

  var 游戏模块 = null;

  function 写日志(级别, 模块, 内容) {
    if (!模块日志数[模块]) 模块日志数[模块] = 0;
    if (模块日志数[模块] >= 最大日志数) return;
    模块日志数[模块]++;

    var 文本 = '[极速枪托v2.1][' + 模块 + '] ' + 内容;
    console.log('[' + 级别 + '] ' + 文本);
    try {
      send({ type: '日志', level: 级别, module: '极速枪托/' + 模块, message: 内容 });
    } catch (e) {}
  }

  function 当前时间() {
    return Date.now();
  }

  function 取游戏模块() {
    if (游戏模块) return 游戏模块;
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        状态.最后错误 = '没有找到 GameAssembly.dll';
        写日志('错误', '初始化', 状态.最后错误);
        return null;
      }
      游戏模块 = mod;
      写日志('成功', '初始化', 'GameAssembly 基址=' + mod.base);
      return mod;
    } catch (e) {
      状态.最后错误 = '获取 GameAssembly.dll 失败：' + e.message;
      写日志('错误', '初始化', 状态.最后错误);
      return null;
    }
  }

  function 读指针(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var p = addr.readPointer();
      if (!p || p.isNull()) return null;
      return p;
    } catch (e) {
      return null;
    }
  }

  function 读整数(addr, 默认值) {
    try {
      if (!addr || addr.isNull()) return 默认值;
      return addr.readS32();
    } catch (e) {
      return 默认值;
    }
  }

  function 写整数(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeS32(value);
      return true;
    } catch (e) {
      状态.最后错误 = '写入整数失败：' + e.message;
      return false;
    }
  }

  function 初始化函数() {
    if (状态.已初始化) return true;

    var mod = 取游戏模块();
    if (!mod) return false;

    try {
      var 地址右键 = mod.base.add(RVA.枪_右键入口);
      var 地址伤害 = mod.base.add(RVA.枪_枪托伤害事件);
      var 地址退出 = mod.base.add(RVA.枪_枪托退出);
      var 地址本地 = mod.base.add(RVA.武器_是否本地武器);

      状态.原始右键入口 = new NativeFunction(
        地址右键,
        'void',
        ['pointer', 'pointer'],
        调用约定
      );

      状态.原始枪托伤害事件 = new NativeFunction(
        地址伤害,
        'void',
        ['pointer', 'int', 'pointer'],
        调用约定
      );

      状态.原始枪托退出 = new NativeFunction(
        地址退出,
        'void',
        ['pointer', 'pointer'],
        调用约定
      );

      状态.是否本地武器函数 = new NativeFunction(
        地址本地,
        'bool',
        ['pointer', 'pointer'],
        调用约定
      );

      状态.已初始化 = true;
      写日志('成功', '初始化', 'NativeFunction 初始化完成');
      return true;
    } catch (e) {
      状态.最后错误 = 'NativeFunction 初始化失败：' + e.message;
      写日志('错误', '初始化', 状态.最后错误);
      return false;
    }
  }

  function 是本地武器(weapon) {
    if (!weapon || weapon.isNull()) return false;
    if (!初始化函数()) return false;
    try {
      return 状态.是否本地武器函数(weapon, ptr(0)) ? true : false;
    } catch (e) {
      状态.最后错误 = '判断本地武器失败：' + e.message;
      return false;
    }
  }

  function 有枪托攻击(weapon) {
    if (!weapon || weapon.isNull()) return false;

    var count = 读整数(weapon.add(偏移.枪_枪托数量), 0);
    if (count > 0) return true;

    var realData = 读指针(weapon.add(偏移.枪_realData));
    if (!realData) return false;

    var attacks = 读指针(realData.add(偏移.枪托_攻击数据数组));
    if (!attacks) return false;

    var length = 读整数(attacks.add(0x0C), 0);
    return length > 0;
  }

  function 武器键(weapon) {
    try {
      return weapon.toString();
    } catch (e) {
      return '';
    }
  }

  function 当前攻击属于(weapon) {
    if (!状态.当前攻击 || !weapon || weapon.isNull()) return false;
    return 状态.当前攻击.weaponKey === 武器键(weapon);
  }

  function 清理当前攻击(原因) {
    if (状态.当前攻击) {
      写日志('信息', '保护', '清理当前攻击：' + 原因);
    }
    状态.当前攻击 = null;
  }

  function 当前保护是否有效() {
    if (!状态.当前攻击) return false;

    var now = 当前时间();
    var age = now - 状态.当前攻击.startMs;

    if (age > 状态.保护超时ms) {
      状态.保护超时恢复次数++;
      写日志('警告', '保护', '保护窗口超时，自动恢复。耗时=' + age + 'ms');
      清理当前攻击('超时恢复');
      return false;
    }

    return true;
  }

  function 写入解锁(weapon, 来源) {
    if (!weapon || weapon.isNull()) return false;
    var ok = 写整数(weapon.add(偏移.枪_枪托动画锁), 0);
    if (ok) {
      写日志('信息', '解锁', 来源 + '：写入 knifeAttackAnim=0');
    }
    return ok;
  }

  function 调用退出并解锁(weapon, 来源) {
    if (!weapon || weapon.isNull()) return false;
    if (!初始化函数()) return false;

    var ok = false;

    try {
      状态.原始枪托退出(weapon, ptr(0));
      ok = true;
      写日志('信息', '解锁', 来源 + '：已调用 OnKnifeAttackExit');
    } catch (e) {
      状态.最后错误 = '调用 OnKnifeAttackExit 失败：' + e.message;
      写日志('警告', '解锁', 状态.最后错误);
    }

    ok = 写入解锁(weapon, 来源) || ok;

    状态.解锁次数++;
    return ok;
  }

  function 安排解锁(seq, weapon, 来源) {
    var delay = Math.max(0, 状态.伤害后解锁延迟ms | 0);

    setTimeout(function() {
      try {
        if (!状态.已开启) return;
        if (!状态.当前攻击) return;
        if (状态.当前攻击.seq !== seq) return;

        调用退出并解锁(weapon, 来源 + '，延迟=' + delay + 'ms');

        if (状态.当前攻击 && 状态.当前攻击.seq === seq) {
          状态.当前攻击.unlockDone = true;
          清理当前攻击('伤害后已解锁，允许下一次枪托');
        }
      } catch (e) {
        状态.最后错误 = '安排解锁执行失败：' + e.message;
        写日志('错误', '解锁', 状态.最后错误);
        清理当前攻击('解锁异常');
      }
    }, delay);
  }

  function 标记伤害完成(seq, weapon, 类型) {
    if (!状态.当前攻击) return;
    if (状态.当前攻击.seq !== seq) return;

    状态.当前攻击.damageDone = true;
    状态.当前攻击.damageMs = 当前时间();

    写日志('成功', '伤害', 类型 + '已完成，准备延迟解锁。seq=' + seq);
    安排解锁(seq, weapon, 类型);
  }

  function 手动触发提前伤害(seq) {
    try {
      if (!状态.已开启) return;
      if (!状态.当前攻击) return;
      if (状态.当前攻击.seq !== seq) return;

      var attack = 状态.当前攻击;
      if (attack.damageDone) return;

      var weapon = attack.weapon;
      if (!weapon || weapon.isNull()) {
        清理当前攻击('武器指针无效');
        return;
      }

      状态.正在手动调用伤害 = true;
      try {
        状态.原始枪托伤害事件(weapon, attack.attackIndex, ptr(0));
        状态.提前伤害次数++;
        attack.earlyFired = true;
        写日志('成功', '提前伤害',
          '已手动触发 KnifeAttackEvent，延迟=' + 状态.提前伤害延迟ms +
          'ms，attackIndex=' + attack.attackIndex + '，seq=' + seq
        );
      } finally {
        状态.正在手动调用伤害 = false;
      }

      标记伤害完成(seq, weapon, '提前伤害');
    } catch (e) {
      状态.正在手动调用伤害 = false;
      状态.最后错误 = '提前伤害失败：' + e.message;
      写日志('错误', '提前伤害', 状态.最后错误);
      清理当前攻击('提前伤害异常');
    }
  }

  function 安排提前伤害(seq) {
    var delay = Math.max(1, 状态.提前伤害延迟ms | 0);
    setTimeout(function() {
      手动触发提前伤害(seq);
    }, delay);
  }

  function 安装Hook() {
    if (状态.已安装) return true;

    var mod = 取游戏模块();
    if (!mod) return false;
    if (!初始化函数()) return false;

    try {
      var 地址右键 = mod.base.add(RVA.枪_右键入口);
      var 地址伤害 = mod.base.add(RVA.枪_枪托伤害事件);

      // ------------------------------------------------------------
      // 1. replace 右键入口：
      //    - 保护窗口未结束时，吞掉第二次右键，不让第二次动画抢掉第一次伤害。
      //    - 保护窗口结束后，才允许原游戏右键入口执行。
      // ------------------------------------------------------------
      Interceptor.replace(地址右键, new NativeCallback(function(weapon, methodInfo) {
        try {
          if (!状态.已开启) {
            状态.原始右键入口(weapon, methodInfo);
            return;
          }

          状态.右键进入次数++;

          if (!weapon || weapon.isNull()) {
            状态.原始右键入口(weapon, methodInfo);
            return;
          }

          if (!是本地武器(weapon)) {
            状态.原始右键入口(weapon, methodInfo);
            return;
          }

          if (!有枪托攻击(weapon)) {
            状态.右键非枪托跳过++;
            状态.原始右键入口(weapon, methodInfo);
            return;
          }

          // 关键：第一次伤害完成并解锁前，吞掉后续右键。
          if (当前保护是否有效()) {
            状态.右键吞掉次数++;
            if (状态.右键吞掉次数 <= 30 || 状态.右键吞掉次数 % 50 === 0) {
              var age = 当前时间() - 状态.当前攻击.startMs;
              写日志('信息', '保护',
                '已吞掉一次过早右键，等待第一次伤害完成。已等待=' + age + 'ms'
              );
            }
            return;
          }

          var lockValue = 读整数(weapon.add(偏移.枪_枪托动画锁), 0);
          if (lockValue !== 0) {
            // 如果旧锁残留，先解一下，再允许进入，避免卡死。
            状态.右键锁中跳过++;
            写入解锁(weapon, '右键入口发现旧锁');
          }

          状态.序号++;
          var seq = 状态.序号;

          状态.当前攻击 = {
            seq: seq,
            weapon: weapon,
            weaponKey: 武器键(weapon),
            attackIndex: 状态.attackIndex | 0,
            startMs: 当前时间(),
            damageDone: false,
            unlockDone: false,
            earlyFired: false
          };

          状态.右键放行次数++;
          写日志('信息', '右键',
            '放行第一次枪托，开始保护窗口。seq=' + seq +
            '，提前伤害延迟=' + 状态.提前伤害延迟ms +
            'ms，伤害后解锁=' + 状态.伤害后解锁延迟ms + 'ms'
          );

          // 先让原游戏开始播放枪托流程。
          状态.原始右键入口(weapon, methodInfo);

          // 再预约提前伤害。
          安排提前伤害(seq);
          return;
        } catch (e) {
          状态.最后错误 = '右键入口处理失败：' + e.message;
          写日志('错误', '右键', 状态.最后错误);
          try {
            状态.原始右键入口(weapon, methodInfo);
          } catch (e2) {}
          return;
        }
      }, 'void', ['pointer', 'pointer'], 调用约定));

      // ------------------------------------------------------------
      // 2. replace 枪托伤害事件：
      //    - 如果自然伤害先到，就承认自然伤害，并开始解锁。
      //    - 如果提前伤害已经打过，后面的自然重复事件吞掉，避免重复伤害/乱状态。
      // ------------------------------------------------------------
      Interceptor.replace(地址伤害, new NativeCallback(function(weapon, attackIndex, methodInfo) {
        try {
          if (!状态.已开启) {
            状态.原始枪托伤害事件(weapon, attackIndex, methodInfo);
            return;
          }

          if (状态.正在手动调用伤害) {
            状态.原始枪托伤害事件(weapon, attackIndex, methodInfo);
            return;
          }

          if (当前攻击属于(weapon)) {
            var attack = 状态.当前攻击;

            if (!attack.damageDone) {
              状态.自然伤害次数++;
              状态.原始枪托伤害事件(weapon, attackIndex, methodInfo);
              写日志('成功', '自然伤害',
                '原游戏自然伤害先到，取消等待提前伤害。attackIndex=' +
                attackIndex + '，seq=' + attack.seq
              );
              标记伤害完成(attack.seq, weapon, '自然伤害');
              return;
            }

            // 提前伤害已打出，原动画后续又触发自然伤害时吞掉，避免重复。
            if (attack.damageDone) {
              状态.重复自然伤害吞掉次数++;
              if (状态.重复自然伤害吞掉次数 <= 20 ||
                  状态.重复自然伤害吞掉次数 % 50 === 0) {
                写日志('信息', '去重',
                  '已吞掉重复自然伤害，避免一次枪托重复出伤害。seq=' + attack.seq
                );
              }
              return;
            }
          }

          // 不属于我们当前保护窗口的伤害，按原游戏流程放行。
          状态.原始枪托伤害事件(weapon, attackIndex, methodInfo);
          return;
        } catch (e) {
          状态.最后错误 = '伤害事件处理失败：' + e.message;
          写日志('错误', '伤害', 状态.最后错误);
          try {
            状态.原始枪托伤害事件(weapon, attackIndex, methodInfo);
          } catch (e2) {}
          return;
        }
      }, 'void', ['pointer', 'int', 'pointer'], 调用约定));

      状态.已安装 = true;
      写日志('成功', 'Hook', '防打断 Hook 已安装：右键入口 + 枪托伤害事件');
      return true;
    } catch (e) {
      状态.最后错误 = 'Hook 安装失败：' + e.message;
      写日志('错误', 'Hook', 状态.最后错误);
      return false;
    }
  }

  function 开启() {
    try {
      if (!安装Hook()) {
        状态.已开启 = false;
        return false;
      }
      状态.已开启 = true;
      写日志('成功', '状态',
        '极速枪托防打断已开启：提前伤害=' + 状态.提前伤害延迟ms +
        'ms，伤害后解锁=' + 状态.伤害后解锁延迟ms + 'ms'
      );
      return true;
    } catch (e) {
      状态.已开启 = false;
      状态.最后错误 = '开启失败：' + e.message;
      写日志('错误', '状态', 状态.最后错误);
      return false;
    }
  }

  function 关闭() {
    状态.已开启 = false;
    清理当前攻击('手动关闭');
    写日志('信息', '状态', '极速枪托防打断已关闭');
    return true;
  }

  function 清理() {
    关闭();
    // Interceptor.replace 不能像 attach 一样在这里简单 detach。
    // 实际退出脚本时 Frida 会随 script unload 清理替换。
    写日志('成功', '状态', '脚本清理完成');
    return true;
  }

  function 设置提前伤害延迟(value) {
    var v = parseInt(value, 10);
    if (!(v >= 30 && v <= 300)) {
      写日志('警告', '参数', '提前伤害延迟必须在 30 到 300ms 之间');
      return false;
    }
    状态.提前伤害延迟ms = v;
    写日志('成功', '参数', '提前伤害延迟已设置为 ' + v + 'ms');
    return true;
  }

  function 设置伤害后解锁延迟(value) {
    var v = parseInt(value, 10);
    if (!(v >= 0 && v <= 200)) {
      写日志('警告', '参数', '伤害后解锁延迟必须在 0 到 200ms 之间');
      return false;
    }
    状态.伤害后解锁延迟ms = v;
    写日志('成功', '参数', '伤害后解锁延迟已设置为 ' + v + 'ms');
    return true;
  }

  function 设置保护超时(value) {
    var v = parseInt(value, 10);
    if (!(v >= 300 && v <= 1500)) {
      写日志('警告', '参数', '保护超时必须在 300 到 1500ms 之间');
      return false;
    }
    状态.保护超时ms = v;
    写日志('成功', '参数', '保护超时已设置为 ' + v + 'ms');
    return true;
  }

  function 设置攻击序号(value) {
    var v = parseInt(value, 10);
    if (!(v >= 0 && v <= 5)) {
      写日志('警告', '参数', 'attackIndex 必须在 0 到 5 之间');
      return false;
    }
    状态.attackIndex = v;
    写日志('成功', '参数', 'attackIndex 已设置为 ' + v);
    return true;
  }

  function 状态查询() {
    var 当前 = 状态.当前攻击;
    return {
      已开启: 状态.已开启,
      已初始化: 状态.已初始化,
      已安装: 状态.已安装,

      提前伤害延迟ms: 状态.提前伤害延迟ms,
      伤害后解锁延迟ms: 状态.伤害后解锁延迟ms,
      保护超时ms: 状态.保护超时ms,
      attackIndex: 状态.attackIndex,

      右键进入次数: 状态.右键进入次数,
      右键放行次数: 状态.右键放行次数,
      右键吞掉次数: 状态.右键吞掉次数,
      右键非枪托跳过: 状态.右键非枪托跳过,
      右键锁中跳过: 状态.右键锁中跳过,

      提前伤害次数: 状态.提前伤害次数,
      自然伤害次数: 状态.自然伤害次数,
      重复自然伤害吞掉次数: 状态.重复自然伤害吞掉次数,
      解锁次数: 状态.解锁次数,
      保护超时恢复次数: 状态.保护超时恢复次数,

      正在保护: 当前 ? true : false,
      当前序号: 当前 ? 当前.seq : 0,
      当前已出伤害: 当前 ? 当前.damageDone : false,
      当前已解锁: 当前 ? 当前.unlockDone : false,

      最后错误: 状态.最后错误
    };
  }

  rpc.exports = {
    enable: 开启,
    disable: 关闭,
    cleanup: 清理,
    status: 状态查询,
    setearlydelay: 设置提前伤害延迟,
    setunlockdelay: 设置伤害后解锁延迟,
    setguardtimeout: 设置保护超时,
    setattackindex: 设置攻击序号
  };

  写日志('成功', '初始化', '极速枪托 v2.1 防打断脚本已加载');
  写日志('信息', '说明', '打开开关后生效：第一次伤害完成前，会吞掉过早的第二次右键');
})();
