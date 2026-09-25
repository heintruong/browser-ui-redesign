---
description: Redesign and browser-verify a website or web flow
subagent: false
---

Use the `browser-ui-redesign` skill for the following target:

$ARGUMENTS

Requirements:

- Load `browser-skill`, `impeccable`, and `web-design-guidelines`.
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

If the target URL, route, or user flow is missing or ambiguous, inspect the
project and ask for confirmation before editing.
