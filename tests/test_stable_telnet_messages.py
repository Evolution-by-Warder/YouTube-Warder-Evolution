"""Verify next-stable YouTube Enigma2 opkg/Telnet hook messages."""
import subprocess
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "packaging" / "CONTROL"
BAR = "*" * 66

def output(name, event):
    return subprocess.run(["sh", str(SCRIPTS / name), event],
                          capture_output=True, text=True, check=True).stdout

class StableTelnetMessagesTests(unittest.TestCase):
    def test_all_hooks_are_valid_shell_with_radio_style_separator(self):
        for hook in ("preinst", "postinst", "prerm", "postrm"):
            with self.subTest(hook=hook):
                code = (SCRIPTS / hook).read_text()
                self.assertTrue(code.startswith("#!/bin/sh"))
                self.assertIn('echo "' + BAR + '"', code)
                subprocess.run(["sh", "-n", str(SCRIPTS / hook)], check=True)

    def test_install_and_upgrade_print_the_correct_status(self):
        for event, expected in (("install", "installation/reinstall"),
                                ("upgrade", "upgrade/reinstall")):
            msg = output("preinst", event)
            self.assertIn(expected, msg)
            self.assertIn("settings, favourites and history", msg)
            self.assertEqual(msg.splitlines()[0], BAR)
            self.assertEqual(msg.splitlines()[-1], BAR)

    def test_uninstall_messages_are_not_printed_on_upgrade(self):
        self.assertIn("Removing YouTube Warder Evolution", output("prerm", "remove"))
        self.assertIn("upgrade/reinstall", output("prerm", "upgrade"))
        self.assertNotIn("Removing", output("prerm", "upgrade"))
        self.assertEqual(output("postrm", "upgrade"), "")
        msg = output("postrm", "remove")
        self.assertIn("Removal finished: YouTube Warder Evolution", msg)
        self.assertIn("favourites and history were preserved", msg)
        self.assertIn("external components were left intact", msg)

    def test_postinst_still_runs_existing_component_check(self):
        code = (SCRIPTS / "postinst").read_text()
        self.assertIn('nohup /bin/sh "$WORKER" "$PPID"', code)
        self.assertIn("Install/upgrade/reinstall finished: YouTube Warder Evolution", code)
        self.assertIn("settings, favourites and history were preserved", code)
        self.assertIn("Please restart GUI to activate changes.", code)
        self.assertIn("/tmp/warder-youtube-deps.log", code)
        for dangerous in ("rm -rf", "opkg install", "opkg remove",
                          "killall", "reboot", "init 4"):
            self.assertNotIn(dangerous, code)

if __name__ == "__main__":
    unittest.main()
