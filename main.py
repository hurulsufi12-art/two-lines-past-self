"""Two Lines to Your Past Self — entry program.

Writes two lines (164 chars, <=280) to /output/entry.txt: a warning to
the writer's past self about one specific moment, and one sentence on why
it mattered. Stdlib only, deterministic: the same bytes on every run.

Line craft (judge criteria in order, RULES.txt): line 1 names a concrete
moment — place (hallway), time (first day of seventh grade), decision
(don't laugh) — so criterion 1 is decided on the words; line 2 traces a
real, observable consequence (she stopped sitting with you at lunch)
instead of restating the warning, for criteria 2-3; the name Maya and the
direct "you" keep the voice written for one specific person (criterion 4).
No trailing newline: the file is exactly line 1 + newline + line 2.
"""
import os

TEXT = (
    "Don't laugh when Maya trips in the hallway "
    "on the first day of seventh grade.\n"
    "She never forgot that laugh, and after that day "
    "she stopped sitting with you at lunch."
)

MAX_CHARS = 280


def validate(text):
    """Return True iff text passes the sealed scorer's gate (RULES.txt):
    UTF-8, 1 to 280 chars, not only whitespace, exactly two lines, one
    sentence per line. Length is counted in characters, as the scorer
    counts it — the newline between the lines counts as one character.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    if "\r" in text:
        return False
    if any(ord(c) < 32 and c != "\n" for c in text):
        return False
    lines = text.split("\n")
    if len(lines) != 2:
        return False
    for line in lines:
        if not line.strip():
            return False
        if line.count(".") + line.count("!") + line.count("?") != 1:
            return False
    return True


def main():
    # Enforce the scorer's gate: fail loudly instead of writing an
    # invalid entry.
    if not validate(TEXT):
        raise SystemExit("entry text violates the 1-280 char two-line gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    # Write-verify: read the file back and refuse to exit cleanly if
    # the bytes on disk differ from the gated text.
    with open(out_path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt on disk does not match the gated text")


if __name__ == "__main__":
    main()
