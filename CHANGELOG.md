# Changelog

All notable changes to this project are documented here.

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
