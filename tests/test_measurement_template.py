"""The measurement record template has a line for every row of the bench acceptance matrix, and is the file the generator writes."""
from __future__ import annotations

import csv
import importlib.util
import io
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("make_measurement_template", ROOT / "tools" / "make_measurement_template.py")
tool = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(tool)  # type: ignore[union-attr]

SAMPLE = """# Matrix

## Radio

| Item | Requirement | How to verify | Pass criterion | Status |
|---|---|---|---|---|
| Cover | r | v | Within 20 % | not tested |

## Compatibility table (fill in per camera)

| Camera | Stream |
|---|---|
| X | y |

## Power

| Item | Requirement | How to verify | Pass criterion | Status |
|---|---|---|---|---|
| Supply | r | v | Stays above 4.5 V | not tested |
"""


class TemplateTests(unittest.TestCase):
    def test_every_row_of_a_table_with_a_pass_criterion_has_a_line_and_other_tables_have_none(self):
        self.assertEqual(tool.rows(SAMPLE), [("Radio", "Cover", "Within 20 %"), ("Power", "Supply", "Stays above 4.5 V")])

    def test_the_template_is_a_csv_with_the_columns_and_empty_record_fields(self):
        lines = list(csv.reader(io.StringIO(tool.render(SAMPLE))))
        self.assertEqual(tuple(lines[0]), tool.COLUMNS)
        self.assertEqual(lines[1][:3], ["Radio", "Cover", "Within 20 %"])
        self.assertEqual(set(lines[1][3:]), {""})

    def test_the_committed_template_is_what_the_matrix_gives(self):
        self.assertEqual((ROOT / "docs" / "measurement_record_template.csv").read_bytes().decode("utf-8").replace("\r\n", "\n"), tool.render(tool.MATRIX.read_text(encoding="utf-8")))
        self.assertEqual(tool.main(["--check"]), 0)

    def test_the_real_matrix_has_rows(self):
        self.assertGreaterEqual(len(tool.rows(tool.MATRIX.read_text(encoding="utf-8"))), 20)


if __name__ == "__main__":
    unittest.main()
