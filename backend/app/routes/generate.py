import logging
import time
from functools import lru_cache
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.frameworks import (
    FrameworkNotFoundError,
    get_framework,
    list_competencies,
    load_frameworks,
)
from app.models.candidate import (
    FrameworkSummary,
    FrameworksResponse,
    GenerateRequest,
    GenerateResponse,
)
from app.services.claude_service import (
    ClaudeService,
    ClaudeServiceError,
)
from app.utils.logging import log_event
from app.utils.prompt_builder import PROMPT_VERSION
from app.utils.sanitise import sanitise_notes

logger = logging.getLogger("talentlens.api")

router = APIRouter(prefix="/api", tags=["generate"])


@lru_cache(maxsize=1)
def _service_singleton() -> ClaudeService:
    return ClaudeService()


def get_claude_service() -> ClaudeService:
    return _service_singleton()


@router.get("/frameworks", response_model=FrameworksResponse)
def list_frameworks() -> FrameworksResponse:
    raw = load_frameworks()
    items = [
        FrameworkSummary(
            key=key,
            label=str(value.get("label", key)),
            competencies=[str(c) for c in value.get("competencies", [])],
        )
        for key, value in raw.items()
    ]
    return FrameworksResponse(frameworks=items)


@router.post("/generate", response_model=GenerateResponse)
def generate_report(
    request: GenerateRequest,
    service: ClaudeService = Depends(get_claude_service),
) -> GenerateResponse:
    started = time.perf_counter()
    framework_key = request.competency_framework or "saville_wave"

    try:
        framework = get_framework(framework_key)
    except FrameworkNotFoundError:
        latency_ms = int((time.perf_counter() - started) * 1000)
        log_event(
            logger,
            "generate_unknown_framework",
            endpoint="/api/generate",
            latency_ms=latency_ms,
            prompt_version=PROMPT_VERSION,
            framework=framework_key,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"unknown competency_framework '{framework_key}'",
        )

    framework_label = str(framework.get("label", framework_key))
    competencies = list_competencies(framework_key)
    sanitised_notes = sanitise_notes(request.notes)
    if len(sanitised_notes) < 50:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return GenerateResponse(
            success=False,
            error="notes are too short after sanitisation (min 50 chars)",
            latency_ms=latency_ms,
        )

    error_msg: Optional[str] = None
    competency_count = 0
    fit_score: Optional[int] = None
    parse_strategy: Optional[str] = None

    try:
        result = service.generate_report(
            notes=sanitised_notes,
            framework_label=framework_label,
            competencies=competencies,
            role=request.role,
        )
        competency_count = len(result.report.competencies)
        fit_score = result.report.fit_score
        parse_strategy = result.parse_strategy
        latency_ms = int((time.perf_counter() - started) * 1000)
        log_event(
            logger,
            "generate_ok",
            endpoint="/api/generate",
            latency_ms=latency_ms,
            prompt_version=result.prompt_version,
            competency_count=competency_count,
            fit_score=fit_score,
            parse_strategy=parse_strategy,
            framework=framework_key,
            model=service.model,
        )
        return GenerateResponse(
            success=True,
            data=result.report,
            latency_ms=latency_ms,
        )
    except ClaudeServiceError as exc:
        error_msg = str(exc)
    except Exception as exc:  # pragma: no cover — last-resort guard
        logger.exception("generate_unexpected_error")
        error_msg = f"unexpected error: {exc}"

    latency_ms = int((time.perf_counter() - started) * 1000)
    log_event(
        logger,
        "generate_error",
        endpoint="/api/generate",
        latency_ms=latency_ms,
        prompt_version=PROMPT_VERSION,
        competency_count=competency_count,
        fit_score=fit_score,
        parse_strategy=parse_strategy,
        framework=framework_key,
        error=error_msg,
    )
    return GenerateResponse(
        success=False,
        error=error_msg,
        latency_ms=latency_ms,
    )
