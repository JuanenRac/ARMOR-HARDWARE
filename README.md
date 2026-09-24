<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a></p>

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

## 1. 🛠️ OVERVIEW

* **The real design is `CAD/CARCASA_SENSORES.scad`** (with STL, 3MF and AMF exports): a 90-degree corner base with a visor, roof and floor, retaining steps, a sliding 2 mm front cover and side flaps, all driven by named parameters. `scad/node_enclosure.scad` is only a placeholder box.
* **Reserved volumes** for three radar modules, the ESP32-S3-ETH-PoE board, the sensor window, a cable gland, the PoE magnetics and the PTC heater. No metallic, conductive or carbon-loaded material in front of a 24 GHz aperture without measured attenuation.
* **Bench acceptance matrix:** the radio, environment, power, network and camera checks with a method and a proposed pass criterion each, and a camera compatibility table to fill in.
* Before fabrication, record exact board outlines, connectors, screw positions, antenna keep-outs, the thermal path and the ingress target ([design inputs](docs/DESIGN_INPUTS.md)).

---

## 2. 🔧 BUILD & RUN

```powershell
openscad -o build/CARCASA_SENSORES.stl CAD/CARCASA_SENSORES.scad
```

See the [validation boundary](docs/VALIDATION.md). The intended hardware licence is CERN-OHL-S-2.0; add its full text before releasing the designs.

---

## 📂 DIRECTORY STRUCTURE

```text
ARMOR-HARDWARE/
├── CAD/     CARCASA_SENSORES.scad (+ stl, 3mf, amf)
├── scad/    node_enclosure.scad (placeholder)
├── EDA/     KiCad (empty)
└── docs/    DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
```

---

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

GPL-3.0-or-later - see [LICENSE](LICENSE).
