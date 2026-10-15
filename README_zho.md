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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### 外壳、电子器件和台架验收矩阵

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/EDA-KiCad-314cb0.svg" alt="EDA">
  <img src="https://img.shields.io/badge/Maturity-mechanical%20baseline-FFB020.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天真正能运行的部分:** 外壳是一个**可打印的机械起点，不是 IP、射频或热学认证。** 没有在原型上测量过任何东西；[台架验收矩阵](docs/BENCH_ACCEPTANCE.md)的每一行都是*未测试*。

---

## 🎯 概述

* **真正的设计是 `CAD/CARCASA_SENSORES.scad`**（附 STL、3MF 和 AMF 导出）：带遮光檐、顶部和底板的 90 度拐角底座、固位台阶、2 mm 滑动前盖和侧翼，全部由命名参数驱动。`scad/node_enclosure.scad` 只是占位盒。
* **预留空间**：三个雷达模块、ESP32-S3-ETH-PoE 开发板、传感器窗口、电缆固定头、PoE 磁性元件和 PTC 加热器。在没有实测衰减的情况下，24 GHz 窗口前不得使用金属、导电或含碳材料。
* **台架验收矩阵：** 射频、环境、电源、网络和摄像头检查，每项都有方法和建议的通过标准，另有待填写的摄像头兼容性表。
* 制造前，记录开发板的精确外形、连接器、螺丝位置、天线禁区、热路径和防护目标（[设计输入](docs/DESIGN_INPUTS.md)）。

## 📂 仓库结构

```text
ARMOR-HARDWARE/
├── CAD/     CARCASA_SENSORES.scad (+ stl, 3mf, amf)
├── scad/    node_enclosure.scad (placeholder)
├── EDA/     KiCad (empty)
└── docs/    DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
```

## 🛠️ 开发环境

```powershell
openscad -o build/CARCASA_SENSORES.stl CAD/CARCASA_SENSORES.scad
```

参见[验证边界](docs/VALIDATION.md)。预期的硬件许可证是 CERN-OHL-S-2.0；发布设计前请补上其完整文本。

## 🔗 相关项目

**A.R.M.O.R.**（Autonomous Radar & Multimodal Observation Range）是由若干独立仓库组成的周界安防系统。每个仓库都有自己的版本、测试和 README；家族成员如下：

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - 消息契约、验证器、一致性向量和生成的类型
* **[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)** - 适用于 ESP32-S3 的现场节点固件，带三个雷达和自带网页面板
* **[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)** - 太阳能逆变器与电池的协议，以及网关节点的消息
* **[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)** - 电气节点：电表、电网读数消息和开关规则
* **[ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI)** - 触摸面板：墙面屏幕上的系统状态、布防与确认，以及语音助手的所在
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - 本地网络：其设备、互联网以及变化
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - 中央协调器：遥测、报警、设备、太阳能读数和摄像头
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - 网页控制台：摄像头、雷达、报警、太阳能和 2D/3D 场地设计器
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - 带实时 2D/3D 雷达的 Android 操作员客户端
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - 会解释决策且从不执行动作的视觉推理策略
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - 带无法伪造确认的离线语音意图
* **ARMOR-HARDWARE** (本仓库) - 外壳、电子器件和台架验收矩阵
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - 部署、CM5 测试台、备份与 TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - 带可重复故障的离线遥测模拟器
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - 发现、安装并更新生态系统自身的仓库
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - 架构、安全基线和能力矩阵

## 📚 文档与社区

更多阅读：

* [能力矩阵：哪些已被证实，哪些没有](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [项目目录：版本以及各仓库之间的依赖](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [本仓库的变更记录](CHANGELOG.md)
* [许可证（GPL-3.0-or-later）](LICENSE)
* 问题、想法与反馈：electrohobby3d@gmail.com

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

GPL-3.0-or-later - 见 [LICENSE](LICENSE)。
