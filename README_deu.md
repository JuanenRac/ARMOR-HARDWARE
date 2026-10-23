<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  🇩🇪 <b>Deutsch</b> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Gehäuse, Elektronik und die Abnahmematrix am Prüfstand

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Version-0.2.5-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**Ehrlichkeitsprüfung - was heute läuft:** Das Radargehäuse ist ein **druckbarer mechanischer Ausgangspunkt, keine IP-, HF- oder Thermikeinstufung**, und die parametrische Box für die Knoten Solar, Elektro und Alarm wird von den `assert`-Prüfungen ihres Quelltexts geprüft (die Platine passt, die Kabellöcher passen, der Deckel liegt frei von den Pfosten), aber **keine wurde gedruckt oder vermessen** (die Platinengrößen stammen aus Datenblättern; das Touchpanel hat keine gedruckte Box, es behält sein Werksgehäuse). Jede Zeile der [Prüfstand-Abnahmematrix](docs/BENCH_ACCEPTANCE.md) ist *ungetestet*.

---

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.2.5` |
| Reifegrad | Funktionsfähig |
| Technik | OpenSCAD |
| Auf echter Hardware | Noch keiner: nichts wurde gedruckt oder vermessen; die drei Boxen werden nur durch die `assert`-Prüfungen ihres Quelltexts geprüft |

## 🎯 Überblick

* **Das Radargehäuse ist `scad/node_enclosure_radar.scad`** (mit STL-, 3MF- und AMF-Exporten und zwei Slicer-Projekten, der Basis und dem Schiebedeckel): eine 90-Grad-Eckbasis mit Blende, Dach und Boden, Haltestufen, einem 2 mm dicken Schiebedeckel vorn und Seitenklappen, alles über benannte Parameter gesteuert.
* **Eine parametrische Box für die Knoten Solar, Elektro und Alarm** (`scad/node_box.scad`, Voreinstellungen `solar`, `electrical` und `alarm`): Wände, Pfosten für die Platine, Löcher für Kabelverschraubungen, eine Lüftung, eine Aufnahme für einen Sabotage-Mikroschalter unter dem Deckel und ein Deckel mit ringförmiger Lippe. Es ist eine Kleinspannungsbox, kein Gehäuse für Netzverdrahtung.
* **Halter** für drei Radarmodule, eine Kabelverschraubung und Ablaufbohrungen. Für die Platine ESP32-S3-ETH-PoE, die PoE-Magnetik, die PTC-Heizung und das Lichtsensorfenster, die die Prüfstandmatrix testen will, gibt es noch keine Volumina. Kein metallisches, leitendes oder kohlenstoffhaltiges Material vor einer 24-GHz-Öffnung, ohne es vorher zu messen.
* **Prüfstand-Abnahmematrix:** die Prüfungen für Funk, Umgebung, Stromversorgung, Netzwerk und Kamera, jeweils mit Methode und vorgeschlagenem Bestehenskriterium, und eine auszufüllende Kamera-Kompatibilitätstabelle.
* Vor der Fertigung genaue Platinenumrisse, Steckverbinder, Schraubpositionen, Antennenfreiräume, den Wärmepfad und das Schutzziel festhalten ([Entwurfsangaben](docs/DESIGN_INPUTS.md)).

## 🧩 Rolle in A.R.M.O.R.

ARMOR-HARDWARE ist das, was die Knoten hält. Es enthält das Gehäuse des Radarknotens, die parametrische Box der Knoten Solar, Elektro, Alarm und Touchpanel und die Abnahmematrix, die sagt, wie ein Prototyp beurteilt wird, bevor er an die Wand kommt. Seine Entwürfe sind der Ausgangspunkt für die Platinen, auf denen [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) und [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI) laufen.

## 📂 Struktur des Repositorys

```text
ARMOR-HARDWARE/
├── scad/   node_enclosure_radar.scad (+ stl, amf, 3mf and two slicer projects: the base and the sliding cover), node_box.scad (the box of the solar, electrical and alarm nodes)
├── docs/   DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
├── tests/  checks that need no OpenSCAD: the sources, the presets of the box, the model files and the numbers the documents quote
└── images/ brand assets
```

## 🛠️ Entwicklungsumgebung

**Voraussetzungen:** OpenSCAD 2021.01+ (zum Rendern der Gehäuse), ein 3D-Drucker (FDM), um sie auszuprobieren

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
python -m unittest discover -s tests   # the checks that need no OpenSCAD
```

Siehe die [Validierungsgrenze](docs/VALIDATION.md). Die vorgesehene Hardware-Lizenz ist CERN-OHL-S-2.0; fügen Sie ihren vollständigen Text hinzu, bevor Sie die Entwürfe veröffentlichen.

## 🔗 Verwandte Projekte

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) ist ein Perimeter-Sicherheitssystem aus unabhängigen Repositorys. Jedes hat eine eigene Version, eigene Tests und ein eigenes README; hier ist die Familie:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Nachrichtenverträge, Validierer, Konformitätsvektoren und generierte Typen
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Feldknoten-Firmware für ESP32-S3 mit drei Radaren und eigenem Web-Panel
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protokolle für Solar-Wechselrichter und -Batterien und die Nachrichten eines Gateway-Knotens
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Elektroknoten: Zähler, die Nachricht der Netzmesswerte und die Regeln fürs Schalten
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Alarmknoten und Alarmzentrale: Zonen, Scharfschalten, Verzögerungen, Sirene und PIN, mit dem Server oder ohne ihn
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Touch-Panel: der Systemzustand auf einem Wandbildschirm, Scharf- und Quittieren sowie das Zuhause des Sprachassistenten
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - Das lokale Netzwerk: seine Geräte, das Internet und was sich ändert
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Zentraler Koordinator: Telemetrie, Alarme, Geräte, Solarmesswerte und Kameras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Web-Konsole: Kameras, Radar, Alarme, Solarenergie und 2D/3D-Standortdesigner
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Android-Bedienclient mit Live-Radar in 2D/3D
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - iPhone-Bedienclient
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Visuelle Inferenzrichtlinie, die ihre Entscheidungen erklärt und nie handelt
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Kamerazonen, Masken und Erkennungsregeln für den Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Offline-Sprachabsichten mit einer nicht fälschbaren Bestätigung
* **ARMOR-HARDWARE** (dieses Repository) - Gehäuse, Elektronik und die Abnahmematrix am Prüfstand
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Bereitstellung, CM5-Prüfstand, Backup und TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Offline-Telemetriesimulator mit wiederholbaren Fehlern
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Erkennt, installiert und aktualisiert die eigenen Repositories des Ökosystems
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Architektur, Sicherheitsgrundlage und die Fähigkeitsmatrix

## 📚 Dokumentation und Community

Hier gibt es mehr zu lesen:

* [Fähigkeitsmatrix: was belegt ist und was nicht](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Projektkatalog: Versionen und wie die Repositorys voneinander abhängen](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Änderungsverlauf dieses Repositorys](CHANGELOG.md)
* [Lizenz (GPL-3.0-or-later)](LICENSE)
* Fragen, Ideen und Meldungen: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

GPL-3.0-or-later - siehe [LICENSE](LICENSE).
