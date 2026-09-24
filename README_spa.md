<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b></p>

### Carcasas, electrónica y la matriz de aceptación de banco

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/EDA-KiCad-314cb0.svg" alt="EDA">
  <img src="https://img.shields.io/badge/Maturity-mechanical%20baseline-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - qué funciona hoy:** La carcasa es un **punto de partida mecánico imprimible, no una clasificación IP, RF ni térmica.** No se ha medido nada en un prototipo; cada fila de la [matriz de aceptación de banco](docs/BENCH_ACCEPTANCE.md) está *sin probar*.

---

## 1. 🛠️ DESCRIPCIÓN

* **El diseño real es `CAD/CARCASA_SENSORES.scad`** (con exportaciones STL, 3MF y AMF): una base de esquina de 90 grados con visera, techo y suelo, escalones de retención, una tapa frontal deslizante de 2 mm y solapas laterales, todo gobernado por parámetros con nombre. `scad/node_enclosure.scad` es solo una caja de ejemplo.
* **Volúmenes reservados** para tres módulos de radar, la placa ESP32-S3-ETH-PoE, la ventana del sensor, un prensaestopas, la magnética PoE y el calefactor PTC. Ningún material metálico, conductor o cargado de carbono delante de una apertura de 24 GHz sin atenuación medida.
* **Matriz de aceptación de banco:** las comprobaciones de radio, entorno, alimentación, red y cámaras con un método y un criterio propuesto cada una, y una tabla de compatibilidad de cámaras por rellenar.
* Antes de fabricar, registrar contornos exactos de placas, conectores, posición de tornillos, zonas libres de antena, el camino térmico y el objetivo de estanqueidad ([entradas de diseño](docs/DESIGN_INPUTS.md)).

---

## 2. 🔧 COMPILAR Y EJECUTAR

```powershell
openscad -o build/CARCASA_SENSORES.stl CAD/CARCASA_SENSORES.scad
```

Véase el [límite de validación](docs/VALIDATION.md). La licencia de hardware prevista es CERN-OHL-S-2.0; añade su texto completo antes de publicar los diseños.

---

## 📂 ESTRUCTURA DE DIRECTORIOS

```text
ARMOR-HARDWARE/
├── CAD/     CARCASA_SENSORES.scad (+ stl, 3mf, amf)
├── scad/    node_enclosure.scad (ejemplo)
├── EDA/     KiCad (vacío)
└── docs/    DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
```

---

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

GPL-3.0-or-later - véase [LICENSE](LICENSE).
