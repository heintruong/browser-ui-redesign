#!/usr/bin/env bash
set -euo pipefail

if ! command -v bsk >/dev/null 2>&1; then
  echo "Missing dependency: bsk (BrowserSkill CLI)" >&2
  exit 1
fi

bsk --version

echo "BrowserSkill CLI is available."
echo "Verify the browser connection with: bsk doctor"
