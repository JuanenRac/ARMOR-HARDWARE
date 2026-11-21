"""ARMOR-HARDWARE - the presets of the box as the documents state them, against the presets of the model source: every README of the eight languages quotes the same sizes as
node_box.scad, the export lists exactly the pieces the source offers, and the sizes of the presets are consistent with each other. No OpenSCAD is needed.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))

import export_models  # noqa: E402
import test_enclosure_sources as sources  # noqa: E402

READMES = ["README.md", "README_spa.md", "README_fra.md", "README_ita.md", "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md"]
PRESETS = sources.PRESETS


def dims(values) -> str:
    return " × ".join(f"{v:g}" for v in values)


def source_rows() -> dict[str, tuple[str, str]]:
    inside = sources.preset_values("inside")
    board = sources.preset_values("board")
    return {name: (dims(sources.vector_list(inside[name])[0]), dims(sources.vector_list(board[name])[0])) for name in PRESETS}


class ReadmeSizesTests(unittest.TestCase):
    def test_every_readme_quotes_the_sizes_of_the_source(self):
        rows = source_rows()
        for readme in READMES:
            text = (ROOT / readme).read_text(encoding="utf-8")
            for name, (inside, board) in rows.items():
                self.assertIn(f"| `{name}` | {inside} | {board} |", text, f"{readme}: {name}")

    def test_the_eight_readmes_exist_and_declare_the_same_test_count(self):
        counts = set()
        for readme in READMES:
            text = (ROOT / readme).read_text(encoding="utf-8")
            found = re.search(r"^\| (?:Tests?|Pruebas|テスト|测试|Testes) \| (\d+)", text, re.M)
            self.assertIsNotNone(found, readme)
            counts.add(found.group(1))
        self.assertEqual(len(counts), 1, counts)

    def test_no_readme_quotes_a_preset_that_the_source_does_not_have(self):
        for readme in READMES:
            text = (ROOT / readme).read_text(encoding="utf-8")
            rows = re.findall(r"^\| `([a-z]+)` \| \d+ × \d+ × \d+ \|", text, re.M)
            self.assertEqual(sorted(rows), sorted(PRESETS), readme)


class PresetConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.inside = {k: sources.vector_list(v)[0] for k, v in sources.preset_values("inside").items()}
        self.board = {k: sources.vector_list(v)[0] for k, v in sources.preset_values("board").items()}
        self.gland_x = {k: sources.vector_list(v)[0] for k, v in sources.preset_values("gland_x").items()}

    def test_the_inside_sizes_never_shrink_from_solar_to_alarm(self):
        for axis in range(3):
            values = [self.inside[name][axis] for name in PRESETS]
            self.assertEqual(values, sorted(values), f"axis {axis}")

    def test_the_gland_positions_are_strictly_increasing_and_inside_the_width(self):
        for name in PRESETS:
            xs = self.gland_x[name]
            self.assertEqual(xs, sorted(set(xs)), name)
            self.assertGreater(xs[0], 0, name)
            self.assertLess(xs[-1], self.inside[name][0], name)

    def test_every_board_is_smaller_than_the_inside_in_both_directions(self):
        for name in PRESETS:
            self.assertLess(self.board[name][0], self.inside[name][0], name)
            self.assertLess(self.board[name][1], self.inside[name][1], name)

    def test_every_dimension_is_positive_and_a_plausible_millimetre_value(self):
        for name in PRESETS:
            for value in self.inside[name] + self.board[name]:
                self.assertTrue(10 <= value <= 400, f"{name}: {value}")

    def test_the_electrical_and_alarm_boards_share_the_larger_base_board(self):
        self.assertEqual(self.board["electrical"], self.board["alarm"])
        self.assertGreater(self.board["alarm"][0], self.board["solar"][0])


class ExportListTests(unittest.TestCase):
    def test_the_export_presets_are_the_source_presets(self):
        self.assertEqual(tuple(export_models.PRESETS), PRESETS)

    def test_one_box_and_one_lid_per_preset_plus_four_radar_views(self):
        names = [piece.name for piece in export_models.pieces()]
        self.assertEqual(len(names), 4 + 2 * len(PRESETS))
        self.assertEqual(len(set(names)), len(names))
        for preset in PRESETS:
            for part in ("box", "lid"):
                self.assertIn(f"node_box_{preset}_{part}", names)

    def test_each_piece_names_a_source_that_exists(self):
        for piece in export_models.pieces():
            self.assertTrue((ROOT / "scad" / piece.source).is_file(), piece.name)

    def test_each_command_ends_with_its_source_and_writes_its_own_file(self):
        out = Path("out")
        for piece in export_models.pieces():
            for fmt in export_models.FORMATS:
                command = export_models.command(piece, fmt, out)
                self.assertTrue(command[-1].endswith(piece.source), piece.name)
                self.assertIn(str(out / f"{piece.name}.{fmt}"), command)

    def test_an_unknown_format_is_refused(self):
        piece = export_models.pieces()[0]
        for bad in ("obj", "", "STL", "stl "):
            with self.assertRaises(ValueError):
                export_models.command(piece, bad, Path("out"))

    def test_the_defines_of_a_box_piece_are_quoted_strings(self):
        piece = next(p for p in export_models.pieces() if p.name == "node_box_alarm_lid")
        self.assertEqual(dict(piece.defines), {"part": '"lid"', "preset": '"alarm"'})


if __name__ == "__main__":
    unittest.main()
