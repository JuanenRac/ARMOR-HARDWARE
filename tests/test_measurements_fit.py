"""ARMOR-HARDWARE - checks of the real calliper measurements against the source of the enclosures, and a model with made-up numbers that shows the checks work.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.

tests/data/measurements.json holds what is measured on the real parts; a value of null is not measured yet and its check passes. The synthetic cases below use invented numbers to prove the
rules (a hole pitch the posts do not match, a stack too tall for the box) fail when they should: they are not measurements and they say nothing about the real board.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = (ROOT / "scad" / "node_box.scad").read_text(encoding="utf-8")
MEASURED = json.loads((ROOT / "tests" / "data" / "measurements.json").read_text(encoding="utf-8"))

SCREW_PLAY_MM = 0.4        # how far a post may be from a hole before an M3 screw no longer goes in square (a pilot of 2.8 mm in a post for a 3.2 mm clearance)


def box_number(name: str) -> float:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*(-?[0-9.]+)\s*;", BOX)
    assert match, name
    return float(match.group(1))


POST_MARGIN_MM = box_number("post_margin")   # the posts of the board sit this far inside each corner of the board rectangle
SCREW_THREAD_MM = box_number("screw_d") - 0.2   # the thread of the M3 screw: the hole of the board has to let it through


def inside_of(preset: str) -> tuple[float, float, float]:
    """The size inside a box, read from `function inside(p)` of node_box.scad (the order there is solar, electrical and the rest, which is alarm)."""
    match = re.search(r'(?m)^function\s+inside\(p\)\s*=\s*p == "solar" \? \[([^\]]+)\] : p == "electrical" \? \[([^\]]+)\] : \[([^\]]+)\];', BOX)
    assert match, "function inside(p) in node_box.scad is not in the form this test reads"
    row = match.group({"solar": 1, "electrical": 2, "alarm": 3}[preset])
    x, y, z = (float(part) for part in row.split(","))
    return x, y, z


def post_pitch(board: tuple[float, float]) -> tuple[float, float]:
    """The distance between the posts of the board along X and Y."""
    return board[0] - 2 * POST_MARGIN_MM, board[1] - 2 * POST_MARGIN_MM


def holes_fit(board: tuple[float, float], holes_pitch: tuple[float, float]) -> bool:
    pitch = post_pitch(board)
    return all(abs(a - b) <= SCREW_PLAY_MM for a, b in zip(pitch, holes_pitch, strict=True))


def stack_fits(stack_height: float, post_height: float, inside_height: float, lid_clear: float = 3.0) -> bool:
    """The board stands on the posts: post + stack + a clear gap to the lid must fit in the height inside."""
    return post_height + stack_height + lid_clear <= inside_height


def screw_goes_through(hole_diameter: float) -> bool:
    return hole_diameter >= SCREW_THREAD_MM


def cover_distance_problems(distances: dict, behind: float | None) -> list[str]:
    """Why the measured distances to the cover are not acceptable. A measured distance without the antenna plane of the module is a problem of its own: it is never judged against zero."""
    measured = {name: value for name, value in distances.items() if value is not None}
    if not measured:
        return []
    if behind is None:
        return ["measure antenna_plane_behind_front_edge_mm of the module: a distance to the cover means nothing without it"]
    wavelength = 299792458.0 / 24.125e9 * 1000.0
    return [f"{name}: {value} mm" for name, value in measured.items() if not any(abs(value + behind - wanted) <= 1.2 for wanted in (wavelength, 1.5 * wavelength))]


class SyntheticRulesTests(unittest.TestCase):
    def test_the_posts_of_a_66_by_53_board_are_58_by_45_apart(self):
        self.assertEqual(post_pitch((66, 53)), (58.0, 45.0))

    def test_holes_at_the_post_pitch_fit_and_holes_a_millimetre_away_do_not(self):
        self.assertTrue(holes_fit((66, 53), (58.0, 45.0)))
        self.assertTrue(holes_fit((66, 53), (58.3, 44.8)))
        self.assertFalse(holes_fit((66, 53), (59.0, 45.0)))
        self.assertFalse(holes_fit((66, 53), (58.0, 47.5)))

    def test_a_stack_fits_the_solar_box_only_when_it_is_low_enough(self):
        inside = inside_of("solar")[2]
        self.assertTrue(stack_fits(20.0, box_number("post_h"), inside))
        self.assertFalse(stack_fits(37.0, box_number("post_h"), inside))

    def test_the_sizes_inside_the_boxes_are_read_from_the_source(self):
        self.assertEqual(inside_of("solar"), (110.0, 80.0, 45.0))
        self.assertEqual(inside_of("electrical"), (140.0, 100.0, 50.0))
        self.assertEqual(inside_of("alarm"), (150.0, 110.0, 60.0))

    def test_the_margin_of_the_posts_is_one_name_of_the_source(self):
        self.assertIn("bd[0] + 2 * post_margin + 2 * post_d / 2", BOX)
        self.assertIn("x = [post_margin, bd[0] - post_margin], y = [post_margin, bd[1] - post_margin]", BOX)

    def test_a_hole_too_small_for_the_screw_is_caught(self):
        self.assertTrue(screw_goes_through(3.0))
        self.assertTrue(screw_goes_through(3.2))
        self.assertFalse(screw_goes_through(2.7))

    def test_a_distance_to_the_cover_without_the_antenna_plane_fails(self):
        self.assertEqual(cover_distance_problems({"s1": None, "s2": None}, None), [])
        self.assertEqual(len(cover_distance_problems({"s1": 12.4, "s2": None}, None)), 1)

    def test_distances_are_judged_against_the_two_windows_of_the_manual(self):
        self.assertEqual(cover_distance_problems({"s1": 10.4, "s2": 16.6}, 2.0), [])
        self.assertEqual(cover_distance_problems({"s1": 10.4, "s2": 7.0}, 2.0), ["s2: 7.0 mm"])


class RealMeasurementsTests(unittest.TestCase):
    """Run on the numbers of tests/data/measurements.json; every null is skipped until the piece is measured."""

    def test_the_file_has_the_expected_shape(self):
        self.assertEqual(MEASURED["format"], 1)
        for key in ("esp32_s3_eth_board", "ld2450_module", "printed_radar_piece"):
            self.assertIn(key, MEASURED)

    def test_the_measured_holes_match_the_posts_of_the_box(self):
        board = MEASURED["esp32_s3_eth_board"]
        if None in board["size_mm"] or None in board["mounting_holes_pitch_mm"]:
            self.skipTest("the board is not measured yet")
        self.assertTrue(holes_fit(tuple(board["size_mm"]), tuple(board["mounting_holes_pitch_mm"])), "move the posts of node_box.scad to the measured holes")

    def test_the_measured_stack_fits_the_solar_box(self):
        stack = MEASURED["esp32_s3_eth_board"]["stacked_height_with_poe_module_mm"]
        if stack is None:
            self.skipTest("the stack with the PoE module is not measured yet")
        self.assertTrue(stack_fits(float(stack), box_number("post_h"), inside_of("solar")[2]))

    def test_the_measured_hole_of_the_board_lets_the_screw_through(self):
        diameter = MEASURED["esp32_s3_eth_board"]["mounting_hole_diameter_mm"]
        if diameter is None:
            self.skipTest("the holes of the board are not measured yet")
        self.assertTrue(screw_goes_through(float(diameter)), "the holes of the board are too small for an M3 screw")

    def test_the_measured_distance_to_the_cover_is_inside_the_guide(self):
        distances = MEASURED["printed_radar_piece"]["inner_face_to_holder_front_mm"]
        if all(value is None for value in distances.values()):
            self.skipTest("the printed piece is not measured yet")
        self.assertEqual(cover_distance_problems(distances, MEASURED["ld2450_module"]["antenna_plane_behind_front_edge_mm"]), [])


if __name__ == "__main__":
    unittest.main()
