# 虚拟环境经验手册实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增一份兼顾 Python 新手和项目维护者的虚拟环境经验手册，并以本项目的 `.venv-build` 实践提炼可供其他项目复用的规范。

**Architecture:** 文档采用“基础原理—本项目实践—标准操作—故障排查—通用模板—检查清单”的递进结构。项目专用做法与通用建议分开说明，避免把多个版本共用一个构建环境误用到彼此无关的项目中。

**Tech Stack:** Markdown、Windows PowerShell、Python 3.12、`venv`、`pip`、PyInstaller

---

### Task 1: 创建经验手册

**Files:**

- Create: `虚拟环境经验手册.md`

- [ ] **Step 1: 编写基础原理**

说明虚拟环境是什么、隔离了什么、没有隔离什么，以及系统 Python、虚拟环境 Python、项目源码和依赖清单之间的关系。

- [ ] **Step 2: 记录本项目实践**

记录共享环境位置 `04-正式发行版/.venv-build`、各版本独立保存 `requirements-build.txt` 的职责，以及正式打包必须显式调用共享环境解释器。

- [ ] **Step 3: 写入可复制的标准流程**

提供创建、安装、验证、打包、切换版本、更新依赖、重建环境和退出环境的 PowerShell 命令，并避免写死 `全功能整合包x.x` 的版本号。

- [ ] **Step 4: 写入真实经验和故障排查**

说明 Windows 虚拟环境不能依赖直接移动或复制；记录启动器可能保留旧绝对路径、全局包污染可能影响 PyInstaller 收集结果，以及 `pip check`、解释器路径和依赖版本的核对方法。

- [ ] **Step 5: 提炼其他项目适用的规范**

明确无关项目默认“一项目一环境”；只有同一产品的多个版本、Python 主次版本一致且依赖清单受控时，才考虑共用构建环境。

### Task 2: 验证文档

**Files:**

- Verify: `虚拟环境经验手册.md`

- [ ] **Step 1: 检查需求覆盖**

确认文档包含功能、作用、优点、限制、本项目案例、通用经验、操作命令、排错方法和检查清单。

- [ ] **Step 2: 检查 Markdown**

确认标题层级、代码围栏和表格结构完整，无空占位内容。

- [ ] **Step 3: 检查工作区改动**

确认只新增计划和经验手册，没有改动程序、虚拟环境或已有版本文件。
