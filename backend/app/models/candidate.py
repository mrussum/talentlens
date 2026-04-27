from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class FitLevel(str, Enum):
    strong_fit = "strong_fit"
    good_fit = "good_fit"
    possible_fit = "possible_fit"
    not_recommended = "not_recommended"


class CompetencyRating(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)
    evidence: str = Field(min_length=1, max_length=2000)
    development_area: bool = False


class CandidateReport(BaseModel):
    candidate_name: Optional[str] = None
    role_applied: Optional[str] = None
    summary: str = Field(min_length=1, max_length=1500)
    overall_fit: FitLevel
    fit_score: int = Field(ge=0, le=100)
    fit_rationale: str = Field(min_length=1, max_length=2000)
    strengths: List[str] = Field(min_length=1, max_length=8)
    development_areas: List[str] = Field(min_length=1, max_length=8)
    competencies: List[CompetencyRating] = Field(default_factory=list, max_length=20)
    suggested_questions: List[str] = Field(min_length=1, max_length=10)
    recommendation: str = Field(min_length=1, max_length=600)
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("strengths", "development_areas", "suggested_questions")
    @classmethod
    def _strip_blank_items(cls, value: List[str]) -> List[str]:
        cleaned = [item.strip() for item in value if item and item.strip()]
        if not cleaned:
            raise ValueError("must contain at least one non-empty item")
        return cleaned


class GenerateRequest(BaseModel):
    notes: str = Field(min_length=50, max_length=15000)
    role: Optional[str] = Field(default=None, max_length=200)
    competency_framework: Optional[str] = Field(default="saville_wave", max_length=64)


class GenerateResponse(BaseModel):
    success: bool
    data: Optional[CandidateReport] = None
    error: Optional[str] = None
    latency_ms: int = Field(ge=0)


class FrameworkSummary(BaseModel):
    key: str
    label: str
    competencies: List[str]


class FrameworksResponse(BaseModel):
    frameworks: List[FrameworkSummary]


class HealthResponse(BaseModel):
    status: str
    version: str
