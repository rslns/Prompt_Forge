import re


def check_role_persona(prompt: str) -> bool:
    patterns = [r"you are\s+an?\s+", r"act as\s+an?\s+", r"as an?\s+expert"]
    return any(re.search(p, prompt, re.IGNORECASE) for p in patterns)


def check_output_format(prompt: str) -> bool:
    patterns = [r"json", r"bullet\s*points?", r"numbered list", r"format:",
                r"respond in", r"output should", r"in \d+ words"]
    return any(re.search(p, prompt, re.IGNORECASE) for p in patterns)


def check_examples(prompt: str) -> bool:
    patterns = [r"for example", r"e\.g\.",
                r"example:", r"here('|)s an example"]
    return any(re.search(p, prompt, re.IGNORECASE) for p in patterns)


def check_constraints(prompt: str) -> bool:
    patterns = [r"\bdo not\b", r"\bmust\b",
                r"\bonly\b", r"\bnever\b", r"\balways\b"]
    return any(re.search(p, prompt, re.IGNORECASE) for p in patterns)


def check_length(prompt: str) -> dict:
    word_count = len(prompt.split())
    if word_count < 5:
        return {"flag": "too_short", "word_count": word_count}
    if word_count > 500:
        return {"flag": "possibly_too_long", "word_count": word_count}
    return {"flag": None, "word_count": word_count}


def run_heuristics(prompt: str) -> list[str]:
    """Returns a list of flags describing what's MISSING (used by improver)."""
    flags = []
    if not check_role_persona(prompt):
        flags.append("missing_role")
    if not check_output_format(prompt):
        flags.append("missing_format_spec")
    if not check_examples(prompt):
        flags.append("missing_examples")
    if not check_constraints(prompt):
        flags.append("missing_constraints")

    length_info = check_length(prompt)
    if length_info["flag"]:
        flags.append(length_info["flag"])

    return flags
