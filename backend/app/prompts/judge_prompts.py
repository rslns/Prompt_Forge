DIMENSION_DEFINITIONS = {
    "clarity": "whether the instruction is unambiguous and easy to understand on first read",
    "specificity": "whether the prompt constrains output format, scope, and boundaries clearly enough to reduce ambiguity",
    "context_sufficiency": "whether the prompt gives the model enough background, constraints, or examples to succeed",
    "task_alignment": "whether the prompt's structure matches what the task actually requires (e.g. reasoning tasks should invite step-by-step thinking)",
}

JUDGE_PROMPT_TEMPLATE = """You are evaluating a prompt's {dimension_name} on a 1-5 scale.

Definition: {dimension_name} measures {dimension_definition}.

Rubric:
1 = Almost entirely absent
2 = Weak, major gaps
3 = Adequate but with clear room for improvement
4 = Strong, minor gaps only
5 = Excellent, no meaningful gaps

Prompt to evaluate:
\"\"\"{prompt}\"\"\"

Think through what is and isn't present for this dimension, THEN score it.
Respond ONLY in this exact JSON format, no other text:
{{"reasoning": "<your reasoning>", "score": <integer 1-5>, "missing_elements": ["<short phrase>", "..."]}}
"""

TASK_CLASSIFY_PROMPT = """Classify this prompt into exactly one category:
generation, classification, extraction, reasoning, summarization, conversational

Prompt:
\"\"\"{prompt}\"\"\"

Respond ONLY in this JSON format: {{"task_type": "<category>"}}
"""
