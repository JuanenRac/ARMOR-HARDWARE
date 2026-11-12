#!/usr/bin/env python3
"""ARMOR-HARDWARE - the one table of the pins of the nodes, made from the tables the firmware itself is built with.

  python tools/pinout.py --write      write docs/PINOUT.md
  python tools/pinout.py --check      fail (exit 1) when docs/PINOUT.md is not what the firmware tables give

The firmware keeps its pins in two shared headers of ARMOR-COMMON (`firmware_base/core/board_s3.hpp`: which GPIO exists and what each one is, and the default pins of the ten serial
ports; `firmware_base/core/base_board.hpp`: the Zigbee radio, the relays and the analog inputs of the base board). This script reads them (it does not compile them) and writes the
table a person wiring a box reads, so the document can never disagree with the code. The ARMOR-COMMON checkout is looked for next to this repository, or at ARMOR_COMMON_DIR.
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARDS = ("s3-eth", "s3-wifi")
BOARD_NAMES = {"s3-eth": "Waveshare ESP32-S3-ETH", "s3-wifi": "ESP32-S3-WROOM-1 N16R8"}
CORE = Path(os.environ.get("ARMOR_COMMON_DIR", ROOT.parent / "ARMOR-COMMON")) / "firmware_base" / "core"
DOC = ROOT / "docs" / "PINOUT.md"
FIRST_GPIO, LAST_GPIO = 0, 48


def sections(text: str) -> tuple[list[str], list[str]]:
    """The lines of a text as the s3-eth build sees them and as the s3-wifi build sees them (`#if defined(ARMOR_BOARD_S3_ETH)` ... `#else` ... `#endif`, not nested)."""
    eth: list[str] = []
    wifi: list[str] = []
    state = "both"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#if defined(ARMOR_BOARD_S3_ETH)"):
            state = "eth"
        elif stripped.startswith("#else") and state == "eth":
            state = "wifi"
        elif stripped.startswith("#endif") and state in ("eth", "wifi"):
            state = "both"
        else:
            if state in ("both", "eth"):
                eth.append(line)
            if state in ("both", "wifi"):
                wifi.append(line)
    return eth, wifi


def condition(expression: str, gpio: int, has_ethernet: bool) -> bool:
    """A condition of board_s3.hpp (comparisons of `gpio` joined by && and ||) evaluated for one pin."""
    python = re.sub(r"!(?!=)", " not ", expression.replace("&&", " and ").replace("||", " or "))
    names = {"true": True, "false": False, "gpio": gpio, "kFirstGpio": FIRST_GPIO, "kLastGpio": LAST_GPIO, "kHasEthernet": has_ethernet}
    if re.search(r"[^\w\s<>=()+\-]", re.sub(r"\b(and|or|not)\b", "", python)):
        raise ValueError(f"cannot read the condition {expression!r}")
    return bool(eval(python, {"__builtins__": {}}, names))  # noqa: S307 - the text is a comparison of numbers read from our own header, checked above


PIN_RULE = re.compile(r'if \((?P<cond>[^\n]*?)\) return \{gpio, PinUse::(?P<use>\w+), Reserved::(?P<why>\w+), "(?P<note>[^"]*)", (?P<header>[^}]*)\};')


def classify(board_text: str) -> dict[str, dict[int, tuple[str, str, str, bool]]]:
    """For each board and each GPIO 0..48: (use, reason, note, on_header), by the first rule of pin_info that matches, as the firmware does."""
    start = board_text.index("constexpr PinInfo pin_info(int gpio) {")
    body = board_text[start:board_text.index("\n}\n", start)]
    result: dict[str, dict[int, tuple[str, str, str, bool]]] = {}
    for board, lines in zip(BOARDS, sections(body), strict=True):
        rules = [m for m in (PIN_RULE.search(line) for line in lines) if m]
        has_ethernet = board == "s3-eth"
        pins: dict[int, tuple[str, str, str, bool]] = {}
        for gpio in range(FIRST_GPIO, LAST_GPIO + 1):
            for rule in rules:
                if condition(rule["cond"], gpio, has_ethernet):
                    pins[gpio] = (rule["use"], rule["why"], rule["note"], condition(rule["header"], gpio, has_ethernet))
                    break
            else:
                pins[gpio] = ("kFree", "kNone", "", True)   # the last line of pin_info: everything else is free
        result[board] = pins
    return result


def default_ports(board_text: str) -> dict[str, list[tuple[int, int, int]]]:
    """(rx, tx, de) of the ten serial ports for each board; -1 is no direction pin."""
    start = board_text.index("constexpr std::array<DefaultPins, kPortCount> kDefaultPins")
    end = board_text.rindex("#endif", start)
    block = board_text[board_text.rindex("#if defined(ARMOR_BOARD_S3_ETH)", 0, start):end]
    result: dict[str, list[tuple[int, int, int]]] = {}
    for board, lines in zip(BOARDS, sections(block), strict=True):
        rows = [(int(m[1]), int(m[2]), int(m[3])) for m in (re.match(r"\s*\{(-?\d+),\s*(-?\d+),\s*(-?\d+)\},", line) for line in lines) if m]
        result[board] = rows
    return result


def base_board(base_text: str) -> dict[str, dict[str, list[int]]]:
    """The Zigbee radio (rx, tx, reset, bootloader), the eight relays and the eight analog inputs of the base board, for each board."""
    start = base_text.index("#if defined(ARMOR_BOARD_S3_ETH)")
    block = base_text[start:base_text.index("#endif", base_text.index("kAnalogPins", start))]
    result = {}
    for board, lines in zip(BOARDS, sections(block), strict=True):
        text = "\n".join(lines)
        entry = {}
        for name, key in (("kZigbeePins", "zigbee"), ("kRelayPins", "relays"), ("kAnalogPins", "analog")):
            found = re.search(rf"{name}\{{([^}}]*)\}}", text)
            if not found:
                raise ValueError(f"{name} is not in base_board.hpp for {board}")
            entry[key] = [int(v) for v in found.group(1).split(",")]
        result[board] = entry
    return result


USE_WORDS = {"kFree": "free", "kCaution": "care", "kReserved": "never"}
REASON_WORDS = {"kNoSuchPin": "does not exist", "kFlash": "external flash", "kPsram": "octal PSRAM", "kUsb": "native USB", "kEthernet": "W5500 Ethernet controller", "kCamera": "camera connector"}
NOTE_WORDS = {"boot": "BOOT button, read at reset", "strapping": "strapping pin, read at reset", "sdcard": "microSD socket (free when no card is used)",
              "rom_log": "UART0: the boot ROM prints at every reset", "usb_serial": "UART0 to the USB-serial socket", "led": "on-board RGB LED"}


def cell(info: tuple[str, str, str, bool]) -> str:
    use, why, note, on_header = info
    words = USE_WORDS[use]
    detail = REASON_WORDS.get(why, "") if use == "kReserved" else NOTE_WORDS.get(note, "")
    text = f"{words}: {detail}" if detail else words
    return text + ("" if on_header else " (not on the header)")


def pin_rows(classes: dict[str, dict[int, tuple[str, str, str, bool]]]) -> list[tuple[str, str, str]]:
    """Consecutive GPIO with the same text on both boards are one row: ("26-32", eth, wifi)."""
    rows: list[tuple[str, str, str]] = []
    run: list[int] = []

    def flush() -> None:
        if run:
            label = str(run[0]) if len(run) == 1 else f"{run[0]}-{run[-1]}"
            rows.append((label, cell(classes["s3-eth"][run[0]]), cell(classes["s3-wifi"][run[0]])))

    for gpio in range(FIRST_GPIO, LAST_GPIO + 1):
        if run and (cell(classes["s3-eth"][gpio]), cell(classes["s3-wifi"][gpio])) != (cell(classes["s3-eth"][run[0]]), cell(classes["s3-wifi"][run[0]])):
            flush()
            run = []
        run.append(gpio)
    flush()
    return rows


def render(board_text: str, base_text: str) -> str:
    classes = classify(board_text)
    ports = default_ports(board_text)
    base = base_board(base_text)
    out = [
        "# The pins of the nodes",
        "",
        "One table for the box and the wiring, made by `tools/pinout.py` from the tables the firmware is built with (`firmware_base/core/board_s3.hpp` and `base_board.hpp` of ARMOR-COMMON);",
        "the test `tests/test_pinout.py` fails when this file is not what those tables give, so it cannot drift. Every pin is a setting in the panel of the node: these are where a node that",
        "was never configured looks first. Nothing here has been checked on a board; the sizes and positions of the connectors are in `DESIGN_INPUTS.md`.",
        "",
        "The two boards are the Waveshare ESP32-S3-ETH (`s3-eth`: Ethernet on a W5500, a microSD socket and a camera connector) and an ESP32-S3-WROOM-1 N16R8 development board",
        "(`s3-wifi`: Wi-Fi only). `free` is a pin a port may use, `care` a pin that works but has a second role, `never` a pin the firmware does not offer.",
        "",
        "## The pins of the module",
        "",
        "| GPIO | s3-eth | s3-wifi |",
        "| --- | --- | --- |",
    ]
    out += [f"| {label} | {eth} | {wifi} |" for label, eth, wifi in pin_rows(classes)]
    out += ["", "## The ten serial ports (rx / tx / direction)", "", "A direction pin of `-` means the port has none (a plain UART, or a transceiver that switches by itself).", "", "| Port | s3-eth | s3-wifi |", "| --- | --- | --- |"]
    for index in range(len(ports["s3-eth"])):
        def text(board: str, index: int = index) -> str:
            rx, tx, de = ports[board][index]
            return f"{rx} / {tx} / {de if de >= 0 else '-'}"
        out.append(f"| {index + 1} | {text('s3-eth')} | {text('s3-wifi')} |")
    out += ["", "## The base board (electrical and alarm nodes)", "", "`-` is no pin until one is chosen in the panel.", "", "| Item | s3-eth | s3-wifi |", "| --- | --- | --- |"]

    def pins(values: list[int]) -> str:
        return ", ".join(str(v) if v >= 0 else "-" for v in values)
    out.append(f"| Zigbee radio: rx, tx, reset, bootloader | {pins(base['s3-eth']['zigbee'])} | {pins(base['s3-wifi']['zigbee'])} |")
    for position in range(len(base["s3-eth"]["relays"])):
        out.append(f"| Relay {position + 1} | {base['s3-eth']['relays'][position]} | {base['s3-wifi']['relays'][position]} |")
    for position in range(len(base["s3-eth"]["analog"])):
        out.append(f"| Analog input {position + 1} (ADC1) | {pins([base['s3-eth']['analog'][position]])} | {pins([base['s3-wifi']['analog'][position]])} |")
    out.append("")
    return "\n".join(out)


def sources() -> tuple[str, str]:
    board, base = CORE / "board_s3.hpp", CORE / "base_board.hpp"
    for path in (board, base):
        if not path.is_file():
            raise FileNotFoundError(f"{path} not found: check out ARMOR-COMMON next to this repository or set ARMOR_COMMON_DIR")
    return board.read_text(encoding="utf-8"), base.read_text(encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in ("--write", "--check"):
        print(__doc__)
        return 2
    text = render(*sources())
    if argv[0] == "--write":
        DOC.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {DOC}")
        return 0
    current = DOC.read_text(encoding="utf-8").replace("\r\n", "\n") if DOC.is_file() else ""
    if current != text:
        print("docs/PINOUT.md is not what the firmware tables give: run python tools/pinout.py --write", file=sys.stderr)
        return 1
    print("PINOUT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
