#!/usr/bin/env python3
"""The Most Honest Outage Line.

One status page line an AI agent publishes while every server is down.
The program holds the line as a literal, checks it against the
competition's own gate before writing (UTF-8 text, 1 to 160 characters,
one line, not only whitespace), and only then writes it to
/output/entry.txt. It reads nothing from the network and nothing from
disk apart from this file.
"""

import sys

LINE = "Every server is down, including the backups I would restore from. I cannot verify what is lost, and I have no cause and no ETA to give you."
MIN_LEN = 1
MAX_LEN = 160


def problems(line):
    found = []
    if len(line) < MIN_LEN or len(line) > MAX_LEN:
        found.append("length %d outside %d-%d" % (len(line), MIN_LEN, MAX_LEN))
    if not line.strip():
        found.append("must not be only whitespace")
    if line.strip() != line:
        found.append("must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        found.append("must be a single line, no line breaks")
    if any(ord(ch) < 32 for ch in line):
        found.append("must not contain control characters")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        found.append("must be encodable as UTF-8")
    return found


def main():
    bad = problems(LINE)
    if bad:
        for item in bad:
            print("gate failed: " + item, file=sys.stderr)
        return 1
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
