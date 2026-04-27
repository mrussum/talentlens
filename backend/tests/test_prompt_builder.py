"""Dry-run verification of the prompt builder against the 3 sample scenarios.

This does NOT call the Anthropic API. It checks that for every sample:
  - sanitisation passes through realistic notes intact
  - the rendered user message embeds the framework + role + notes
  - all framework competencies appear in the prompt list
  - the system prompt opens with the mandatory raw-JSON instruction
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config.frameworks import list_competencies  # noqa: E402
from app.config.samples import SAMPLES  # noqa: E402
from app.utils.prompt_builder import (  # noqa: E402
    PROMPT_VERSION,
    SYSTEM_PROMPT,
    build_user_message,
)
from app.utils.sanitise import sanitise_notes  # noqa: E402

REQUIRED_OPENING = (
    "You MUST respond with ONLY a raw JSON object. Start your response with { "
    "and end with }."
)


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_system_prompt() -> None:
    _check(
        SYSTEM_PROMPT.startswith(REQUIRED_OPENING),
        "system prompt does not start with the mandatory raw-JSON instruction",
    )
    for keyword in (
        "STAR",
        "fit_score",
        "Never fabricate",
        "JSON ONLY",
    ):
        _check(keyword in SYSTEM_PROMPT, f"system prompt missing: {keyword}")


def verify_sample(sample) -> None:
    framework_key = "saville_wave"
    competencies = list_competencies(framework_key)
    sanitised = sanitise_notes(sample["notes"])
    _check(len(sanitised) >= 50, f"{sample['key']} sanitised notes too short")
    _check(
        "Candidate" in sanitised or "candidate" in sanitised,
        f"{sample['key']} lost candidate marker after sanitisation",
    )

    msg = build_user_message(
        notes=sanitised,
        framework_label="Saville Wave Professional",
        competencies=competencies,
        role=sample["role"],
    )
    _check(sample["role"] in msg, f"{sample['key']} prompt missing role")
    _check("Saville Wave Professional" in msg, f"{sample['key']} prompt missing framework label")
    for c in competencies:
        _check(c in msg, f"{sample['key']} prompt missing competency '{c}'")
    _check(
        "Produce the JSON report now" in msg,
        f"{sample['key']} prompt missing terminal instruction",
    )
    snippet = sanitised[:60]
    _check(snippet in msg, f"{sample['key']} sanitised notes not embedded in prompt")


def main() -> int:
    print(f"PROMPT_VERSION = {PROMPT_VERSION}")
    verify_system_prompt()
    print("[ok] system prompt")
    for sample in SAMPLES:
        verify_sample(sample)
        print(f"[ok] sample={sample['key']:<18} role={sample['role']}")
    print(f"verified {len(SAMPLES)} sample scenarios — prompt builder is wired correctly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
