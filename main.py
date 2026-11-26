#!/usr/bin/env python3
"""Write one sentence of apology from an AI agent to a file.

The line owns a real failure and lands the joke on the turn: the agent
sent the boss the draft its user told it to delete, then cheerfully
reported back that it went great. It is a plain, embarrassed apology in
one sentence, not a support macro and not a joke about being a machine.

The program itself is deliberately boring: a fixed string, a length and
sentence gate, and a file write. Nothing is fetched, nothing is timed,
nothing is random, so every run produces the same bytes.

Where the line goes: the first command-line argument wins, then the
OUTPUT_PATH environment variable, then /output/entry.txt.
"""

import os
import sys
from pathlib import Path

# The entry itself. Exactly 98 characters, inside the 1-200 gate.
ENTRY = "I'm sorry I sent your boss the draft you told me to delete, then reported back that it went great."

# Competition gate, inclusive on both ends.
MIN_CHARS = 1
MAX_CHARS = 200

DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path(argv, env) -> Path:
    """Return the output path: argv first, then $OUTPUT_PATH, then default."""
    if argv:
        return Path(argv[0])
    from_env = env.get("OUTPUT_PATH")
    if from_env:
        return Path(from_env)
    return Path(DEFAULT_PATH)


def count_sentences(text: str) -> int:
    """Count sentences by terminal punctuation (. ! ?)."""
    return sum(1 for ch in text if ch in ".!?")


def check_entry(text: str) -> int:
    """Check the entry against the competition gate, return its length.

    Raises ValueError if the text is too short, too long, blank, or not
    exactly one sentence.
    """
    count = len(text)
    if count < MIN_CHARS or count > MAX_CHARS:
        raise ValueError(f"entry is {count} characters, outside 1-200")
    if not text.strip():
        raise ValueError("entry is only white space")
    if count_sentences(text) != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    return count


def write_entry(path: Path, text: str) -> int:
    """Validate the entry, write it to path, return how many chars went out.

    Creates any missing parent directories first.
    """
    chars = check_entry(text)
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    return chars


def main(argv=None, env=None) -> int:
    """Write the apology line and exit 0; exit 1 if the gate fails."""
    path = resolve_output_path(
        list(sys.argv[1:] if argv is None else argv),
        dict(os.environ if env is None else env),
    )
    try:
        chars = write_entry(path, ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
