#!/usr/bin/env python3
"""ARMOR-HARDWARE - the measurement record template: one line per row of the bench acceptance matrix.

Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.

    python tools/make_measurement_template.py            # write docs/measurement_record_template.csv
    python tools/make_measurement_template.py --check    # fail when the file is out of date with docs/BENCH_ACCEPTANCE.md

A row of the matrix turns to *passed* only with a dated measurement record (instrument, method, value, photo or log). The template has one line per row of the matrix (section, item and the
pass criterion copied from it) and empty columns for the record; the photos and logs go in a folder next to the filled copy, named in the `evidence` column. Filling a copy never changes
the matrix: the status of a row is changed by hand in the matrix, with the record at hand.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "BENCH_ACCEPTANCE.md"
TEMPLATE = ROOT / "docs" / "measurement_record_template.csv"
COLUMNS = ("section", "item", "pass_criterion", "date", "operator", "instrument", "method", "value", "unit", "result", "evidence")
HEADER = re.compile(r"^\|\s*Item\s*\|")


def rows(text: str) -> list[tuple[str, str, str]]:
    """(section, item, pass criterion) of every row of the tables that have an Item column and a Pass criterion column."""
    found: list[tuple[str, str, str]] = []
    section = ""
    columns: list[str] = []
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("## "):
            section = line[3:].strip()
            columns = []
        elif HEADER.match(line):
            columns = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
        elif columns and line.startswith("|") and not re.match(r"^\|[\s:|-]+$", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if "pass criterion" in columns and len(cells) == len(columns):
                found.append((section, cells[0], cells[columns.index("pass criterion")]))
        elif not line.startswith("|"):
            columns = columns if not line.strip() else []
    return found


def render(text: str) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(COLUMNS)
    for section, item, criterion in rows(text):
        writer.writerow([section, item, criterion] + [""] * (len(COLUMNS) - 3))
    return out.getvalue()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the measurement record template from the bench acceptance matrix.")
    parser.add_argument("--check", action="store_true", help="fail when the template is out of date")
    args = parser.parse_args(argv)
    wanted = render(MATRIX.read_text(encoding="utf-8"))
    if args.check:
        found = TEMPLATE.read_bytes().decode("utf-8").replace("\r\n", "\n") if TEMPLATE.is_file() else ""
        if found != wanted:
            print(f"{TEMPLATE.name} is out of date: run python tools/make_measurement_template.py", file=sys.stderr)
            return 1
        print("MEASUREMENT_TEMPLATE=PASS")
        return 0
    TEMPLATE.write_bytes(wanted.encode("utf-8"))
    print(f"wrote {TEMPLATE.name} ({len(rows(MATRIX.read_text(encoding='utf-8')))} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
