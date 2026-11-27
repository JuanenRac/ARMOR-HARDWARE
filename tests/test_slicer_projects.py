"""ARMOR-HARDWARE - the slicer projects of the radar enclosure agree with the source they were made from.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.

Everything here is read from files; OpenSCAD is not needed. Nothing has been printed or measured.
"""
from __future__ import annotations

import contextlib
import io
import json
import math
import re
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import slicer_projects  # noqa: E402

RADAR = (ROOT / "scad" / "node_enclosure_radar.scad").read_text(encoding="utf-8")
COMMON = (ROOT / "scad" / "node_common.scad").read_text(encoding="utf-8")


def number(text: str, name: str) -> float:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*(-?[0-9.]+)\s*;", text)
    assert match, name
    return float(match.group(1))


def piece(project: str):
    """The mesh of a project moved back to the coordinates of the source (a project keeps a piece centred on its envelope)."""
    points, triangles = slicer_projects.project_mesh(ROOT / "scad" / project)
    low, _high = slicer_projects.envelope(points)
    return points, triangles, low


def base_in_source_coordinates():
    points, _triangles, low = piece("node_enclosure_radar_1.3mf")
    corner = (-number(RADAR, "flap_y_overhang_x"), -number(RADAR, "flap_x_overhang_y"), number(RADAR, "floor_z_offset"))
    return [tuple(p[i] - low[i] + corner[i] for i in range(3)) for p in points]


class RecordTests(unittest.TestCase):
    def setUp(self):
        folder = Path(tempfile.mkdtemp(prefix="armor-slicer-"))
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        shutil.copytree(ROOT / "scad", folder / "scad")
        self.root = folder

    def test_the_projects_of_the_repository_were_made_from_the_sources_of_today(self):
        self.assertEqual(slicer_projects.stale(), [])

    def test_a_source_that_changes_leaves_both_projects_behind(self):
        source = self.root / "scad" / "node_common.scad"
        source.write_text(source.read_text(encoding="utf-8") + "\n// a change\n", encoding="utf-8")
        problems = slicer_projects.stale(self.root)
        self.assertEqual(len(problems), 2, problems)
        self.assertTrue(all("node_common.scad changed" in problem for problem in problems), problems)

    def test_the_line_endings_of_a_checkout_do_not_count(self):
        for name in slicer_projects.SOURCES:
            path = self.root / "scad" / name
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertEqual(slicer_projects.stale(self.root), [])

    def test_a_missing_record_or_entry_is_said(self):
        record = self.root / "scad" / "slicer_projects.json"
        body = json.loads(record.read_text(encoding="utf-8"))
        del body["projects"]["node_enclosure_radar_2.3mf"]
        record.write_text(json.dumps(body), encoding="utf-8")
        self.assertEqual(slicer_projects.stale(self.root), ["node_enclosure_radar_2.3mf: not recorded as node_enclosure_radar_cover"])
        record.unlink()
        self.assertEqual(slicer_projects.stale(self.root), ["slicer_projects.json is missing"])

    def test_the_command_says_pass(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(slicer_projects.main([]), 0)
        self.assertIn("SLICER_PROJECTS=PASS", out.getvalue())


class MeshTests(unittest.TestCase):
    def test_the_base_has_the_envelope_of_the_source(self):
        points, _triangles, _low = piece("node_enclosure_radar_1.3mf")
        low, high = slicer_projects.envelope(points)
        height = number(RADAR, "ceiling_z_offset") + number(RADAR, "ceiling_thickness_z") - number(RADAR, "floor_z_offset")
        self.assertAlmostEqual(high[0] - low[0], number(RADAR, "face_length_x") + number(RADAR, "flap_y_overhang_x"), places=2)
        self.assertAlmostEqual(high[1] - low[1], number(RADAR, "face_length_y") + number(RADAR, "flap_x_overhang_y"), places=2)
        self.assertAlmostEqual(high[2] - low[2], height, places=2)

    def test_the_cable_hole_of_the_base_is_the_gland_of_the_source(self):
        self.assertRegex(RADAR, r"(?m)^cable_gland_d = gland_hole\(gland_pg9\);")
        radius = (number(COMMON, "gland_pg9") + number(COMMON, "gland_play")) / 2
        match = re.search(r"(?m)^cable_gland_pos = \[([^\]]+)\];", RADAR)
        assert match
        x, _y, z = (float(part) for part in match.group(1).split(","))
        wall_y = number(RADAR, "face_length_y")
        face = wall_y - number(RADAR, "flap_y_thickness")
        around = [math.hypot(p[0] - x, p[2] - z) for p in base_in_source_coordinates() if face - 0.01 <= p[1] <= wall_y + 0.01]
        rim = [distance for distance in around if distance < radius + 0.5]
        self.assertGreaterEqual(len(rim), 80, "the rim of the cable hole, on both faces of the flap")
        self.assertAlmostEqual(min(rim), radius, places=3)
        self.assertAlmostEqual(max(rim), radius, places=3)

    def test_the_cover_has_the_thickness_of_the_source(self):
        points, triangles, low = piece("node_enclosure_radar_2.3mf")
        xs = sorted({round(p[0] - low[0], 3) for p in points})
        self.assertAlmostEqual(xs[1] - xs[0], number(RADAR, "cover_thickness"), places=3)
        self.assertGreater(len(triangles), 10)

    def test_no_project_names_the_account_that_saved_it(self):
        for project in slicer_projects.PROJECTS:
            with zipfile.ZipFile(ROOT / "scad" / project) as archive:
                text = archive.read("3D/3dmodel.model").decode("utf-8")
            self.assertNotRegex(text, r'name="DesignerUserId">[^<]+<', project)


class RemeshTests(unittest.TestCase):
    def setUp(self):
        folder = Path(tempfile.mkdtemp(prefix="armor-remesh-"))
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        self.folder = folder
        self.project = folder / "node_enclosure_radar_2.3mf"
        shutil.copyfile(ROOT / "scad" / self.project.name, self.project)

    def export(self, scale: float, shift: float) -> Path:
        points, triangles = slicer_projects.project_mesh(self.project)
        body = "".join(f'<vertex x="{p[0] * scale + shift}" y="{p[1] * scale + shift}" z="{p[2] * scale + shift}"/>' for p in points)
        body += "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles)
        path = self.folder / "export.3mf"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("3D/3dmodel.model", f"<model><mesh>{body}</mesh></model>")
        return path

    def test_a_piece_with_the_same_envelope_goes_in_centred_and_the_settings_stay(self):
        with zipfile.ZipFile(self.project) as archive:
            settings = archive.read("Metadata/project_settings.config")
        before = slicer_projects.project_mesh(self.project)
        self.assertEqual(slicer_projects.remesh(self.project, self.export(1.0, 25.5)), len(before[1]))
        after = slicer_projects.project_mesh(self.project)
        self.assertEqual(after[1], before[1])
        for old, new in zip(before[0], after[0], strict=True):
            for a, b in zip(old, new, strict=True):
                self.assertAlmostEqual(a, b, places=5)
        with zipfile.ZipFile(self.project) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.read("Metadata/project_settings.config"), settings)

    def test_a_piece_of_another_size_is_refused_and_the_project_is_left_alone(self):
        before = self.project.read_bytes()
        with self.assertRaisesRegex(ValueError, "envelope"):
            slicer_projects.remesh(self.project, self.export(1.1, 0.0))
        self.assertEqual(self.project.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
