'use strict';
// ==========================================================================
// 负向用例：脚本默认配置（death_diag_raise = false）
// --------------------------------------------------------------------------
//   · 异常漏斗探针（Il2Cpp_Exception_Raise）必须**不装**：装了就会吞掉托管
//     异常的 unwind -> int3 -> 0x80000003 秒退（2026-10-14 18:26 那次）。
//   · "跳过原函数"手势遗留的两个断言在默认路径下不适用，这里一并跳过
//     （正面用例 run_smoke.js 覆盖）。
//   其余（补发死亡广播 / 复活兜底新闸门 / 硬闸门）与正面用例完全共用。
// 用法：
//   node 06-测试/_crash18_26/run_smoke2.js 06-测试/_crash18_26/smoke_no_raise.js <script.js>
// ==========================================================================
const path = require('path');
const { runSmoke } = require(path.resolve(__dirname, '..', 'death-diag-stub', 'smoke_death_diag.js'));

module.exports = {
    runSmoke: function (scriptPath) {
        return runSmoke(scriptPath, { raiseProbe: false, skipGesture: false });
    }
};
