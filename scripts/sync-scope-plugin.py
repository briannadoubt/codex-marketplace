#!/usr/bin/env python3
"""Sync the Scope plugin skill from the canonical Scope repository."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


SOURCE_SKILL = Path("skills/claude/scope/SKILL.md")
DESTINATION_SKILL = Path("plugins/scope/skills/scope/SKILL.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy Scope's canonical SKILL.md into this Codex marketplace plugin."
    )
    parser.add_argument(
        "--scope-repo",
        help=(
            "Path to a checkout of https://github.com/briannadoubt/scope. "
            "Defaults to $SCOPE_REPO, ../Scope, then ../scope."
        ),
    )
    parser.add_argument(
        "--marketplace-repo",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Path to this codex-marketplace checkout.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the marketplace copy differs instead of writing it.",
    )
    return parser.parse_args()


def candidate_scope_repos(raw_scope_repo: str | None, marketplace_repo: Path) -> list[Path]:
    candidates: list[Path] = []
    if raw_scope_repo:
        candidates.append(Path(raw_scope_repo))
    if os.environ.get("SCOPE_REPO"):
        candidates.append(Path(os.environ["SCOPE_REPO"]))
    candidates.extend(
        [
            marketplace_repo.parent / "Scope",
            marketplace_repo.parent / "scope",
        ]
    )
    return candidates


def resolve_scope_repo(raw_scope_repo: str | None, marketplace_repo: Path) -> Path:
    candidates = candidate_scope_repos(raw_scope_repo, marketplace_repo)
    for candidate in candidates:
        expanded = candidate.expanduser().resolve()
        if (expanded / SOURCE_SKILL).is_file():
            return expanded

    checked = "\n".join(f"  - {candidate.expanduser()}" for candidate in candidates)
    raise SystemExit(
        "Could not find Scope's canonical skill file. Checked:\n"
        f"{checked}\n"
        "Pass --scope-repo /path/to/Scope or set SCOPE_REPO."
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"Unable to read {path}: {error}") from error


def validate_skill_contents(contents: str, source_path: Path) -> None:
    if not contents.startswith("---\n"):
        raise SystemExit(f"{source_path} must start with YAML frontmatter.")
    if "\nname: scope\n" not in contents[:500]:
        raise SystemExit(f"{source_path} does not look like the Scope skill.")


def main() -> None:
    args = parse_args()
    marketplace_repo = args.marketplace_repo.expanduser().resolve()
    scope_repo = resolve_scope_repo(args.scope_repo, marketplace_repo)

    source_path = scope_repo / SOURCE_SKILL
    destination_path = marketplace_repo / DESTINATION_SKILL
    source_contents = read_text(source_path)
    validate_skill_contents(source_contents, source_path)

    destination_contents = read_text(destination_path) if destination_path.exists() else None
    if args.check:
        if destination_contents != source_contents:
            print(f"{destination_path} is out of sync with {source_path}.", file=sys.stderr)
            return sys.exit(1)
        print(f"{destination_path} is in sync with {source_path}.")
        return

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if destination_contents == source_contents:
        print(f"{destination_path} already matches {source_path}.")
        return

    destination_path.write_text(source_contents, encoding="utf-8")
    print(f"Synced {destination_path} from {source_path}.")


if __name__ == "__main__":
    main()
