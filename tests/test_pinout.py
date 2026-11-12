"""ARMOR-HARDWARE - the table of the pins (docs/PINOUT.md) against the tables the firmware is built with: the document is made from the shared headers of ARMOR-COMMON and
this test fails when it is not what they give, and checks the rules the table must keep (nothing offered twice on a board, nothing reserved used as a default).
Copyright (C) 2026 JuanenRac (Electro Hobby 3D). GPL-3.0-or-later."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import pinout  # noqa: E402

CORE = pinout.CORE
HAVE = (CORE / "board_s3.hpp").is_file() and (CORE / "base_board.hpp").is_file()
REQUIRED = bool(os.environ.get("ARMOR_REQUIRE_SIBLINGS"))


def sources() -> tuple[str, str]:
    if not HAVE:
        if REQUIRED:
            raise AssertionError(f"ARMOR-COMMON is not next to this repository ({CORE})")
        raise unittest.SkipTest("ARMOR-COMMON is not next to this repository")
    return pinout.sources()


class SectionsTests(unittest.TestCase):
    def test_a_conditional_block_is_read_for_each_board(self):
        eth, wifi = pinout.sections("a\n#if defined(ARMOR_BOARD_S3_ETH)\nb\n#else\nc\n#endif\nd")
        self.assertEqual(eth, ["a", "b", "d"])
        self.assertEqual(wifi, ["a", "c", "d"])

    def test_conditions_are_evaluated_and_nothing_else_is_run(self):
        self.assertTrue(pinout.condition("gpio >= 26 && gpio <= 32", 30, True))
        self.assertFalse(pinout.condition("gpio >= 26 && gpio <= 32", 33, True))
        self.assertTrue(pinout.condition("gpio >= 35 && !kHasEthernet", 36, False))
        self.assertFalse(pinout.condition("gpio >= 35 && !kHasEthernet", 36, True))
        self.assertTrue(pinout.condition("gpio == 19 || gpio == 20", 20, False))
        for hostile in ("__import__('os').system('x')", "gpio; 1", "open('f')"):
            with self.assertRaises((ValueError, SyntaxError, NameError, TypeError)):
                pinout.condition(hostile, 1, True)

    def test_a_pin_rule_is_read_from_a_line_of_the_firmware(self):
        line = '  if (gpio >= 33 && gpio <= 37) return {gpio, PinUse::kReserved, Reserved::kPsram, "", gpio >= 35 && !kHasEthernet};'
        found = pinout.PIN_RULE.search(line)
        self.assertEqual((found["use"], found["why"], found["note"]), ("kReserved", "kPsram", ""))


class TableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board, cls.base = sources()
        cls.classes = pinout.classify(cls.board)
        cls.ports = pinout.default_ports(cls.board)
        cls.base_pins = pinout.base_board(cls.base)

    def test_the_document_is_what_the_firmware_tables_give(self):
        written = pinout.DOC.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(written, pinout.render(self.board, self.base), "run python tools/pinout.py --write")

    def test_every_gpio_is_classified_on_both_boards(self):
        for board in pinout.BOARDS:
            self.assertEqual(sorted(self.classes[board]), list(range(pinout.FIRST_GPIO, pinout.LAST_GPIO + 1)), board)

    def test_the_pins_the_chip_keeps_are_never_offered(self):
        for board in pinout.BOARDS:
            for gpio in (*range(22, 38), 19, 20):
                self.assertEqual(self.classes[board][gpio][0], "kReserved", (board, gpio))

    def test_the_ethernet_controller_and_the_camera_take_their_pins_only_on_the_ethernet_board(self):
        for gpio in range(8, 15):
            self.assertEqual(self.classes["s3-eth"][gpio][0], "kReserved", gpio)
            self.assertNotEqual(self.classes["s3-wifi"][gpio][0], "kReserved", gpio)

    def test_ten_ports_on_each_board_and_none_on_a_reserved_pin(self):
        for board in pinout.BOARDS:
            self.assertEqual(len(self.ports[board]), 10, board)
            for rx, tx, de in self.ports[board]:
                for gpio in (rx, tx, de):
                    if gpio >= 0:
                        self.assertNotEqual(self.classes[board][gpio][0], "kReserved", (board, gpio))

    def test_no_pin_is_the_default_of_two_ports(self):
        for board in pinout.BOARDS:
            used: dict[int, str] = {}
            for index, (rx, tx, de) in enumerate(self.ports[board], 1):
                for gpio in (rx, tx, de):
                    if gpio >= 0:
                        self.assertNotIn(gpio, used, f"{board}: GPIO {gpio} is the default of port {index} and of {used.get(gpio)}")
                        used[gpio] = f"port {index}"

    def test_the_base_board_uses_pins_that_exist_and_the_analog_ones_can_be_read(self):
        for board in pinout.BOARDS:
            entry = self.base_pins[board]
            self.assertEqual((len(entry["zigbee"]), len(entry["relays"]), len(entry["analog"])), (4, 8, 8), board)
            for gpio in (*entry["zigbee"], *entry["relays"]):
                self.assertNotEqual(self.classes[board][gpio][0], "kReserved", (board, gpio))
            for gpio in entry["analog"]:
                if gpio >= 0:
                    self.assertTrue(1 <= gpio <= 10, f"{board}: analog GPIO {gpio} is not an ADC1 pin")
                    self.assertNotEqual(self.classes[board][gpio][0], "kReserved", (board, gpio))
            self.assertEqual(len(set(entry["relays"])), 8, f"{board}: a relay pin is used twice")

    def test_the_document_has_the_sections_a_person_looks_for(self):
        text = pinout.DOC.read_text(encoding="utf-8")
        for heading in ("## The pins of the module", "## The ten serial ports", "## The base board"):
            self.assertIn(heading, text)
        for board in pinout.BOARDS:
            self.assertIn(board, text)


if __name__ == "__main__":
    unittest.main()
