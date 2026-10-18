"""ARMOR-HARDWARE - checks of the enclosure sources and of the model files that need no OpenSCAD: the delimiters of the sources, the presets of the box re-checked by hand,
the model files in the repository (STL, AMF, 3MF) well formed and agreeing with each other and with the source, and the numbers the documents quote.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later."""
from __future__ import annotations

import math
import re
import struct
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAD = ROOT / "scad"
RADAR = (SCAD / "node_enclosure_radar.scad").read_text(encoding="utf-8")
BOX = (SCAD / "node_box.scad").read_text(encoding="utf-8")
PRESETS = ("solar", "electrical", "alarm")


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r'//[^\n]*', "", text)


def number(text: str, name: str) -> float:
    match = re.search(rf"(?m)^\s*(?:[a-z_0-9]+\s*=\s*[^;]*;\s*)*{re.escape(name)}\s*=\s*(-?[0-9.]+)\s*;", text) or re.search(rf"\b{re.escape(name)}\s*=\s*(-?[0-9.]+)\s*;", text)
    if not match:
        raise AssertionError(f"{name} is not defined as a number")
    return float(match.group(1))


def vector_list(text: str) -> list[list[float]]:
    return [[float(item) for item in group.split(",")] for group in re.findall(r"\[([-0-9.,\s]+)\]", text)]


def preset_values(function: str) -> dict[str, list]:
    """The value a preset function gives for each preset, read from its chain of ternaries: `p == "solar" ? A : p == "electrical" ? B : C`."""
    body = re.search(rf"function {function}\(p\)\s*=\s*(.*?);\s*(?://|$)", BOX, re.S | re.M).group(1)
    first = re.match(r'p == "solar" \? (.*?) : (?:p == "electrical" \? (.*) : (.*))$', body.strip(), re.S)
    if first:
        solar, electrical, alarm = first.groups()
        return {"solar": solar.strip(), "electrical": (electrical or "").strip(), "alarm": (alarm or "").strip()}
    two = re.match(r'p == "solar" \? (.*?) : (.*)$', body.strip(), re.S)
    solar, other = two.groups()
    return {"solar": solar.strip(), "electrical": other.strip(), "alarm": other.strip()}


class SourceTests(unittest.TestCase):
    def test_delimiters_are_balanced_in_every_source(self):
        for path in SCAD.glob("*.scad"):
            text = re.sub(r'"[^"\n]*"', '""', strip_comments(path.read_text(encoding="utf-8")))
            for opening, closing in ("()", "[]", "{}"):
                self.assertEqual(text.count(opening), text.count(closing), f"{path.name}: {opening}{closing}")
            depth = 0
            for character in text:
                depth += character == "{"
                depth -= character == "}"
                self.assertGreaterEqual(depth, 0, path.name)

    def test_every_statement_ends_properly(self):
        # a line that assigns a value and does not end in ; , or an opening bracket is a typo that OpenSCAD reports only when it renders
        for path in SCAD.glob("*.scad"):
            lines = strip_comments(path.read_text(encoding="utf-8")).splitlines()
            for number_, line in enumerate(lines, 1):
                text = line.strip()
                if re.fullmatch(r"[a-z_0-9]+\s*=\s*[^;{}\[\]()]*", text) and text:
                    self.fail(f"{path.name}:{number_}: '{text}' has no ;")

    def test_the_box_keeps_its_asserts_and_its_three_presets(self):
        self.assertGreaterEqual(BOX.count("assert("), 5)
        self.assertIn('assert(preset == "solar" || preset == "electrical" || preset == "alarm"', BOX)
        self.assertIn('assert(part == "box" || part == "lid" || part == "both"', BOX)
        for preset in PRESETS:
            self.assertIn(f'"{preset}"', BOX)

    def test_the_radar_source_has_the_four_views_the_build_renders(self):
        for mode in (0, 1, 2, 3):
            self.assertRegex(RADAR, rf"view_mode == {mode}\)")
        self.assertRegex(RADAR, r"(?m)^view_mode = 0;")   # the file as committed renders the exploded view, and the build overrides it with -D

    def test_the_build_renders_what_the_sources_offer(self):
        tool = (ROOT / "tools" / "armor_project_tool.py").read_text(encoding="utf-8")
        rendered = re.findall(r'for preset in \(([^)]*)\)', tool)[0].replace('"', "").replace(" ", "").split(",")
        self.assertEqual(set(rendered), set(PRESETS))
        for part in ("box", "lid"):
            self.assertIn(f'"{part}"', tool)
            self.assertIn(f'part == "{part}"', BOX)


class PresetGeometryTests(unittest.TestCase):
    """The asserts of node_box.scad, evaluated here from the numbers in the file, so a bad edit is caught without OpenSCAD (the build still renders every piece)."""

    @classmethod
    def setUpClass(cls):
        text = strip_comments(BOX)
        cls.inside = {name: vector_list(value)[0] if name else None for name, value in preset_values("inside").items()}
        cls.board = {name: vector_list(value)[0] for name, value in preset_values("board").items()}
        cls.glands = {name: vector_list(value) for name, value in preset_values("glands").items()}
        cls.post_d = number(text, "post_d")
        cls.lip_w = number(text, "lip_w")
        cls.wall = number(text, "wall")

    def test_the_numbers_are_read(self):
        for preset in PRESETS:
            self.assertEqual(len(self.inside[preset]), 3, preset)
            self.assertEqual(len(self.board[preset]), 2, preset)
            self.assertEqual(len(self.glands[preset]), 4, preset)

    def test_the_board_and_its_posts_fit(self):
        for preset in PRESETS:
            inside, board = self.inside[preset], self.board[preset]
            self.assertLessEqual(board[0] + 2 * 4 + 2 * self.post_d / 2, inside[0], preset)
            self.assertLessEqual(board[1] + 2 * 4 + 2 * self.post_d / 2, inside[1], preset)

    def test_no_cable_hole_is_cut_by_a_wall_or_a_corner_post(self):
        for preset in PRESETS:
            width = self.inside[preset][0]
            for x, diameter in self.glands[preset]:
                self.assertGreaterEqual(x - diameter / 2, 9, (preset, x))
                self.assertLessEqual(x + diameter / 2, width - 9, (preset, x))

    def test_the_cable_holes_do_not_overlap_each_other_and_fit_the_height(self):
        for preset in PRESETS:
            glands = sorted(self.glands[preset])
            for (x1, d1), (x2, d2) in zip(glands, glands[1:]):
                self.assertGreater(x2 - x1, (d1 + d2) / 2, f"{preset}: two cable holes touch")
            for _x, diameter in glands:
                self.assertLessEqual(diameter, self.inside[preset][2] - 2, preset)

    def test_the_lip_of_the_lid_is_a_ring_between_the_limits_of_the_source(self):
        self.assertTrue(1.2 <= self.lip_w <= 3)

    def test_the_presets_grow_with_the_electronics(self):
        solar, electrical, alarm = (self.inside[name] for name in PRESETS)
        for axis in range(3):
            self.assertLessEqual(solar[axis], electrical[axis])
            self.assertLessEqual(electrical[axis], alarm[axis])


def read_binary_stl(path: Path):
    data = path.read_bytes()
    count = struct.unpack("<I", data[80:84])[0]
    return count, data, len(data) == 84 + 50 * count


class ModelFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.floor = number(RADAR, "floor_z_offset")
        cls.top = number(RADAR, "ceiling_z_offset") + number(RADAR, "ceiling_thickness_z")

    def test_the_stl_is_a_complete_binary_mesh_inside_the_envelope_of_the_source(self):
        count, data, sized = read_binary_stl(SCAD / "node_enclosure_radar.stl")
        self.assertTrue(sized, "the size of the file does not match its triangle count")
        self.assertGreater(count, 100)
        zs = []
        for index in range(count):
            values = struct.unpack("<12fH", data[84 + 50 * index:134 + 50 * index])
            self.assertTrue(all(math.isfinite(value) for value in values[:12]), f"triangle {index}")
            zs.extend(values[5:12:3])
        self.assertAlmostEqual(min(zs), self.floor, places=3)
        self.assertAlmostEqual(max(zs), self.top, places=3)

    def test_the_stl_has_no_degenerate_triangles(self):
        count, data, _ = read_binary_stl(SCAD / "node_enclosure_radar.stl")
        for index in range(count):
            v = struct.unpack("<12fH", data[84 + 50 * index:134 + 50 * index])
            a, b, c = (v[3:6]), (v[6:9]), (v[9:12])
            ab = [b[i] - a[i] for i in range(3)]
            ac = [c[i] - a[i] for i in range(3)]
            cross = [ab[1] * ac[2] - ab[2] * ac[1], ab[2] * ac[0] - ab[0] * ac[2], ab[0] * ac[1] - ab[1] * ac[0]]
            self.assertGreater(math.sqrt(sum(item * item for item in cross)), 0, f"triangle {index} has no area")

    def test_the_3mf_of_the_enclosure_is_valid_and_has_the_triangles_of_the_stl(self):
        count, _data, _ = read_binary_stl(SCAD / "node_enclosure_radar.stl")
        with zipfile.ZipFile(SCAD / "node_enclosure_radar.3mf") as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("[Content_Types].xml", archive.namelist())
            root = ET.fromstring(archive.read("3D/3dmodel.model"))
        self.assertEqual(root.get("unit"), "millimeter")
        namespace = {"m": root.tag.split("}")[0][1:]}
        vertices = root.findall(".//m:vertex", namespace)
        triangles = root.findall(".//m:triangle", namespace)
        self.assertEqual(len(triangles), count)
        top = max(int(t.get(k)) for t in triangles for k in ("v1", "v2", "v3"))
        self.assertLess(top, len(vertices))
        zs = [float(v.get("z")) for v in vertices]
        self.assertAlmostEqual(min(zs), self.floor, places=3)
        self.assertAlmostEqual(max(zs), self.top, places=3)

    def test_the_amf_is_valid_and_agrees_with_the_3mf(self):
        root = ET.parse(SCAD / "node_enclosure_radar.amf").getroot()
        self.assertEqual(root.tag, "amf")
        self.assertEqual(root.get("unit"), "millimeter")
        vertices = root.findall(".//vertex")
        triangles = root.findall(".//triangle")
        count, _data, _ = read_binary_stl(SCAD / "node_enclosure_radar.stl")
        self.assertEqual(len(triangles), count)
        indices = [int(item.text) for t in triangles for item in t if item.tag in ("v1", "v2", "v3")]
        self.assertEqual(len(indices), 3 * count)
        self.assertLess(max(indices), len(vertices))
        zs = [float(v.find("coordinates/z").text) for v in vertices]
        self.assertAlmostEqual(min(zs), self.floor, places=3)
        self.assertAlmostEqual(max(zs), self.top, places=3)

    def test_the_slicer_projects_are_valid_archives_with_well_formed_models(self):
        for name in ("node_enclosure_radar_1.3mf", "node_enclosure_radar_2.3mf"):
            with zipfile.ZipFile(SCAD / name) as archive:
                self.assertIsNone(archive.testzip(), name)
                names = archive.namelist()
                self.assertIn("3D/3dmodel.model", names, name)
                for part in names:
                    if part.endswith((".model", ".rels", "[Content_Types].xml")):
                        ET.fromstring(archive.read(part))   # raises when it is not well-formed XML
                meshes = [part for part in names if part.endswith(".model")]
                triangles_found = 0
                for part in meshes:
                    root = ET.fromstring(archive.read(part))
                    namespace = {"m": root.tag.split("}")[0][1:]}
                    vertices = root.findall(".//m:vertex", namespace)
                    triangles = root.findall(".//m:triangle", namespace)
                    triangles_found += len(triangles)
                    if triangles:
                        self.assertLess(max(int(t.get(k)) for t in triangles for k in ("v1", "v2", "v3")), len(vertices), f"{name}:{part}")
                self.assertGreater(triangles_found, 0, name)

    def test_no_model_file_is_empty_or_a_leftover(self):
        for path in SCAD.iterdir():
            self.assertGreater(path.stat().st_size, 1000, path.name)
            self.assertIn(path.suffix, {".scad", ".stl", ".amf", ".3mf"}, path.name)


class DocumentedNumbersTests(unittest.TestCase):
    """What the documents say about the front cover, recomputed from the source and from physics."""

    FREQUENCY = 24.125e9
    PERMITTIVITY = 2.5

    def wavelength_mm(self) -> float:
        return 299792458.0 / self.FREQUENCY * 1000

    def test_the_documents_quote_the_cover_thickness_of_the_source(self):
        thickness = number(RADAR, "cover_thickness")
        self.assertEqual(thickness, 2)
        for name in ("VALIDATION.md", "DESIGN_INPUTS.md", "BENCH_ACCEPTANCE.md"):
            text = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertRegex(text, r"\b2 mm\b|cover_thickness = 2", name)

    def test_the_wavelengths_of_the_manual_are_the_ones_quoted(self):
        wavelength = self.wavelength_mm()
        text = (ROOT / "docs" / "DESIGN_INPUTS.md").read_text(encoding="utf-8")
        self.assertAlmostEqual(wavelength, 12.43, places=1)
        self.assertIn("**12.4 mm or 18.6 mm**", text)
        self.assertAlmostEqual(1.5 * wavelength, 18.6, delta=0.1)
        in_material = wavelength / math.sqrt(self.PERMITTIVITY)
        self.assertAlmostEqual(in_material / 2, 3.9, delta=0.1)
        self.assertIn("about **3.9 mm**", text)
        self.assertAlmostEqual(in_material / 8, 1.0, delta=0.05)

    def test_a_two_millimetre_cover_is_about_a_quarter_wavelength_in_the_material(self):
        in_material = self.wavelength_mm() / math.sqrt(self.PERMITTIVITY)
        self.assertAlmostEqual(number(RADAR, "cover_thickness") / in_material, 0.25, delta=0.02)
        text = (ROOT / "docs" / "VALIDATION.md").read_text(encoding="utf-8")
        self.assertIn("quarter", text)

    def test_every_file_a_document_names_exists(self):
        for document in (ROOT / "docs").glob("*.md"):
            for reference in re.findall(r"`((?:scad|docs|tools)/[A-Za-z0-9_./-]+)`", document.read_text(encoding="utf-8")):
                self.assertTrue((ROOT / reference).exists(), f"{document.name} names {reference}")

    def test_the_documents_do_not_promise_a_rating_the_model_does_not_have(self):
        text = (ROOT / "docs" / "VALIDATION.md").read_text(encoding="utf-8").lower()
        self.assertIn("not an ip", text)
        self.assertIn("starting point", BOX)


if __name__ == "__main__":
    unittest.main()
