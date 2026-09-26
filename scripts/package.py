#!/usr/bin/env python3
"""Check release consistency, sync the adapter, or set a release version (stdlib)."""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json")
MARKETPLACES = (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json")
SKILL = Path("skills/browser-ui-redesign/SKILL.md")
ADAPTER = Path(".opencode/skills/browser-ui-redesign/SKILL.md")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def sync():
    (ROOT / ADAPTER).write_bytes((ROOT / SKILL).read_bytes())


def set_version(version):
    if not VERSION.fullmatch(version):
        raise ValueError("Use a stable semantic version, for example 0.1.2")
    for name in MANIFESTS:
        path = ROOT / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = version
        write_json(path, data)
    path = ROOT / MARKETPLACES[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    data["metadata"]["version"] = version
    write_json(path, data)
    path = ROOT / SKILL
    source = path.read_text(encoding="utf-8")
    source, count = re.subn(r'^  version: "[^"]+"$', f'  version: "{version}"', source, count=1, flags=re.M)
    if count != 1:
        raise ValueError("Missing skill metadata.version")
    path.write_text(source, encoding="utf-8")
    sync()


def check():
    manifests = [json.loads((ROOT / name).read_text(encoding="utf-8")) for name in MANIFESTS]
    version = manifests[0]["version"]
    if not VERSION.fullmatch(version):
        raise ValueError("Release version must be stable semver")
    for name, data in zip(MANIFESTS, manifests):
        if data.get("name") != "browser-ui-redesign" or data.get("version") != version:
            raise ValueError(f"Inconsistent name/version: {name}")
    for name in MARKETPLACES:
        data = json.loads((ROOT / name).read_text(encoding="utf-8"))
        if data.get("name") != "browser-ui-redesign-marketplace":
            raise ValueError(f"Unexpected marketplace name: {name}")
        entry = data["plugins"][0]
        expected_source = "." if name == MARKETPLACES[0] else {"source": "local", "path": "./"}
        if len(data["plugins"]) != 1 or entry["name"] != "browser-ui-redesign" or entry["source"] != expected_source:
            raise ValueError(f"Unexpected plugin source: {name}")
        if name == MARKETPLACES[0] and data["metadata"]["version"] != version:
            raise ValueError("Marketplace version differs from plugin version")
    source = (ROOT / SKILL).read_text(encoding="utf-8")
    if not source.startswith("---\nname: browser-ui-redesign\n"):
        raise ValueError("Skill name must match its directory")
    if f'  version: "{version}"' not in source.split("---", 2)[1]:
        raise ValueError("Skill metadata.version differs from plugin version")
    if (ROOT / SKILL).read_bytes() != (ROOT / ADAPTER).read_bytes():
        raise ValueError("OpenCode adapter differs; run python3 scripts/package.py sync")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        raise ValueError(f"Missing changelog entry for {version}")
    print(f"Package {version}: manifests, marketplace sources, skill name, adapter, and changelog OK")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Validate release consistency without third-party dependencies")
    commands.add_parser("sync", help="Copy the canonical skill to the OpenCode adapter")
    commands.add_parser("version", help="Update all release version fields and sync the adapter").add_argument("version")
    args = parser.parse_args()
    try:
        if args.command == "version":
            set_version(args.version)
        elif args.command == "sync":
            sync()
        else:
            check()
    except (ValueError, KeyError, IndexError, OSError) as error:
        parser.exit(1, f"Package error: {error}\n")


if __name__ == "__main__":
    main()
