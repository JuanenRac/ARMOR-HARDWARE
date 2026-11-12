"""ARMOR-HARDWARE - the export of every piece as its own model file (tools/export_models.py), checked without OpenSCAD: which pieces there are, that each one names a switch its source
really has, how the command is built, and that the model files are made and not kept in the repository.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later."""
from __future__ import annotations

import io
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import export_models  # noqa: E402


class PieceTests(unittest.TestCase):
    def test_the_pieces_are_the_four_views_of_the_radar_and_a_box_and_a_lid_for_each_preset(self):
        names = [piece.name for piece in export_models.pieces()]
        self.assertEqual(len(names), len(set(names)), "a piece is listed twice")
        self.assertEqual(len(names), 4 + 2 * 3)
        for label in ("exploded", "assembled", "base", "cover"):
            self.assertIn(f"node_enclosure_radar_{label}", names)
        for preset in ("solar", "electrical", "alarm"):
            for part in ("box", "lid"):
                self.assertIn(f"node_box_{preset}_{part}", names)

    def test_every_piece_sets_a_switch_its_source_has_and_the_source_exists(self):
        for piece in export_models.pieces():
            source = (ROOT / "scad" / piece.source).read_text(encoding="utf-8")
            for name, _value in piece.defines:
                self.assertRegex(source, rf"(?m)^{name}\s*=", f"{piece.name}: {piece.source} has no {name}")

    def test_the_radar_views_are_the_ones_the_source_documents(self):
        source = (ROOT / "scad" / "node_enclosure_radar.scad").read_text(encoding="utf-8")
        for mode, _label in export_models.RADAR_VIEWS:
            self.assertRegex(source, rf"view_mode == {mode}\)")

    def test_the_box_pieces_match_what_the_build_of_the_project_renders(self):
        tool = (ROOT / "tools" / "armor_project_tool.py").read_text(encoding="utf-8")
        rendered = re.findall(r"for preset in \(([^)]*)\)", tool)[0].replace('"', "").replace(" ", "").split(",")
        self.assertEqual(set(rendered), set(export_models.PRESETS))


class CommandTests(unittest.TestCase):
    def test_the_command_sets_the_switches_names_the_file_and_ends_with_the_source(self):
        piece = next(p for p in export_models.pieces() if p.name == "node_box_alarm_lid")
        command = export_models.command(piece, "stl", Path("out"), "openscad")
        self.assertEqual(command[0], "openscad")
        self.assertIn('part="lid"', command)
        self.assertIn('preset="alarm"', command)
        self.assertEqual(command[command.index("-o") + 1], str(Path("out") / "node_box_alarm_lid.stl"))
        self.assertTrue(command[-1].endswith("node_box.scad"))

    def test_a_format_that_is_not_offered_is_refused(self):
        with self.assertRaises(ValueError):
            export_models.command(export_models.pieces()[0], "obj", Path("out"))

    def test_both_formats_are_made(self):
        self.assertEqual(set(export_models.FORMATS), {"stl", "3mf"})


class MainTests(unittest.TestCase):
    def run_main(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = export_models.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_list_prints_the_pieces_and_renders_nothing(self):
        with mock.patch.object(subprocess, "run") as run:
            code, out, _ = self.run_main(["--list"])
        self.assertEqual(code, 0)
        self.assertEqual(out.split(), [piece.name for piece in export_models.pieces()])
        run.assert_not_called()

    def test_an_unknown_piece_is_refused(self):
        code, _, err = self.run_main(["--piece", "nothing"])
        self.assertEqual(code, 2)
        self.assertIn("unknown piece", err)

    def test_without_openscad_it_says_so(self):
        with mock.patch.object(export_models.shutil, "which", return_value=None), tempfile.TemporaryDirectory() as folder:
            code, _, err = self.run_main(["--out", folder])
        self.assertEqual(code, 2)
        self.assertIn("OpenSCAD is required", err)

    def test_each_piece_and_format_is_one_run_and_a_failed_one_fails_the_export(self):
        def fake(command, **_kwargs):
            target = Path(command[command.index("-o") + 1])
            if "base" in target.name and target.suffix == ".3mf":
                return subprocess.CompletedProcess(command, 1, "", "ERROR: assert failed")
            target.write_bytes(b"model")
            return subprocess.CompletedProcess(command, 0, "", "")
        with mock.patch.object(export_models.shutil, "which", return_value="openscad"), mock.patch.object(subprocess, "run", side_effect=fake) as run, \
                tempfile.TemporaryDirectory() as folder:
            code, out, err = self.run_main(["--out", folder, "--piece", "node_enclosure_radar_base", "--piece", "node_box_solar_box"])
        self.assertEqual(run.call_count, 2 * 2)
        self.assertEqual(code, 1)
        self.assertIn("FAIL node_enclosure_radar_base.3mf", err)
        self.assertIn("EXPORT_MODELS=FAIL", out)

    def test_every_piece_exported_is_a_pass(self):
        def fake(command, **_kwargs):
            Path(command[command.index("-o") + 1]).write_bytes(b"model")
            return subprocess.CompletedProcess(command, 0, "", "")
        with mock.patch.object(export_models.shutil, "which", return_value="openscad"), mock.patch.object(subprocess, "run", side_effect=fake) as run, \
                tempfile.TemporaryDirectory() as folder:
            code, out, _ = self.run_main(["--out", folder])
        self.assertEqual(code, 0)
        self.assertEqual(run.call_count, len(export_models.pieces()) * len(export_models.FORMATS))
        self.assertIn("EXPORT_MODELS=PASS", out)


class NotKeptInTheRepositoryTests(unittest.TestCase):
    def is_tracked(self, name: str) -> bool:
        done = subprocess.run(["git", "ls-files", "--error-unmatch", name], cwd=ROOT, capture_output=True, check=False)
        return done.returncode == 0

    def test_the_model_files_that_are_made_from_the_sources_are_not_committed(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for name in ("scad/node_enclosure_radar.stl", "scad/node_enclosure_radar.amf", "scad/node_enclosure_radar.3mf"):
            self.assertIn(name, gitignore)
            self.assertFalse(self.is_tracked(name), f"{name} is committed")

    def test_a_workflow_exports_them_as_an_artifact(self):
        workflow = (ROOT / ".github" / "workflows" / "export-models.yml").read_text(encoding="utf-8")
        self.assertIn("tools/export_models.py --out build/models", workflow)
        self.assertIn("upload-artifact", workflow)
        self.assertRegex(workflow, r"(?m)^permissions:\s*\n\s+contents: read")


if __name__ == "__main__":
    unittest.main()
