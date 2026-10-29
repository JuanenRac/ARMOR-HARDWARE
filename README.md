<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  🇺🇸 <b>English</b> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Enclosures, electronics and the bench acceptance matrix

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Version-0.2.6-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**Honesty check - what runs today:** The radar enclosure is a **printable mechanical starting point, not an IP, RF or thermal rating**, and the parametric box for the solar, electrical and alarm nodes is checked by the asserts of its source (the board fits, the cable holes fit, the lid clears the posts), but **none has been printed or measured** (the board sizes come from data sheets; the touch panel has no printed box, it keeps its factory enclosure). Every row of the [bench acceptance matrix](docs/BENCH_ACCEPTANCE.md) is *not tested*.

---

## 📋 At a glance

| | |
|---|---|
| Version | `0.2.6` |
| Maturity | Functional |
| Role | Enclosures, electronics and the bench acceptance matrix (family: Hardware, parent: ARMOR-NODE-RADAR) |
| Stack | OpenSCAD 2021.01+ (CAD), Python 3.11+ (checks) |
| Tests | 22 (`python -m unittest discover -s tests`) |
| Designs | The radar enclosure and the box of 3 node presets (solar, electrical, alarm) |
| Runs on | Any computer with OpenSCAD |
| On real hardware | None yet: nothing has been printed or measured; the three boxes are only checked by the asserts of their source |
| License | GPL-3.0-or-later |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Security](#-security--safety) · [Configuration](#-configuration) · [Quick start](#-quick-start) · [Testing](#-testing) · [Troubleshooting](#-troubleshooting) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Software | 🟡 | The radar enclosure and the parametric box of the solar, electrical and alarm nodes are OpenSCAD sources; the radar box is a printable starting point, not an IP, RF or thermal rating. |
| Tests | 🟡 | 22 tests pass (`python -m unittest discover -s tests`): the sources, the presets of the box, the model files and the numbers the documents quote. The boxes are also checked by the asserts of their source; none has been printed or measured. |
| Hardware | 🔴 | Nothing has been printed or measured, the board sizes come from data sheets, and every row of the bench acceptance matrix is not tested. |
| Documentation | 🟢 | Eight languages, the design inputs and the bench acceptance matrix are written and up to date. |

## 🎯 Overview

* **The radar enclosure is `scad/node_enclosure_radar.scad`** (with STL, 3MF and AMF exports and two slicer projects, the base and the sliding cover): a 90-degree corner base with a visor, roof and floor, retaining steps, a sliding 2 mm front cover and side flaps, all driven by named parameters.
* **A parametric box for the solar, electrical and alarm nodes** (`scad/node_box.scad`, presets `solar`, `electrical` and `alarm`): walls, posts for the board, cable-gland holes, a vent, a pocket for a tamper micro-switch under the lid and a lid with a ring-shaped lip. It is a low-voltage box, not an enclosure for mains wiring.
* **Holders** for three radar modules, a cable gland and drain holes. There are no volumes yet for the ESP32-S3-ETH-PoE board, the PoE magnetics, the PTC heater or the light-sensor window that the bench matrix wants to test. No metallic, conductive or carbon-loaded material in front of a 24 GHz aperture without measuring it first.
* **Bench acceptance matrix:** the radio, environment, power, network and camera checks with a method and a proposed pass criterion each, and a camera compatibility table to fill in.
* Before fabrication, record exact board outlines, connectors, screw positions, antenna keep-outs, the thermal path and the ingress target ([design inputs](docs/DESIGN_INPUTS.md)).

## 🧩 Role in A.R.M.O.R.

ARMOR-HARDWARE is what holds the nodes. It carries the enclosure of the radar node, the parametric box of the solar, electrical, alarm and touch-panel nodes, and the bench acceptance matrix that says how a prototype is to be judged before it goes on a wall. Its designs are the starting point for the boards that [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) and [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI) run on.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="ARMOR-HARDWARE architecture: who calls it, what it holds and what it depends on" width="100%">
</p>

## 🔒 Security & Safety

| Threat | Defence |
|---|---|
| Mains wiring in a plastic box | `node_box.scad` is a low-voltage box, not an enclosure for mains wiring |
| A blocked 24 GHz radar | No metallic, conductive or carbon-loaded material in front of a 24 GHz aperture without measuring it first; the 2 mm cover thickness is a row of the bench matrix |
| A preset or a part that does not exist | `assert` stops the render: `preset must be solar, electrical or alarm`, `part must be box, lid or both` |
| A print that does not fit | The asserts of the source catch it when the file is rendered: the board and its posts fit, the cable holes are not cut by a wall or a post nor taller than the inside, the lid lip is 1.2 to 3 mm |

The radar enclosure is a printable mechanical starting point, **not an IP, RF or thermal rating**. Nothing has been printed or measured.

## ⚙️ Configuration

| Name | Value | What it sets |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | Wall and lid thickness of `node_box.scad` |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | The posts for the board and for the lid screws |
| `screw_d` | 3.2 mm | M3 self-tapping screws into the posts |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | Play between lid and box; width of the ring-shaped lip (1.2 to 3 mm) |
| `preset`, `part` | `alarm` | `solar`, `electrical` or `alarm`; `box`, `lid` or `both` |
| `vent` | `true` | A row of slots in the lid so the heat can leave |

| Piece | Inside size (mm) | Board (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 Quick start

**Requirements:** OpenSCAD 2021.01+ (to render the enclosures), a 3D printer (FDM) to try them.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

See the [validation boundary](docs/VALIDATION.md). The intended hardware licence is CERN-OHL-S-2.0; add its full text before releasing the designs.

## 🧪 Testing

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| Test file | Tests | What it covers |
|---|---|---|
| `test_enclosure_sources.py` | 22 | The sources, the presets of the box, the model files and the numbers the documents quote |

OpenSCAD renders every piece on a machine that has it: the radar base and cover, and the box and lid of the three presets. The [bench acceptance matrix](docs/BENCH_ACCEPTANCE.md) is where a printed prototype is judged.

## 🩺 Troubleshooting

| You see | Because | Do |
|---|---|---|
| `preset must be solar, electrical or alarm` | The `preset` is something else | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | A parameter made the posts too big for the inside | Restore `post_d` or choose a bigger preset |
| The lid does not close | Your printer is tighter than the 0.3 mm of play | Raise `clear` and print again |

## 📂 Repository Structure

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository structure of ARMOR-HARDWARE" width="100%">
</p>

<details>
<summary>Text version of the tree</summary>

```text
ARMOR-HARDWARE/
├── scad/                                the enclosures and their model files
├── docs/                                the guides of this repository
├── tests/                               the tests
├── tools/                               the shared CI checks and project tooling
├── .github/                             CI workflow, issue and pull-request templates
├── images/                              banner, icon and the two pictures of this README
├── build.sh build.bat                   build through the shared project workflow
├── test.sh test.bat                     run the tests through the shared workflow
├── run.sh run.bat                       start through the shared project workflow
├── armor.project.json                   manifest: version, role, maturity, build command
├── CHANGELOG.md                         what changed in each version
├── SECURITY.md SUPPORT.md LICENSE       security policy, support and license
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   how to contribute and the code of conduct
├── build-test.sh build-test.bat         run the tests through the shared workflow
└── .gitattributes .gitignore            Git settings
```

</details>

## 🗺️ Roadmap & Known limits

**Known limits today**

* Nothing has been printed or measured; the board sizes come from data sheets and every row of the bench acceptance matrix is *not tested*.
* There are no volumes yet for the ESP32-S3-ETH-PoE board, the PoE magnetics, the PTC heater or the light-sensor window; the touch panel has no printed box (it keeps its factory enclosure).
* The hardware licence intended for the designs is CERN-OHL-S-2.0, and its full text is not in the repository yet.

**Next**

* Record the exact board outlines, connectors, screw positions, antenna keep-outs, the thermal path and the ingress target ([design inputs](docs/DESIGN_INPUTS.md)).
* Print the prototypes and fill in the bench acceptance matrix with dated measurements.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) is a perimeter-security system made of independent repositories. Each one has its own version, its own tests and its own README; this is the family:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Message contracts, validators, conformance vectors and generated types
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Field-node firmware for ESP32-S3 with three radars and its own web panel
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Solar inverter and battery protocols and the messages of a gateway node
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Electrical node: meters, the message of the network's readings and the rules for switching
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Alarm node and panel: zones, arming, delays, siren and PIN, with the server or without it
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Touch panel: the state of the system on a wall screen, arming and acknowledging, and the home of the voice assistant
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - The local network: its devices, the internet and what changes
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Central coordinator: telemetry, alarms, devices, solar readings and cameras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Web console: cameras, radar, alarms, solar energy and the 2D/3D site designer
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Android operator client with a live 2D/3D radar
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - iPhone operator client
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Visual inference policy that explains its decisions and never actuates
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Camera zones, masks and detection rules for the Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Offline voice intents with a confirmation that cannot be forged
* **ARMOR-HARDWARE** (this repository) - Enclosures, electronics and the bench acceptance matrix
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Deployment, the CM5 test bench, backup and TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Offline telemetry simulator with repeatable faults
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Detects, installs and updates the ecosystem's own repositories
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Architecture, security baseline and the capability matrix

## 📚 Documentation

* [Design inputs](docs/DESIGN_INPUTS.md): what to record before fabrication
* [Validation boundary](docs/VALIDATION.md): what is and is not validated
* [Bench acceptance matrix](docs/BENCH_ACCEPTANCE.md): the checks, their methods and proposed pass criteria
* [Capability matrix: what is proven and what is not](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Project catalogue: versions and how the repositories depend on each other](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Changelog of this repository](CHANGELOG.md)

## 🤝 Contributing & Community

* Before a pull request run `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py`: it must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages and is generated from the sources in ARMOR-DOCS: a change to the text is made there.
* A change to a message between components starts in ARMOR-COMMON.
* Do not describe as working on a board what has only been built.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

GPL-3.0-or-later - see [LICENSE](LICENSE).
