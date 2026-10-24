<p align="center">
  <img src="images/ARMOR_BANNER.svg" alt="ARMOR-HARDWARE banner" width="100%">
</p>

# 🧱 ARMOR-HARDWARE

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  🇵🇹 <b>Português</b>
</p>

### Caixas, eletrónica e a matriz de aceitação de bancada

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Version-0.2.6-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-00E5FF.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** A caixa do radar é um **ponto de partida mecânico imprimível, não uma classificação IP, RF ou térmica**, e a caixa paramétrica para os nós solar, elétrico e de alarme é verificada pelos `assert` do seu código (a placa cabe, os furos dos cabos cabem, a tampa liberta os pilares), mas **nenhuma foi impressa nem medida** (os tamanhos das placas vêm das folhas de dados; o painel tátil não tem caixa impressa, mantém a sua caixa de fábrica). Cada linha da [matriz de aceitação em bancada](docs/BENCH_ACCEPTANCE.md) está *por testar*.

---

## 📋 Num relance

| | |
|---|---|
| Versão | `0.2.6` |
| Maturidade | Funcional |
| Tecnologia | OpenSCAD |
| Em hardware real | Nenhum ainda: nada foi impresso nem medido; as três caixas só são verificadas pelos `assert` do seu código |

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Software | 🟡 | A caixa do radar e a caixa paramétrica dos nós solar, elétrico e de alarme são fontes de OpenSCAD; a caixa do radar é um ponto de partida imprimível, não uma classificação IP, RF nem térmica. |
| Testes | 🟡 | As caixas são verificadas pelas asserções da sua fonte (a placa cabe, os furos dos cabos cabem, a tampa liberta os pilares); nenhuma foi impressa nem medida. |
| Hardware | 🔴 | Nada foi impresso nem medido, as medidas das placas vêm de folhas de dados, e cada linha da matriz de aceitação em bancada está por testar. |
| Documentação | 🟢 | Oito idiomas, os dados de projeto e a matriz de aceitação em bancada estão escritos e atualizados. |

## 🎯 Visão geral

* **A caixa do radar é `scad/node_enclosure_radar.scad`** (com exportações STL, 3MF e AMF e dois projetos de fatiador, a base e a tampa deslizante): uma base de canto de 90 graus com viseira, teto e chão, degraus de retenção, uma tampa frontal deslizante de 2 mm e abas laterais, tudo governado por parâmetros com nome.
* **Uma caixa paramétrica para os nós solar, elétrico e de alarme** (`scad/node_box.scad`, predefinidos `solar`, `electrical` e `alarm`): paredes, pilares para a placa, furos para bucins, uma ventilação, um espaço para um microinterruptor antissabotagem sob a tampa e uma tampa com lábio anular. É uma caixa de baixa tensão, não um invólucro para cablagem de rede.
* **Suportes** para três módulos de radar, um bucim e furos de drenagem. Ainda não há volumes para a placa ESP32-S3-ETH-PoE, a magnética PoE, o aquecedor PTC nem a janela do sensor de luz que a matriz de bancada quer testar. Nenhum material metálico, condutor ou carregado de carbono à frente de uma abertura de 24 GHz sem o medir.
* **Matriz de aceitação em bancada:** as verificações de rádio, ambiente, alimentação, rede e câmara com um método e um critério de aprovação proposto cada uma, e uma tabela de compatibilidade de câmaras por preencher.
* Antes de fabricar, registe os contornos exatos das placas, conectores, posições de parafusos, zonas livres de antena, o caminho térmico e o objetivo de proteção ([dados de desenho](docs/DESIGN_INPUTS.md)).

## 🧩 Papel no A.R.M.O.R.

O ARMOR-HARDWARE é o que contém os nós. Leva a caixa do nó radar, a caixa paramétrica dos nós solar, elétrico, de alarme e de painel tátil, e a matriz de aceitação em bancada que diz como julgar um protótipo antes de o pôr numa parede. Os seus desenhos são o ponto de partida para as placas em que correm o [ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR), o [ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR), o [ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL), o [ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM) e o [ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI).

## 📂 Estrutura do repositório

```text
ARMOR-HARDWARE/
├── scad/   node_enclosure_radar.scad (+ stl, amf, 3mf and two slicer projects: the base and the sliding cover), node_box.scad (the box of the solar, electrical and alarm nodes)
├── docs/   DESIGN_INPUTS, VALIDATION, BENCH_ACCEPTANCE
├── tests/  checks that need no OpenSCAD: the sources, the presets of the box, the model files and the numbers the documents quote
├── tools/  the shared CI checks (armor_ci_validate.py, armor_project_tool.py, _armor_readme_parity.py)
└── images/ brand assets
```

## 🛠️ Ambiente de desenvolvimento

**Requisitos:** OpenSCAD 2021.01+ (para gerar as caixas), uma impressora 3D (FDM) para as experimentar

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
python -m unittest discover -s tests   # the checks that need no OpenSCAD
```

Veja o [limite de validação](docs/VALIDATION.md). A licença de hardware prevista é CERN-OHL-S-2.0; acrescente o seu texto completo antes de publicar os desenhos.

## 🔗 Projetos relacionados

O **A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) é um sistema de segurança perimetral feito de repositórios independentes. Cada um tem a sua própria versão, os seus próprios testes e o seu próprio README; esta é a família:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratos de mensagens, validadores, vetores de conformidade e tipos gerados
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Firmware de nó de campo para ESP32-S3 com três radares e o seu próprio painel web
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protocolos de inversores e baterias solares e as mensagens de um nó de ligação
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Nó elétrico: contadores, a mensagem das leituras da rede e as regras de comutação
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Nó e central de alarme: zonas, armar, atrasos, sirene e PIN, com o servidor ou sem ele
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Painel tátil: o estado do sistema num ecrã de parede, armar e reconhecer, e a casa do assistente de voz
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - A rede local: os seus dispositivos, a internet e o que muda
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordenador central: telemetria, alarmes, dispositivos, leituras solares e câmaras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Consola web: câmaras, radar, alarmes, energia solar e o desenhador de local 2D/3D
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Cliente Android de operador com um radar 2D/3D em direto
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - Cliente de operador para iPhone
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Política de inferência visual que explica as suas decisões e nunca atua
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zonas de câmara, máscaras e regras de deteção para o Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intenções de voz offline com uma confirmação que não se pode falsificar
* **ARMOR-HARDWARE** (este repositório) - Caixas, eletrónica e a matriz de aceitação de bancada
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Implementação, a bancada de testes CM5, cópias de segurança e TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulador de telemetria offline com falhas repetíveis
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Deteta, instala e atualiza os próprios repositórios do ecossistema
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Arquitetura, linha de base de segurança e a matriz de capacidades

## 📚 Documentação e comunidade

Onde ler mais:

* [Matriz de capacidades: o que está provado e o que não](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catálogo de projetos: versões e como os repositórios dependem uns dos outros](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Registo de alterações deste repositório](CHANGELOG.md)
* [Licença (GPL-3.0-or-later)](LICENSE)
* Perguntas, ideias e relatórios: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

GPL-3.0-or-later - veja [LICENSE](LICENSE).
