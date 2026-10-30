<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  🇨🇳 <b>简体中文</b> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### 外壳、电子器件和台架验收矩阵

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Version-0.2.7-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天真正能运行的部分：** 雷达外壳是**可打印的机械起点，不是 IP、射频或热学等级**；用于太阳能、电气和报警节点的参数化盒子由其源文件中的 `assert` 检查（板子放得下、电缆孔放得下、盖子避开立柱），但**都没有打印或测量过**（板子尺寸来自数据手册；触摸屏没有打印的盒子，沿用出厂外壳）。[台架验收矩阵](docs/BENCH_ACCEPTANCE.md)的每一行都是*未测试*。

---

## 📋 速览

| | |
|---|---|
| 版本 | `0.2.7` |
| 成熟度 | 可用 |
| 角色 | 外壳、电子元件和台架验收矩阵（家族：Hardware，上级：ARMOR-NODE-RADAR） |
| 技术栈 | OpenSCAD 2021.01+（CAD）、Python 3.11+（检查） |
| 测试 | 22 (`python -m unittest discover -s tests`) |
| 设计 | 雷达外壳和 3 种节点预设（太阳能、电气、报警）的盒子 |
| 运行位置 | 任何装有 OpenSCAD 的计算机 |
| 真实硬件 | 暂无：没有任何东西被打印或测量过；三个盒子只由源文件中的 `assert` 检查 |
| 许可证 | GPL-3.0-or-later |

**跳转到：** [概述](#-概述) · [架构](#-架构) · [安全](#-安全与防护) · [配置](#-配置) · [快速开始](#-快速开始) · [测试](#-测试) · [故障排除](#-故障排除) · [结构](#-仓库结构) · [相关项目](#-相关项目)

## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 软件 | 🟡 | 雷达外壳以及光伏、电气和报警节点的参数化盒子都是 OpenSCAD 源文件；雷达盒子是可打印的起点，并非 IP、射频或温度等级。 |
| 测试 | 🟡 | 22 个测试通过（`python -m unittest discover -s tests`）：源文件、盒子预设、模型文件以及文档中引用的数字。盒子也由其源码中的 `assert` 检查；都没有打印或测量过。 |
| 硬件 | 🔴 | 没有任何东西被打印或测量过，板子的尺寸来自数据手册，测试台验收矩阵的每一行都未测试。 |
| 文档 | 🟢 | 八种语言、设计输入和测试台验收矩阵均已编写并保持最新。 |

## 🎯 概述

* **雷达外壳是 `scad/node_enclosure_radar.scad`**（带 STL、3MF 和 AMF 导出以及两个切片项目：底座和滑动盖）：带遮阳罩、顶和底的 90 度转角底座、固定台阶、2 毫米的滑动前盖和侧翼，全部由命名参数驱动。
* **用于太阳能、电气和报警节点的参数化盒子**（`scad/node_box.scad`，预设 `solar`、`electrical` 和 `alarm`）：墙壁、板子立柱、电缆格兰头孔、通风孔、盖下的防拆微动开关槽，以及带环形唇边的盖子。这是低压盒子，不是市电布线的外壳。
* **支架**用于三个雷达模块、一个电缆格兰头和排水孔。台架矩阵要测试的 ESP32-S3-ETH-PoE 板、PoE 磁件、PTC 加热器和光传感器窗口还没有预留空间。未经测量，24 GHz 孔径前不要放置金属、导电或含碳的材料。
* **台架验收矩阵：**射频、环境、电源、网络和摄像头检查，每项都有方法和建议的通过标准，另有待填写的摄像头兼容性表。
* 制造之前，记录板子的确切轮廓、连接器、螺丝位置、天线净空区、热路径和防护目标（[设计输入](docs/DESIGN_INPUTS.md)）。

## 🧩 在 A.R.M.O.R. 中的角色

ARMOR-HARDWARE 是容纳各节点的部分。它包含雷达节点的外壳、太阳能、电气、报警和触摸屏节点的参数化盒子，以及说明原型上墙前如何评判的台架验收矩阵。它的设计是 [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)、[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)、[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)、[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) 和 [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI) 所运行的板子的起点。

## 🏛️ 架构

<p align="center">
  <img src="images/architecture.svg" alt="ARMOR-HARDWARE 的架构：谁调用它、它包含什么、它依赖什么" width="100%">
</p>

## 🔒 安全与防护

| 威胁 | 防御 |
|---|---|
| 在塑料盒中布设市电线路 | `node_box.scad` 是低压盒子，不是市电布线外壳 |
| 被遮挡的 24 GHz 雷达 | 未经测量，不要在 24 GHz 开口前放置金属、导电或含碳材料；盖板 2 mm 的厚度是台架矩阵中的一行 |
| 不存在的预设或部件 | `assert` 会中止渲染：`preset must be solar, electrical or alarm`、`part must be box, lid or both` |
| 无法装配的打印件 | 源码中的 `assert` 在渲染时拦截：电路板及其立柱能装下，电缆孔不被墙或立柱截断也不高于内部，盖唇宽 1.2 到 3 mm |

雷达外壳是可打印的机械起点，**不是 IP、射频或热学等级**。尚未打印或测量过任何东西。

## ⚙️ 配置

| 名称 | 值 | 作用 |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | `node_box.scad` 的壁厚与盖厚 |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | 电路板与盖板螺钉的立柱 |
| `screw_d` | 3.2 mm | 拧入立柱的 M3 自攻螺钉 |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | 盖与盒之间的间隙；环形唇的宽度（1.2 到 3 mm） |
| `preset`, `part` | `alarm` | `solar`、`electrical` 或 `alarm`；`box`、`lid` 或 `both` |
| `vent` | `true` | 盖上用于散热的一排槽 |

| 部件 | 内部尺寸 (mm) | 电路板 (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 快速开始

**要求:** OpenSCAD 2021.01+ (用于渲染外壳), 用于试制的 3D 打印机（FDM）.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

参见[验证边界](docs/VALIDATION.md)。预期的硬件许可证是 CERN-OHL-S-2.0；发布设计前请加入其完整文本。

## 🧪 测试

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| 测试文件 | 测试数 | 覆盖内容 |
|---|---|---|
| `test_enclosure_sources.py` | 22 | 源文件、盒子预设、模型文件以及文档中引用的数字 |

在装有 OpenSCAD 的机器上会渲染每个部件：雷达底座和盖板，以及三种预设的盒子和盖子。打印出的原型由[台架验收矩阵](docs/BENCH_ACCEPTANCE.md)评判。

## 🩺 故障排除

| 现象 | 原因 | 处理 |
|---|---|---|
| `preset must be solar, electrical or alarm` | `preset` 取了其他值 | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | 某个参数使立柱对内部来说太大 | 恢复 `post_d` 或选择更大的预设 |
| 盖子盖不上 | 打印机比 0.3 mm 的间隙更紧 | 增大 `clear` 后重新打印 |

## 📂 仓库结构

<p align="center">
  <img src="images/repository-structure.svg" alt="ARMOR-HARDWARE 的仓库结构" width="100%">
</p>

<details>
<summary>目录树的文本版</summary>

```text
ARMOR-HARDWARE/
├── scad/                                外壳及其模型文件
├── docs/                                本仓库的指南
├── tests/                               测试
├── tools/                               共享的 CI 检查和项目工具
├── .github/                             CI 工作流以及 Issue 和 Pull Request 模板
├── images/                              横幅、图标和本 README 的两幅图
├── build.sh build.bat                   通过共享的项目工作流构建
├── test.sh test.bat                     通过共享工作流运行测试
├── run.sh run.bat                       通过共享的项目工作流启动
├── armor.project.json                   清单：版本、角色、成熟度、构建命令
├── CHANGELOG.md                         每个版本的变化
├── SECURITY.md SUPPORT.md LICENSE       安全策略、支持和许可证
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   如何贡献与行为准则
├── build-test.sh build-test.bat         通过共享工作流运行测试
└── .gitattributes .gitignore            Git 设置
```

</details>

## 🗺️ 路线图与已知限制

**目前已知的限制**

* 尚未打印或测量；电路板尺寸来自数据手册，台架验收矩阵的每一行都是*未测试*。
* 尚未绘制 ESP32-S3-ETH-PoE 电路板、PoE 磁性元件、PTC 加热器和光传感器窗口的立体模型；触摸面板没有打印的盒子（保留出厂外壳）。
* 设计拟采用的硬件许可证是 CERN-OHL-S-2.0，其全文尚未放入仓库。

**下一步**

* 记录精确的电路板轮廓、连接器、螺钉位置、天线净空区、散热路径和防护目标（[设计输入](docs/DESIGN_INPUTS.md)）。
* 打印原型，并用带日期的测量结果填写台架验收矩阵。

## 🌍 语言

README 和文本提供英语、西班牙语、法语、意大利语、德语、汉语、日语和欧洲葡萄牙语版本。

## 🔗 相关项目

**A.R.M.O.R.**（Autonomous Radar & Multimodal Observation Range）是一个由相互独立的仓库组成的周界安全系统。每个仓库都有自己的版本、自己的测试和自己的 README；这是整个系列：

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - 消息契约、验证器、一致性向量和生成的类型
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - 面向 ESP32-S3 的现场节点固件，配三个雷达和自带的网页面板
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - 太阳能逆变器和电池的协议，以及网关节点的消息
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - 电气节点：电表、电网读数的消息和切换规则
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - 报警节点与面板：防区、布防、延时、警笛和 PIN，可配合服务器也可独立使用
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - 触摸面板：壁挂屏幕上的系统状态、布防与确认，以及语音助手的所在
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - 本地网络：其设备、互联网以及变化
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - 中央协调器：遥测、报警、设备、太阳能读数和摄像头
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - 网页控制台：摄像头、雷达、报警、太阳能以及 2D/3D 场地设计器
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - 带实时 2D/3D 雷达的 Android 操作员客户端
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - iPhone 操作员客户端
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - 视觉推理策略，会解释其决策且从不驱动设备
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - 面向 Jetson Orin NX 的摄像头区域、遮罩和检测规则
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - 离线语音意图，附带无法伪造的确认
* **ARMOR-HARDWARE**（本仓库） - 外壳、电子器件和台架验收矩阵
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - 部署、CM5 测试台、备份和 TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - 带可重复故障的离线遥测模拟器
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - 检测、安装和更新生态系统自身的仓库
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - 架构、安全基线和能力矩阵

## 📚 文档

* [设计输入](docs/DESIGN_INPUTS.md)：制造前要记录的内容
* [验证边界](docs/VALIDATION.md)：哪些已验证、哪些未验证
* [台架验收矩阵](docs/BENCH_ACCEPTANCE.md)：检查项、方法和建议的通过标准
* [能力矩阵：哪些已被证明，哪些没有](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [项目目录：版本以及各仓库之间如何相互依赖](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [本仓库的更新日志](CHANGELOG.md)

## 🤝 参与贡献与社区

* 提交 Pull Request 之前请运行 `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py`：必须通过。参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。
* README 提供八种语言，由 ARMOR-DOCS 中的源文件生成：文本的修改在那里进行。
* 组件之间消息的变更从 ARMOR-COMMON 开始。
* 不要把仅仅构建过的东西描述为已在板子上运行。
* 请私下报告漏洞：[SECURITY.md](SECURITY.md)。问题、想法和报告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

GPL-3.0-or-later - 见 [LICENSE](LICENSE)。
