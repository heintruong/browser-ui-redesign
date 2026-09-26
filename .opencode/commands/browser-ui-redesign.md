---
description: Redesign and browser-verify a website or web flow
subagent: false
---

Use the `browser-ui-redesign` skill for the following target:

$ARGUMENTS

Requirements:

- Load `browser-skill`, `impeccable`, and `web-design-guidelines`.
- Before any browser command, read browser-skill's applicable environment,
  launcher, recovery, and profile instructions. Use only its `bsk` CLI.
- On startup failure, follow documented recovery and retry; if still blocked,
  report it. Never fall back to Chrome DevTools MCP or another browser backend.
- For a named profile, resolve its instance ID with `bsk browsers --json` and
  start the session with `bsk session start --browser <id> --json`.
- Inspect the current implementation before editing.
- Start or reuse the project's documented development server.
- Use a new BrowserSkill session-controlled tab; do not borrow a user tab.
- Capture desktop and mobile baselines before changing code.
- Apply Impeccable for design direction and implementation.
- Apply Vercel Web Design Guidelines for the final UX/accessibility audit.
- Preserve backend behavior and existing brand constraints unless explicitly
  asked to change them.
- Run no more than two browser correction passes.
- Run relevant lint, typecheck, build, and tests.
- Always stop the browser session, including on failure.

If the target URL, route, or user flow is missing, inspect the project first.
Ask for clarification only when ambiguity would materially change the work.
