#!/usr/bin/env python3
"""Fail if any personal string appears in the repository before you publish it.

    python scripts/leakcheck.py                 scan every file in the working tree
    python scripts/leakcheck.py --publishable   scan only what git would publish
                                                (tracked files plus untracked files that are not ignored)

The strings to look for are read from .leakcheck-terms.txt at the repository root, one per
line, matched case-insensitively. Lines starting with # are comments. That file is listed in
.gitignore, so your personal strings are never published by the check that guards them.
Copy .leakcheck-terms.example.txt to .leakcheck-terms.txt and put your own strings in it:
your name, email, phone, home town, employers, clients, internal project names, salary
figures, local paths.

The check looks at file and folder names and at the contents of every text file. Binary files
(images, for example) are checked by name only. It also fails on em dashes, which this
project does not use.

Allowed: the copyright line of LICENSE may name the copyright holder.

Exit status: 0 clean, 1 something found, 2 no terms file.
"""

import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TERMS_FILE = ROOT / ".leakcheck-terms.txt"
SELF = pathlib.Path(__file__).resolve()
SKIP_DIRS = {".git"}
SKIP_FILES = {TERMS_FILE.resolve(), SELF}
EM_DASH = "—"


def load_terms():
    if not TERMS_FILE.exists():
        print(f"No {TERMS_FILE.name} found. Copy .leakcheck-terms.example.txt to "
              f"{TERMS_FILE.name} and list your personal strings in it.")
        sys.exit(2)
    terms = []
    for line in TERMS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def all_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield pathlib.Path(dirpath) / name


def publishable_files():
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode("utf-8")
    for rel in out.split("\0"):
        if rel:
            p = ROOT / rel
            if p.exists():
                yield p


def read_text(path):
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def allowed_line(rel, line):
    return rel == "LICENSE" and line.strip().lower().startswith("copyright")


def main():
    terms = load_terms()
    lowered = [(t, t.lower()) for t in terms]
    files = publishable_files() if "--publishable" in sys.argv else all_files()
    findings = []
    scanned = 0
    for path in sorted(set(files)):
        if path.resolve() in SKIP_FILES:
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        rel_l = rel.lower()
        for term, tl in lowered:
            if tl in rel_l:
                findings.append(f"{rel}: file name contains '{term}'")
        text = read_text(path)
        if text is None:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if allowed_line(rel, line):
                continue
            ll = line.lower()
            for term, tl in lowered:
                if tl in ll:
                    findings.append(f"{rel}:{n}: contains '{term}'")
            if EM_DASH in line:
                findings.append(f"{rel}:{n}: contains an em dash")
    if findings:
        print("\n".join(findings))
        print(f"\nFAIL: {len(findings)} finding(s) in {scanned} file(s) scanned, {len(terms)} term(s).")
        sys.exit(1)
    print(f"PASS: {scanned} file(s) scanned, {len(terms)} term(s), nothing found.")


if __name__ == "__main__":
    main()
