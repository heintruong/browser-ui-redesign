"""Catch release drift before an unchanged version leaves users on cached files."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        for name in (".agents", ".claude-plugin", ".codex-plugin", ".opencode", "skills"):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ("plugin.json", "CHANGELOG.md", "scripts/package.py"):
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)

    def run_package(self, *args, success=True):
        result = subprocess.run([sys.executable, str(self.root / "scripts/package.py"), *args],
                                capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)

    def test_release_updates_every_version_and_requires_changelog(self):
        self.run_package("version", "0.1.2")
        for name in ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            self.assertEqual(json.loads((self.root / name).read_text())["version"], "0.1.2")
        self.assertEqual(json.loads((self.root / ".claude-plugin/marketplace.json").read_text())["metadata"]["version"], "0.1.2")
        self.run_package("check", success=False)
        changelog = self.root / "CHANGELOG.md"
        changelog.write_text(changelog.read_text() + "\n## [0.1.2]\n\nTest release.\n")
        self.run_package("check")

    def test_adapter_drift_is_detected_and_sync_repairs_it(self):
        adapter = self.root / ".opencode/skills/browser-ui-redesign/SKILL.md"
        adapter.write_text("Stale adapter")
        self.run_package("check", success=False)
        self.run_package("sync")
        self.run_package("check")

    def test_version_drift_is_detected(self):
        path = self.root / ".codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "0.0.1"
        path.write_text(json.dumps(data))
        self.run_package("check", success=False)

    def test_invalid_version_does_not_change_files(self):
        before = (self.root / "plugin.json").read_bytes()
        self.run_package("version", "01.2.3", success=False)
        self.assertEqual((self.root / "plugin.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
