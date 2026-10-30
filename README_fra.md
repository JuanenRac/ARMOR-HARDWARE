<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="Bannière d'ARMOR-HARDWARE" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  🇫🇷 <b>Français</b> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Boîtiers, électronique et matrice d'acceptation sur banc

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 ou ultérieure">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Version-0.2.7-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturité">
</p>

---

**Vérification d'honnêteté - ce qui fonctionne aujourd'hui :** Le boîtier du radar est un **point de départ mécanique imprimable, pas un classement IP, RF ou thermique**, et la boîte paramétrique pour les nœuds solaire, électrique et alarme est vérifiée par les `assert` de sa source (la carte tient, les trous de câbles tiennent, le couvercle dégage les plots), mais **aucune n'a été imprimée ni mesurée** (les dimensions des cartes viennent des fiches techniques ; le panneau tactile n'a pas de boîte imprimée, il garde son boîtier d'origine). Chaque ligne de la [matrice d'acceptation sur banc](docs/BENCH_ACCEPTANCE.md) est *non testée*.

---

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.2.7` |
| Maturité | Fonctionnel |
| Rôle | Boîtiers, électronique et la matrice d'acceptation sur banc (famille : Hardware, parent : ARMOR-NODE-RADAR) |
| Technologie | OpenSCAD 2021.01+ (CAO), Python 3.11+ (contrôles) |
| Tests | 22 (`python -m unittest discover -s tests`) |
| Conceptions | Le boîtier du radar et la boîte de 3 préréglages de nœud (solaire, électrique, alarme) |
| Fonctionne sur | N'importe quel ordinateur avec OpenSCAD |
| Sur matériel réel | Aucun pour l'instant : rien n'a été imprimé ni mesuré ; les trois boîtes ne sont vérifiées que par les `assert` de leur source |
| Licence | GPL-3.0-or-later |

**Aller à :** [Présentation](#-présentation) · [Architecture](#-architecture) · [Sécurité](#-sécurité-et-protection) · [Configuration](#-configuration) · [Démarrage rapide](#-démarrage-rapide) · [Tests](#-tests) · [Dépannage](#-dépannage) · [Structure](#-structure-du-dépôt) · [Liés](#-projets-liés)

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Logiciel | 🟡 | Le boîtier du radar et la boîte paramétrique des nœuds solaire, électrique et d'alarme sont des sources OpenSCAD ; la boîte du radar est un point de départ imprimable, pas une classe IP, RF ou thermique. |
| Tests | 🟡 | 22 tests réussissent (`python -m unittest discover -s tests`) : les sources, les préréglages de la boîte, les fichiers de modèle et les chiffres cités par les documents. Les boîtes sont aussi vérifiées par les `assert` de leur source ; aucune n'a été imprimée ni mesurée. |
| Matériel | 🔴 | Rien n'a été imprimé ni mesuré, les dimensions des cartes viennent de fiches techniques, et chaque ligne de la matrice d'acceptation sur banc n'est pas testée. |
| Documentation | 🟢 | Huit langues, les données de conception et la matrice d'acceptation sur banc sont écrites et à jour. |

## 🎯 Présentation

* **Le boîtier du radar est `scad/node_enclosure_radar.scad`** (avec exports STL, 3MF et AMF et deux projets de trancheur, la base et le couvercle coulissant) : une base d'angle à 90 degrés avec visière, toit et plancher, des gradins de retenue, un couvercle avant coulissant de 2 mm et des volets latéraux, le tout piloté par des paramètres nommés.
* **Une boîte paramétrique pour les nœuds solaire, électrique et alarme** (`scad/node_box.scad`, préréglages `solar`, `electrical` et `alarm`) : parois, plots pour la carte, trous de presse-étoupe, une aération, un logement pour un micro-interrupteur anti-sabotage sous le couvercle et un couvercle à lèvre annulaire. C'est une boîte basse tension, pas un coffret pour câblage secteur.
* **Supports** pour trois modules radar, un presse-étoupe et des trous de drainage. Il n'y a pas encore de volumes pour la carte ESP32-S3-ETH-PoE, la magnétique PoE, le chauffage PTC ni la fenêtre du capteur de lumière que la matrice de banc veut tester. Aucun matériau métallique, conducteur ou chargé de carbone devant une ouverture 24 GHz sans l'avoir mesuré.
* **Matrice d'acceptation sur banc :** les contrôles radio, environnement, alimentation, réseau et caméra avec une méthode et un critère de réussite proposé chacun, et un tableau de compatibilité des caméras à remplir.
* Avant fabrication, notez les contours exacts des cartes, les connecteurs, les positions de vis, les zones libres d'antenne, le chemin thermique et l'objectif de protection ([données de conception](docs/DESIGN_INPUTS.md)).

## 🧩 Rôle dans A.R.M.O.R.

ARMOR-HARDWARE est ce qui contient les nœuds. Il porte le boîtier du nœud radar, la boîte paramétrique des nœuds solaire, électrique, alarme et panneau tactile, et la matrice d'acceptation sur banc qui dit comment juger un prototype avant de le mettre au mur. Ses conceptions sont le point de départ des cartes sur lesquelles tournent [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) et [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI).

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="Architecture de ARMOR-HARDWARE : qui l'appelle, ce qu'il contient et de quoi il dépend" width="100%">
</p>

## 🔒 Sécurité et protection

| Menace | Défense |
|---|---|
| Câblage secteur dans une boîte en plastique | `node_box.scad` est une boîte basse tension, pas un boîtier pour câblage secteur |
| Un radar 24 GHz bloqué | Aucun matériau métallique, conducteur ou chargé de carbone devant une ouverture 24 GHz sans l'avoir mesuré ; l'épaisseur de 2 mm du couvercle est une ligne de la matrice de banc |
| Un préréglage ou une pièce qui n'existe pas | Un `assert` arrête le rendu : `preset must be solar, electrical or alarm`, `part must be box, lid or both` |
| Une impression qui ne s'ajuste pas | Les `assert` de la source l'attrapent au rendu : la carte et ses plots tiennent, les trous de câble ne sont coupés ni par un mur ni par un plot et ne dépassent pas l'intérieur, la lèvre du couvercle fait de 1,2 à 3 mm |

Le boîtier du radar est un point de départ mécanique imprimable, **pas une classe IP, RF ou thermique**. Rien n'a été imprimé ni mesuré.

## ⚙️ Configuration

| Nom | Valeur | Ce qu'elle règle |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | Épaisseur de paroi et de couvercle de `node_box.scad` |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | Les plots de la carte et des vis du couvercle |
| `screw_d` | 3.2 mm | Vis M3 autotaraudeuses dans les plots |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | Jeu entre couvercle et boîte ; largeur de la lèvre annulaire (1,2 à 3 mm) |
| `preset`, `part` | `alarm` | `solar`, `electrical` ou `alarm` ; `box`, `lid` ou `both` |
| `vent` | `true` | Une rangée de fentes dans le couvercle pour évacuer la chaleur |

| Pièce | Intérieur (mm) | Carte (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 Démarrage rapide

**Prérequis:** OpenSCAD 2021.01+ (pour rendre les boîtiers), une imprimante 3D (FDM) pour les essayer.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

Voir la [frontière de validation](docs/VALIDATION.md). La licence matérielle prévue est CERN-OHL-S-2.0 ; ajoutez son texte complet avant de publier les conceptions.

## 🧪 Tests

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| Fichier de tests | Tests | Ce qu'il couvre |
|---|---|---|
| `test_enclosure_sources.py` | 22 | Les sources, les préréglages de la boîte, les fichiers de modèle et les chiffres cités par les documents |

OpenSCAD rend chaque pièce sur une machine qui l'a : la base et le couvercle du radar, la boîte et le couvercle des trois préréglages. La [matrice d'acceptation sur banc](docs/BENCH_ACCEPTANCE.md) sert à juger un prototype imprimé.

## 🩺 Dépannage

| Vous voyez | Parce que | Faites |
|---|---|---|
| `preset must be solar, electrical or alarm` | Le `preset` est autre chose | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | Un paramètre a rendu les plots trop grands pour l'intérieur | Rétablissez `post_d` ou choisissez un préréglage plus grand |
| Le couvercle ne ferme pas | Votre imprimante est plus serrée que le jeu de 0,3 mm | Augmentez `clear` et réimprimez |

## 📂 Structure du dépôt

<p align="center">
  <img src="images/repository-structure.svg" alt="Structure du dépôt de ARMOR-HARDWARE" width="100%">
</p>

<details>
<summary>Version texte de l'arborescence</summary>

```text
ARMOR-HARDWARE/
├── scad/                                les boîtiers et leurs fichiers de modèle
├── docs/                                les guides de ce dépôt
├── tests/                               les tests
├── tools/                               les contrôles CI partagés et les outils du projet
├── .github/                             workflow CI et modèles d'issues et de pull requests
├── images/                              bannière, icône et les deux images de ce README
├── build.sh build.bat                   build par le flux de projet partagé
├── test.sh test.bat                     lancer les tests par le flux partagé
├── run.sh run.bat                       démarrer par le flux de projet partagé
├── armor.project.json                   manifeste : version, rôle, maturité, commande de build
├── CHANGELOG.md                         ce qui a changé à chaque version
├── SECURITY.md SUPPORT.md LICENSE       politique de sécurité, support et licence
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   comment contribuer et le code de conduite
├── build-test.sh build-test.bat         lancer les tests par le flux partagé
└── .gitattributes .gitignore            réglages Git
```

</details>

## 🗺️ Feuille de route et limites connues

**Limites connues aujourd'hui**

* Rien n'a été imprimé ni mesuré ; les tailles de carte viennent des fiches techniques et chaque ligne de la matrice d'acceptation sur banc est *non testée*.
* Il n'y a pas encore de volumes pour la carte ESP32-S3-ETH-PoE, les magnétiques PoE, le chauffage PTC ni la fenêtre du capteur de lumière ; le panneau tactile n'a pas de boîte imprimée (il garde son boîtier d'origine).
* La licence matérielle prévue pour les conceptions est CERN-OHL-S-2.0 et son texte complet n'est pas encore dans le dépôt.

**Ensuite**

* Noter les contours exacts des cartes, les connecteurs, les positions de vis, les zones libres d'antenne, le chemin thermique et l'objectif de protection ([données de conception](docs/DESIGN_INPUTS.md)).
* Imprimer les prototypes et remplir la matrice d'acceptation sur banc avec des mesures datées.

## 🌍 Langues

Le README et les textes existent en anglais, espagnol, français, italien, allemand, chinois, japonais et portugais européen.

## 🔗 Projets liés

**A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) est un système de sécurité périmétrique composé de dépôts indépendants. Chacun a sa propre version, ses propres tests et son propre README ; voici la famille :

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contrats de messages, validateurs, vecteurs de conformité et types générés
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Firmware du nœud de terrain pour ESP32-S3 avec trois radars et son propre panneau web
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protocoles des onduleurs et batteries solaires et messages d'un nœud passerelle
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Nœud électrique : compteurs, le message des mesures du réseau et les règles de commutation
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Nœud et centrale d'alarme : zones, armement, temporisations, sirène et PIN, avec ou sans le serveur
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Panneau tactile : l'état du système sur un écran mural, armer et acquitter, et la maison de l'assistant vocal
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - Le réseau local : ses appareils, internet et ce qui change
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordinateur central : télémétrie, alarmes, appareils, relevés solaires et caméras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Console web : caméras, radar, alarmes, énergie solaire et concepteur de site 2D/3D
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Client Android de l'opérateur avec radar 2D/3D en direct
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - Client opérateur iPhone
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Politique d'inférence visuelle qui explique ses décisions et n'agit jamais
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zones de caméra, masques et règles de détection pour la Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intentions vocales hors ligne avec une confirmation impossible à falsifier
* **ARMOR-HARDWARE** (ce dépôt) - Boîtiers, électronique et matrice d'acceptation sur banc
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Déploiement, banc d'essai CM5, sauvegarde et TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulateur de télémétrie hors ligne avec des pannes reproductibles
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Détecte, installe et met à jour les propres dépôts de l'écosystème
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Architecture, base de sécurité et matrice des capacités

## 📚 Documentation

* [Données de conception](docs/DESIGN_INPUTS.md) : à noter avant la fabrication
* [Limite de la validation](docs/VALIDATION.md) : ce qui est et n'est pas validé
* [Matrice d'acceptation sur banc](docs/BENCH_ACCEPTANCE.md) : les contrôles, leurs méthodes et critères proposés
* [Matrice des capacités : ce qui est prouvé et ce qui ne l'est pas](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catalogue des projets : versions et dépendances entre les dépôts](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Historique des modifications de ce dépôt](CHANGELOG.md)

## 🤝 Contribuer et communauté

* Avant une pull request, lancez `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py` : il doit réussir. Voir [CONTRIBUTING.md](CONTRIBUTING.md) et le [code de conduite](CODE_OF_CONDUCT.md).
* Le README existe en huit langues et est généré à partir des sources d'ARMOR-DOCS : une modification du texte se fait là-bas.
* Une modification d'un message entre composants commence dans ARMOR-COMMON.
* Ne décrivez pas comme fonctionnant sur une carte ce qui a seulement été compilé.
* Signalez une vulnérabilité en privé : [SECURITY.md](SECURITY.md). Questions, idées et rapports : electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

GPL-3.0-or-later - voir [LICENSE](LICENSE).
