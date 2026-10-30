<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="Banner de ARMOR-HARDWARE" width="100%">
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
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 o posterior">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Pruebas">
  <img src="https://img.shields.io/badge/Version-0.2.7-0f6cbd.svg" alt="Versión">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Madurez">
</p>

---

**Comprobación de honestidad - qué funciona hoy:** La carcasa del radar es un **punto de partida mecánico imprimible, no una clasificación IP, RF ni térmica**, y la caja paramétrica para los nodos solar, eléctrico y de alarma está comprobada por los `assert` de su fuente (la placa cabe, los agujeros de cables caben, la tapa libra los postes), pero **ninguna se ha imprimido ni medido** (los tamaños de las placas salen de las hojas de datos; el panel táctil no tiene caja impresa, conserva su carcasa de fábrica). Cada fila de la [matriz de aceptación en banco](docs/BENCH_ACCEPTANCE.md) está *sin probar*.

---

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.2.7` |
| Madurez | Funcional |
| Función | Cajas, electrónica y la matriz de aceptación en banco (familia: Hardware, padre: ARMOR-NODE-RADAR) |
| Tecnología | OpenSCAD 2021.01+ (CAD), Python 3.11+ (comprobaciones) |
| Pruebas | 22 (`python -m unittest discover -s tests`) |
| Diseños | La caja del radar y la caja de 3 presets de nodo (solar, eléctrico, alarma) |
| Funciona en | Cualquier ordenador con OpenSCAD |
| En hardware real | Ninguno todavía: nada se ha impreso ni medido; las tres cajas solo las comprueban los `assert` de su fuente |
| Licencia | GPL-3.0-or-later |

**Ir a:** [Resumen](#-resumen) · [Arquitectura](#-arquitectura) · [Seguridad](#-seguridad-y-protección) · [Configuración](#-configuración) · [Inicio rápido](#-inicio-rápido) · [Pruebas](#-pruebas) · [Problemas](#-resolución-de-problemas) · [Estructura](#-estructura-del-repositorio) · [Relacionados](#-proyectos-relacionados)

## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Está escrito con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo que está planeado.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Parcial o sin verificar todavía · 🔴 No hecho o no funciona

| Área | Estado | Qué significa aquí |
|---|---|---|
| Software | 🟡 | La carcasa del radar y la caja paramétrica de los nodos solar, eléctrico y de alarma son fuentes de OpenSCAD; la caja del radar es un punto de partida imprimible, no una clasificación IP, RF ni térmica. |
| Pruebas | 🟡 | Pasan 22 pruebas (`python -m unittest discover -s tests`): las fuentes, los presets de la caja, los ficheros de modelo y las cifras que citan los documentos. Las cajas también las comprueban los `assert` de su fuente; ninguna se ha impreso ni medido. |
| Hardware | 🔴 | Nada se ha impreso ni medido, las medidas de las placas salen de hojas de datos, y cada fila de la matriz de aceptación en banco está sin probar. |
| Documentación | 🟢 | Ocho idiomas, los datos de diseño y la matriz de aceptación en banco están escritos y al día. |

## 🎯 Resumen

* **La carcasa del radar es `scad/node_enclosure_radar.scad`** (con exportaciones STL, 3MF y AMF y dos proyectos de laminador, la base y la tapa corredera): una base de esquina de 90 grados con visera, techo y suelo, escalones de retención, una tapa frontal corredera de 2 mm y aletas laterales, todo gobernado por parámetros con nombre.
* **Una caja paramétrica para los nodos solar, eléctrico y de alarma** (`scad/node_box.scad`, preajustes `solar`, `electrical` y `alarm`): paredes, postes para la placa, agujeros para prensaestopas, una ventilación, un hueco para un microinterruptor antisabotaje bajo la tapa y una tapa con labio anular. Es una caja de baja tensión, no una envolvente para cableado de red.
* **Soportes** para tres módulos de radar, un prensaestopas y agujeros de drenaje. Todavía no hay volúmenes para la placa ESP32-S3-ETH-PoE, la magnética PoE, el calefactor PTC ni la ventana del sensor de luz que la matriz de banco quiere probar. Ningún material metálico, conductor o cargado de carbono delante de una apertura de 24 GHz sin medirlo antes.
* **Matriz de aceptación en banco:** las comprobaciones de radio, entorno, alimentación, red y cámara con un método y un criterio de aprobado propuesto cada una, y una tabla de compatibilidad de cámaras por rellenar.
* Antes de fabricar, anota los contornos exactos de las placas, conectores, posiciones de tornillos, zonas libres de antena, el camino térmico y el objetivo de protección ([datos de diseño](docs/DESIGN_INPUTS.md)).

## 🧩 Papel en A.R.M.O.R.

ARMOR-HARDWARE es lo que contiene a los nodos. Lleva la carcasa del nodo radar, la caja paramétrica de los nodos solar, eléctrico, de alarma y de panel táctil, y la matriz de aceptación en banco que dice cómo juzgar un prototipo antes de ponerlo en una pared. Sus diseños son el punto de partida para las placas en las que corren [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) y [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI).

## 🏛️ Arquitectura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitectura de ARMOR-HARDWARE: quién lo llama, qué contiene y de qué depende" width="100%">
</p>

## 🔒 Seguridad y protección

| Amenaza | Defensa |
|---|---|
| Cableado de red en una caja de plástico | `node_box.scad` es una caja de bajo voltaje, no una caja para cableado de red |
| Un radar de 24 GHz bloqueado | Ningún material metálico, conductor o con carbono delante de una apertura de 24 GHz sin medirlo antes; el grosor de 2 mm de la tapa es una fila de la matriz de banco |
| Un preset o una pieza que no existe | Un `assert` detiene el renderizado: `preset must be solar, electrical or alarm`, `part must be box, lid or both` |
| Una impresión que no encaja | Los `assert` de la fuente lo detectan al renderizar: la placa y sus postes caben, los agujeros de cable no los corta una pared o poste ni son más altos que el interior, el labio de la tapa mide de 1,2 a 3 mm |

La caja del radar es un punto de partida mecánico imprimible, **no una clasificación IP, RF ni térmica**. Nada se ha impreso ni medido.

## ⚙️ Configuración

| Nombre | Valor | Qué define |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | Grosor de pared y tapa de `node_box.scad` |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | Los postes de la placa y de los tornillos de la tapa |
| `screw_d` | 3.2 mm | Tornillos M3 autorroscantes en los postes |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | Holgura entre tapa y caja; ancho del labio anular (1,2 a 3 mm) |
| `preset`, `part` | `alarm` | `solar`, `electrical` o `alarm`; `box`, `lid` o `both` |
| `vent` | `true` | Una fila de ranuras en la tapa para que salga el calor |

| Pieza | Interior (mm) | Placa (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 Inicio rápido

**Requisitos:** OpenSCAD 2021.01+ (para renderizar las cajas), una impresora 3D (FDM) para probarlas.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

Véase el [límite de validación](docs/VALIDATION.md). La licencia de hardware prevista es CERN-OHL-S-2.0; añade su texto completo antes de publicar los diseños.

## 🧪 Pruebas

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| Fichero de pruebas | Pruebas | Qué cubre |
|---|---|---|
| `test_enclosure_sources.py` | 22 | Las fuentes, los presets de la caja, los ficheros de modelo y las cifras que citan los documentos |

OpenSCAD renderiza cada pieza en una máquina que lo tenga: la base y la tapa del radar, y la caja y la tapa de los tres presets. La [matriz de aceptación en banco](docs/BENCH_ACCEPTANCE.md) es donde se juzga un prototipo impreso.

## 🩺 Resolución de problemas

| Ves | Porque | Haz |
|---|---|---|
| `preset must be solar, electrical or alarm` | El `preset` es otro valor | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | Un parámetro hizo los postes demasiado grandes para el interior | Restaura `post_d` o elige un preset mayor |
| La tapa no cierra | Tu impresora es más ajustada que los 0,3 mm de holgura | Sube `clear` y vuelve a imprimir |

## 📂 Estructura del repositorio

<p align="center">
  <img src="images/repository-structure.svg" alt="Estructura del repositorio de ARMOR-HARDWARE" width="100%">
</p>

<details>
<summary>Versión en texto del árbol</summary>

```text
ARMOR-HARDWARE/
├── scad/                                las cajas y sus ficheros de modelo
├── docs/                                las guías de este repositorio
├── tests/                               las pruebas
├── tools/                               las comprobaciones de CI compartidas y las herramientas del proyecto
├── .github/                             flujo de CI y plantillas de issues y pull requests
├── images/                              banner, icono y las dos imágenes de este README
├── build.sh build.bat                   compilar con el flujo de proyecto compartido
├── test.sh test.bat                     ejecutar las pruebas con el flujo compartido
├── run.sh run.bat                       arrancar con el flujo de proyecto compartido
├── armor.project.json                   manifiesto: versión, rol, madurez, comando de build
├── CHANGELOG.md                         qué cambió en cada versión
├── SECURITY.md SUPPORT.md LICENSE       política de seguridad, soporte y licencia
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   cómo contribuir y el código de conducta
├── build-test.sh build-test.bat         ejecutar las pruebas con el flujo compartido
└── .gitattributes .gitignore            ajustes de Git
```

</details>

## 🗺️ Hoja de ruta y límites conocidos

**Límites conocidos hoy**

* Nada se ha impreso ni medido; los tamaños de placa salen de hojas de datos y cada fila de la matriz de aceptación en banco está *sin probar*.
* Aún no hay volúmenes para la placa ESP32-S3-ETH-PoE, las magnéticas PoE, el calefactor PTC ni la ventana del sensor de luz; el panel táctil no tiene caja impresa (conserva su carcasa de fábrica).
* La licencia de hardware prevista para los diseños es CERN-OHL-S-2.0 y su texto completo aún no está en el repositorio.

**Lo siguiente**

* Anotar los contornos exactos de placa, conectores, posiciones de tornillos, zonas libres de antena, el camino térmico y el objetivo de protección ([entradas de diseño](docs/DESIGN_INPUTS.md)).
* Imprimir los prototipos y rellenar la matriz de aceptación en banco con mediciones fechadas.

## 🌍 Idiomas

El README y los textos existen en inglés, español, francés, italiano, alemán, chino, japonés y portugués de Portugal.

## 🔗 Proyectos relacionados

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) es un sistema de seguridad perimetral hecho de repositorios independientes. Cada uno tiene su propia versión, sus propias pruebas y su propio README; esta es la familia:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratos de mensajes, validadores, vectores de conformidad y tipos generados
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Firmware de nodo de campo para ESP32-S3 con tres radares y su propio panel web
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protocolos de inversores y baterías solares y los mensajes de un nodo pasarela
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Nodo eléctrico: medidores, el mensaje de las lecturas de la red y las reglas de maniobra
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Nodo y panel de alarma: zonas, armado, retardos, sirena y PIN, con el servidor o sin él
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Panel táctil: el estado del sistema en una pantalla de pared, armar y reconocer, y el hogar del asistente de voz
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - La red local: sus dispositivos, internet y lo que cambia
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordinador central: telemetría, alarmas, dispositivos, lecturas solares y cámaras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Consola web: cámaras, radar, alarmas, energía solar y el diseñador 2D/3D del emplazamiento
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Cliente de operador Android con radar 2D/3D en vivo
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - Cliente de operador para iPhone
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Política de inferencia visual que explica sus decisiones y nunca actúa
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zonas de cámara, máscaras y reglas de detección para la Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intenciones de voz sin conexión con una confirmación que no se puede falsificar
* **ARMOR-HARDWARE** (este repositorio) - Cajas, electrónica y la matriz de aceptación en banco
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Despliegue, el banco de pruebas de la CM5, copias de seguridad y TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulador de telemetría sin conexión con fallos repetibles
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Detecta, instala y actualiza los repositorios del propio ecosistema
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Arquitectura, base de seguridad y la matriz de capacidades

## 📚 Documentación

* [Entradas de diseño](docs/DESIGN_INPUTS.md): qué anotar antes de fabricar
* [Límite de la validación](docs/VALIDATION.md): qué está y qué no está validado
* [Matriz de aceptación en banco](docs/BENCH_ACCEPTANCE.md): las comprobaciones, sus métodos y criterios propuestos
* [Matriz de capacidades: qué está demostrado y qué no](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catálogo de proyectos: versiones y cómo dependen unos repositorios de otros](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Registro de cambios de este repositorio](CHANGELOG.md)

## 🤝 Contribuir y comunidad

* Antes de un pull request ejecuta `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py`: debe pasar. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md).
* El README existe en ocho idiomas y se genera desde las fuentes de ARMOR-DOCS: un cambio de texto se hace allí.
* Un cambio en un mensaje entre componentes empieza en ARMOR-COMMON.
* No describas como funcionando en una placa lo que solo se ha compilado.
* Informa de una vulnerabilidad en privado: [SECURITY.md](SECURITY.md). Preguntas, ideas e informes: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

GPL-3.0-or-later - véase [LICENSE](LICENSE).
