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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### Contenitori, elettronica e matrice di accettazione da banco

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/EDA-KiCad-314cb0.svg" alt="EDA">
  <img src="https://img.shields.io/badge/Maturity-mechanical%20baseline-FFB020.svg" alt="Maturity">
</p>

---

**Controllo di onestà - cosa funziona oggi:** Il contenitore è un **punto di partenza meccanico stampabile, non una certificazione IP, RF o termica.** Nulla è stato misurato su un prototipo; ogni riga della [matrice di accettazione da banco](docs/BENCH_ACCEPTANCE.md) è *non testata*.

---

## 🎯 Panoramica

* **Il vero progetto è `scad/node_enclosure_radar.scad`** (con esportazioni STL, 3MF e AMF, più `node_enclosure_radar_1.3mf` e `node_enclosure_radar_2.3mf`, progetti per lo slicer della base e del coperchio): una base d'angolo a 90 gradi con visiera, tetto e fondo, gradini di ritegno, un coperchio frontale scorrevole da 2 mm e alette laterali, tutto guidato da parametri con nome. `view_mode` sceglie cosa viene disegnato o esportato: 0 esploso, 1 assemblato, 2 solo la base, 3 solo il coperchio.
* **Volumi riservati** per tre moduli radar, la scheda ESP32-S3-ETH-PoE, la finestra del sensore, un passacavo, la magnetica PoE e il riscaldatore PTC. Nessun materiale metallico, conduttivo o caricato di carbonio davanti a un'apertura a 24 GHz senza attenuazione misurata.
* **Matrice di accettazione da banco:** i controlli di radio, ambiente, alimentazione, rete e telecamera, ciascuno con un metodo e un criterio di superamento proposto, e una tabella di compatibilità delle telecamere da compilare.
* Prima della fabbricazione, registrare i contorni esatti delle schede, i connettori, la posizione delle viti, le aree di esclusione delle antenne, il percorso termico e l'obiettivo di tenuta ([dati di progetto](docs/DESIGN_INPUTS.md)).

## 📂 Struttura del repository

```text
ARMOR-HARDWARE/
├── scad/    node_enclosure_radar.scad (+ stl, 3mf, amf, _1.3mf, _2.3mf)
├── docs/    DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
├── tools/   script di build, test e CI condivisi da tutti i repository A.R.M.O.R.
└── images/  immagini del marchio
```

## 🛠️ Ambiente di sviluppo

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D view_mode=3 -o build/node_enclosure_radar_cover.stl scad/node_enclosure_radar.scad
```

Vedi il [confine di validazione](docs/VALIDATION.md). La licenza hardware prevista è CERN-OHL-S-2.0; aggiungi il testo completo prima di pubblicare i progetti.

## 🔗 Progetti correlati

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) è un sistema di sicurezza perimetrale fatto di repository indipendenti. Ognuno ha la propria versione, i propri test e il proprio README; ecco la famiglia:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratti dei messaggi, validatori, vettori di conformità e tipi generati
* **[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)** - Firmware del nodo di campo per ESP32-S3 con tre radar e un proprio pannello web
* **[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)** - Protocolli di inverter e batterie solari e messaggi di un nodo gateway
* **[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)** - Nodo elettrico: contatori, il messaggio delle letture della rete e le regole di manovra
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - La rete locale: i suoi dispositivi, internet e ciò che cambia
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordinatore centrale: telemetria, allarmi, dispositivi, letture solari e telecamere
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Console web: telecamere, radar, allarmi, energia solare e progettista del sito 2D/3D
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Client Android dell'operatore con radar 2D/3D in tempo reale
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Politica di inferenza visiva che spiega le sue decisioni e non agisce mai
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
