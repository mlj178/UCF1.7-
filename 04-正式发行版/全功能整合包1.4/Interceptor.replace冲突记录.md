# Interceptor.replace 冲突记录

## 发现的冲突：射速变快 vs 无后座力

两个模块都 `replace` 了同一个函数 `Recoil.OnGunShot`（地址 `0xB19980`）：

| 模块 | 替换回调 | 参数签名 |
|------|---------|---------|
| 无后座力 (recoilModule) | 清零 4 个后座力浮点字段 | `['pointer', 'pointer']` ✅ |
| 射速变快 (speedGunModule) | **空函数 `{}`** | `['pointer']` ❌ 少一个参数 |

后开启的模块会**直接顶掉**先开启的 replace。但射速变快有 4 个 hook 在不同地址（`getShootIntervalTime`、`gunShootNoCheck`、`recoilGetCurrentPerturb`），主要射速逻辑不在 `OnGunShot` 上，所以即使被顶了，射速效果依然生效。

## 测试结论

| 开启顺序 | 现象 | 解释 |
|---------|------|------|
| recoil → speedgun | recoil 失效，speedgun 射速仍在 | `OnGunShot` 被空回调顶了，但射速靠其他 hook 维持 |
| speedgun → recoil | 两者效果都在 | recoil 的清零回调覆盖空回调，speedgun 其他 hook 不受影响 |
| 开 recoil → 关 recoil → 再开任一个 | 行为不可预期 | `revert` 恢复的是最后一次 replace 的回调，不是原始函数 |

## 其他未发现冲突的模块

逐一检查过所有模块，**没有其他函数被两个模块同时 replace**。`isMyPlayer` 虽被多个模块用到，但仅 isbot 做了 replace，其他只是 `new NativeFunction` 调用它。

## 后续解决思路

将可能冲突的 replace 统一管理：脚本启动时只 replace 一次，之后通过修改配置变量来控制回调行为，不再重复调用 `Interceptor.replace`。
