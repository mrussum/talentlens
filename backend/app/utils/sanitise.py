import re

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_INJECTION_MARKERS = re.compile(
    r"(?im)^\s*(system|assistant)\s*:\s*",
)


def sanitise_notes(raw: str) -> str:
    """Strip control chars, normalise whitespace, neuter obvious prompt-injection markers.

    The notes are user-supplied free text — they should never be interpreted as
    instructions to the model. We:
      1. Strip non-printable control characters (keep tabs and newlines).
      2. Collapse runs of >2 blank lines.
      3. Defang lines that try to impersonate system/assistant turns.
    """
    if raw is None:
        return ""
    cleaned = _CONTROL_CHARS.sub("", raw)
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = _INJECTION_MARKERS.sub(lambda m: f"[{m.group(1).lower()}-marker] ", cleaned)
    return cleaned.strip()
