# Shared Hooks

Reusable hooks for AI agent workflows.

## CLI Preferences

- `enforce-cli.rb` blocks shell command verbs that conflict with local CLI preferences.
- `enforce-cli-agent.rb` emits the same CLI preferences as context for subagents.

The CLI preference hook directs agents to use `fd` instead of `find`, `rg`
instead of `grep`, and `bat` instead of `cat`.

