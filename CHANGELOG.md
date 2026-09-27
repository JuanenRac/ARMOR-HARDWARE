# Changelog

All notable changes to this project are documented here.

## [0.2.2]

- A GitHub Actions CI baseline (`.github/workflows/ci.yml`): validates the manifest, the version, CHANGELOG.md's heading, the seven README translations' structure and its own local Markdown links, then runs this project's real build/test through `tools/armor_project_tool.py build-test .` (vendored from ARMOR-COMMON, alongside `tools/armor_ci_validate.py` and `tools/_armor_readme_parity.py`, which do the manifest/docs checking).

## [0.2.1] - What the LD2450 manual asks of the enclosure

- Recorded the manual's supply, range, mounting and cover guidance, and worked out that the 2 mm front cover is close to a quarter wavelength in an ABS-like plastic (not one of the two recommended cases). This is arithmetic, not a measurement; the bench matrix gains rows to measure cover thickness and distance, mounting height and the back lobe.

## [0.2.0]

- Bench acceptance matrix and design-input checklist.
- README describes the real `CARCASA_SENSORES.scad` design and its limits.
