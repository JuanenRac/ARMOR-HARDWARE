"""The command of the pin table (tools/pinout.py): its arguments, the files it writes and checks, and the message when the firmware tables are not next to the repository. The tables of
the firmware are replaced by a stand-in (the table itself is the work of test_pinout.py), so these tests need no other repository."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import pinout  # noqa: E402


def run(*arguments: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = pinout.main(list(arguments))
    return code, out.getvalue(), err.getvalue()


class PinoutCommandTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)

    def test_a_wrong_or_missing_argument_prints_the_help_and_exits_with_2(self):
        for arguments in ((), ("--nonsense",), ("--write", "--check")):
            code, out, _err = run(*arguments)
            self.assertEqual(code, 2, arguments)
            self.assertTrue(out.strip())

    def test_the_sources_say_where_to_check_out_the_firmware_tables_when_they_are_missing(self):
        with mock.patch.object(pinout, "CORE", self.folder):
            with self.assertRaises(FileNotFoundError) as caught:
                pinout.sources()
        self.assertIn("ARMOR_COMMON_DIR", str(caught.exception))

    def test_the_sources_are_read_when_both_files_are_there(self):
        (self.folder / "board_s3.hpp").write_text("board", encoding="utf-8")
        (self.folder / "base_board.hpp").write_text("base", encoding="utf-8")
        with mock.patch.object(pinout, "CORE", self.folder):
            self.assertEqual(pinout.sources(), ("board", "base"))

    def test_write_makes_the_document_and_check_passes_until_it_is_changed(self):
        document = self.folder / "PINOUT.md"
        with mock.patch.object(pinout, "DOC", document), mock.patch.object(pinout, "sources", return_value=("b", "a")), mock.patch.object(pinout, "render", return_value="# table\n"):
            code, out, _err = run("--write")
            self.assertEqual(code, 0)
            self.assertIn("wrote", out)
            self.assertEqual(document.read_text(encoding="utf-8"), "# table\n")
            code, out, _err = run("--check")
            self.assertEqual((code, out.strip()), (0, "PINOUT=PASS"))
            document.write_text("# an edit by hand\n", encoding="utf-8")
            code, _out, err = run("--check")
            self.assertEqual(code, 1)
            self.assertIn("run python tools/pinout.py --write", err)

    def test_check_with_line_endings_of_windows_still_passes_and_a_missing_document_fails(self):
        document = self.folder / "PINOUT.md"
        with mock.patch.object(pinout, "DOC", document), mock.patch.object(pinout, "sources", return_value=("b", "a")), mock.patch.object(pinout, "render", return_value="# table\nrow\n"):
            self.assertEqual(run("--check")[0], 1)   # there is no document yet
            document.write_bytes(b"# table\r\nrow\r\n")
            self.assertEqual(run("--check")[0], 0)


if __name__ == "__main__":
    unittest.main()
