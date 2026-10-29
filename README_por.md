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
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/CAD-OpenSCAD-f9d72c.svg" alt="CAD">
  <img src="https://img.shields.io/badge/Tests-22%20passing-2ea44f.svg" alt="Tests">
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
| Função | Caixas, eletrónica e a matriz de aceitação em bancada (família: Hardware, pai: ARMOR-NODE-RADAR) |
| Tecnologia | OpenSCAD 2021.01+ (CAD), Python 3.11+ (verificações) |
| Testes | 22 (`python -m unittest discover -s tests`) |
| Desenhos | A caixa do radar e a caixa de 3 presets de nó (solar, elétrico, alarme) |
| Funciona em | Qualquer computador com OpenSCAD |
| Em hardware real | Nenhum ainda: nada foi impresso nem medido; as três caixas só são verificadas pelos `assert` do seu código |
| Licença | GPL-3.0-or-later |

**Ir para:** [Visão geral](#-visão-geral) · [Arquitetura](#-arquitetura) · [Segurança](#-segurança-e-proteção) · [Configuração](#-configuração) · [Início rápido](#-início-rápido) · [Testes](#-testes) · [Problemas](#-resolução-de-problemas) · [Estrutura](#-estrutura-do-repositório) · [Relacionados](#-projetos-relacionados)

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Software | 🟡 | A caixa do radar e a caixa paramétrica dos nós solar, elétrico e de alarme são fontes de OpenSCAD; a caixa do radar é um ponto de partida imprimível, não uma classificação IP, RF nem térmica. |
| Testes | 🟡 | Passam 22 testes (`python -m unittest discover -s tests`): as fontes, os presets da caixa, os ficheiros de modelo e os números que os documentos citam. As caixas também são verificadas pelos `assert` da sua fonte; nenhuma foi impressa nem medida. |
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

## 🏛️ Arquitetura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitetura de ARMOR-HARDWARE: quem o chama, o que contém e de que depende" width="100%">
</p>

## 🔒 Segurança e proteção

| Ameaça | Defesa |
|---|---|
| Cablagem de rede numa caixa de plástico | `node_box.scad` é uma caixa de baixa tensão, não uma caixa para cablagem de rede |
| Um radar de 24 GHz bloqueado | Nenhum material metálico, condutor ou com carbono diante de uma abertura de 24 GHz sem o medir; a espessura de 2 mm da tampa é uma linha da matriz de bancada |
| Um preset ou uma peça que não existe | Um `assert` pára a renderização: `preset must be solar, electrical or alarm`, `part must be box, lid or both` |
| Uma impressão que não encaixa | Os `assert` da fonte apanham-no ao renderizar: a placa e os seus postes cabem, os furos de cabo não são cortados por uma parede ou poste nem são mais altos que o interior, o lábio da tampa mede de 1,2 a 3 mm |

A caixa do radar é um ponto de partida mecânico imprimível, **não uma classificação IP, RF nem térmica**. Nada foi impresso nem medido.

## ⚙️ Configuração

| Nome | Valor | O que define |
|---|---|---|
| `wall`, `lid_t` | 3 mm, 3 mm | Espessura da parede e da tampa de `node_box.scad` |
| `post_d`, `post_h`, `post_cap` | 7, 6, 9 mm | Os postes da placa e dos parafusos da tampa |
| `screw_d` | 3.2 mm | Parafusos M3 autorroscantes nos postes |
| `clear`, `lip_w` | 0.3 mm, 1.6 mm | Folga entre tampa e caixa; largura do lábio em anel (1,2 a 3 mm) |
| `preset`, `part` | `alarm` | `solar`, `electrical` ou `alarm`; `box`, `lid` ou `both` |
| `vent` | `true` | Uma fila de ranhuras na tampa para sair o calor |

| Peça | Interior (mm) | Placa (mm) |
|---|---|---|
| `solar` | 110 × 80 × 45 | 66 × 53 |
| `electrical` | 140 × 100 × 50 | 120 × 80 |
| `alarm` | 150 × 110 × 60 | 120 × 80 |

## 🚀 Início rápido

**Requisitos:** OpenSCAD 2021.01+ (para renderizar as caixas), uma impressora 3D (FDM) para as experimentar.

```powershell
openscad -o build/node_enclosure_radar.stl scad/node_enclosure_radar.scad
openscad -D 'part="both"' -D 'preset="alarm"' -o build/node_box_alarm.stl scad/node_box.scad   # presets: solar, electrical, alarm
```

Veja o [limite de validação](docs/VALIDATION.md). A licença de hardware prevista é CERN-OHL-S-2.0; acrescente o seu texto completo antes de publicar os desenhos.

## 🧪 Testes

```powershell
python -m unittest discover -s tests   # 22 tests, no OpenSCAD needed
python -I tools/armor_ci_validate.py
```

| Ficheiro de testes | Testes | O que cobre |
|---|---|---|
| `test_enclosure_sources.py` | 22 | As fontes, os presets da caixa, os ficheiros de modelo e os números que os documentos citam |

O OpenSCAD renderiza cada peça numa máquina que o tenha: a base e a tampa do radar, e a caixa e a tampa dos três presets. A [matriz de aceitação em bancada](docs/BENCH_ACCEPTANCE.md) é onde se avalia um protótipo impresso.

## 🩺 Resolução de problemas

| Vê | Porque | Faça |
|---|---|---|
| `preset must be solar, electrical or alarm` | O `preset` é outro valor | `-D 'preset="alarm"'` |
| `the board and its posts do not fit inside the box` | Um parâmetro tornou os postes demasiado grandes para o interior | Reponha `post_d` ou escolha um preset maior |
| A tampa não fecha | A sua impressora é mais apertada do que a folga de 0,3 mm | Aumente `clear` e imprima de novo |

## 📂 Estrutura do repositório

<p align="center">
  <img src="images/repository-structure.svg" alt="Estrutura do repositório de ARMOR-HARDWARE" width="100%">
</p>

<details>
<summary>Versão em texto da árvore</summary>

```text
ARMOR-HARDWARE/
├── scad/                                as caixas e os seus ficheiros de modelo
├── docs/                                os guias deste repositório
├── tests/                               os testes
├── tools/                               as verificações de CI partilhadas e as ferramentas do projeto
├── .github/                             fluxo de CI e modelos de issues e pull requests
├── images/                              faixa, ícone e as duas imagens deste README
├── build.sh build.bat                   compilar pelo fluxo de projeto partilhado
├── test.sh test.bat                     executar os testes pelo fluxo partilhado
├── run.sh run.bat                       arrancar pelo fluxo de projeto partilhado
├── armor.project.json                   manifesto: versão, função, maturidade, comando de build
├── CHANGELOG.md                         o que mudou em cada versão
├── SECURITY.md SUPPORT.md LICENSE       política de segurança, apoio e licença
├── CONTRIBUTING.md CODE_OF_CONDUCT.md   como contribuir e o código de conduta
├── build-test.sh build-test.bat         executar os testes pelo fluxo partilhado
└── .gitattributes .gitignore            definições do Git
```

</details>

## 🗺️ Roteiro e limites conhecidos

**Limites conhecidos hoje**

* Nada foi impresso nem medido; os tamanhos das placas vêm de folhas de dados e cada linha da matriz de aceitação em bancada está *por testar*.
* Ainda não há volumes para a placa ESP32-S3-ETH-PoE, os magnéticos PoE, o aquecedor PTC nem a janela do sensor de luz; o painel tátil não tem caixa impressa (mantém a caixa de fábrica).
* A licença de hardware prevista para os desenhos é a CERN-OHL-S-2.0 e o seu texto completo ainda não está no repositório.

**A seguir**

* Registar os contornos exatos das placas, conectores, posições dos parafusos, zonas livres da antena, o caminho térmico e o objetivo de proteção ([dados de projeto](docs/DESIGN_INPUTS.md)).
* Imprimir os protótipos e preencher a matriz de aceitação em bancada com medições datadas.

## 🌍 Idiomas

O README e os textos existem em inglês, espanhol, francês, italiano, alemão, chinês, japonês e português europeu.

## 🔗 Projetos relacionados

O **A.R.M.O.R.** (Autonomous Radar & Multimodal Observation Range) é um sistema de segurança perimetral feito de repositórios independentes. Cada um tem a sua própria versão, os seus próprios testes e o seu próprio README; esta é a família:

* **[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)** - Contratos de mensagens, validadores, vetores de conformidade e tipos gerados
* **[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)** - Firmware de nó de campo para ESP32-S3 com três radares e o seu próprio painel web
* **[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)** - Protocolos de inversores e baterias solares e as mensagens de um nó porta de ligação
* **[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)** - Nó elétrico: contadores, a mensagem das leituras da rede e as regras de comutação
* **[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)** - Nó e painel de alarme: zonas, armar, atrasos, sirene e PIN, com o servidor ou sem ele
* **[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)** - Painel tátil: o estado do sistema num ecrã de parede, armar e reconhecer, e a casa do assistente de voz
* **[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)** - A rede local: os seus dispositivos, a internet e o que muda
* **[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)** - Coordenador central: telemetria, alarmes, dispositivos, leituras solares e câmaras
* **[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)** - Consola web: câmaras, radar, alarmes, energia solar e o desenhador 2D/3D do local
* **[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)** - Cliente de operador Android com radar 2D/3D em direto
* **[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)** - Cliente de operador para iPhone
* **[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)** - Política de inferência visual que explica as suas decisões e nunca atua
* **[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)** - Zonas de câmara, máscaras e regras de deteção para o Jetson Orin NX
* **[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)** - Intenções de voz offline com uma confirmação que não pode ser falsificada
* **ARMOR-HARDWARE** (este repositório) - Caixas, eletrónica e a matriz de aceitação em bancada
* **[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)** - Implantação, a bancada de testes do CM5, cópias de segurança e TLS
* **[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)** - Simulador de telemetria offline com falhas repetíveis
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - Deteta, instala e atualiza os repositórios do próprio ecossistema
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Arquitetura, base de segurança e a matriz de capacidades

## 📚 Documentação

* [Dados de projeto](docs/DESIGN_INPUTS.md): o que registar antes de fabricar
* [Limite da validação](docs/VALIDATION.md): o que está e o que não está validado
* [Matriz de aceitação em bancada](docs/BENCH_ACCEPTANCE.md): as verificações, os métodos e os critérios propostos
* [Matriz de capacidades: o que está demonstrado e o que não está](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/CAPABILITY_MATRIX.md)
* [Catálogo de projetos: versões e como os repositórios dependem uns dos outros](https://github.com/JuanenRac/ARMOR-DOCS/blob/main/docs/PROJECT_CATALOG.md)
* [Registo de alterações deste repositório](CHANGELOG.md)

## 🤝 Contribuir e comunidade

* Antes de um pull request, execute `python -m unittest discover -s tests` and `python -I tools/armor_ci_validate.py`: tem de passar. Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
* O README existe em oito idiomas e é gerado a partir das fontes do ARMOR-DOCS: uma alteração ao texto faz-se lá.
* Uma alteração a uma mensagem entre componentes começa no ARMOR-COMMON.
* Não descreva como a funcionar numa placa aquilo que só foi compilado.
* Comunique uma vulnerabilidade em privado: [SECURITY.md](SECURITY.md). Perguntas, ideias e relatórios: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

GPL-3.0-or-later - consulte [LICENSE](LICENSE).
