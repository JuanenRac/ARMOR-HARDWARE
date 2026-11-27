#!/usr/bin/env python3
"""ARMOR-HARDWARE - checks of a filled measurement record and of the matrix it feeds.

  python tools/check_measurement_record.py RECORD.csv      check one filled copy of docs/measurement_record_template.csv
  python tools/check_measurement_record.py --matrix        every row of docs/BENCH_ACCEPTANCE.md that is not "not tested" needs a record under docs/records/

A line with a result is a record only with a date, an instrument, a value, a unit and a piece of evidence that exists next to the file (docs/MEASUREMENT_RECORD.md). A line
without a result is a line not measured yet. Nothing has been measured today.

Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_measurement_template import COLUMNS, HEADER, rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ("passed", "failed", "not applicable")
NEEDED = ("date", "instrument", "value", "unit", "evidence")
NOT_TESTED = "not tested"


def read_record(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            return [], [f"{path.name}: the columns {', '.join(missing)} are missing"]
        return [{key: (value or "").strip() for key, value in row.items() if key in COLUMNS} for row in reader], []


def record_problems(path: Path) -> list[str]:
    lines, problems = read_record(path)
    for number, line in enumerate(lines, start=2):
        result = line["result"].lower()
        if not result:
            continue
        where = f"{path.name} line {number} ({line['item'] or 'no item'})"
        if result not in RESULTS:
            problems.append(f"{where}: result must be one of {', '.join(RESULTS)}")
        empty = [column for column in NEEDED if not line[column]]
        if empty:
            problems.append(f"{where}: a result needs {', '.join(empty)}")
        if line["date"]:
            try:
                datetime.date.fromisoformat(line["date"])
            except ValueError:
                problems.append(f"{where}: the date must be written YYYY-MM-DD")
        evidence = line["evidence"]
        if evidence:
            target = (path.parent / evidence).resolve()
            if not target.is_relative_to(path.parent.resolve()) or not target.is_file():
                problems.append(f"{where}: the evidence {evidence} is not a file next to the record")
    return problems


def matrix_statuses(text: str) -> list[tuple[str, str, str]]:
    """(section, item, status) of every row of the matrix that has a Status column (and of the table of cameras, whose column is Result)."""
    found: list[tuple[str, str, str]] = []
    section = ""
    columns: list[str] = []
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("## "):
            section, columns = line[3:].strip(), []
        elif HEADER.match(line):
            columns = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
        elif columns and line.startswith("|") and not re.match(r"^\|[\s:|-]+$", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if "status" in columns and len(cells) == len(columns):
                found.append((section, cells[0], cells[columns.index("status")].strip("* ").lower()))
        elif not line.strip():
            columns = []
    return found


def matrix_problems(root: Path = ROOT) -> list[str]:
    text = (root / "docs" / "BENCH_ACCEPTANCE.md").read_text(encoding="utf-8")
    known = {(section, item) for section, item, _criterion in rows(text)}
    records = sorted((root / "docs" / "records").rglob("*.csv"))
    problems: list[str] = []
    recorded: set[tuple[str, str, str]] = set()
    for path in records:
        found = record_problems(path)
        problems += found
        if not found:
            for line in read_record(path)[0]:
                key = (line["section"], line["item"])
                if line["result"] and key not in known:
                    problems.append(f"{path.name}: {line['item']} is not a row of the matrix")
                elif line["result"]:
                    recorded.add((*key, line["result"].lower()))
    for section, item, status in matrix_statuses(text):
        if status != NOT_TESTED and (section, item, status) not in recorded:
            problems.append(f"the matrix says {item} is {status}, and no record under docs/records says so")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a filled measurement record, or the matrix against the records.")
    parser.add_argument("record", nargs="?", type=Path, help="a filled copy of docs/measurement_record_template.csv")
    parser.add_argument("--matrix", action="store_true", help="check docs/BENCH_ACCEPTANCE.md against docs/records/")
    options = parser.parse_args(argv)
    if (options.record is None) == (not options.matrix):
        parser.error("give a record file or --matrix, one of the two")
    if options.matrix:
        problems = matrix_problems()
    elif options.record.is_file():
        problems = record_problems(options.record)
    else:
        problems = [f"{options.record} does not exist"]
    for problem in problems:
        print(problem, file=sys.stderr)
    print(f"MEASUREMENT_RECORD={'FAIL' if problems else 'PASS'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
