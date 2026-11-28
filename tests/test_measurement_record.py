"""ARMOR-HARDWARE - a filled measurement record and the matrix are checked before any real measurement exists.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.

The records written here are made up to try the rules; they are not measurements.
"""
from __future__ import annotations

import contextlib
import csv
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_measurement_record as check  # noqa: E402
from make_measurement_template import COLUMNS, rows  # noqa: E402

MATRIX = (ROOT / "docs" / "BENCH_ACCEPTANCE.md").read_text(encoding="utf-8")
SECTION, ITEM, CRITERION = rows(MATRIX)[0]


def line(**changes: str) -> dict[str, str]:
    base = {column: "" for column in COLUMNS}
    base.update(section=SECTION, item=ITEM, pass_criterion=CRITERION, date="2000-01-02", operator="nobody", instrument="made-up meter", method="made up", value="1", unit="m",
                result="passed", evidence="evidence/photo.txt")
    base.update(changes)
    return base


class Folder(unittest.TestCase):
    def setUp(self):
        folder = Path(tempfile.mkdtemp(prefix="armor-record-"))
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        (folder / "docs" / "records" / "evidence").mkdir(parents=True)
        (folder / "docs" / "records" / "evidence" / "photo.txt").write_text("made up", encoding="utf-8")
        shutil.copyfile(ROOT / "docs" / "BENCH_ACCEPTANCE.md", folder / "docs" / "BENCH_ACCEPTANCE.md")
        self.root = folder

    def write(self, *lines: dict[str, str]) -> Path:
        path = self.root / "docs" / "records" / "record.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(lines)
        return path


class RecordTests(Folder):
    def test_a_complete_line_and_a_line_not_measured_are_accepted(self):
        self.assertEqual(check.record_problems(self.write(line(), line(result="", date="", instrument="", value="", unit="", evidence=""))), [])

    def test_the_template_as_generated_is_accepted(self):
        self.assertEqual(check.record_problems(ROOT / "docs" / "measurement_record_template.csv"), [])

    def test_a_result_without_instrument_value_or_unit_is_refused(self):
        problems = check.record_problems(self.write(line(instrument="", value="", unit="")))
        self.assertEqual(len(problems), 1)
        self.assertIn("instrument, value, unit", problems[0])

    def test_evidence_that_is_not_a_file_next_to_the_record_is_refused(self):
        for evidence in ("evidence/missing.jpg", "../BENCH_ACCEPTANCE.md", "evidence"):
            self.assertIn("is not a file next to the record", " ".join(check.record_problems(self.write(line(evidence=evidence)))), evidence)

    def test_an_unknown_result_and_a_date_written_another_way_are_refused(self):
        problems = " ".join(check.record_problems(self.write(line(result="ok", date="02/01/2000"))))
        self.assertIn("result must be one of", problems)
        self.assertIn("YYYY-MM-DD", problems)

    def test_a_file_without_the_columns_of_the_template_is_refused(self):
        path = self.root / "docs" / "records" / "bad.csv"
        path.write_text("item,result\nx,passed\n", encoding="utf-8")
        self.assertIn("are missing", check.record_problems(path)[0])


class MatrixTests(Folder):
    def mark(self, status: str) -> None:
        path = self.root / "docs" / "BENCH_ACCEPTANCE.md"
        text = path.read_text(encoding="utf-8")
        start = text.index(f"| {ITEM} |")
        end = text.index("\n", start)
        path.write_text(text[:start] + text[start:end].replace("| not tested |", f"| {status} |") + text[end:], encoding="utf-8")

    def test_the_matrix_of_the_repository_rests_on_its_records(self):
        self.assertEqual(check.matrix_problems(), [])
        self.assertTrue(check.matrix_statuses(MATRIX))

    def test_a_row_marked_without_a_record_is_refused(self):
        self.mark("passed")
        problems = check.matrix_problems(self.root)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("no record under docs/records", problems[0])

    def test_the_record_of_the_row_with_the_same_result_makes_it_good(self):
        self.mark("passed")
        self.write(line())
        self.assertEqual(check.matrix_problems(self.root), [])
        self.write(line(result="failed"))
        self.assertEqual(len(check.matrix_problems(self.root)), 1)

    def test_a_record_of_a_row_that_is_not_in_the_matrix_is_said(self):
        self.write(line(item="Something else"))
        self.assertIn("is not a row of the matrix", check.matrix_problems(self.root)[0])


class CommandTests(Folder):
    def run_main(self, arguments):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            return check.main(arguments), out.getvalue()

    def test_the_command_says_pass_or_fail(self):
        self.assertEqual(self.run_main(["--matrix"]), (0, "MEASUREMENT_RECORD=PASS\n"))
        self.assertEqual(self.run_main([str(self.write(line()))])[0], 0)
        self.assertEqual(self.run_main([str(self.write(line(unit="")))])[0], 1)
        self.assertEqual(self.run_main([str(self.root / "nothing.csv")])[0], 1)

    def test_it_wants_a_file_or_the_matrix(self):
        for arguments in ([], ["x.csv", "--matrix"]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                check.main(arguments)


if __name__ == "__main__":
    unittest.main()
