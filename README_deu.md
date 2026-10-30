<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE-Banner" width="100%">
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
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 oder neuer">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Version-0.2.7-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Reifegrad">
</p>

---

**Ehrlichkeitsprüfung - was heute läuft:** Das Radargehäuse ist ein **druckbarer mechanischer Ausgangspunkt, keine IP-, HF- oder Thermikeinstufung**, und die parametrische Box für die Knoten Solar, Elektro und Alarm wird von den `assert`-Prüfungen ihres Quelltexts geprüft (die Platine passt, die Kabellöcher passen, der Deckel liegt frei von den Pfosten), aber **keine wurde gedruckt oder vermessen** (die Platinengrößen stammen aus Datenblättern; das Touchpanel hat keine gedruckte Box, es behält sein Werksgehäuse). Jede Zeile der [Prüfstand-Abnahmematrix](docs/BENCH_ACCEPTANCE.md) ist *ungetestet*.

---

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.2.7` |
| Reifegrad | Funktionsfähig |
| Rolle | Gehäuse, Elektronik und die Prüfstand-Abnahmematrix (Familie: Hardware, übergeordnet: ARMOR-NODE-RADAR) |
| Technik | OpenSCAD 2021.01+ (CAD), Python 3.11+ (Prüfungen) |
| Tests | 22 (`python -m unittest discover -s tests`) |
| Entwürfe | Das Radargehäuse und die Box für 3 Knoten-Presets (Solar, Elektro, Alarm) |
| Läuft auf | Jeder Computer mit OpenSCAD |
| Auf echter Hardware | Noch keiner: nichts wurde gedruckt oder vermessen; die drei Boxen werden nur durch die `assert`-Prüfungen ihres Quelltexts geprüft |
| Lizenz | GPL-3.0-or-later |

**Springe zu:** [Überblick](#-überblick) · [Architektur](#-architektur) · [Sicherheit](#-sicherheit-und-schutz) · [Konfiguration](#-konfiguration) · [Schnellstart](#-schnellstart) · [Tests](#-tests) · [Probleme](#-fehlerbehebung) · [Struktur](#-struktur-des-repositorys) · [Verwandte](#-verwandte-projekte)

## 🚦 Projektstatus

Jede Zeile ist ein Teil dieses Repositorys, und die Ampel sagt, wie weit er heute ist. Sie beruht auf dem, was das Repository zeigen kann (Tests, Builds, Läufe), nicht auf dem, was geplant ist.

🟢 Fertig und überprüft · 🟡 Funktioniert, mit bekannten Grenzen · 🟠 Teilweise fertig oder noch nicht überprüft · 🔴 Nicht gemacht oder funktioniert nicht

| Bereich | Stand | Was das hier bedeutet |
|---|---|---|
| Software | 🟡 | Das Radargehäuse und die parametrische Box der Solar-, Elektrik- und Alarmknoten sind OpenSCAD-Quellen; die Radarbox ist ein druckbarer Ausgangspunkt, keine IP-, HF- oder Temperatur-Einstufung. |
| Tests | 🟡 | 22 Tests bestehen (`python -m unittest discover -s tests`): die Quellen, die Presets der Box, die Modelldateien und die Zahlen, die die Dokumente nennen. Die Boxen prüfen auch die Asserts ihrer Quelle; keine wurde gedruckt oder gemessen. |
| Hardware | 🔴 | Nichts wurde gedruckt oder vermessen, die Maße der Platinen stammen aus Datenblättern, und jede Zeile der Prüfstand-Abnahmematrix ist ungetestet. |
| Dokumentation | 🟢 | Acht Sprachen, die Entwurfsvorgaben und die Prüfstand-Abnahmematrix sind geschrieben und aktuell. |

## 🎯 Überblick

* **Das Radargehäuse ist `scad/node_enclosure_radar.scad`** (mit STL-, 3MF- und AMF-Exporten und zwei Slicer-Projekten, der Basis und dem Schiebedeckel): eine 90-Grad-Eckbasis mit Blende, Dach und Boden, Haltestufen, einem 2 mm dicken Schiebedeckel vorn und Seitenklappen, alles über benannte Parameter gesteuert.
* **Eine parametrische Box für die Knoten Solar, Elektro und Alarm** (`scad/node_box.scad`, Voreinstellungen `solar`, `electrical` und `alarm`): Wände, Pfosten für die Platine, Löcher für Kabelverschraubungen, eine Lüftung, eine Aufnahme für einen Sabotage-Mikroschalter unter dem Deckel und ein Deckel mit ringförmiger Lippe. Es ist eine Kleinspannungsbox, kein Gehäuse für Netzverdrahtung.
* **Halter** für drei Radarmodule, eine Kabelverschraubung und Ablaufbohrungen. Für die Platine ESP32-S3-ETH-PoE, die PoE-Magnetik, die PTC-Heizung und das Lichtsensorfenster, die die Prüfstandmatrix testen will, gibt es noch keine Volumina. Kein metallisches, leitendes oder kohlenstoffhaltiges Material vor einer 24-GHz-Öffnung, ohne es vorher zu messen.
* **Prüfstand-Abnahmematrix:** die Prüfungen für Funk, Umgebung, Stromversorgung, Netzwerk und Kamera, jeweils mit Methode und vorgeschlagenem Bestehenskriterium, und eine auszufüllende Kamera-Kompatibilitätstabelle.
* Vor der Fertigung genaue Platinenumrisse, Steckverbinder, Schraubpositionen, Antennenfreiräume, den Wärmepfad und das Schutzziel festhalten ([Entwurfsangaben](docs/DESIGN_INPUTS.md)).

## 🧩 Rolle in A.R.M.O.R.

ARMOR-HARDWARE ist das, was die Knoten hält. Es enthält das Gehäuse des Radarknotens, die parametrische Box der Knoten Solar, Elektro, Alarm und Touchpanel und die Abnahmematrix, die sagt, wie ein Prototyp beurteilt wird, bevor er an die Wand kommt. Seine Entwürfe sind der Ausgangspunkt für die Platinen, auf denen [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) und [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI) laufen.

## 🏛️ Architektur

<p align="center">
  <img src="images/architecture.svg" alt="Architektur von ARMOR-HARDWARE: wer es aufruft, was es enthält und wovon es abhängt" width="100%">
</p>

## 🔒 Sicherheit und Schutz

| Bedrohung | Abwehr |
|---|---|
| Netzverdrahtung in einer Kunststoffbox | `node_box.scad` ist eine Kleinspannungsbox, kein Gehäuse für Netzverdrahtung |
| Ein blockiertes 24-GHz-Radar | Kein metallisches, leitfähiges oder kohlenstoffhaltiges Material vor einer 24-GHz-Öffnung, ohne es zuvor zu messen; die Deckeldicke von 2 mm ist eine Zeile der Prüfstandsmatrix |
| Ein Preset oder Teil, das es nicht gibt | Ein `assert` stoppt das Rendern: `preset must be solar, electrical or alarm`, `part must be box, lid or both` |
| Ein Druck, der nicht passt | Die Asserts der Quelle fangen es beim Rendern ab: Platine und Pfosten passen, Kabellöcher werden weder von Wand oder Pfosten geschnitten noch sind sie höher als das Innere, die Deckellippe misst 1,2 bis 3 mm |

Das Radargehäuse ist ein druckbarer mechanischer Ausgangspunkt, **keine IP-, HF- oder Wärmeklassifizierung**. Nichts wurde gedruckt oder gemessen.

## ⚙️ Konfiguration

| Name | Wert | Was sie festlegt |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | Wand- und Deckelstärke von `node_box.scad` |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | Die Pfosten für die Platine und die Deckelschrauben |
| `screw_d` | 3.2 mm | M3-Schneidschrauben in die Pfosten |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | Spiel zwischen Deckel und Box; Breite der ringförmigen Lippe (1,2 bis 3 mm) |
| `preset`, `part` | `alarm` | `solar`, `electrical` oder `alarm`; `box`, `lid` oder `both` |
| `vent` | `true` | Eine Reihe Schlitze im Deckel, damit die Wärme entweichen kann |

| Teil | Innenmaß (mm) | Platine (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 Schnellstart

**Voraussetzungen:** OpenSCAD 2021.01+ (zum Rendern der Gehäuse), ein 3D-Drucker (FDM) zum Ausprobieren.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

Siehe die [Validierungsgrenze](docs/VALIDATION.md). Die vorgesehene Hardware-Lizenz ist CERN-OHL-S-2.0; fügen Sie ihren vollständigen Text hinzu, bevor Sie die Entwürfe veröffentlichen.

## 🧪 Tests

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| Testdatei | Tests | Was sie abdeckt |
|---|---|---|
| `test_enclosure_sources.py` | 22 | Die Quellen, die Presets der Box, die Modelldateien und die Zahlen, die die Dokumente nennen |

OpenSCAD rendert jedes Teil auf einem Rechner, der es hat: Radarbasis und -deckel sowie Box und Deckel der drei Presets. In der [Prüfstand-Abnahmematrix](docs/BENCH_ACCEPTANCE.md) wird ein gedruckter Prototyp beurteilt.

## 🩺 Fehlerbehebung

| Sie sehen | Weil | Tun Sie |
|---|---|---|
| `preset must be solar, electrical or alarm` | Das `preset` ist etwas anderes | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | Ein Parameter machte die Pfosten für das Innere zu groß | Setze `post_d` zurück oder wähle ein größeres Preset |
| Der Deckel schließt nicht | Dein Drucker ist enger als das Spiel von 0,3 mm | Erhöhe `clear` und drucke neu |

## 📂 Struktur des Repositorys

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository-Struktur von ARMOR-HARDWARE" width="100%">
</p>

<details>
<summary>Textversion des Baums</summary>

```text
ARMOR-HARDWARE/
├── scad/                                die Gehäuse und ihre Modelldateien
├── docs/                                die Anleitungen dieses Repositorys
├── tests/                               die Tests
├── tools/                               die gemeinsamen CI-Prüfungen und Projektwerkzeuge
├── .github/                             CI-Workflow sowie Vorlagen für Issues und Pull Requests
├── images/                              Banner, Symbol und die zwei Bilder dieses READMEs
├── build.sh build.bat                   Build über den gemeinsamen Projekt-Workflow
├── test.sh test.bat                     Tests über den gemeinsamen Workflow ausführen
├── run.sh run.bat                       Start über den gemeinsamen Projekt-Workflow
├── armor.project.json                   Manifest: Version, Rolle, Reifegrad, Build-Befehl
├── CHANGELOG.md                         was sich in jeder Version geändert hat
├── SECURITY.md SUPPORT.md LICENSE       Sicherheitsrichtlinie, Support und Lizenz
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   Mitwirkung und Verhaltenskodex
├── build-test.sh build-test.bat         Tests über den gemeinsamen Workflow ausführen
└── .gitattributes .gitignore            Git-Einstellungen
```

</details>

## 🗺️ Roadmap und bekannte Grenzen

**Bekannte Grenzen heute**

* Nichts wurde gedruckt oder gemessen; die Platinengrößen stammen aus Datenblättern, und jede Zeile der Prüfstand-Abnahmematrix ist *nicht getestet*.
* Es gibt noch keine Volumen für die ESP32-S3-ETH-PoE-Platine, die PoE-Magnetik, die PTC-Heizung oder das Lichtsensorfenster; das Touchpanel hat keine gedruckte Box (es behält sein Werksgehäuse).
* Die für die Entwürfe vorgesehene Hardwarelizenz ist CERN-OHL-S-2.0; ihr vollständiger Text liegt noch nicht im Repository.

**Als Nächstes**

* Die genauen Platinenumrisse, Steckverbinder, Schraubenpositionen, Antennenfreiräume, den Wärmepfad und das Schutzziel festhalten ([Entwurfseingaben](docs/DESIGN_INPUTS.md)).
* Die Prototypen drucken und die Prüfstand-Abnahmematrix mit datierten Messungen füllen.

## 🌍 Sprachen

README und Texte gibt es auf Englisch, Spanisch, Französisch, Italienisch, Deutsch, Chinesisch, Japanisch und europäischem Portugiesisch.

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
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Erkennt, installiert und aktualisiert die eigenen Repositorys des Ökosystems
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Architektur, Sicherheitsgrundlage und die Fähigkeitsmatrix

## 📚 Dokumentation

* [Entwurfseingaben](docs/DESIGN_INPUTS.md): was vor der Fertigung festzuhalten ist
* [Validierungsgrenze](docs/VALIDATION.md): was validiert ist und was nicht
* [Prüfstand-Abnahmematrix](docs/BENCH_ACCEPTANCE.md): die Prüfungen, ihre Methoden und vorgeschlagenen Kriterien
* [Fähigkeitsmatrix: was belegt ist und was nicht](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Projektkatalog: Versionen und wie die Repositorys voneinander abhängen](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Änderungsverlauf dieses Repositorys](CHANGELOG.md)

## 🤝 Mitwirken und Community

* Führe vor einem Pull Request `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py` aus: Es muss bestehen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md) und den [Verhaltenskodex](CODE_OF_CONDUCT.md).
* Das README gibt es in acht Sprachen, und es wird aus den Quellen in ARMOR-DOCS erzeugt: Eine Textänderung erfolgt dort.
* Eine Änderung an einer Nachricht zwischen Komponenten beginnt in ARMOR-COMMON.
* Beschreibe nichts als auf einer Platine funktionierend, was nur gebaut wurde.
* Melde eine Schwachstelle privat: [SECURITY.md](SECURITY.md). Fragen, Ideen und Meldungen: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

GPL-3.0-or-later - siehe [LICENSE](LICENSE).
