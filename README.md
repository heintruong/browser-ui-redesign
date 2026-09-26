# Browser UI Redesign

Improve an existing web interface with a real browser baseline, focused UI/UX
changes, and desktop/mobile verification. Works as a **Codex or Claude Code
marketplace plugin**, or as an **OpenCode skill and command**.

The workflow uses `browser-skill` for live browser work, `impeccable` for design
and implementation, and `web-design-guidelines` for the final interface audit.
It inspects the project, exercises the requested flows, makes focused changes,
runs relevant checks, and verifies the result in at most two browser correction
passes. BrowserSkill sessions are stopped on success or failure.

## Before you install

Have Git and a harness version that supports the commands below. Install the
three companion skills using their upstream instructions:

| Dependency | Setup | Verify in your harness |
| --- | --- | --- |
| `browser-skill` | [BrowserSkill setup](https://github.com/Tencent/BrowserSkill/blob/main/AGENT_INSTALL.md) | Skill is available; `bsk` and its browser extension connect |
| `impeccable` | [Impeccable](https://github.com/pbakaus/impeccable) | Skill is available |
| `web-design-guidelines` | [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | Skill is available |

The plugin supplies workflow instructions, not a browser or bundled companion
skills. Installing it does not install those dependencies. Python 3.9+ is only
needed for the OpenCode installer and repository maintenance scripts.

Read browser-skill's installed launcher, environment, recovery, and profile
instructions **before any `bsk` command**. In a source checkout,
`bash scripts/check-runtime.sh` checks CLI startup only; run it in that documented
environment. Browser connectivity and companion skill availability are separate
checks. If a dependency is missing, the workflow reports it.

## Install

### Codex

Run once:

```bash
codex plugin marketplace add https://github.com/heintruong/browser-ui-redesign.git
codex plugin add browser-ui-redesign@browser-ui-redesign-marketplace
```

Start a new thread, then invoke:

```text
$browser-ui-redesign http://localhost:5173 — improve the homepage and mobile navigation; preserve the brand.
```

You can also install through the Codex plugin picker after adding the
marketplace. The plugin card is **Browser UI Redesign**. If `plugin add` is not
available in your CLI, use the picker or update Codex. Check the installation
with `codex plugin list`. Codex requires explicit invocation of this skill.

### Claude Code

```bash
claude plugin marketplace add https://github.com/heintruong/browser-ui-redesign.git
claude plugin install browser-ui-redesign@browser-ui-redesign-marketplace
```

For a project-scoped installation, append `--scope project` to the install
command. Restart Claude Code, then invoke the namespaced skill:

```text
/browser-ui-redesign:browser-ui-redesign http://localhost:5173 — improve the homepage and mobile navigation; preserve the brand.
```

Check the installation with `claude plugin list`. The full namespace above
avoids ambiguity with standalone copies of the skill.

### OpenCode

Clone once to a location you will keep for future updates:

```bash
git clone https://github.com/heintruong/browser-ui-redesign.git
cd browser-ui-redesign
python3 scripts/install-opencode.py --target /absolute/path/to/your-app/.opencode --dry-run
python3 scripts/install-opencode.py --target /absolute/path/to/your-app/.opencode
```

Replace the target with your application's config directory. For a user-wide
installation instead, use `--target ~/.config/opencode` (or your configured
OpenCode config directory). Choose one scope to avoid duplicate skill copies.

The installer writes only:

- `skills/browser-ui-redesign/SKILL.md`
- `commands/browser-ui-redesign.md`

It backs up any changed existing files under
`<target>/.browser-ui-redesign-backups/`, preserves other files/settings, and
prints the backup path. Re-running it is safe: identical files are left alone.
An interrupted update can be completed by re-running the same command.

Start a new OpenCode session in your application, then run:

```text
/browser-ui-redesign http://localhost:5173 — improve the homepage and mobile navigation; preserve the brand.
```

This is a local skill/command adapter, not an npm runtime plugin. When working
inside this repository itself, OpenCode can discover the checked-in adapter
directly; no installation into this checkout is needed.

## Update an existing installation

Published updates must reach the marketplace or checkout first. Editing a
separate local clone does not update an installed cached plugin. Keep the same
plugin and marketplace names when upgrading from `0.1.0`.

### Codex marketplace installation

```bash
codex plugin marketplace upgrade browser-ui-redesign-marketplace
codex plugin add browser-ui-redesign@browser-ui-redesign-marketplace
codex plugin list
```

Start a **new thread** after updating. `marketplace upgrade` refreshes a Git
marketplace; `plugin add` installs from the refreshed source. If you registered
a local directory instead, update that checkout first and then run `plugin add`.

### Claude Code marketplace installation

```bash
claude plugin marketplace update browser-ui-redesign-marketplace
claude plugin update browser-ui-redesign@browser-ui-redesign-marketplace
claude plugin list
```

Use the same install scope; append `--scope project` to `plugin update` if
appropriate. Restart Claude Code after the update. Optional marketplace
auto-update is controlled by the user/host, not by this plugin. See
[Claude Code's update guidance](https://code.claude.com/docs/en/plugins/host-marketplace#keep-users-up-to-date).

### OpenCode installation

In the retained source checkout:

```bash
git pull --ff-only
python3 scripts/install-opencode.py --target /absolute/path/to/your-app/.opencode
python3 scripts/install-opencode.py --target /absolute/path/to/your-app/.opencode --check
```

Use the same target as the original installation, then start a new session.
`--check` compares both installed files to this checkout and exits nonzero when
they are missing or different; it does not contact GitHub. Local customizations
to the two managed files are backed up before replacement.

### Migrating older manual copies

If you previously used `cp -R` to copy this skill into `.agents/skills`,
`.codex/skills`, `.claude/skills`, or another local skill directory, that copy has
no update connection to this repository.

For Codex or Claude Code, install from the marketplace above, then move the old
`browser-ui-redesign` copy to a backup **outside all skill discovery paths**.
Keep any customizations and port them deliberately. For OpenCode, the installer
can update the old `.opencode` copy directly and back it up. Also check for
duplicate user-wide copies. Start a new session after migration.

Older README versions misspelled the GitHub owner as `heinturong`. The canonical
repository is **`heintruong/browser-ui-redesign`**. If refresh fails, inspect the
registered marketplace with `codex plugin marketplace list` or
`claude plugin marketplace list` and correct its source using the harness's
marketplace management UI/commands. Preserve existing install scopes/settings.

## Use it effectively

Include the URL or app directory, routes/flows, design constraints, and any
named browser profile. For example:

```text
$browser-ui-redesign ./frontend — improve the checkout flow on desktop and mobile, preserve API behavior, and use browser profile Work.
```

The skill inspects the project to infer missing details and asks when ambiguity
would materially change the work. It reports flows tested, screenshot paths,
changes, verification results, and remaining uncertainty. It does not claim
conversion or business gains from visual inspection alone.

All live browser work uses `browser-skill` through `bsk`, including delegated
work. A failed launcher or `bsk status` triggers documented recovery and retry;
it never authorizes fallback to Chrome DevTools MCP or another backend. If
recovery cannot complete, the workflow reports the blocker and pending checks
as `Not verified`. Redesign edits require a rendered baseline.

For a named profile, the workflow runs `bsk browsers --json`, resolves the
profile's instance ID, and starts with
`bsk session start --browser <id> --json`. It never guesses an ID or silently
uses the default profile. It uses a new session-controlled tab, avoids secrets,
and attempts session cleanup on success and failure.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Installed but skill is missing | Start a new session/thread; confirm the plugin is installed/enabled and use the invocation for your harness |
| Old behavior after updating | Refresh marketplace **and** update/install plugin; check the installed version and duplicate manual copies |
| Marketplace cannot refresh | Check registered URL, network/authentication, and whether it is a Git source or local directory |
| `bsk` crashes or times out | Read browser-skill's launcher/environment instructions; follow documented recovery and retry; report failure without switching backend |
| Named profile missing/ambiguous | Reconnect according to browser-skill instructions and list browsers again; do not guess |
| OpenCode reports different files | Pull the retained checkout, run installer with the original target, then `--check` |
| Missing companion skill | Install it from the upstream setup links, then restart the harness |

This package cannot hide tools exposed by the host. For stronger enforcement,
disable competing browser backends in a dedicated host session where supported.
The no-fallback instruction still applies when other tools are visible.

## Development and releases

`skills/browser-ui-redesign/SKILL.md` is the canonical workflow. After editing:

```bash
python3 scripts/package.py sync
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
claude plugin validate . --strict
claude plugin validate .claude-plugin/plugin.json --strict
```

The stdlib package check verifies names, versions, marketplace sources, adapter
consistency, and changelog presence. It does not replace harness schema checks
or real browser testing. CI runs package checks and isolated installer tests
without accessing a user's browser or installing companion skills.

Before publishing the next release:

1. Add a changelog entry and use `python3 scripts/package.py version 0.1.2` to
   update all release versions and the adapter together. Use the intended next
   version instead of the example. Never reuse a published version for changed
   plugin content.
2. Run the checks above and inspect the diff. Confirm that old installations can
   update with the documented commands.
3. Smoke-test the skill in the supported harnesses on a non-production page.
   Exercise a launcher failure, documented recovery/retry, a blocked recovery,
   and named-profile selection with multiple browsers. Confirm no backend
   fallback and that created sessions are stopped.
4. Commit and push the release to the marketplace's tracked branch. Create a
   matching Git tag if distributing tagged releases. Existing users then use
   the update instructions above; a push alone does not refresh active sessions.

See [CHANGELOG.md](CHANGELOG.md) for release notes. Native harness command
availability depends on the installed harness version; consult its `--help`
when updating older clients.

## License

[MIT](LICENSE).
