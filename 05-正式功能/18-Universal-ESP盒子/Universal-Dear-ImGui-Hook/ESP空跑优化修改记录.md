# ESP 空跑优化修改记录

## 修改目的

保留方框透视和 DLL 自动注入机制，停止 ESP 关闭时无意义的 ImGui 帧处理，并停用当前发行版不使用的 DLL 内置菜单输入路径。

## 已停用的内容

- D3D11 `Present` 中的 F10 菜单按键检测。
- `menu::Init()` 内置菜单绘制调用。
- 游戏窗口 `inputhook::Init()` 菜单输入 Hook。
- `mousehooks::Init()` 对 `SetCursorPos`、`ClipCursor` 的 Hook。
- ESP 关闭时每帧执行的 `NewFrame`、`Render` 和 `RenderDrawData`。

上述源码和函数仍然保留，只是不再由当前发行路径引用，后续需要内置菜单时可以恢复。

## 保留的内容

- DLL 注入和 D3D11 `Present` Hook。
- 命名管道控制，用于外部修改器开启、关闭方框。
- `LoadLibraryA/W` Hook，用于捕获晚加载的 DirectX 后端。
- Insert 键紧急卸载 DLL。
- ESP 开启时所需的 ImGui 上下文和完整绘制帧。
- GameManager、玩家列表、Bot、坐标和碰撞体数据读取。

## 方框绘制路径

```text
外部修改器
  → 命名管道 set_state(esp_box=true)
  → ESPState::SetBoxEnabled(true)
  → D3D11 Present Hook
  → ImGui_ImplDX11_NewFrame / ImGui::NewFrame
  → ESPRenderer::Render
  → GameManager::RefreshSession / GetAllPlayers / GetBotPlayers
  → TransformHelper::GetHitboxData
  → ESPRenderer::DrawBox
  → ImGui::GetBackgroundDrawList()->AddRect
  → ImGui::Render
  → ImGui_ImplDX11_RenderDrawData
```

方框本身使用 ImGui DrawList 绘制。因此 ESP 开启时不能注释 `NewFrame`、`ImGui::Render` 或 `RenderDrawData`，否则方框不会显示。

## 预期运行状态

- ESP 关闭：首次运行仍完成一次 D3D11/ImGui 后端初始化，保证 Hook 状态确认和命名管道能够启动；之后不创建 ImGui Frame，也不查询玩家和坐标。
- ESP 开启：按原路径实时查询玩家并绘制方框，方框显示不受影响。
- ESP 再次关闭：立即停止 ImGui Frame 和玩家数据处理；已经创建的资源保留到 DLL 卸载时统一释放。
- DLL 内置菜单：源码保留，但 F10、菜单绘制和鼠标输入 Hook 不再生效。

## DLL 代码文件使用情况

以下结论来自 `Universal-ImGui-Hook.vcxproj` 的实际编译清单。

### 当前 DX11 方框功能必须使用

| 文件 | 做什么 | 没有它的效果 |
|---|---|---|
| `dllmain.cpp` | DLL 入口，初始化 Hook、命名管道和卸载流程 | DLL 加载后不会工作 |
| `globals.cpp`、`namespaces.h` | 保存模块、窗口、按键和渲染后端等公共状态 | 各模块无法共享状态或无法编译 |
| `stdafx.h` | 集中引用 Windows、DirectX、ImGui 和 ESP 头文件，并提供日志 | 大量源码无法编译 |
| `d3d11hook.cpp` | Hook D3D11 `Present`，驱动 ESP 和 ImGui 方框绘制 | 没有方框显示 |
| `minhook/include/MinHook.h`、`minhook/lib/libMinHook.x86.lib` | 提供函数 Hook 能力，并静态链接进 x86 DLL | 无法安装 `Present` 和游戏函数 Hook |
| `esp/named_pipe_server.cpp/.h` | 接收外部修改器的开启、关闭和卸载命令 | 修改器无法控制 ESP |
| `esp/esp_state.h` | 保存 `esp_box` 开关状态 | 无法判断是否需要运行 ESP |
| `esp/il2cpp_bridge.cpp/.h` | 连接 GameAssembly，取得 GameManager | 找不到游戏对象 |
| `esp/game_manager.cpp/.h` | 取得本地玩家、其他玩家和 Bot，处理房间切换 | 没有玩家数据，切房后可能使用旧对象 |
| `esp/transform_helper.cpp/.h` | 读取玩家位置、碰撞体和边界 | 无法计算方框位置和大小 |
| `esp/coord_converter.cpp/.h` | 把游戏世界坐标转换为屏幕坐标 | 方框无法画到正确屏幕位置 |
| `esp/esp_renderer.cpp/.h` | 组织玩家数据并调用 `AddRect` 绘制方框 | 有坐标数据也不会出现方框 |
| `esp/esp_common.h` | 定义偏移、颜色、尺寸和安全读取工具 | ESP 数据结构和参数缺失 |
| `imgui/imgui.cpp`、`imgui_draw.cpp` | 创建 ImGui 帧并提供 DrawList/`AddRect` | 方框无法生成 |
| `imgui/imgui_impl_dx11.cpp/.h` | 把 ImGui 绘制数据提交给 D3D11 | 方框生成了也无法显示 |
| `imgui/imgui_impl_win32.cpp/.h` | 为 ImGui 提供窗口和每帧基础信息 | ImGui 帧初始化不完整 |

### 会编译进工程，但当前 DX11 方框路径没有使用

| 文件 | 原用途 | 当前状态 |
|---|---|---|
| `menu.cpp` | DLL 内置 F10 菜单 | 调用已注释，方框不依赖它 |
| `inputhooks.cpp` | 菜单打开时接管游戏窗口输入 | 初始化已注释，方框不需要输入 |
| `mousehooks.cpp` | 菜单打开时解除鼠标锁定 | 初始化已注释，方框不需要鼠标 |
| `d3d9hook.cpp` | D3D9 游戏渲染 Hook | 当前游戏走 D3D11，不使用 |
| `d3d10hook.cpp` | D3D10 游戏渲染 Hook | 当前游戏走 D3D11，不使用 |
| `d3d12hook.cpp`、`hooks.cpp` | D3D12 游戏渲染 Hook | 当前游戏走 D3D11，不使用 |
| `imgui_impl_dx9.cpp`、`imgui_impl_dx10.cpp`、`imgui_impl_dx12.cpp` | 其他 DirectX 后端的 ImGui 支持 | DX11 方框不使用 |
| `imgui_widgets.cpp`、`imgui_tables.cpp` | 菜单控件和表格 | 内置菜单停用后，方框路径不直接使用 |

这些文件仍在 `.vcxproj` 中，所以会参与 DLL 工程编译；只是当前 DX11 方框运行路径不会调用它们。

### 不会编译进 DLL

| 文件/目录 | 用途 |
|---|---|
| `inject.cs`、`run_inject.bat` | 独立注入器及启动脚本，不属于 DLL 代码 |
| `build_mingw.bat`、`.sln`、`.vcxproj`、`.filters` | 构建配置文件 |
| `使用教程.md`、日志 `.txt`、`tools/` | 说明、运行日志和检查工具 |
| `intermediate/`、已有 `Universal-ImGui-Hook.dll` | 编译中间产物和旧 DLL 成品 |
| `imgui/misc/` | ImGui 示例、字体和辅助工具，当前工程没有加入编译 |

本次未编译 DLL。重新编译后，需要把生成的 `Universal-ImGui-Hook.dll` 更新到 1.7 修复版的 `game_modifier/plugins/universal_hook/` 目录。
