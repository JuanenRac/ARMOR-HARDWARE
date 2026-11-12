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

POST_MARGIN_MM = 4.0       # the posts of the board sit this far inside each corner of the board rectangle (node_box.scad)
SCREW_PLAY_MM = 0.4        # how far a post may be from a hole before an M3 screw no longer goes in square (a pilot of 2.8 mm in a post for a 3.2 mm clearance)


def box_number(name: str) -> float:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*(-?[0-9.]+)\s*;", BOX)
    assert match, name
    return float(match.group(1))


def post_pitch(board: tuple[float, float]) -> tuple[float, float]:
    """The distance between the posts of the board along X and Y."""
    return board[0] - 2 * POST_MARGIN_MM, board[1] - 2 * POST_MARGIN_MM


def holes_fit(board: tuple[float, float], holes_pitch: tuple[float, float]) -> bool:
    pitch = post_pitch(board)
    return all(abs(a - b) <= SCREW_PLAY_MM for a, b in zip(pitch, holes_pitch, strict=True))


def stack_fits(stack_height: float, post_height: float, inside_height: float, lid_clear: float = 3.0) -> bool:
    """The board stands on the posts: post + stack + a clear gap to the lid must fit in the height inside."""
    return post_height + stack_height + lid_clear <= inside_height


class SyntheticRulesTests(unittest.TestCase):
    def test_the_posts_of_a_66_by_53_board_are_58_by_45_apart(self):
        self.assertEqual(post_pitch((66, 53)), (58.0, 45.0))

    def test_holes_at_the_post_pitch_fit_and_holes_a_millimetre_away_do_not(self):
        self.assertTrue(holes_fit((66, 53), (58.0, 45.0)))
        self.assertTrue(holes_fit((66, 53), (58.3, 44.8)))
        self.assertFalse(holes_fit((66, 53), (59.0, 45.0)))
        self.assertFalse(holes_fit((66, 53), (58.0, 47.5)))

    def test_a_stack_fits_the_solar_box_only_when_it_is_low_enough(self):
        inside = 45.0
        self.assertTrue(stack_fits(20.0, box_number("post_h"), inside))
        self.assertFalse(stack_fits(37.0, box_number("post_h"), inside))


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
        self.assertTrue(stack_fits(float(stack), box_number("post_h"), 45.0))

    def test_the_measured_distance_to_the_cover_is_inside_the_guide(self):
        distances = MEASURED["printed_radar_piece"]["inner_face_to_holder_front_mm"]
        measured = {name: value for name, value in distances.items() if value is not None}
        if not measured:
            self.skipTest("the printed piece is not measured yet")
        wavelength = 299792458.0 / 24.125e9 * 1000.0
        for name, value in measured.items():
            behind = MEASURED["ld2450_module"]["antenna_plane_behind_front_edge_mm"] or 0.0
            self.assertTrue(any(abs(value + behind - wanted) <= 1.2 for wanted in (wavelength, 1.5 * wavelength)), f"{name}: {value} mm")


if __name__ == "__main__":
    unittest.main()
