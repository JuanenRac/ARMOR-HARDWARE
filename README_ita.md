<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="Banner di ARMOR-HARDWARE" width="100%">
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
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 o successiva">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Test">
  <img src="https://img.shields.io/badge/Version-0.2.6-0f6cbd.svg" alt="Versione">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturità">
</p>

---

**Controllo di onestà - cosa funziona oggi:** L'involucro del radar è un **punto di partenza meccanico stampabile, non una classificazione IP, RF o termica**, e la scatola parametrica per i nodi solare, elettrico e allarme è verificata dagli `assert` del suo sorgente (la scheda ci sta, i fori dei cavi ci stanno, il coperchio libera le colonnine), ma **nessuna è stata stampata né misurata** (le dimensioni delle schede vengono dai datasheet; il pannello touch non ha una scatola stampata, mantiene il suo involucro di fabbrica). Ogni riga della [matrice di accettazione al banco](docs/BENCH_ACCEPTANCE.md) è *non provata*.

---

## 📋 In breve

| | |
|---|---|
| Versione | `0.2.6` |
| Maturità | Funzionale |
| Ruolo | Involucri, elettronica e la matrice di accettazione al banco (famiglia: Hardware, padre: ARMOR-NODE-RADAR) |
| Tecnologia | OpenSCAD 2021.01+ (CAD), Python 3.11+ (verifiche) |
| Test | 22 (`python -m unittest discover -s tests`) |
| Progetti | L'involucro del radar e la scatola di 3 preset di nodo (solare, elettrico, allarme) |
| Gira su | Qualsiasi computer con OpenSCAD |
| Su hardware reale | Ancora nessuno: nulla è stato stampato né misurato; le tre scatole sono verificate solo dagli `assert` del sorgente |
| Licenza | GPL-3.0-or-later |

**Vai a:** [Panoramica](#-panoramica) · [Architettura](#-architettura) · [Sicurezza](#-sicurezza-e-protezione) · [Configurazione](#-configurazione) · [Avvio rapido](#-avvio-rapido) · [Test](#-test) · [Problemi](#-risoluzione-dei-problemi) · [Struttura](#-struttura-del-repository) · [Correlati](#-progetti-correlati)

## 🚦 Stato del progetto

Ogni riga è una parte di questo repository e il semaforo dice a che punto è oggi. È scritta in base a ciò che il repository può mostrare (test, compilazioni, esecuzioni), non a ciò che è previsto.

🟢 Fatto e verificato · 🟡 Funziona, con limiti noti · 🟠 Fatto a metà o non ancora verificato · 🔴 Non fatto o non funzionante

| Area | Stato | Cosa significa qui |
|---|---|---|
| Software | 🟡 | L'involucro del radar e la scatola parametrica dei nodi solare, elettrico e d'allarme sono sorgenti OpenSCAD; la scatola del radar è un punto di partenza stampabile, non una classificazione IP, RF o termica. |
| Test | 🟡 | 22 test passano (`python -m unittest discover -s tests`): i sorgenti, i preset della scatola, i file di modello e i numeri citati dai documenti. Le scatole sono verificate anche dagli `assert` del loro sorgente; nessuna è stata stampata né misurata. |
| Hardware | 🔴 | Nulla è stato stampato né misurato, le dimensioni delle schede vengono dai datasheet e ogni riga della matrice di accettazione al banco non è testata. |
| Documentazione | 🟢 | Otto lingue, i dati di progetto e la matrice di accettazione al banco sono scritti e aggiornati. |

## 🎯 Panoramica

* **L'involucro del radar è `scad/node_enclosure_radar.scad`** (con esportazioni STL, 3MF e AMF e due progetti dello slicer, la base e il coperchio scorrevole): una base d'angolo a 90 gradi con visiera, tetto e pavimento, gradini di ritenuta, un coperchio frontale scorrevole da 2 mm e alette laterali, tutto governato da parametri con nome.
* **Una scatola parametrica per i nodi solare, elettrico e allarme** (`scad/node_box.scad`, preset `solar`, `electrical` e `alarm`): pareti, colonnine per la scheda, fori per pressacavi, una ventilazione, un alloggiamento per un microinterruttore antimanomissione sotto il coperchio e un coperchio con labbro ad anello. È una scatola a bassa tensione, non un involucro per cablaggio di rete.
* **Supporti** per tre moduli radar, un pressacavo e fori di drenaggio. Non ci sono ancora volumi per la scheda ESP32-S3-ETH-PoE, la magnetica PoE, il riscaldatore PTC né la finestra del sensore di luce che la matrice di banco vuole provare. Nessun materiale metallico, conduttivo o caricato con carbonio davanti a un'apertura a 24 GHz senza averlo misurato.
* **Matrice di accettazione al banco:** i controlli di radio, ambiente, alimentazione, rete e telecamera con un metodo e un criterio di superamento proposto ciascuno, e una tabella di compatibilità delle telecamere da compilare.
* Prima della fabbricazione, registra i contorni esatti delle schede, i connettori, le posizioni delle viti, le zone libere d'antenna, il percorso termico e l'obiettivo di protezione ([dati di progetto](docs/DESIGN_INPUTS.md)).

## 🧩 Ruolo in A.R.M.O.R.

ARMOR-HARDWARE è ciò che contiene i nodi. Porta l'involucro del nodo radar, la scatola parametrica dei nodi solare, elettrico, allarme e pannello touch, e la matrice di accettazione al banco che dice come giudicare un prototipo prima di metterlo a una parete. I suoi progetti sono il punto di partenza per le schede su cui girano [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) e [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI).

## 🏛️ Architettura

<p align="center">
  <img src="images/architecture.svg" alt="Architettura di ARMOR-HARDWARE: chi lo chiama, cosa contiene e da cosa dipende" width="100%">
</p>

## 🔒 Sicurezza e protezione

| Minaccia | Difesa |
|---|---|
| Cablaggio di rete in una scatola di plastica | `node_box.scad` è una scatola a bassa tensione, non un involucro per cablaggio di rete |
| Un radar a 24 GHz bloccato | Nessun materiale metallico, conduttivo o caricato di carbonio davanti a un'apertura a 24 GHz senza misurarlo; lo spessore di 2 mm del coperchio è una riga della matrice di banco |
| Un preset o un pezzo che non esiste | Un `assert` ferma il rendering: `preset must be solar, electrical or alarm`, `part must be box, lid or both` |
| Una stampa che non combacia | Gli `assert` del sorgente lo intercettano al rendering: la scheda e i suoi supporti ci stanno, i fori dei cavi non sono tagliati da una parete o un supporto né più alti dell'interno, il labbro del coperchio è tra 1,2 e 3 mm |

L'involucro del radar è un punto di partenza meccanico stampabile, **non una classificazione IP, RF o termica**. Nulla è stato stampato né misurato.

## ⚙️ Configurazione

| Nome | Valore | Cosa imposta |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | Spessore di parete e coperchio di `node_box.scad` |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | I supporti della scheda e delle viti del coperchio |
| `screw_d` | 3.2 mm | Viti M3 autofilettanti nei supporti |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | Gioco tra coperchio e scatola; larghezza del labbro ad anello (da 1,2 a 3 mm) |
| `preset`, `part` | `alarm` | `solar`, `electrical` o `alarm`; `box`, `lid` o `both` |
| `vent` | `true` | Una fila di fessure nel coperchio per far uscire il calore |

| Pezzo | Interno (mm) | Scheda (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 Avvio rapido

**Requisiti:** OpenSCAD 2021.01+ (per renderizzare gli involucri), una stampante 3D (FDM) per provarli.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

Vedi il [confine di validazione](docs/VALIDATION.md). La licenza hardware prevista è CERN-OHL-S-2.0; aggiungi il suo testo completo prima di pubblicare i progetti.

## 🧪 Test

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| File di test | Test | Cosa copre |
|---|---|---|
| `test_enclosure_sources.py` | 22 | I sorgenti, i preset della scatola, i file di modello e i numeri citati dai documenti |

OpenSCAD è in grado di renderizzare ogni pezzo su una macchina che lo ha: base e coperchio del radar, scatola e coperchio dei tre preset. Nella [matrice di accettazione al banco](docs/BENCH_ACCEPTANCE.md) si giudica un prototipo stampato.

## 🩺 Risoluzione dei problemi

| Vedi | Perché | Fai |
|---|---|---|
| `preset must be solar, electrical or alarm` | Il `preset` è un altro valore | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | Un parametro ha reso i supporti troppo grandi per l'interno | Ripristina `post_d` o scegli un preset più grande |
| Il coperchio non si chiude | La tua stampante è più stretta del gioco di 0,3 mm | Aumenta `clear` e ristampa |

## 📂 Struttura del repository

<p align="center">
  <img src="images/repository-structure.svg" alt="Struttura del repository di ARMOR-HARDWARE" width="100%">
</p>

<details>
<summary>Versione testuale dell'albero</summary>

```text
ARMOR-HARDWARE/
├── scad/                                gli involucri e i loro file di modello
├── docs/                                le guide di questo repository
├── tests/                               i test
├── tools/                               i controlli CI condivisi e gli strumenti del progetto
├── .github/                             workflow CI e modelli per issue e pull request
├── images/                              banner, icona e le due immagini di questo README
├── build.sh build.bat                   build tramite il flusso di progetto condiviso
├── test.sh test.bat                     eseguire i test tramite il flusso condiviso
├── run.sh run.bat                       avvio tramite il flusso di progetto condiviso
├── armor.project.json                   manifesto: versione, ruolo, maturità, comando di build
├── CHANGELOG.md                         cosa è cambiato in ogni versione
├── SECURITY.md SUPPORT.md LICENSE       politica di sicurezza, supporto e licenza
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   come contribuire e il codice di condotta
├── build-test.sh build-test.bat         eseguire i test tramite il flusso condiviso
└── .gitattributes .gitignore            impostazioni di Git
```

</details>

## 🗺️ Roadmap e limiti noti

**Limiti noti oggi**

* Nulla è stato stampato né misurato; le dimensioni delle schede vengono dai datasheet e ogni riga della matrice di accettazione al banco è *non testata*.
* Non ci sono ancora volumi per la scheda ESP32-S3-ETH-PoE, i magnetici PoE, il riscaldatore PTC né la finestra del sensore di luce; il pannello touch non ha una scatola stampata (conserva l'involucro di fabbrica).
* La licenza hardware prevista per i progetti è CERN-OHL-S-2.0 e il suo testo completo non è ancora nel repository.

**Prossimi passi**

* Registrare i contorni esatti delle schede, i connettori, le posizioni delle viti, le zone libere dell'antenna, il percorso termico e l'obiettivo di protezione ([dati di progetto](docs/DESIGN_INPUTS.md)).
* Stampare i prototipi e compilare la matrice di accettazione al banco con misure datate.

## 🌍 Lingue

Il README e i testi esistono in inglese, spagnolo, francese, italiano, tedesco, cinese, giapponese e portoghese europeo.

## 🔗 Progetti correlati

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) è un sistema di sicurezza perimetrale fatto di repository indipendenti. Ognuno ha la propria versione, i propri test e il proprio README; ecco la famiglia:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratti dei messaggi, validatori, vettori di conformità e tipi generati
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Firmware del nodo di campo per ESP32-S3 con tre radar e un proprio pannello web
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protocolli di inverter e batterie solari e messaggi di un nodo gateway
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Nodo elettrico: contatori, il messaggio delle letture della rete e le regole di manovra
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Nodo e centrale d'allarme: zone, inserimento, ritardi, sirena e PIN, con il server o senza
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Pannello touch: lo stato del sistema su uno schermo a parete, attivare e riconoscere gli allarmi, e la casa dell'assistente vocale
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - La rete locale: i suoi dispositivi, internet e ciò che cambia
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordinatore centrale: telemetria, allarmi, dispositivi, letture solari e telecamere
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Console web: telecamere, radar, allarmi, energia solare e progettista del sito 2D/3D
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Client Android dell'operatore con radar 2D/3D in tempo reale
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - Client operatore per iPhone
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Politica di inferenza visiva che spiega le sue decisioni e non agisce mai
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zone delle telecamere, maschere e regole di rilevamento per la Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intenti vocali offline con una conferma impossibile da falsificare
* **ARMOR-HARDWARE** (questo repository) - Contenitori, elettronica e matrice di accettazione da banco
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Distribuzione, banco di prova CM5, backup e TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulatore di telemetria offline con guasti ripetibili
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Rileva, installa e aggiorna i repository stessi dell'ecosistema
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Architettura, base di sicurezza e matrice delle capacità

## 📚 Documentazione

* [Dati di progetto](docs/DESIGN_INPUTS.md): cosa registrare prima della fabbricazione
* [Limite della validazione](docs/VALIDATION.md): cosa è e cosa non è validato
* [Matrice di accettazione al banco](docs/BENCH_ACCEPTANCE.md): le verifiche, i metodi e i criteri proposti
* [Matrice delle capacità: cosa è provato e cosa no](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catalogo dei progetti: versioni e dipendenze tra i repository](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Cronologia delle modifiche di questo repository](CHANGELOG.md)

## 🤝 Contribuire e comunità

* Prima di una pull request esegui `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py`: deve passare. Vedi [CONTRIBUTING.md](CONTRIBUTING.md) e il [codice di condotta](CODE_OF_CONDUCT.md).
* Il README esiste in otto lingue ed è generato dalle sorgenti in ARMOR-DOCS: una modifica al testo si fa lì.
* Una modifica a un messaggio tra componenti parte da ARMOR-COMMON.
* Non descrivere come funzionante su una scheda ciò che è stato solo compilato.
* Segnala una vulnerabilità in privato: [SECURITY.md](SECURITY.md). Domande, idee e segnalazioni: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

GPL-3.0-or-later - vedi [LICENSE](LICENSE).
