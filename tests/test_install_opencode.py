"""Exercise install/update behavior against isolated config directories."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/install-opencode.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.target = Path(self.workspace.name) / "project with spaces" / ".opencode"

    def run_installer(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), "--target", str(self.target), *args],
                                capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_preview_and_check_do_not_create_target(self):
        self.run_installer("--dry-run")
        self.run_installer("--check", success=False)
        self.assertFalse(self.target.exists())

    def test_install_and_repeat_preserve_unrelated_files(self):
        self.target.mkdir(parents=True)
        unrelated = self.target / "opencode.json"
        unrelated.write_text('{"theme":"system"}')
        self.run_installer()
        self.run_installer("--check")
        self.run_installer()
        self.assertEqual(unrelated.read_text(), '{"theme":"system"}')
        self.assertFalse((self.target / ".browser-ui-redesign-backups").exists())
        self.assertEqual((self.target / "skills/browser-ui-redesign/SKILL.md").read_bytes(),
                         (ROOT / "skills/browser-ui-redesign/SKILL.md").read_bytes())

    def test_update_backs_up_old_or_customized_content(self):
        self.run_installer()
        skill = self.target / "skills/browser-ui-redesign/SKILL.md"
        skill.write_text("Previous customized skill")
        self.run_installer("--check", success=False)
        self.run_installer()
        backups = list((self.target / ".browser-ui-redesign-backups").glob("*/skills/browser-ui-redesign/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "Previous customized skill")
        self.run_installer("--check")

    def test_symlink_is_rejected_without_touching_destination(self):
        outside = Path(self.workspace.name) / "outside"
        outside.mkdir()
        self.target.mkdir(parents=True)
        (self.target / "skills").symlink_to(outside, target_is_directory=True)
        self.run_installer(success=False)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.target / "commands").exists())

    def test_invalid_second_destination_does_not_partially_install(self):
        blocked = self.target / "commands/browser-ui-redesign.md"
        blocked.mkdir(parents=True)
        self.run_installer(success=False)
        self.assertFalse((self.target / "skills").exists())


if __name__ == "__main__":
    unittest.main()
