#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "memory"


def claude_project_key(cwd: str) -> str:
    path = str(Path(cwd).expanduser().resolve())
    return path.replace("/", "-")


def markdown_title(title: str) -> str:
    return title.strip().strip("#").strip()


def codex_body(title: str, body: str) -> str:
    return f"# {title}\n\n{body.strip()}\n"


def claude_body(title: str, body: str, source: str) -> str:
    safe_description = body.strip().splitlines()[0][:100] if body.strip() else title
    return (
        "---\n"
        f"name: {title}\n"
        f"description: {safe_description}\n"
        "type: feedback\n"
        f"origin: add-to-memory:{source}\n"
        "---\n"
        f"{body.strip()}\n"
    )


def upsert_index(memory_index: Path, title: str, filename: str) -> None:
    if not memory_index.exists():
        memory_index.write_text(
            "# Memory\n\n## User Preferences\n"
            f"- [{title}]({filename})\n",
            encoding="utf-8",
        )
        return

    content = memory_index.read_text(encoding="utf-8")
    link = f"- [{title}]({filename})"
    if f"]({filename})" in content:
        return

    marker = "## User Preferences"
    if marker in content:
        lines = content.splitlines()
        for index, line in enumerate(lines):
            if line.strip() == marker:
                insert_at = index + 1
                while insert_at < len(lines) and lines[insert_at].startswith("- "):
                    insert_at += 1
                lines.insert(insert_at, link)
                memory_index.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
                return

    memory_index.write_text(
        content.rstrip() + f"\n\n## User Preferences\n{link}\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write one memory note to both Codex and Claude memory stores."
    )
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--source", choices=["codex", "claude"], default="claude")
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--slug")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    title = markdown_title(args.title)
    body = args.body.strip()
    if not title:
        print("error: --title cannot be empty", file=sys.stderr)
        return 2
    if not body:
        print("error: --body cannot be empty", file=sys.stderr)
        return 2

    slug = slugify(args.slug or title)
    filename = f"{slug}.md"
    home = Path.home()

    codex_dir = home / ".codex" / "memories"
    codex_dir.mkdir(parents=True, exist_ok=True)
    codex_path = codex_dir / filename
    codex_path.write_text(codex_body(title, body), encoding="utf-8")

    project_key = claude_project_key(args.cwd)
    claude_dir = home / ".claude" / "projects" / project_key / "memory"
    claude_dir.mkdir(parents=True, exist_ok=True)
    claude_path = claude_dir / filename
    claude_path.write_text(claude_body(title, body, args.source), encoding="utf-8")
    upsert_index(claude_dir / "MEMORY.md", title, filename)

    print(f"codex={codex_path}")
    print(f"claude={claude_path}")
    print(f"claude_index={claude_dir / 'MEMORY.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
