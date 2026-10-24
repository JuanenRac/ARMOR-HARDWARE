<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  🇪🇸 <b>Español</b> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Carcasas, electrónica y la matriz de aceptación de banco

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Version-0.2.6-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - qué funciona hoy:** La carcasa del radar es un **punto de partida mecánico imprimible, no una clasificación IP, RF ni térmica**, y la caja paramétrica para los nodos solar, eléctrico y de alarma está comprobada por los `assert` de su fuente (la placa cabe, los agujeros de cables caben, la tapa libra los postes), pero **ninguna se ha imprimido ni medido** (los tamaños de las placas salen de las hojas de datos; el panel táctil no tiene caja impresa, conserva su carcasa de fábrica). Cada fila de la [matriz de aceptación en banco](docs/BENCH_ACCEPTANCE.md) está *sin probar*.

---

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.2.6` |
| Madurez | Funcional |
| Tecnología | OpenSCAD |
| En hardware real | Ninguno todavía: nada se ha impreso ni medido; las tres cajas solo las comprueban los `assert` de su fuente |

## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Se escribe con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo previsto.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Hecho a medias o sin verificar · 🔴 Sin hacer o sin funcionar

| Área | Estado | Qué significa aquí |
|---|---|---|
| Software | 🟡 | La carcasa del radar y la caja paramétrica de los nodos solar, eléctrico y de alarma son fuentes de OpenSCAD; la caja del radar es un punto de partida imprimible, no una clasificación IP, RF ni térmica. |
| Pruebas | 🟡 | Las cajas se comprueban con las aserciones de su fuente (la placa cabe, los orificios de cables caben, la tapa libra los postes); ninguna se ha impreso ni medido. |
| Hardware | 🔴 | Nada se ha impreso ni medido, las medidas de las placas salen de hojas de datos, y cada fila de la matriz de aceptación en banco está sin probar. |
| Documentación | 🟢 | Ocho idiomas, los datos de diseño y la matriz de aceptación en banco están escritos y al día. |

## 🎯 Descripción general

* **La carcasa del radar es `scad/node_enclosure_radar.scad`** (con exportaciones STL, 3MF y AMF y dos proyectos de laminador, la base y la tapa corredera): una base de esquina de 90 grados con visera, techo y suelo, escalones de retención, una tapa frontal corredera de 2 mm y aletas laterales, todo gobernado por parámetros con nombre.
* **Una caja paramétrica para los nodos solar, eléctrico y de alarma** (`scad/node_box.scad`, preajustes `solar`, `electrical` y `alarm`): paredes, postes para la placa, agujeros para prensaestopas, una ventilación, un hueco para un microinterruptor antisabotaje bajo la tapa y una tapa con labio anular. Es una caja de baja tensión, no una envolvente para cableado de red.
* **Soportes** para tres módulos de radar, un prensaestopas y agujeros de drenaje. Todavía no hay volúmenes para la placa ESP32-S3-ETH-PoE, la magnética PoE, el calefactor PTC ni la ventana del sensor de luz que la matriz de banco quiere probar. Ningún material metálico, conductor o cargado de carbono delante de una apertura de 24 GHz sin medirlo antes.
* **Matriz de aceptación en banco:** las comprobaciones de radio, entorno, alimentación, red y cámara con un método y un criterio de aprobado propuesto cada una, y una tabla de compatibilidad de cámaras por rellenar.
* Antes de fabricar, anota los contornos exactos de las placas, conectores, posiciones de tornillos, zonas libres de antena, el camino térmico y el objetivo de protección ([datos de diseño](docs/DESIGN_INPUTS.md)).

## 🧩 Papel en A.R.M.O.R.

ARMOR-HARDWARE es lo que contiene a los nodos. Lleva la carcasa del nodo radar, la caja paramétrica de los nodos solar, eléctrico, de alarma y de panel táctil, y la matriz de aceptación en banco que dice cómo juzgar un prototipo antes de ponerlo en una pared. Sus diseños son el punto de partida para las placas en las que corren [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) y [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI).

## 📂 Estructura del repositorio

```text
ARMOR-HARDWARE/
├── scad/   node_enclosure_radar.scad (+ stl, amf, 3mf and two slicer projects: the base and the sliding cover), node_box.scad (the box of the solar, electrical and alarm nodes)
├── docs/   DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
├── tests/  checks that need no OpenSCAD: the sources, the presets of the box, the model files and the numbers the documents quote
└── images/ brand assets
```

## 🛠️ Entorno de desarrollo

**Requisitos:** OpenSCAD 2021.01+ (para renderizar las cajas), una impresora 3D (FDM) para probarlas

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
python -m unittest discover -s tests   # the checks that need no OpenSCAD
```

Véase el [límite de validación](docs/VALIDATION.md). La licencia de hardware prevista es CERN-OHL-S-2.0; añade su texto completo antes de publicar los diseños.

## 🔗 Proyectos relacionados

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) es un sistema de seguridad perimetral hecho de repositorios independientes. Cada uno tiene su propia versión, sus propias pruebas y su propio README; esta es la familia:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratos de mensajes, validadores, vectores de conformidad y tipos generados
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Firmware del nodo de campo para ESP32-S3 con tres radares y su propio panel web
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protocolos de inversores y baterías solares y los mensajes de un nodo pasarela
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Nodo eléctrico: contadores, el mensaje de las lecturas de la red y las reglas para maniobrar
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Nodo y central de alarma: zonas, armado, retardos, sirena y PIN, con el servidor o sin él
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Panel táctil: el estado del sistema en una pantalla de pared, armar y reconocer alarmas, y el hogar del asistente de voz
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - La red local: sus dispositivos, internet y lo que cambia
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordinador central: telemetría, alarmas, dispositivos, lecturas solares y cámaras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Consola web: cámaras, radar, alarmas, energía solar y el diseñador de sitio 2D/3D
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Cliente Android del operador con radar 2D/3D en vivo
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - Cliente de operador para iPhone
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Política de inferencia visual que explica sus decisiones y nunca actúa
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zonas de cámara, máscaras y reglas de detección para la Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intenciones de voz sin conexión con una confirmación imposible de falsificar
* **ARMOR-HARDWARE** (este repositorio) - Cajas, electrónica y la matriz de aceptación en banco
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Despliegue, el banco de pruebas de la CM5, copias de seguridad y TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulador de telemetría sin conexión con fallos repetibles
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Detecta, instala y actualiza los propios repositorios del ecosistema
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Arquitectura, base de seguridad y la matriz de capacidades

## 📚 Documentación y comunidad

Dónde leer más:

* [Matriz de capacidades: qué está probado y qué no](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catálogo de proyectos: versiones y cómo dependen unos de otros](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Historial de cambios de este repositorio](CHANGELOG.md)
* [Licencia (GPL-3.0-or-later)](LICENSE)
* Preguntas, ideas e informes: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

GPL-3.0-or-later - véase [LICENSE](LICENSE).
