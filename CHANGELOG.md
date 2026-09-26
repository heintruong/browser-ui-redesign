# Changelog

## [0.1.1] - 2026-09-26

- Require BrowserSkill for all live browser work, including delegated work.
  Recover documented launcher failures and retry; never silently switch to
  Chrome DevTools MCP or another backend.
- Resolve named browser profiles to instance IDs before starting a session.
- Normalize the skill identifier to `browser-ui-redesign` for harness discovery.
  Keep Codex explicit invocation through `agents/openai.yaml`; remove the shared
  `disable-model-invocation` flag that the Codex plugin validator rejects.
- Correct installation URLs and document native marketplace updates, migration
  from 0.1.0, verification, and troubleshooting.
- Add an OpenCode installer/updater with preview, backups, and installed-content
  checks; keep the adapter synchronized with the canonical skill.
- Add release consistency checks, installer tests, and CI.
- Add Codex plugin display metadata and remove project-specific scope rules.

## [0.1.0]

- Initial BrowserSkill, Impeccable, and Vercel Web Design Guidelines workflow.
- Claude Code and Codex marketplace manifests and OpenCode adapter.
- MIT license.
