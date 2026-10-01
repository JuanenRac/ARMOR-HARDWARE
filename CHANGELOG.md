# Changelog

All notable changes to this project are documented here.

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
