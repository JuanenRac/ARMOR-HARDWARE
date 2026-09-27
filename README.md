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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### Enclosures, electronics and the bench acceptance matrix

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/EDA-KiCad-314cb0.svg" alt="EDA">
  <img src="https://img.shields.io/badge/Maturity-mechanical%20baseline-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what runs today:** The enclosure is a **printable mechanical starting point, not an IP, RF or thermal rating.** Nothing has been measured on a prototype; every row of the [bench acceptance matrix](docs/BENCH_ACCEPTANCE.md) is *not tested*.

---

## 🎯 Overview

* **The real design is `CAD/CARCASA_SENSORES.scad`** (with STL, 3MF and AMF exports): a 90-degree corner base with a visor, roof and floor, retaining steps, a sliding 2 mm front cover and side flaps, all driven by named parameters. `scad/node_enclosure.scad` is only a placeholder box.
* **Reserved volumes** for three radar modules, the ESP32-S3-ETH-PoE board, the sensor window, a cable gland, the PoE magnetics and the PTC heater. No metallic, conductive or carbon-loaded material in front of a 24 GHz aperture without measured attenuation.
* **Bench acceptance matrix:** the radio, environment, power, network and camera checks with a method and a proposed pass criterion each, and a camera compatibility table to fill in.
* Before fabrication, record exact board outlines, connectors, screw positions, antenna keep-outs, the thermal path and the ingress target ([design inputs](docs/DESIGN_INPUTS.md)).

## 📂 Repository Structure

```text
ARMOR-HARDWARE/
├── CAD/     CARCASA_SENSORES.scad (+ stl, 3mf, amf)
├── scad/    node_enclosure.scad (placeholder)
├── EDA/     KiCad (empty)
└── docs/    DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
```

## 🛠️ Development Environment

```powershell
openscad -o build/CARCASA_SENSORES.stl CAD/CARCASA_SENSORES.scad
```

See the [validation boundary](docs/VALIDATION.md). The intended hardware licence is CERN-OHL-S-2.0; add its full text before releasing the designs.

## 🔗 Related Projects

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) is a perimeter-security system made of independent repositories. Each one has its own version, its own tests and its own README; this is the family:

* **[ARMOR-COMMON](../ARMOR-COMMON)** - Message contracts, validators, conformance vectors and generated types
* **[ARMOR-RADAR](../ARMOR-RADAR)** - Field-node firmware for ESP32-S3 with three radars and its own web panel
* **[ARMOR-SOLAR](../ARMOR-SOLAR)** - Solar inverter and battery protocols and the messages of a gateway node
* **[ARMOR-ELECTRICAL](../ARMOR-ELECTRICAL)** - Electrical node: meters, the message of the network's readings and the rules for switching
* **[ARMOR-NETWORK](../ARMOR-NETWORK)** - The local network: its devices, the internet and what changes
* **[ARMOR-SERVER](../ARMOR-SERVER)** - Central coordinator: telemetry, alarms, devices, solar readings and cameras
* **[ARMOR-STUDIO](../ARMOR-STUDIO)** - Web console: cameras, radar, alarms, solar energy and the 2D/3D site designer
* **[ARMOR-ANDROID-CONTROL](../ARMOR-ANDROID-CONTROL)** - Android operator client with a live 2D/3D radar
* **[ARMOR-SERVER-AI](../ARMOR-SERVER-AI)** - Visual inference policy that explains its decisions and never actuates
* **[ARMOR-VOICE-AI](../ARMOR-VOICE-AI)** - Offline voice intents with a confirmation that cannot be forged
* **ARMOR-HARDWARE** (this repository) - Enclosures, electronics and the bench acceptance matrix
* **[ARMOR-DEVOPS](../ARMOR-DEVOPS)** - Deployment, the CM5 test bench, backup and TLS
* **[ARMOR-SIMULATOR](../ARMOR-SIMULATOR)** - Offline telemetry simulator with repeatable faults
* **[ARMOR-UPDATER](../ARMOR-UPDATER)** - Detects, installs and updates the ecosystem's own repositories
* **[ARMOR-DOCS](../ARMOR-DOCS)** - Architecture, security baseline and the capability matrix

## 📚 Documentation & Community

Where to read more:

* [Capability matrix: what is proven and what is not](../ARMOR-DOCS/docs/CAPABILITY_MATRIX.md)
* [Project catalogue: versions and how the repositories depend on each other](../ARMOR-DOCS/docs/PROJECT_CATALOG.md)
* [Changelog of this repository](CHANGELOG.md)
* [License (GPL-3.0-or-later)](LICENSE)
* Questions, ideas and reports: electrohobby3d@gmail.com

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

GPL-3.0-or-later - see [LICENSE](LICENSE).
