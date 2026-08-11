from app.services.llm_client import call_groq_json, STRONG_MODEL, FAST_MODEL
from app.prompts.judge_prompts import DIMENSION_DEFINITIONS, JUDGE_PROMPT_TEMPLATE, TASK_CLASSIFY_PROMPT


async def classify_task_type(prompt: str) -> str:
    result = await call_groq_json(TASK_CLASSIFY_PROMPT.format(prompt=prompt), model=FAST_MODEL)
    return result.get("task_type", "generation") if not result.get("error") else "generation"


async def judge_dimension(prompt: str, dimension: str) -> dict:
    template_prompt = JUDGE_PROMPT_TEMPLATE.format(
        dimension_name=dimension,
        dimension_definition=DIMENSION_DEFINITIONS[dimension],
        prompt=prompt,
    )
    result = await call_groq_json(template_prompt, model=STRONG_MODEL, temperature=0.1)

    if result.get("error"):
        return {"dimension": dimension, "score": None, "reasoning": "evaluation failed", "missing_elements": []}

    return {
        "dimension": dimension,
        "score": result.get("score"),
        "reasoning": result.get("reasoning", ""),
        "missing_elements": result.get("missing_elements", []),
    }


async def judge_all_dimensions(prompt: str) -> list[dict]:
    results = []
    for dimension in DIMENSION_DEFINITIONS.keys():
        result = await judge_dimension(prompt, dimension)
        results.append(result)
    return results
