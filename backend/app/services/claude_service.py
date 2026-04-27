import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from anthropic import Anthropic, APIError
from pydantic import ValidationError

from app.models.candidate import CandidateReport
from app.utils.prompt_builder import PROMPT_VERSION, SYSTEM_PROMPT, build_user_message

logger = logging.getLogger("talentlens.claude")

DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
DEFAULT_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "2400"))
DEFAULT_TEMPERATURE = float(os.getenv("CLAUDE_TEMPERATURE", "0.3"))


class ClaudeServiceError(Exception):
    """Raised when Claude returns content we cannot turn into a CandidateReport."""


@dataclass
class GenerationResult:
    report: CandidateReport
    raw_text: str
    parse_strategy: str
    prompt_version: str


_MARKDOWN_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)
_FIRST_JSON_OBJECT = re.compile(r"\{[\s\S]*\}")


def _extract_text(message: Any) -> str:
    """Pull the concatenated text content from an Anthropic Messages response."""
    parts: List[str] = []
    for block in getattr(message, "content", []) or []:
        text = getattr(block, "text", None)
        if isinstance(text, str):
            parts.append(text)
    return "".join(parts).strip()


def _try_validate(payload: Dict[str, Any]) -> CandidateReport:
    return CandidateReport.model_validate(payload)


def parse_claude_response(raw: str) -> Tuple[CandidateReport, str]:
    """Defensive parse pipeline.

    Order is significant — each strategy is tried only if the previous failed.
    Returns (report, strategy_name) on success or raises ClaudeServiceError.
    """
    if not raw:
        raise ClaudeServiceError("empty response from model")

    last_err: Optional[Exception] = None

    # 1. Raw json.loads
    try:
        return _try_validate(json.loads(raw)), "raw_json"
    except (json.JSONDecodeError, ValidationError) as exc:
        last_err = exc

    # 2. Strip markdown fences and retry
    stripped = _MARKDOWN_FENCE.sub("", raw).strip()
    if stripped and stripped != raw:
        try:
            return _try_validate(json.loads(stripped)), "fence_stripped"
        except (json.JSONDecodeError, ValidationError) as exc:
            last_err = exc

    # 3. Regex extract first {...} block
    match = _FIRST_JSON_OBJECT.search(stripped or raw)
    if match:
        candidate = match.group(0)
        try:
            return _try_validate(json.loads(candidate)), "regex_extracted"
        except (json.JSONDecodeError, ValidationError) as exc:
            last_err = exc

    raise ClaudeServiceError(
        f"could not parse Claude response into a CandidateReport: {last_err}"
    )


class ClaudeService:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
    ):
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set — refusing to start ClaudeService"
            )
        self._client = Anthropic(api_key=key)
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    @property
    def model(self) -> str:
        return self._model

    def generate_report(
        self,
        notes: str,
        framework_label: str,
        competencies: List[str],
        role: Optional[str],
    ) -> GenerationResult:
        user_message = build_user_message(
            notes=notes,
            framework_label=framework_label,
            competencies=competencies,
            role=role,
        )
        try:
            message = self._client.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                temperature=self._temperature,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
        except APIError as exc:
            logger.error(
                "claude_api_error",
                extra={"extras": {"prompt_version": PROMPT_VERSION, "error": str(exc)}},
            )
            raise ClaudeServiceError(f"Claude API error: {exc}") from exc

        raw_text = _extract_text(message)
        report, strategy = parse_claude_response(raw_text)
        return GenerationResult(
            report=report,
            raw_text=raw_text,
            parse_strategy=strategy,
            prompt_version=PROMPT_VERSION,
        )
