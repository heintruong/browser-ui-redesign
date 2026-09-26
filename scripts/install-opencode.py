#!/usr/bin/env python3
"""Install/update the OpenCode adapter into an explicit config directory."""

import argparse
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    Path("skills/browser-ui-redesign/SKILL.md"): ROOT / "skills/browser-ui-redesign/SKILL.md",
    Path("commands/browser-ui-redesign.md"): ROOT / ".opencode/commands/browser-ui-redesign.md",
}


def safe_destination(target, relative):
    destination = target / relative
    for path in (destination, *destination.parents):
        if path == target:
            break
        if path.is_symlink():
            raise ValueError(f"Refusing symlink inside target: {path}")
        if path.exists() and path != destination and not path.is_dir():
            raise ValueError(f"Expected a directory: {path}")
    if destination.exists() and not destination.is_file():
        raise ValueError(f"Expected a file: {destination}")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path,
                        help="OpenCode config directory, e.g. /project/.opencode or ~/.config/opencode")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    modes.add_argument("--check", action="store_true", help="Exit 0 only when installed files match this checkout")
    args = parser.parse_args()
    try:
        target = args.target.expanduser().resolve()
        if target == ROOT / ".opencode":
            raise ValueError("This checkout already contains the adapter; install into your application's config directory")
        if target.exists() and not target.is_dir():
            raise ValueError(f"Expected a config directory: {target}")
        version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
        # Resolve and read every file before writing anything.
        destinations = {relative: safe_destination(target, relative) for relative in FILES}
        content = {relative: source.read_bytes() for relative, source in FILES.items()}
        changed = [relative for relative, destination in destinations.items()
                   if not destination.exists() or destination.read_bytes() != content[relative]]
        print(f"Source version: {version}; target: {target}")
        if not changed:
            print("Installed files match this checkout. No changes needed.")
            return
        for relative in changed:
            print(f"{'Update' if destinations[relative].exists() else 'Install'}: {relative}")
        if args.check:
            parser.exit(1, "Installed files differ or are missing. Run again without --check to install/update.\n")
        if args.dry_run:
            print("Preview only; no files written.")
            return

        # Back up only the files this adapter replaces, outside skill discovery.
        backup_root = target / ".browser-ui-redesign-backups"
        safe_destination(target, Path(".browser-ui-redesign-backups/.probe"))
        existing = [relative for relative in changed if destinations[relative].exists()]
        if existing:
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = Path(tempfile.mkdtemp(prefix=f"before-{version}-", dir=backup_root))
            for relative in existing:
                saved = backup / relative
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destinations[relative], saved)
            print(f"Previous files backed up to: {backup}")
        for relative in changed:
            destination = destinations[relative]
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Atomic replacement keeps each file intact if the process is interrupted.
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(content[relative])
            try:
                temporary.chmod(0o644)
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
        print(f"Installed {version}. Start a new OpenCode session and run /browser-ui-redesign.")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Install error: {error}\n")


if __name__ == "__main__":
    main()
