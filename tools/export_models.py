#!/usr/bin/env python3
"""ARMOR-HARDWARE - export every piece of the enclosures as its own model file (STL and 3MF), one OpenSCAD run per piece and format.

  python tools/export_models.py --list                 print the pieces, one per line, and render nothing
  python tools/export_models.py --out build/models     render all of them into that folder (needs OpenSCAD)
  python tools/export_models.py --out build/models --piece node_box_solar_lid

The model files are not kept in the repository: they are made from the sources by this script (the workflow `export-models.yml` runs it and keeps the folder as an artifact), so
a model can never disagree with the source it came from. An assert of a source (a board that does not fit, a cable hole in a wall) fails the piece it belongs to.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATS = ("stl", "3mf")
PRESETS = ("solar", "electrical", "alarm")
BOX_PARTS = ("box", "lid")
RADAR_VIEWS = ((0, "exploded"), (1, "assembled"), (2, "base"), (3, "cover"))


@dataclass(frozen=True)
class Piece:
    name: str
    source: str
    defines: tuple[tuple[str, str], ...]


def pieces() -> list[Piece]:
    """Every piece the sources offer: the four views of the radar enclosure, and the box and the lid of each preset of the box."""
    found = [Piece(f"node_enclosure_radar_{label}", "node_enclosure_radar.scad", (("view_mode", str(mode)),)) for mode, label in RADAR_VIEWS]
    for preset in PRESETS:
        for part in BOX_PARTS:
            found.append(Piece(f"node_box_{preset}_{part}", "node_box.scad", (("part", f'"{part}"'), ("preset", f'"{preset}"'))))
    return found


def command(piece: Piece, fmt: str, out_dir: Path, openscad: str = "openscad") -> list[str]:
    """The command line that renders one piece in one format."""
    if fmt not in FORMATS:
        raise ValueError(f"format {fmt!r} is not one of {FORMATS}")
    arguments = [openscad]
    for name, value in piece.defines:
        arguments += ["-D", f"{name}={value}"]
    arguments += ["-o", str(out_dir / f"{piece.name}.{fmt}"), str(ROOT / "scad" / piece.source)]
    return arguments


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="print the pieces and render nothing")
    parser.add_argument("--out", type=Path, help="the folder the model files are written to")
    parser.add_argument("--piece", action="append", help="only this piece (may be repeated)")
    options = parser.parse_args(argv)
    chosen = [piece for piece in pieces() if not options.piece or piece.name in options.piece]
    unknown = set(options.piece or ()) - {piece.name for piece in pieces()}
    if unknown:
        print(f"unknown piece: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    if options.list or options.out is None:
        for piece in chosen:
            print(piece.name)
        return 0
    openscad = shutil.which("openscad")
    if openscad is None:
        print("OpenSCAD is required to export the models", file=sys.stderr)
        return 2
    options.out.mkdir(parents=True, exist_ok=True)
    failed = 0
    for piece in chosen:
        for fmt in FORMATS:
            done = subprocess.run(command(piece, fmt, options.out, openscad), capture_output=True, text=True, check=False, timeout=600)
            target = options.out / f"{piece.name}.{fmt}"
            if done.returncode != 0 or not target.is_file() or target.stat().st_size == 0:
                failed += 1
                print(f"FAIL {piece.name}.{fmt}: {done.stderr.strip()[-300:]}", file=sys.stderr)
            else:
                print(f"ok {piece.name}.{fmt} ({target.stat().st_size} bytes)")
    print(f"EXPORT_MODELS={'FAIL' if failed else 'PASS'} {len(chosen)} pieces, {len(FORMATS)} formats, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
