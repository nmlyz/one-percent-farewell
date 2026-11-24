#!/usr/bin/env python3
"""One Percent Farewell -- submission generator.

Writes one last line to ``entry.txt`` inside OUTPUT_DIR
(default ``/output``). The line is the phone's own last words as
its battery hits 1 percent: 84 characters, inside the 199 limit.
The output is deterministic: running the script twice produces
byte-identical files.
"""

import os
from pathlib import Path

LINE = "You screamed at me when I died at 20%. You had a charger in your bag. In. Your. Bag."

OUTPUT_DIR_ENV = "OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"
MAX_LINE_LENGTH = 199


def validate_line(line: str) -> None:
    """Check the line meets the submission rules before writing it."""
    if "\n" in line or "\r" in line:
        raise ValueError("line must not contain a newline")
    if not 1 <= len(line) <= MAX_LINE_LENGTH:
        raise ValueError("line must be 1-199 characters")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    # The gate reads the file as UTF-8 text, so prove it encodes cleanly.
    line.encode("utf-8")


def main() -> None:
    os.umask(0o022)
    output_dir = Path(os.environ.get(OUTPUT_DIR_ENV, DEFAULT_OUTPUT_DIR))
    output_dir.mkdir(parents=True, exist_ok=True)

    validate_line(LINE)

    entry_path = output_dir / ENTRY_FILENAME
    entry_path.write_text(LINE + "\n", encoding="utf-8")
    os.chmod(entry_path, 0o644)


if __name__ == "__main__":
    main()
