from app.services.llm_client import STRONG_MODEL
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PromptCreate, EvaluationResponse, DimensionScore
from app.services.heuristics import run_heuristics
from app.services.judge import classify_task_type, judge_all_dimensions
from app.models import Prompt, Evaluation
router = APIRouter(prefix="/evaluate", tags=["evaluate"])


@router.post("", response_model=EvaluationResponse)
async def evaluate_prompt(payload: PromptCreate, db: Session = Depends(get_db)):
    raw_text = payload.raw_text

    # 1. Save the prompt
    prompt_record = Prompt(raw_text=raw_text)
    db.add(prompt_record)
    db.commit()
    db.refresh(prompt_record)

    # 2. Cheap heuristics first
    heuristic_flags = run_heuristics(raw_text)

    # 3. Task classification
    task_type = await classify_task_type(raw_text)
    prompt_record.task_type = task_type
    db.commit()

    # 4. LLM judge per dimension
    dimension_results = await judge_all_dimensions(raw_text)

    # 5. Persist evaluations
    scores = []
    for d in dimension_results:
        eval_record = Evaluation(
            prompt_id=prompt_record.id,
            dimension=d["dimension"],
            score=d["score"],
            reasoning=d["reasoning"],
            missing_elements=d["missing_elements"],
            model_used=STRONG_MODEL,
        )
        db.add(eval_record)
        if d["score"] is not None:
            scores.append(d["score"])
    db.commit()

    avg = sum(scores) / len(scores) if scores else None

    return EvaluationResponse(
        prompt_id=prompt_record.id,
        task_type=task_type,
        heuristic_flags=heuristic_flags,
        dimension_scores=[DimensionScore(**d) for d in dimension_results],
        average_score=avg,
    )
