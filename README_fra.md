<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
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
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Version-0.2.6-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui fonctionne aujourd'hui:** Le boîtier du radar est un **point de départ mécanique imprimable, pas un classement IP, RF ou thermique**, et la boîte paramétrique pour les nœuds solaire, électrique et alarme est vérifiée par les `assert` de sa source (la carte tient, les trous de câbles tiennent, le couvercle dégage les plots), mais **aucune n'a été imprimée ni mesurée** (les dimensions des cartes viennent des fiches techniques ; le panneau tactile n'a pas de boîte imprimée, il garde son boîtier d'origine). Chaque ligne de la [matrice d'acceptation sur banc](docs/BENCH_ACCEPTANCE.md) est *non testée*.

---

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.2.6` |
| Maturité | Fonctionnel |
| Technologie | OpenSCAD |
| Sur matériel réel | Aucun pour l'instant : rien n'a été imprimé ni mesuré ; les trois boîtes ne sont vérifiées que par les `assert` de leur source |

## 🎯 Présentation

* **Le boîtier du radar est `scad/node_enclosure_radar.scad`** (avec exports STL, 3MF et AMF et deux projets de trancheur, la base et le couvercle coulissant) : une base d'angle à 90 degrés avec visière, toit et plancher, des gradins de retenue, un couvercle avant coulissant de 2 mm et des volets latéraux, le tout piloté par des paramètres nommés.
* **Une boîte paramétrique pour les nœuds solaire, électrique et alarme** (`scad/node_box.scad`, préréglages `solar`, `electrical` et `alarm`) : parois, plots pour la carte, trous de presse-étoupe, une aération, un logement pour un micro-interrupteur anti-sabotage sous le couvercle et un couvercle à lèvre annulaire. C'est une boîte basse tension, pas un coffret pour câblage secteur.
* **Supports** pour trois modules radar, un presse-étoupe et des trous de drainage. Il n'y a pas encore de volumes pour la carte ESP32-S3-ETH-PoE, la magnétique PoE, le chauffage PTC ni la fenêtre du capteur de lumière que la matrice de banc veut tester. Aucun matériau métallique, conducteur ou chargé de carbone devant une ouverture 24 GHz sans l'avoir mesuré.
* **Matrice d'acceptation sur banc :** les contrôles radio, environnement, alimentation, réseau et caméra avec une méthode et un critère de réussite proposé chacun, et un tableau de compatibilité des caméras à remplir.
* Avant fabrication, notez les contours exacts des cartes, les connecteurs, les positions de vis, les zones libres d'antenne, le chemin thermique et l'objectif de protection ([données de conception](docs/DESIGN_INPUTS.md)).

## 🧩 Rôle dans A.R.M.O.R.

ARMOR-HARDWARE est ce qui contient les nœuds. Il porte le boîtier du nœud radar, la boîte paramétrique des nœuds solaire, électrique, alarme et panneau tactile, et la matrice d'acceptation sur banc qui dit comment juger un prototype avant de le mettre au mur. Ses conceptions sont le point de départ des cartes sur lesquelles tournent [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) et [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI).

## 📂 Structure du dépôt

```text
ARMOR-HARDWARE/
├── scad/   node_enclosure_radar.scad (+ stl, amf, 3mf and two slicer projects: the base and the sliding cover), node_box.scad (the box of the solar, electrical and alarm nodes)
├── docs/   DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
├── tests/  checks that need no OpenSCAD: the sources, the presets of the box, the model files and the numbers the documents quote
└── images/ brand assets
```

## 🛠️ Environnement de développement

**Prérequis:** OpenSCAD 2021.01+ (pour générer les boîtiers), une imprimante 3D (FDM) pour les essayer

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
python -m unittest discover -s tests   # the checks that need no OpenSCAD
```

Voir la [frontière de validation](docs/VALIDATION.md). La licence matérielle prévue est CERN-OHL-S-2.0 ; ajoutez son texte complet avant de publier les conceptions.

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

## 📚 Documentation et communauté

Pour en savoir plus :

* [Matrice des capacités : ce qui est prouvé et ce qui ne l'est pas](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catalogue des projets : versions et dépendances entre les dépôts](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Historique des modifications de ce dépôt](CHANGELOG.md)
* [Licence (GPL-3.0-or-later)](LICENSE)
* Questions, idées et rapports : electrohobby3d@gmail.com

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

GPL-3.0-or-later - voir [LICENSE](LICENSE).
