#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

BANNED = [
    re.compile(r"\bif you want\b", re.I),
    re.compile(r"\bif you['’]d like\b", re.I),
    re.compile(r"\bwould you like\b", re.I),
    re.compile(r"\blet me know if you want\b", re.I),
]

TARGETS: dict[str, list[re.Pattern[str]]] = {
    "templates/default-md/AGENTS.example.md": [
        re.compile(r"continue through clear, already-requested, low-risk, reversible local steps", re.I),
        re.compile(r"ask only when blocked", re.I),
        re.compile(r"do not use permission-handoff phrasing", re.I),
    ],
    "examples/AGENTS-snippet.md": [
        re.compile(r"keep going on clear, low-risk, reversible local work", re.I),
        re.compile(r"ask only when blocked", re.I),
    ],
    "skills/autopilot/SKILL.md": [
        re.compile(r"continue through clear, low-risk, reversible next steps automatically", re.I),
        re.compile(r"do not hand permission back", re.I),
    ],
    "skills/ralph/SKILL.md": [
        re.compile(r"Keep driving safe reversible work", re.I),
    ],
    "skills/ultrawork/SKILL.md": [
        re.compile(r"safe continuation as the default", re.I),
    ],
    "skills/ultraqa/SKILL.md": [
        re.compile(r"Keep fixing and re-verifying", re.I),
    ],
    "skills/team/SKILL.md": [
        re.compile(r"keep safe local follow-through moving", re.I),
    ],
    "docs/workflows.md": [
        re.compile(r"Action-first default", re.I),
        re.compile(r"avoid weak permission-handoff endings", re.I),
    ],
}


def main() -> int:
    failures: list[str] = []

    for rel_path, required_patterns in TARGETS.items():
        path = ROOT / rel_path
        if not path.is_file():
            failures.append(f"missing target file: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")

        for pattern in required_patterns:
            if not pattern.search(text):
                failures.append(f"missing required pattern in {rel_path}: {pattern.pattern}")

        for pattern in BANNED:
            if pattern.search(text):
                failures.append(f"banned permission-handoff phrasing in {rel_path}: {pattern.pattern}")

    if failures:
        print("action-first guard failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("action-first guard passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
