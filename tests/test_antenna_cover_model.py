"""ARMOR-HARDWARE - a geometric model of the distance between each radar holder and the front cover of the radar enclosure, worked out from the numbers of the source.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.

OpenSCAD is not needed: the model takes the positions, the azimuths, the tilts and the thickness of the cover from `scad/node_enclosure_radar.scad` and computes, with plain geometry,
how far the front face of each holder (taken as the antenna plane) is from the inner face of the cover and how far from parallel it is. It is a model, not a measurement: the real
position of the antenna on the LD2450 module and the real printed piece decide the final cotas, and a caliper measurement of the printed piece has to replace the assumptions below.
"""
from __future__ import annotations

import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RADAR = (ROOT / "scad" / "node_enclosure_radar.scad").read_text(encoding="utf-8")

WAVELENGTH_MM = 299792458.0 / 24.125e9 * 1000.0   # 12.43 mm at 24.125 GHz
RECOMMENDED_MM = (WAVELENGTH_MM, 1.5 * WAVELENGTH_MM)   # one or one and a half wavelengths
TOLERANCE_MM = 1.2
FRONT_OF_HOLDER_MM = 12.0   # the front plate of the holder sits 12 mm in front of the sensor position (`translate([0, -12, 0])` of solid_block)


def number(name: str) -> float:
    match = re.search(rf"\b{re.escape(name)}\s*=\s*(-?[0-9.]+)\s*;", RADAR)
    if not match:
        raise AssertionError(f"{name} is not a number of the source")
    return float(match.group(1))


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


class Holder:
    """One radar holder: where its front plate is and where it points (azimuth about Z, then the tilt about the local X axis, as the source applies them)."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.x, self.y = number(f"{name}_x"), number(f"{name}_y")
        self.azimuth = math.radians(number(f"{name}_azimuth"))
        self.tilt = math.radians(number(f"{name}_tilt"))

    def beam(self) -> tuple[float, float, float]:
        """The unit normal of the front plate (the beam): -Y of the holder, tilted, then turned by the azimuth."""
        local = (0.0, -math.cos(self.tilt), -math.sin(self.tilt))
        c, s = math.cos(self.azimuth), math.sin(self.azimuth)
        return (local[0] * c - local[1] * s, local[0] * s + local[1] * c, local[2])

    def centre(self) -> tuple[float, float]:
        """The centre of the front plate seen from above: the sensor position plus 12 mm along the azimuth direction (the tilt moves it in Z only)."""
        c, s = math.cos(self.azimuth), math.sin(self.azimuth)
        return (self.x + FRONT_OF_HOLDER_MM * s, self.y - FRONT_OF_HOLDER_MM * c)


def cover_planes() -> dict[str, tuple[tuple[float, float], float]]:
    """The inner faces of the cover as (horizontal unit normal, offset) with `normal . point = offset`: the stretch along X (y = const), the stretch along Y (x = const) and the diagonal chamfer."""
    overhang_x, overhang_y = number("flap_x_overhang_y"), number("flap_y_overhang_x")
    chamfer, thickness = number("visor_chamfer"), number("cover_thickness")
    inv = 1.0 / math.sqrt(2.0)
    # the outer chamfer joins (-overhang_y + chamfer, -overhang_x) with (-overhang_y, -overhang_x + chamfer); the inner face is `thickness` inside it
    outer = -(overhang_x + overhang_y) + chamfer
    return {
        "x_stretch": ((0.0, 1.0), -overhang_x + thickness),                # the plane y = -35 + 2
        "y_stretch": ((1.0, 0.0), -overhang_y + thickness),                # the plane x = -35 + 2
        "diagonal": ((inv, inv), outer * inv + thickness),                # x + y = outer + thickness * sqrt(2)
    }


def distances(holder: Holder, plane: tuple[tuple[float, float], float]) -> tuple[float, float, float]:
    """(square to the cover, along the beam, angle between the beam and the normal of the cover in degrees) for a holder looking at a stretch of cover."""
    (nx, ny), offset = plane
    cx, cy = holder.centre()
    square = abs(offset - (cx * nx + cy * ny))
    beam = holder.beam()
    cosine = abs(dot(beam, (nx, ny, 0.0)))   # includes the tilt
    horizontal = math.hypot(beam[0], beam[1])
    yaw_cosine = cosine / horizontal   # the turn seen from above, without the tilt
    along = square / yaw_cosine if yaw_cosine > 1e-9 else math.inf   # along the beam seen from above
    angle = math.degrees(math.acos(min(1.0, cosine)))
    return square, along, angle


def meets_the_guide(distance: float) -> bool:
    return any(abs(distance - wanted) <= TOLERANCE_MM for wanted in RECOMMENDED_MM)


class AntennaCoverModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.planes = cover_planes()
        self.s1, self.s2, self.s3 = Holder("s1"), Holder("s2"), Holder("s3")

    def test_the_wavelengths_are_the_ones_of_the_manual(self):
        self.assertAlmostEqual(RECOMMENDED_MM[0], 12.43, places=2)
        self.assertAlmostEqual(RECOMMENDED_MM[1], 18.64, places=2)

    def test_the_diagonal_radar_is_about_12_2_mm_from_the_cover_but_tilted(self):
        square, along, angle = distances(self.s3, self.planes["diagonal"])
        self.assertAlmostEqual(square, 12.2, delta=0.1)
        self.assertTrue(meets_the_guide(square))
        self.assertGreater(angle, 15.0)   # the cover is not parallel to the antenna: the guide asks for parallel
        self.assertGreater(along, square)

    def test_the_side_radars_are_about_17_6_mm_square_to_the_cover_and_further_along_the_beam(self):
        s1_square, s1_along, s1_angle = distances(self.s1, self.planes["x_stretch"])
        s2_square, s2_along, s2_angle = distances(self.s2, self.planes["y_stretch"])
        for square, along, angle in ((s1_square, s1_along, s1_angle), (s2_square, s2_along, s2_angle)):
            self.assertAlmostEqual(square, 17.6, delta=0.5)
            self.assertAlmostEqual(along, 20.3, delta=1.0)
            self.assertGreater(angle, 25.0)   # 30 degrees of yaw and 20 of tilt: far from parallel
            self.assertFalse(meets_the_guide(along), "the distance along the beam is outside both recommended values")

    def test_no_radar_has_a_cover_parallel_to_its_antenna(self):
        angles = [distances(self.s1, self.planes["x_stretch"])[2], distances(self.s2, self.planes["y_stretch"])[2], distances(self.s3, self.planes["diagonal"])[2]]
        self.assertTrue(all(angle > 15.0 for angle in angles), angles)

    def test_a_faceted_cover_square_to_a_holder_would_meet_the_guide(self):
        """The fix proposed in the design notes: a flat window square to the beam at the wanted distance. The model shows what the cover offset would have to be."""
        for holder in (self.s1, self.s2, self.s3):
            beam = holder.beam()
            horizontal = math.hypot(beam[0], beam[1])
            window = (beam[0] / horizontal, beam[1] / horizontal)
            for wanted in RECOMMENDED_MM:
                # a window with its normal along the horizontal beam, at `wanted` mm (square) from the plate centre, is `wanted` mm away by construction
                cx, cy = holder.centre()
                offset = (cx * window[0] + cy * window[1]) + wanted
                square = abs(offset - (cx * window[0] + cy * window[1]))
                self.assertAlmostEqual(square, wanted, places=9)

    def test_a_thicker_or_thinner_cover_moves_the_distance_by_its_thickness(self):
        """What changing the thickness of the cover does to the distances: every millimetre of cover takes a millimetre (square) from the side radars."""
        base = distances(self.s1, self.planes["x_stretch"])[0]
        (nx, ny), offset = self.planes["x_stretch"]
        thicker = distances(self.s1, ((nx, ny), offset + 1.0))[0]
        self.assertAlmostEqual(abs(base - thicker), 1.0, places=9)


if __name__ == "__main__":
    unittest.main()
