/**
 * 手雷模式"按配置分组安装"干跑探针（不需要游戏）。
 *
 * 用桩环境加载 features/26_grenade_mode/script.js，然后对几组真实配置调用 enable()，
 * 打印每一组配置实际安装的 Hook / Replace。用来证明：
 *   - 只开"手雷强化"三个选项时，安装的 Replace 数量必须为 0（武器切换链路完全不受影响）；
 *   - 只有真的开无限手雷才装 PlayerWeapons.Remove；
 *   - GiveWeapon 永远不在 Replace 列表里（只观察，不替换）。
 *
 * 用法：node probe_grenade_gating.js
 */
const fs = require("fs");
const path = require("path");

const SCRIPT = path.resolve(
  __dirname,
  "../../04-正式发行版/全功能整合包2.7/game_modifier/features/26_grenade_mode/script.js"
);

function mkPtr(addr) {
  const value = addr >>> 0;
  const p = {
    value,
    add: (off) => mkPtr((value + (off | 0)) >>> 0),
    sub: (off) => mkPtr((value - (off | 0)) >>> 0),
    isNull: () => value === 0,
    equals: (o) => !!o && o.value === value,
    toString: () => "0x" + value.toString(16),
    readU8: () => 0,
    readU16: () => 0,
    readS32: () => 0,
    readU32: () => 0,
    readFloat: () => 0,
    readPointer: () => mkPtr(0),
    writeU8: () => {},
    writeU32: () => {},
    writeFloat: () => {},
  };
  return p;
}

function runScenario(title, config, mutate) {
  const attached = [];
  const replaced = [];
  const reverted = [];
  const synced = [];

  const g = globalThis;
  g.Process = {
    findModuleByName: (name) =>
      name === "GameAssembly.dll" ? { name, base: mkPtr(0x62550000), size: 0xfb0000 } : null,
    getCurrentThreadId: () => 1,
    findModuleByAddress: () => ({ name: "GameAssembly.dll", base: mkPtr(0x62550000) }),
    findRangeByAddress: () => null,
  };
  g.Module = {};
  g.Interceptor = {
    attach: (address, callbacks) => {
      attached.push({ address: address.toString(), callbacks });
      return { detach: () => {} };
    },
    replace: (address, replacement) => {
      replaced.push(address.toString());
    },
    revert: (address) => {
      reverted.push(address.toString());
    },
    flush: () => {},
  };
  g.NativeFunction = function () {
    return function () {
      return 0;
    };
  };
  g.NativeCallback = function (fn) {
    return fn;
  };
  g.ptr = (v) => mkPtr(typeof v === "number" ? v : 0);
  g.send = (msg) => {
    if (msg && msg.message === "按配置同步 Hook/Replace 完成") {
      synced.push(JSON.parse(msg.dev_detail).data);
    }
  };
  g.rpc = {};

  const source = fs.readFileSync(SCRIPT, "utf8");
  // 每个场景在独立的函数作用域里 eval，避免 const 互相污染
  const load = new Function("require", "module", "exports", "console", "globalThis", source);
  load(require, { exports: {} }, {}, console, g);

  g.rpc.exports.enable(config);

  const last = synced[synced.length - 1] || { needs: {}, replacement_names: [] };
  const result = {
    场景: title,
    需要的分组: last.needs,
    安装的Hook数: attached.length,
    安装的Replace: last.replacement_names,
    已恢复的地址: reverted,
  };
  console.log(JSON.stringify(result, null, 2));
  return result;
}

const BASE = {
  lock999_enabled: false,
  bot_grenade_mode_enabled: false,
  enable_damage: true,
  enable_range: true,
  enable_shoot_speed: true,
};

const A = runScenario("A 只有手雷强化三个选项（用户当前配置）", Object.assign({}, BASE));
runScenario("B 手雷强化 + 无限手雷", Object.assign({}, BASE, { lock999_enabled: true }));
runScenario("C 手雷强化 + 无限手雷 + 手雷模式(bot)", Object.assign({}, BASE, { lock999_enabled: true, bot_grenade_mode_enabled: true }));
runScenario("D 全部关闭", Object.assign({}, BASE, { enable_damage: false, enable_range: false, enable_shoot_speed: false }));

let failed = 0;
function check(desc, ok) {
  console.log((ok ? "  PASS  " : "  FAIL  ") + desc);
  if (!ok) failed++;
}
console.log("\n=== 断言 ===");
check("场景A 替换数为 0", (A.安装的Replace || []).length === 0);
check("场景A 不含 PlayerWeapons.Remove", !(A.安装的Replace || []).includes("PlayerWeapons.Remove"));
check("场景A 不含 GameManager.GiveWeapon", !(A.安装的Replace || []).includes("GameManager.GiveWeapon"));
check("场景A 仍安装手雷强化所需 Hook（capture+tuner）", A.需要的分组.capture === true && A.需要的分组.tuner === true);
process.exit(failed === 0 ? 0 : 1);
