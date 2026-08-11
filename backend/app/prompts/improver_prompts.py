IMPROVER_META_PROMPT = """You are a prompt engineering expert.

Original prompt:
\"\"\"{prompt}\"\"\"

Evaluation identified these weaknesses (JSON): {weaknesses}

Rewrite the prompt to address every weakness listed. Preserve the original
task intent exactly — do not add unrelated instructions or change what the
prompt is asking for.

Return ONLY the rewritten prompt text, with no explanation, no preamble,
no markdown formatting.
"""

RULE_BASED_ADDITIONS = {
    "missing_role": "\n\n(Consider adding: 'You are an expert in [relevant domain].')",
    "missing_format_spec": "\n\nRespond in a clearly structured format (e.g. bullet points, numbered steps, or JSON) appropriate to this task.",
    "missing_examples": "\n\nExample:\n[Insert 1-2 example input/output pairs here.]",
    "missing_constraints": "\n\nConstraints: Only address what is asked. Do not include unrelated information.",
}
