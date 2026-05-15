# Agentic Dev

Shared AI-related skills, prompts, and agent workflow notes.

## Layout

- `skills/` - Reusable skill definitions and supporting files.
- `prompts/` - Prompt templates and workflow starters.
- `hooks/` - Reusable automation hooks for agent workflows, including CLI preference hooks.
- `docs/` - Notes about usage, conventions, and publishing.

## Skill Guidelines

Keep each skill self-contained and include:

- a clear `SKILL.md` entrypoint
- any scripts, templates, or references needed by the skill
- usage notes that explain when an agent should apply it

## Included Skills

- `add-to-memory` - Record durable memory notes for both Claude and Codex.

## Included Hooks

- `enforce-cli` - Block discouraged shell commands and direct agents toward `fd`, `rg`, and `bat`.
- `enforce-cli-agent` - Share the same CLI preferences with subagents.
