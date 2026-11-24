# 新图的脚本放这里

从 `12_TestMap12龙城\tools\` 复制现成的，改三处：

1. `GAME` —— 目标游戏目录的 `UnityCrossFire_Data`
2. `OUT`  —— 输出目录（建议直接指向 `run\gamepatch\NN_...\UnityCrossFire_Data`）
3. `SRCB` —— Unity 构建产物目录

约定：脚本跑完必须能打印每件产物的 `字节数 + sha256`，我们直接抄进 `patch.json`。
