from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime


class PromptCreate(BaseModel):
    raw_text: str


class DimensionScore(BaseModel):
    dimension: str
    score: Optional[int]
    reasoning: Optional[str]
    missing_elements: List[str] = []


class EvaluationResponse(BaseModel):
    prompt_id: uuid.UUID
    task_type: str
    heuristic_flags: List[str]
    dimension_scores: List[DimensionScore]
    average_score: Optional[float]


class ImproveRequest(BaseModel):
    prompt_id: uuid.UUID
    raw_text: str
    strategy: str = "meta_prompt"  # or "rule_based"


class ImprovementResponse(BaseModel):
    improved_text: str
    strategy_used: str
    reevaluation: Optional[EvaluationResponse] = None
