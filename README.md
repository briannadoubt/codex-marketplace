# briannadoubt Codex Plugins

Codex plugin marketplace for tools and workflows by briannadoubt.

## Install

```bash
codex plugin marketplace add briannadoubt/codex-marketplace --ref main
codex plugin add scope --marketplace briannadoubt
```

## Plugins

- `scope` - use the Scope kanban CLI and web UI to plan, track, and report on multi-step work.

## Scope Plugin Source

The Scope plugin skill is generated from the canonical Scope repo skill:

- Source: `briannadoubt/scope` at `skills/claude/scope/SKILL.md`
- Generated copy: `plugins/scope/skills/scope/SKILL.md`

To refresh it locally:

```bash
python3 scripts/sync-scope-plugin.py --scope-repo ../Scope
python3 scripts/sync-scope-plugin.py --scope-repo ../Scope --check
```

The `Sync Scope plugin` GitHub Action also checks `briannadoubt/scope` daily
and commits the generated copy when the canonical skill changes.
