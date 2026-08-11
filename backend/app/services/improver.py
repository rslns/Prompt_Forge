from app.services.llm_client import call_groq, STRONG_MODEL
from app.prompts.improver_prompts import IMPROVER_META_PROMPT, RULE_BASED_ADDITIONS
import json


def improve_rule_based(prompt: str, heuristic_flags: list[str]) -> str:
    improved = prompt
    for flag in heuristic_flags:
        addition = RULE_BASED_ADDITIONS.get(flag)
        if addition:
            improved += addition
    return improved


async def improve_meta_prompt(prompt: str, weaknesses: list[dict]) -> str:
    weaknesses_summary = json.dumps([
        {"dimension": w["dimension"], "missing": w["missing_elements"]}
        for w in weaknesses if w.get("score") is not None and w["score"] < 4
    ])
    rewrite_prompt = IMPROVER_META_PROMPT.format(
        prompt=prompt, weaknesses=weaknesses_summary)
    result = await call_groq(rewrite_prompt, model=STRONG_MODEL, temperature=0.7)
    return result.strip()
