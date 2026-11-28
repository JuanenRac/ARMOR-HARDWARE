#!/usr/bin/env python3
"""ARMOR-HARDWARE - the two slicer projects of the radar enclosure, tied to the OpenSCAD sources they were made from.

  python tools/slicer_projects.py                       fail when a source changed after the projects were last made
  python tools/slicer_projects.py --from build/models   put the meshes of a fresh export (tools/export_models.py) into the projects and record the sources

A slicer project is the file somebody sends to a printer, so it must not stay behind its source. scad/slicer_projects.json keeps, for each project, the piece it holds and the
SHA-256 of every source of that piece (line endings do not count). The settings, the plate and the position of the part are those saved in the slicer and are not touched; only
the triangles are replaced, and only when the new piece has the same envelope (a piece that grew must be placed again in the slicer by hand). Nothing here has been printed.

Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "scad" / "slicer_projects.json"
SOURCES = ("node_enclosure_radar.scad", "node_common.scad")
PROJECTS = {"node_enclosure_radar_1.3mf": "node_enclosure_radar_base", "node_enclosure_radar_2.3mf": "node_enclosure_radar_cover"}
VERTEX = re.compile(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"')
TRIANGLE = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"')
ENVELOPE_PLAY_MM = 0.02

Point = tuple[float, float, float]


def source_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def current_sources(root: Path = ROOT) -> dict[str, str]:
    return {name: source_digest(root / "scad" / name) for name in SOURCES}


def mesh_of(text: str) -> tuple[list[Point], list[tuple[int, int, int]]]:
    points = [(float(x), float(y), float(z)) for x, y, z in VERTEX.findall(text)]
    triangles = [(int(a), int(b), int(c)) for a, b, c in TRIANGLE.findall(text)]
    return points, triangles


def envelope(points: list[Point]) -> tuple[Point, Point]:
    low = (min(p[0] for p in points), min(p[1] for p in points), min(p[2] for p in points))
    high = (max(p[0] for p in points), max(p[1] for p in points), max(p[2] for p in points))
    return low, high


def object_member(archive: zipfile.ZipFile) -> str:
    return next(name for name in archive.namelist() if name.startswith("3D/Objects/"))


def project_mesh(path: Path) -> tuple[list[Point], list[tuple[int, int, int]]]:
    with zipfile.ZipFile(path) as archive:
        return mesh_of(archive.read(object_member(archive)).decode("utf-8"))


def stale(root: Path = ROOT, record: Path | None = None) -> list[str]:
    """Why a project no longer matches its sources; empty when everything does."""
    record = record or root / "scad" / "slicer_projects.json"
    if not record.is_file():
        return [f"{record.name} is missing"]
    kept = json.loads(record.read_text(encoding="utf-8")).get("projects", {})
    problems = []
    wanted = current_sources(root)
    for project, piece in PROJECTS.items():
        entry = kept.get(project)
        if not entry or entry.get("piece") != piece:
            problems.append(f"{project}: not recorded as {piece}")
            continue
        for name, digest in wanted.items():
            if entry.get("sources", {}).get(name) != digest:
                problems.append(f"{project}: {name} changed after the project was made; export the models and run tools/slicer_projects.py --from <folder>")
    return problems


def _number(value: float) -> str:
    text = f"{value:.7f}".rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def remesh(project: Path, export: Path) -> int:
    """Replaces the triangles of one project with those of an exported piece; the number of triangles."""
    with zipfile.ZipFile(export) as archive:
        points, triangles = mesh_of(archive.read("3D/3dmodel.model").decode("utf-8"))
    if not points or not triangles:
        raise ValueError(f"{export.name}: no mesh")
    low, high = envelope(points)
    centre = tuple((a + b) / 2 for a, b in zip(low, high, strict=True))
    moved = [(p[0] - centre[0], p[1] - centre[1], p[2] - centre[2]) for p in points]
    with zipfile.ZipFile(project) as archive:
        member = object_member(archive)
        old_text = archive.read(member).decode("utf-8")
        members = [(info, archive.read(info)) for info in archive.infolist()]
    old_low, old_high = envelope(mesh_of(old_text)[0])
    new_low, new_high = envelope(moved)
    if any(abs(a - b) > ENVELOPE_PLAY_MM for a, b in zip((*old_low, *old_high), (*new_low, *new_high), strict=True)):
        raise ValueError(f"{project.name}: the envelope of the piece changed; open the project in the slicer, place the new piece and save it")
    eol = "\r\n" if "\r\n" in old_text else "\n"
    lines = ["<mesh>", "    <vertices>"]
    lines += [f'     <vertex x="{_number(x)}" y="{_number(y)}" z="{_number(z)}"/>' for x, y, z in moved]
    lines += ["    </vertices>", "    <triangles>"]
    lines += [f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles]
    lines += ["    </triangles>", "   </mesh>"]
    start, end = old_text.index("<mesh>"), old_text.index("</mesh>") + len("</mesh>")
    new_text = old_text[:start] + eol.join(lines) + old_text[end:]
    with zipfile.ZipFile(project, "w", zipfile.ZIP_DEFLATED) as out:
        for info, data in members:
            if info.filename == member:
                data = new_text.encode("utf-8")
            elif info.filename == "Metadata/model_settings.config":
                data = re.sub(rb'face_count="\d+"', f'face_count="{len(triangles)}"'.encode(), data)
            elif info.filename == "3D/3dmodel.model":
                # the account number of whoever saved the project has no place in a public file
                data = re.sub(rb'(<metadata name="DesignerUserId">)[^<]*(</metadata>)', rb"\1\2", data)
            out.writestr(info, data)
    return len(triangles)


def write_record(root: Path = ROOT, record: Path | None = None) -> None:
    record = record or root / "scad" / "slicer_projects.json"
    sources = current_sources(root)
    body = {"format": 1, "note": "What each slicer project was made from; written by tools/slicer_projects.py. Nothing has been printed.",
            "projects": {project: {"piece": piece, "sources": sources} for project, piece in PROJECTS.items()}}
    record.write_bytes((json.dumps(body, indent=2) + "\n").encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--from", dest="exports", type=Path, help="folder of the exported models to put into the projects")
    options = parser.parse_args(argv)
    if options.exports is not None:
        for project, piece in PROJECTS.items():
            export = options.exports / f"{piece}.3mf"
            if not export.is_file():
                print(f"{export} is missing: run tools/export_models.py --out {options.exports}", file=sys.stderr)
                return 2
            try:
                count = remesh(ROOT / "scad" / project, export)
            except ValueError as problem:
                print(str(problem), file=sys.stderr)
                return 1
            print(f"{project}: {count} triangles from {piece}")
        write_record()
    problems = stale()
    for line in problems:
        print(line, file=sys.stderr)
    print(f"SLICER_PROJECTS={'FAIL' if problems else 'PASS'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
