# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- **The command of the pin table is tried:** its wrong arguments, the message when the firmware tables are not next to the repository, the write of the document and its check (a change by hand, a missing document and the line endings of Windows), with a stand-in for the tables so that no other repository is needed.
- **A model of the distance between each radar holder and the front cover, and a file for the real measurements:** `tests/test_antenna_cover_model.py` works out from the numbers of the radar enclosure how far the front face of each holder is from the inner face of the cover (square to the cover and along the beam) and how far from parallel it is, against the wavelengths of the manual (12.4 and 18.6 mm, plus or minus 1.2 mm); `tests/data/measurements.json` is where the calliper measurements of the real board, its mounting holes, the stack with the PoE module and the printed piece go (null until measured), and `tests/test_measurements_fit.py` checks every filled value against the posts and the height of the box. Nothing has been printed or measured.
## [0.2.9] - A floor for the test coverage: the workflow `coverage-floor.yml` runs the Python tests under coverage and fails when the lines or the branches of `tools/pinout.py` and `tools/export_models.py` fall below `docs/coverage_threshold.json` (floo

- **A floor for the test coverage:** the workflow `coverage-floor.yml` runs the Python tests under coverage and fails when the lines or the branches of `tools/pinout.py` and `tools/export_models.py` fall below `docs/coverage_threshold.json` (floor: lines 90.5, branches 85.0; measured 91.26 and 85.90). The shared tools that this repository only carries a copy of are not counted. Raising the floor is a change of that file, made with a figure measured by the workflow.

- **One table of the pins of the nodes:** `docs/PINOUT.md` lists, for the Waveshare ESP32-S3-ETH and the ESP32-S3-WROOM-1 board, what each GPIO is (free, to use with care, never offered and why), the default pins of the ten serial ports, and the Zigbee radio, the eight relays and the eight analog inputs of the base board. It is made by `tools/pinout.py` from the two shared headers of ARMOR-COMMON the firmware is built with, and `tests/test_pinout.py` fails when it differs, when a port defaults to a reserved pin or to a pin another port uses, or when a relay pin repeats.
- **The two enclosures share one file, and the cable holes are the sizes of a shop:** `scad/node_common.scad` holds the wall, the lid thickness, the play of the lid and the cable-gland threads (PG7 12.5 mm, M12 12 mm, PG9 15.2 mm, M16 16 mm); a hole is the thread plus a play of 0.4 mm. The box of the solar node takes PG7 glands and the electrical and alarm boxes M16; the radar enclosure takes a PG9 (its hole was a round 15 mm). The glands of the solar box moved 2 and 3 mm so that the wider hole still clears the corner posts, which the geometry tests caught. Tests check that nothing is defined twice and that every hole is a catalogue thread plus the play.
- **The model files are made from the sources, not kept in the repository:** `tools/export_models.py` renders every piece (the four views of the radar enclosure, and the box and the lid of each preset) as its own STL and 3MF, and the workflow `export-models.yml` keeps them as an artifact of the run. The STL, 3MF and AMF of the radar enclosure that were committed are gone (they could disagree with the source) and the tests that read them now render the file with OpenSCAD in the CI; the two slicer projects stay. Tests without OpenSCAD check the list of pieces, the command of each one, a failed piece failing the export and that the exports are not tracked.

- **Parametric checks of the box, rendered by OpenSCAD in the CI:** `tests/test_parametric_render.py` renders the box and the lid of the three presets and reads the size of each STL back (it must be the inside size plus the walls, the height of the lid plus its switch pocket, the lid set behind the box when both are asked for), changes the shared parameters (`wall`, `lid_t`, `vent`) and checks the piece follows, and checks that the asserts of the source refuse an unknown preset or part, a lip outside 1.2 to 3 mm and posts that do not fit the board, while the edges of what is allowed still render. The evidence is the render, not a print: nothing has been printed or measured. The tests are skipped where OpenSCAD is not installed.
- **The launchers find the shared repository through `ARMOR_COMMON_DIR`:** `build`, `build-test`, `test` and `run` (`.sh` and `.bat`) use the folder named by that variable when it is set and the sibling `ARMOR-COMMON` folder otherwise, so a checkout with another layout builds without changing a file.
## [0.2.8] - The bench acceptance matrix has two more rows, the gap from the antenna to the cover on the side radars and the measured mounting holes of the real board, both marked as not measured

- **Two more rows in the bench acceptance matrix:** the gap from the antenna to the cover on the side radars and the measured mounting holes of the real board, both marked not tested.

## [0.2.7] - The lights of Project status follow the evidence of the manifest, the universal README and the pictures of the README from shared tools

- **The lights of Project status follow the evidence of the manifest:** the manifest says how far the repository has been shown to work (`evidence`: `host-test`, `simulator`, `bench` or `field`) and the validator fails when a light is above what that evidence and the maturity allow (`tools/status_lights.py`), so a green that never ran on real hardware cannot come back.
- **The README follows the universal layout:** security, configuration, testing, troubleshooting and roadmap sections and the architecture and repository-structure pictures, in the eight languages; the test count (22) is stated.
- **The layout of the README is checked in the CI:** the validator runs the shared `tools/universal_readme_check.py` and fails when the README differs from the universal layout.
- **The pictures of the README come from shared tools:** `tools/make_architecture.py` draws `images/architecture.svg` from `docs/architecture.json` and `tools/make_structure.py` draws the Repository Structure (the text tree and the animated picture) from `docs/structure.json`; both measure every text, and `--check` fails when a picture, its description or the code it points to disagree. They are vendored from ARMOR-COMMON like the shared CI checks.

## [0.2.6] - The repository has a security policy, a code of conduct, a contributin

- The repository has a security policy, a code of conduct, a contributing guide and a support file.
- The banner follows the animated style of the ecosystem banners, with the name, the kind and the technologies of the project.

## [0.2.5] - Inputs for the next solar base board: the Pylontech console, the wake output and the dry contacts

- **A note for the next revision of the solar base board:** the pins of the Pylontech console port, the voltage that wakes a sleeping battery and a future output for it, the dry contacts to read with opto-isolated inputs (never driven), and the RS485 and CAN pins and the DIP switch that sets the speed. It is taken from the manuals and not measured on our board.

## [0.2.4] - A box whose lid closes, and documents that tell the truth

- **`scad/node_box.scad`:** the lid's lip is now a ring with a gap for each of the four screw posts (it was a solid plate that sat on the post heads, 2 mm above the rim, so the lid could not close). The tamper micro-switch pocket is two walls that hold a switch of 20 x 10 x 6 mm, not a solid block in the lip's way. Asserts in the source stop the render when the board and its posts do not fit, a cable hole is cut by a wall or a corner post, or the lip is not a ring.
- **The `alarm` battery bay and the `hmi` preset are gone:** the bay overlapped the board and could not hold a 12 V 7 Ah battery, and the alarm node is powered over PoE from a switch behind a UPS (the siren has its own battery); the touch panel keeps the enclosure it comes in, and a window for its screen needs the official drawing. Three presets are left: `solar`, `electrical` and `alarm`.
- **The build test renders every piece** (the radar base and cover, and box and lid of each preset), so a failing assert or a part that is not a solid fails the run.
- **Documents:** three LD2450 draw about 1.8 W (0.6 W each); a 30 W PoE+ port gives the device 25.5 W; the cover thickness and the material figures agree between documents; the matrix says the three radars cover 270° around the outer corner; the README no longer lists volumes the model does not have; the antenna-to-cover distance of the CAD is worked out and does not meet the manual's two distances on the side radars (recorded, the model is unchanged until it is measured on a prototype); a note says the printed box is not an enclosure for mains wiring. The manifest drops KiCad (there is no KiCad file here).

## [0.2.3] - The enclosure moves to `scad/` as the radar enclosure

- The real design, until now `CAD/CARCASA_SENSORES.scad`, is `scad/node_enclosure_radar.scad`, with its STL, 3MF and AMF exports; its parameters and comments are now in English. The placeholder box `scad/node_enclosure.scad` and the `CAD/` folder are gone.
- Two new 3MF slicer project files, `node_enclosure_radar_1.3mf` (the base, about 125 x 125 x 108 mm) and `node_enclosure_radar_2.3mf` (the sliding cover), each ready to slice on its own. `view_mode` (0 exploded, 1 assembled, 2 the base alone, 3 the cover alone) chooses what the file draws or exports.
- The build/test step, CI's OpenSCAD guard and the manifest follow the new path (`armor_project_tool.py` re-synced from ARMOR-COMMON 0.2.7); the seven READMEs describe the new files and the real file tree (they no longer list the empty `CAD/` and `EDA/` folders, which Git never held).

## [0.2.2]

- A GitHub Actions CI baseline (`.github/workflows/ci.yml`): validates the manifest, the version, CHANGELOG.md's heading, the seven README translations' structure and its own local Markdown links, then runs this project's real build/test through `tools/armor_project_tool.py build-test .` (vendored from ARMOR-COMMON, alongside `tools/armor_ci_validate.py` and `tools/_armor_readme_parity.py`, which do the manifest/docs checking).

## [0.2.1] - What the LD2450 manual asks of the enclosure

- Recorded the manual's supply, range, mounting and cover guidance, and worked out that the 2 mm front cover is close to a quarter wavelength in an ABS-like plastic (not one of the two recommended cases). This is arithmetic, not a measurement; the bench matrix gains rows to measure cover thickness and distance, mounting height and the back lobe.

## [0.2.0]

- Bench acceptance matrix and design-input checklist.
- README describes the real `CARCASA_SENSORES.scad` design and its limits.
