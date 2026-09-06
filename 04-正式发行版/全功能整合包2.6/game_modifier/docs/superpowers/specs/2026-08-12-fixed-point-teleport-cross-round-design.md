# 定点瞬移跨回合保留设计

## 目标

同一房间内，点位1和点位2在普通回合结束及新回合开始后继续有效；真正离开房间、模式实例变化、关闭功能或脚本清理时仍清除点位。

## 行为设计

- `GameManager.GameRoundEnd` 和 `GameManager.NewGameRoundStart` 不再调用完整的房间重置。
- 两个回合事件仍保留 Hook，仅取消尚未执行的保存/瞬移动作，防止动作跨回合延迟执行。
- 回合事件不递增 `roomGeneration`，已保存点位因此继续有效。
- `mode_base_changed` 与 `game_manager_destroy` 继续调用完整重置并清空点位。
- 关闭功能和脚本 cleanup 的现有清理行为保持不变。

## 测试

静态测试必须证明：两个回合 Hook 调用轻量的 pending 清理；它们不调用 `handleRoundBoundary`；房间销毁和模式实例变化仍调用完整房间清理。
