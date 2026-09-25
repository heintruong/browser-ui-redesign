# Browser UI Redesign

A portable Agent Skill for bounded, browser-verified UI/UX redesign. The
workflow combines:

- `browser-skill` for real-browser inspection, interaction, and screenshots.
- `impeccable` for design direction and frontend implementation.
- Vercel Web Design Guidelines for UX, accessibility, and interface auditing.

The workflow:

1. Inspects the current source and project instructions.
2. Starts or reuses the documented development server.
3. Captures desktop and mobile browser baselines.
4. Exercises the requested user flows.
5. Groups findings by root cause.
6. Applies Impeccable and Vercel guidance.
7. Runs relevant tests, lint, typecheck, and build.
8. Verifies the result in at most two browser correction passes.
9. Stops the BrowserSkill session and reports remaining uncertainty.

## Repository layout

This repository is the standalone package:

```text
browser-ui-redesign/
├── plugin.json
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── .agents/plugins/
│   └── marketplace.json
├── .opencode/
│   ├── commands/browser-ui-redesign.md
│   └── skills/browser-ui-redesign/SKILL.md
├── skills/
│   └── browser-ui-redesign/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── scripts/check-runtime.sh
└── README.md
```

The root marketplace catalogs expose this repository as the
`browser-ui-redesign` plugin for Claude Code and Codex.

## Runtime requirements

This package does **not** automatically install browser infrastructure or
third-party skills. Each user must have these dependencies available in the
harness:

- BrowserSkill CLI (`bsk`) and its connected browser extension.
- `impeccable` skill.
- `web-design-guidelines` skill.

Check the BrowserSkill CLI:

```bash
./scripts/check-runtime.sh
```

The script only checks that `bsk` is available. Check the browser connection
separately:

```bash
bsk doctor
```

If a dependency is missing, stop and report it. Do not automatically install a
browser, extension, binary, or unrelated package.

## Install from Git

### Claude Code

Add this repository as a marketplace and install the plugin:

```bash
claude plugin marketplace add heinturong/browser-ui-redesign
claude plugin install browser-ui-redesign@browser-ui-redesign-marketplace
```

For a project-only installation:

```bash
claude plugin install browser-ui-redesign@browser-ui-redesign-marketplace --scope project
```

For a local checkout or session-only test without installing:

```bash
git clone https://github.com/heinturong/browser-ui-redesign.git
cd browser-ui-redesign
claude --plugin-dir .
```

After installing the marketplace plugin, invoke the namespaced skill:

```text
/browser-ui-redesign:browser-ui-redesign
```

The namespace is required for a marketplace/plugin install.

### Codex

Add the repository as a Codex marketplace:

```bash
codex plugin marketplace add heinturong/browser-ui-redesign
codex plugin marketplace list
```

Then open the Codex Plugins Directory or plugin picker, select
`Browser UI Redesign`, install `browser-ui-redesign`, and start a new Codex
session. Restart Codex after changing marketplace files.

Invoke the bundled skill explicitly with:

```text
$browser-ui-redesign
```

The Codex app may also expose the plugin in its `@` picker. Do not rely on the
old Codex custom-prompt mechanism; it is deprecated.

For a local checkout without plugin installation, copy the skill into the
location scanned by Codex:

```bash
git clone https://github.com/heinturong/browser-ui-redesign.git
cd browser-ui-redesign
mkdir -p .agents/skills
cp -R skills/browser-ui-redesign .agents/skills/
```

Then restart Codex and invoke:

```text
$browser-ui-redesign
```

Some existing local Codex setups use `.codex/skills`; use that equivalent
location only when the Codex installation is configured to scan it.

### OpenCode

OpenCode discovers the adapter automatically when this repository is the
working directory:

```text
.opencode/commands/browser-ui-redesign.md
.opencode/skills/browser-ui-redesign/SKILL.md
```

Invoke it with:

```text
/browser-ui-redesign
```

## Install the companion skills

The package depends on existing skills; it does not vendor them. Use the
upstream installation instructions for each harness.

### Impeccable

Source:

- GitHub: <https://github.com/pbakaus/impeccable>
- Skills.sh: <https://www.skills.sh/pbakaus/impeccable/impeccable>

Verify that the harness lists `impeccable` before starting a redesign. Impeccable
may require its own setup step and launcher; follow the instructions from the
installed skill.

### Vercel Web Design Guidelines

Source:

- GitHub: <https://github.com/vercel-labs/agent-skills>
- Skills.sh: <https://www.skills.sh/vercel-labs/agent-skills/web-design-guidelines>

Verify that the harness lists `web-design-guidelines`. The skill reviews source
files against the current Vercel interface guidelines. If the current
guidelines cannot be fetched, the workflow reports that portion as `Not
verified` rather than claiming it passed.

### BrowserSkill

Source and setup:

- Repository: <https://github.com/Tencent/BrowserSkill>
- Installation guide:
  <https://github.com/Tencent/BrowserSkill/blob/main/AGENT_INSTALL.md>

Verify:

```bash
bsk --version
bsk doctor
```

The workflow uses a new session-controlled tab and never borrows an existing user
tab. It always attempts to stop the session on completion or failure.

## Invocation examples

### OpenCode

```text
/browser-ui-redesign http://localhost:5173 — redesign the homepage, preserve the brand, and improve hierarchy, CTA, responsive layout, and accessibility.
```

### Claude Code

```text
/browser-ui-redesign:browser-ui-redesign frontend — improve the admin dashboard and primary flows; do not change the API contract.
```

### Codex

```text
$browser-ui-redesign official_website — redesign the marketing homepage, preserve existing content and brand, and improve mobile layout and WCAG issues.
```

If the URL, route, or user flow is missing, the agent must inspect the project
and ask for confirmation before editing.

## Safety boundaries

The skill instructs the agent to:

- Inspect code and rendered UI before editing.
- Preserve backend behavior and existing brand constraints unless explicitly
  asked to change them.
- Use a new BrowserSkill-controlled tab.
- Avoid secrets, cookies, tokens, and credential data.
- Avoid unrelated refactors and generated artifacts in Git.
- Group fixes by root cause and keep changes surgical.
- Run no more than two browser correction passes.
- Stop the BrowserSkill session on success or failure.
- Distinguish observed UI improvements from unproven conversion or business
  impact.

## Validate before publishing

From the repository root, validate the Claude package:

```bash
claude plugin validate . --strict
```

Validate JSON manifests directly when the Claude CLI is not available:

```bash
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugin.json >/dev/null
```

Run the runtime check:

```bash
./scripts/check-runtime.sh
```

## Release checklist

Before publishing a new version:

- Confirm the dependency versions and installation instructions.
- Review `SKILL.md` for harness-specific wording.
- Validate both marketplace manifests.
- Validate both plugin manifests.
- Test the skill in Claude Code, Codex, and OpenCode on a non-production page.
- Verify that the browser session is stopped after success and failure.
- Add a license before treating the repository as reusable open source.
- Update the package version and marketplace version together.

## License

No license is declared yet. The repository is public for distribution, but a
license should be added before treating it as open source or granting broad
reuse rights.
