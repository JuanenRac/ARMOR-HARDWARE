"""ARMOR-HARDWARE - parametric checks of the box of the nodes, rendered by OpenSCAD: the size of every piece of every preset follows the numbers of the source, a change of a
shared parameter changes the piece the way it should, and the asserts of the source refuse what would make a print useless. The evidence is the simulator (a render), not a
print: the pieces have not been printed or measured. The tests are skipped where OpenSCAD is not installed; the CI installs it.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_enclosure_sources import BOX, PRESETS, number, preset_values, strip_comments, vector_list  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OPENSCAD = shutil.which("openscad")
CLEAN = strip_comments(BOX)
INSIDE = {name: vector_list(value)[0] for name, value in preset_values("inside").items()}
WALL = number(CLEAN, "wall")
LID_T = number(CLEAN, "lid_t")
GAP_Y = 15.0           # the lid of "both" is set this far behind the box (translate in the source)
TOLERANCE = 0.05


def render(part: str, preset: str, **overrides: object) -> tuple[int, str, Path]:
    """Renders node_box.scad into a temporary STL; the coarse circle keeps it fast and has the same extremes as the fine one (a multiple of four sides)."""
    folder = Path(tempfile.mkdtemp(prefix="armor-box-"))
    output = folder / "piece.stl"
    command = [str(OPENSCAD), "-D", "$fn=16", "-D", f'part="{part}"', "-D", f'preset="{preset}"']
    for name, value in overrides.items():
        command += ["-D", f"{name}={value}"]
    command += ["-o", str(output), str(ROOT / "scad" / "node_box.scad")]
    done = subprocess.run(command, capture_output=True, text=True, check=False, timeout=240)
    return done.returncode, done.stderr, output


def bounds(stl: Path) -> tuple[list[float], list[float], int]:
    low, high, triangles = [1e9] * 3, [-1e9] * 3, 0
    for line in stl.read_text(encoding="ascii", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("vertex"):
            for axis, text in enumerate(line.split()[1:4]):
                value = float(text)
                low[axis], high[axis] = min(low[axis], value), max(high[axis], value)
        elif line.startswith("endfacet"):
            triangles += 1
    return low, high, triangles


@unittest.skipUnless(OPENSCAD, "OpenSCAD is not installed here (the CI installs it)")
class RenderedBoxTests(unittest.TestCase):
    def test_the_box_of_every_preset_is_the_size_the_source_says(self):
        for preset in PRESETS:
            code, error, output = render("box", preset)
            self.assertEqual(code, 0, f"{preset}: {error[-300:]}")
            low, high, triangles = bounds(output)
            inside = INSIDE[preset]
            for axis, expected in enumerate((inside[0] + 2 * WALL, inside[1] + 2 * WALL, inside[2] + WALL)):
                self.assertAlmostEqual(high[axis] - low[axis], expected, delta=TOLERANCE, msg=f"{preset} axis {axis}")
            self.assertAlmostEqual(low[2], 0.0, delta=TOLERANCE, msg=f"{preset}: the box stands on the bed")
            self.assertGreater(triangles, 200, preset)

    def test_the_lid_of_every_preset_is_as_wide_as_its_box_and_as_tall_as_its_switch_pocket(self):
        for preset in PRESETS:
            code, error, output = render("lid", preset)
            self.assertEqual(code, 0, f"{preset}: {error[-300:]}")
            low, high, _ = bounds(output)
            inside = INSIDE[preset]
            self.assertAlmostEqual(high[0] - low[0], inside[0] + 2 * WALL, delta=TOLERANCE, msg=preset)
            self.assertAlmostEqual(high[1] - low[1], inside[1] + 2 * WALL, delta=TOLERANCE, msg=preset)
            self.assertAlmostEqual(high[2] - low[2], LID_T + 6, delta=TOLERANCE, msg=f"{preset}: the walls of the switch pocket are 6 mm above the lid")

    def test_both_puts_the_lid_behind_the_box_with_a_gap(self):
        code, error, output = render("both", "solar")
        self.assertEqual(code, 0, error[-300:])
        low, high, _ = bounds(output)
        depth = INSIDE["solar"][1] + 2 * WALL
        self.assertAlmostEqual(high[1] - low[1], 2 * depth + GAP_Y, delta=TOLERANCE)

    def test_a_thicker_wall_makes_a_bigger_box_in_every_direction_that_has_walls(self):
        code, error, output = render("box", "solar", wall=4)
        self.assertEqual(code, 0, error[-300:])
        low, high, _ = bounds(output)
        inside = INSIDE["solar"]
        for axis, expected in enumerate((inside[0] + 8, inside[1] + 8, inside[2] + 4)):
            self.assertAlmostEqual(high[axis] - low[axis], expected, delta=TOLERANCE, msg=f"axis {axis}")

    def test_a_thicker_lid_makes_a_taller_lid_and_leaves_the_box_alone(self):
        code, error, output = render("lid", "alarm", lid_t=5)
        self.assertEqual(code, 0, error[-300:])
        low, high, _ = bounds(output)
        self.assertAlmostEqual(high[2] - low[2], 5 + 6, delta=TOLERANCE)
        code, error, box_output = render("box", "alarm", lid_t=5)
        self.assertEqual(code, 0, error[-300:])
        code, error, plain_output = render("box", "alarm")
        self.assertEqual(code, 0, error[-300:])
        self.assertEqual(bounds(box_output)[:2], bounds(plain_output)[:2], "the thickness of the lid does not change the box")

    def test_the_vent_slots_make_the_lid_lighter_and_cost_triangles(self):
        _, _, with_vent = render("lid", "solar")
        _, _, without = render("lid", "solar", vent="false")
        self.assertGreater(bounds(with_vent)[2], bounds(without)[2])
        self.assertEqual(bounds(with_vent)[0], bounds(without)[0])


@unittest.skipUnless(OPENSCAD, "OpenSCAD is not installed here (the CI installs it)")
class AssertsOfTheSourceTests(unittest.TestCase):
    """What would make a print useless is refused when the file is rendered, not on the printer."""

    def refused(self, why: str, **overrides: object) -> None:
        part = str(overrides.pop("part", "box"))
        preset = str(overrides.pop("preset", "solar"))
        code, error, _ = render(part, preset, **overrides)
        self.assertNotEqual(code, 0, why)
        self.assertRegex(error, r"(?i)assert", why)

    def test_an_unknown_preset_or_part_is_refused(self):
        self.refused("preset", preset="garage")
        self.refused("part", part="base")

    def test_a_lip_that_is_too_thin_or_too_wide_is_refused(self):
        self.refused("lip too thin", lip_w=1.0)
        self.refused("lip too wide", lip_w=3.5)

    def test_a_board_that_does_not_fit_is_refused(self):
        self.refused("posts too large for the cavity", post_d=40)

    def test_the_edge_of_what_is_allowed_still_renders(self):
        for lip in (1.2, 3):
            code, error, _ = render("lid", "solar", lip_w=lip)
            self.assertEqual(code, 0, f"lip {lip}: {error[-200:]}")


class RenderHelperTests(unittest.TestCase):
    def test_the_parser_reads_the_corners_of_a_small_stl(self):
        folder = Path(tempfile.mkdtemp(prefix="armor-stl-"))
        stl = folder / "t.stl"
        stl.write_text("solid t\nfacet normal 0 0 1\nouter loop\nvertex 0 0 0\nvertex 4 0 0\nvertex 0 3 2\nendloop\nendfacet\nendsolid t\n", encoding="ascii")
        self.assertEqual(bounds(stl), ([0.0, 0.0, 0.0], [4.0, 3.0, 2.0], 1))

    def test_the_sizes_come_from_the_source_and_are_sensible(self):
        self.assertEqual(set(INSIDE), set(PRESETS))
        self.assertTrue(re.fullmatch(r"[0-9.]+", str(WALL)))
        self.assertGreaterEqual(WALL, 2)
        self.assertGreaterEqual(LID_T, 2)
        for size in INSIDE.values():
            self.assertTrue(all(value > 20 for value in size))


if __name__ == "__main__":
    unittest.main()
