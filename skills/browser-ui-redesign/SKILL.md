---
name: browser-ui-redesign
description: >
  Redesign and improve an existing website or web application by inspecting
  it in a real browser, applying Impeccable design guidance, and auditing
  the result with Vercel Web Design Guidelines. Use for UI/UX redesign,
  responsive fixes, visual polish, accessibility improvements, and
  browser-verified frontend changes.
metadata:
  version: "0.1.1"
---

# Browser UI Redesign

Coordinate the existing skills `browser-skill`, `impeccable`, and
`web-design-guidelines` for a bounded, browser-verified UI/UX workflow.

Before editing, verify that these skills are available in the current harness.
If the harness supports explicit skill loading, load them. Otherwise follow
their installed instructions directly. If one is unavailable, stop and report
it; do not replace a missing skill with an improvised approximation.

## Browser backend and recovery contract

Use `browser-skill` and its `bsk` CLI for all live browser work in this
workflow, including connection checks, inspection, interaction, and screenshots.
Before the first browser command (including `bsk status`), read the installed
`browser-skill` instructions and any applicable environment, launcher, recovery,
and browser-profile references. Follow their required launcher and environment
for every `bsk` command.

Do not switch to Chrome DevTools MCP, another browser MCP, or another browser
backend as a workaround, even if those tools are available. This also applies
to delegated browser work. A launcher crash, timeout, or failed `bsk status`
is not evidence that the browser is unavailable and does not authorize fallback.

If a command fails:

1. Retain the failed command and relevant error, excluding sensitive data.
2. Follow the installed browser-skill's documented recovery for that failure,
   then retry the failed preflight or session command using the documented
   launcher and environment. Do not improvise installation or reset user
   browser data. If recovery requires permission, obtain it first.
3. If recovery is undocumented, cannot be completed, or the retry still fails,
   stop the browser-dependent workflow and report the blocker, recovery tried,
   and required next action. Mark pending browser checks `Not verified`; do not
   proceed to redesign edits without a rendered baseline.

For a requested named browser profile, run `bsk browsers --json`, verify the
requested profile against the returned browser instance ID, and start the
session with `bsk session start --browser <id> --json`. Never guess the ID or
silently choose the default profile. If the profile is missing, follow the
documented connection/recovery steps and list browsers again. If the mapping is
still missing or ambiguous, report it and request the needed clarification.
Retain the confirmed browser ID and session ID for subsequent commands.

## Inputs and safety

Establish:

- Working directory and local URL
- Routes/pages in scope
- Primary user flows
- Existing brand and design constraints
- Whether backend behavior must remain unchanged

Read `AGENTS.md` and project instructions before editing. Inspect the current
code and rendered UI before proposing changes. Preserve product behavior unless
the user explicitly asks otherwise. Do not read or expose secrets, cookies, or
tokens. Do not borrow an existing user browser tab. Use a new session-controlled
tab. Do not commit screenshots or generated artifacts. Keep changes surgical.

Treat separate frontend applications as separate scopes unless the user requests
a cross-site visual system. Infer missing inputs from the project when possible;
ask only when ambiguity would materially change the requested work.

## Workflow

### 1. Project and browser setup

1. Inspect package metadata, routing, component library, styling, and design
   tokens.
2. Start the documented development server only if it is not already running.
3. Use the URL reported by the server.
4. Apply the browser backend and recovery contract above. Verify the CLI with
   `bsk --version` and the connection using the installed skill's documented
   preflight. CLI availability alone does not establish browser connectivity.
5. Resolve any requested profile with `bsk browsers --json` and start a new
   session with `bsk session start --browser <id> --json`. If no profile was
   requested, follow the installed skill's browser-selection rules and use
   `bsk session start --json` only when the default browser is unambiguous.
   Retain the session ID; apply documented recovery to any startup failure.

### 2. Capture a baseline

1. Navigate to the target URL.
2. Run `bsk observe` and `bsk snapshot`.
3. Capture a desktop full-page screenshot.
4. Emulate `iphone-14`, capture a mobile screenshot, then restore with
   `bsk emulate --off`.
5. Save artifacts under `/tmp/opencode/browser-ui-redesign/<run-id>/` and read
   the PNG files before judging visual quality.
6. Inspect console errors and relevant failed requests.

Record hierarchy, spacing, alignment, typography, color, CTA prominence,
navigation, forms, loading/empty/error/disabled states, keyboard focus, and
responsive behavior. DOM text alone is not visual evidence.

### 3. Exercise flows and diagnose

Test only the requested flows: navigation, CTA, forms/validation, modal/drawer,
mobile menu, and loading/error states as applicable. Use fresh browser refs
after navigation or meaningful DOM changes.

Group findings by root cause, not by individual CSS declaration. Prioritize:

1. Broken user flow
2. Accessibility failure
3. Responsive failure
4. Information architecture
5. Visual consistency
6. Motion and polish

For each proposed change, state browser evidence, source location, user impact,
fix, and verification method.

### 4. Apply Impeccable and Vercel guidance

Use Impeccable to define the design direction, preserve the incumbent brand,
apply its craft floor, and implement a coherent batch of related changes.

Use Vercel Web Design Guidelines to review changed source for semantic HTML,
keyboard use, focus, forms, touch targets, contrast, reduced motion, images,
overflow, states, navigation, i18n, and hydration. Adapt the guidelines to this
product. If the current guidelines cannot be fetched, report that portion as
`Not verified`.

### 5. Verify

Run relevant tests, lint, typecheck, and frontend build. Do not claim a check
passed unless it actually ran.

Reload the changed page, re-run affected flows, and capture desktop/mobile
screenshots again. Fix high-impact findings in one batch and allow at most one
additional browser correction pass. Stop after two passes and report remaining
lower-priority items.

Always stop the browser session on success or failure:

```bash
bsk session stop <session-id>
```

## Final report

Include flows tested, devices/viewports tested, baseline/final screenshot
paths, findings, design decisions, changed files, verification results,
remaining unverified items, and the distinction between observed UI improvements
and unproven business impact.
