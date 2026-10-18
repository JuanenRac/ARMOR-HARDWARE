<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  🇮🇹 <b>Italiano</b> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Contenitori, elettronica e matrice di accettazione da banco

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Version-0.2.4-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**Controllo di onestà - cosa funziona oggi:** L'involucro del radar è un **punto di partenza meccanico stampabile, non una classificazione IP, RF o termica**, e la scatola parametrica per i nodi solare, elettrico e allarme è verificata dagli `assert` del suo sorgente (la scheda ci sta, i fori dei cavi ci stanno, il coperchio libera le colonnine), ma **nessuna è stata stampata né misurata** (le dimensioni delle schede vengono dai datasheet; il pannello touch non ha una scatola stampata, mantiene il suo involucro di fabbrica). Ogni riga della [matrice di accettazione al banco](docs/BENCH_ACCEPTANCE.md) è *non provata*.

---

## 📋 In breve

| | |
|---|---|
| Versione | `0.2.4` |
| Maturità | Funzionale |
| Tecnologia | OpenSCAD |
| Su hardware reale | Ancora nessuno: nulla è stato stampato né misurato; le tre scatole sono verificate solo dagli `assert` del sorgente |

## 🎯 Panoramica

* **L'involucro del radar è `scad/node_enclosure_radar.scad`** (con esportazioni STL, 3MF e AMF e due progetti dello slicer, la base e il coperchio scorrevole): una base d'angolo a 90 gradi con visiera, tetto e pavimento, gradini di ritenuta, un coperchio frontale scorrevole da 2 mm e alette laterali, tutto governato da parametri con nome.
* **Una scatola parametrica per i nodi solare, elettrico e allarme** (`scad/node_box.scad`, preset `solar`, `electrical` e `alarm`): pareti, colonnine per la scheda, fori per pressacavi, una ventilazione, un alloggiamento per un microinterruttore antimanomissione sotto il coperchio e un coperchio con labbro ad anello. È una scatola a bassa tensione, non un involucro per cablaggio di rete.
* **Supporti** per tre moduli radar, un pressacavo e fori di drenaggio. Non ci sono ancora volumi per la scheda ESP32-S3-ETH-PoE, la magnetica PoE, il riscaldatore PTC né la finestra del sensore di luce che la matrice di banco vuole provare. Nessun materiale metallico, conduttivo o caricato con carbonio davanti a un'apertura a 24 GHz senza averlo misurato.
* **Matrice di accettazione al banco:** i controlli di radio, ambiente, alimentazione, rete e telecamera con un metodo e un criterio di superamento proposto ciascuno, e una tabella di compatibilità delle telecamere da compilare.
* Prima della fabbricazione, registra i contorni esatti delle schede, i connettori, le posizioni delle viti, le zone libere d'antenna, il percorso termico e l'obiettivo di protezione ([dati di progetto](docs/DESIGN_INPUTS.md)).

## 🧩 Ruolo in A.R.M.O.R.

ARMOR-HARDWARE è ciò che contiene i nodi. Porta l'involucro del nodo radar, la scatola parametrica dei nodi solare, elettrico, allarme e pannello touch, e la matrice di accettazione al banco che dice come giudicare un prototipo prima di metterlo a una parete. I suoi progetti sono il punto di partenza per le schede su cui girano [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR), [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR), [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL), [ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM) e [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI).

## 📂 Struttura del repository

```text
ARMOR-HARDWARE/
├── scad/   node_enclosure_radar.scad (+ stl, amf, 3mf and two slicer projects: the base and the sliding cover), node_box.scad (the box of the solar, electrical and alarm nodes)
├── docs/   DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
├── tests/  checks that need no OpenSCAD: the sources, the presets of the box, the model files and the numbers the documents quote
└── images/ brand assets
```

## 🛠️ Ambiente di sviluppo

**Requisiti:** OpenSCAD 2021.01+ (to render the enclosures), a 3D printer (FDM) to try them

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
python -m unittest discover -s tests   # the checks that need no OpenSCAD
```

Vedi il [confine di validazione](docs/VALIDATION.md). La licenza hardware prevista è CERN-OHL-S-2.0; aggiungi il suo testo completo prima di pubblicare i progetti.

## 🔗 Progetti correlati

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) è un sistema di sicurezza perimetrale fatto di repository indipendenti. Ognuno ha la propria versione, i propri test e il proprio README; ecco la famiglia:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratti dei messaggi, validatori, vettori di conformità e tipi generati
* **[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)** - Firmware del nodo di campo per ESP32-S3 con tre radar e un proprio pannello web
* **[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)** - Protocolli di inverter e batterie solari e messaggi di un nodo gateway
* **[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)** - Nodo elettrico: contatori, il messaggio delle letture della rete e le regole di manovra
* **[ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM)** - Nodo e centrale d'allarme: zone, inserimento, ritardi, sirena e PIN, con il server o senza
* **[ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI)** - Pannello touch: lo stato del sistema su uno schermo a parete, attivare e riconoscere gli allarmi, e la casa dell'assistente vocale
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - La rete locale: i suoi dispositivi, internet e ciò che cambia
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordinatore centrale: telemetria, allarmi, dispositivi, letture solari e telecamere
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Console web: telecamere, radar, allarmi, energia solare e progettista del sito 2D/3D
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Client Android dell'operatore con radar 2D/3D in tempo reale
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Politica di inferenza visiva che spiega le sue decisioni e non agisce mai
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zone delle telecamere, maschere e regole di rilevamento per la Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intenti vocali offline con una conferma impossibile da falsificare
* **ARMOR-HARDWARE** (questo repository) - Contenitori, elettronica e matrice di accettazione da banco
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Distribuzione, banco di prova CM5, backup e TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulatore di telemetria offline con guasti ripetibili
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Rileva, installa e aggiorna i repository stessi dell'ecosistema
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Architettura, base di sicurezza e matrice delle capacità

## 📚 Documentazione e comunità

Dove leggere di più:

* [Matrice delle capacità: cosa è provato e cosa no](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catalogo dei progetti: versioni e dipendenze tra i repository](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Cronologia delle modifiche di questo repository](CHANGELOG.md)
* [Licenza (GPL-3.0-or-later)](LICENSE)
* Domande, idee e segnalazioni: electrohobby3d@gmail.com

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

GPL-3.0-or-later - vedi [LICENSE](LICENSE).
