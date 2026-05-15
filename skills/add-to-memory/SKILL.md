---
name: add-to-memory
description: Record durable user preferences, operating instructions, or agent behavior notes in both Claude and Codex memory. Use when the user says `/add-to-memory`, `$add-to-memory`, "add this to memory", "remember this", "sync this to Codex/Claude", "copy this memory", or otherwise asks to persist an instruction across agents.
---

# Add To Memory

Persist the same memory note for both local agents:

- Claude project memory: `~/.claude/projects/<project-key>/memory/<slug>.md`
- Codex memory: `~/.codex/memories/<slug>.md`

## Workflow

1. Extract the durable memory from the user's request. If the memory content is unclear, ask one concise clarification before writing.
2. Do not persist secrets, credentials, access tokens, personal identifiers, or short-lived task state unless Douglas explicitly asks to store that exact sensitive data.
3. Choose a short title and slug for one atomic topic. Prefer the user's wording when they name the memory.
4. Run the bundled script from this skill directory. Use `--source claude` when invoked from Claude and `--source codex` when invoked from Codex:

```bash
python3 scripts/add_to_memory.py --title "<title>" --body "<memory text>" --source "<claude|codex>" --cwd "$PWD"
```

5. Verify the paths reported by the script with `bat --plain`.
6. Tell Douglas which Codex and Claude memory files were written.

## Notes

- The script writes both agents every time, so the flow works even when the user asks from only one agent.
- Claude project memory is selected from `--cwd` using Claude's project directory convention. If no matching project memory exists, the script creates it.
- Keep entries concise and behavioral. Do not store broad conversation summaries unless the user asks for them.
