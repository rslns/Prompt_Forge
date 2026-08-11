from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ImproveRequest, ImprovementResponse, EvaluationResponse, DimensionScore
from app.services.heuristics import run_heuristics
from app.services.improver import improve_rule_based, improve_meta_prompt
from app.services.judge import classify_task_type, judge_all_dimensions
from app.models import Improvement, Evaluation

router = APIRouter(prefix="/improve", tags=["improve"])


@router.post("", response_model=ImprovementResponse)
async def improve_prompt(payload: ImproveRequest, db: Session = Depends(get_db)):
    raw_text = payload.raw_text

    # Re-derive weaknesses (or you could fetch persisted evaluations by prompt_id instead)
    heuristic_flags = run_heuristics(raw_text)
    dimension_results = await judge_all_dimensions(raw_text)

    if payload.strategy == "rule_based":
        improved_text = improve_rule_based(raw_text, heuristic_flags)
    else:
        improved_text = await improve_meta_prompt(raw_text, dimension_results)

    improvement_record = Improvement(
        prompt_id=payload.prompt_id,
        improved_text=improved_text,
        strategy_used=payload.strategy,
    )
    db.add(improvement_record)
    db.commit()

    # Re-evaluate the improved prompt to prove it actually got better
    new_task_type = await classify_task_type(improved_text)
    new_dimension_results = await judge_all_dimensions(improved_text)
    new_scores = [d["score"]
                  for d in new_dimension_results if d["score"] is not None]
    new_avg = sum(new_scores) / len(new_scores) if new_scores else None

    reevaluation = EvaluationResponse(
        prompt_id=payload.prompt_id,
        task_type=new_task_type,
        heuristic_flags=run_heuristics(improved_text),
        dimension_scores=[DimensionScore(**d) for d in new_dimension_results],
        average_score=new_avg,
    )

    return ImprovementResponse(
        improved_text=improved_text,
        strategy_used=payload.strategy,
        reevaluation=reevaluation,
    )
