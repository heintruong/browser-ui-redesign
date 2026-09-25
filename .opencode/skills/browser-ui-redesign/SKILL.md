---
name: Browser UI Redesign
description: >
  Redesign and improve an existing website or web application by inspecting
  it in a real browser, applying Impeccable design guidance, and auditing
  the result with Vercel Web Design Guidelines. Use for UI/UX redesign,
  responsive fixes, visual polish, accessibility improvements, and
  browser-verified frontend changes.
---

# Browser UI Redesign

Coordinate the existing skills `browser-skill`, `impeccable`, and
`web-design-guidelines` for a bounded, browser-verified UI/UX workflow.

If one of the three skills is unavailable, stop and report it. Do not replace a
missing skill with an improvised approximation.

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

For this repository, treat `frontend/` and `official_website/` as separate
frontends unless the user requests a cross-site visual system.

## Workflow

### 1. Project and browser setup

1. Inspect package metadata, routing, component library, styling, and design
   tokens.
2. Start the documented development server only if it is not already running.
3. Use the URL reported by the server.
4. Verify BrowserSkill with `bsk --version`; if the browser is unavailable,
   follow the browser-skill setup instructions.
5. Start a session with `bsk session start --json` and retain the session ID.

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
