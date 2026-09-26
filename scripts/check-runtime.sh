#!/usr/bin/env bash
set -euo pipefail

if ! command -v bsk >/dev/null 2>&1; then
  echo "Missing dependency: bsk (BrowserSkill CLI)" >&2
  exit 1
fi

if ! bsk --version; then
  echo "BrowserSkill CLI failed to launch. Read browser-skill's environment and recovery instructions, then retry." >&2
  echo "Do not switch to Chrome DevTools MCP or another browser backend." >&2
  exit 1
fi

echo "BrowserSkill CLI is available."
echo "This checks CLI startup only, not browser connectivity or companion skills."
echo "Read browser-skill's launcher/environment instructions before running its connection preflight."
echo "For named profiles: bsk browsers --json, then bsk session start --browser <id> --json"
