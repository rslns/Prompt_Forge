import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Fast/cheap model for classification-type calls
FAST_MODEL = "llama-3.1-8b-instant"
# Larger model for judging and rewriting — check console.groq.com for current available models
STRONG_MODEL = "llama-3.3-70b-versatile"


async def call_groq(prompt: str, model: str = STRONG_MODEL,
                    temperature: float = 0.2, json_mode: bool = False) -> str:
    kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


async def call_groq_json(prompt: str, model: str = STRONG_MODEL,
                         temperature: float = 0.2, retries: int = 2) -> dict:
    """Call Groq expecting JSON back. Retries on parse failure."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            raw = await call_groq(prompt, model=model, temperature=temperature, json_mode=True)
            return json.loads(raw)
        except (json.JSONDecodeError, Exception) as e:
            last_error = e
            continue
    # graceful failure — caller must handle "error" key
    return {"error": True, "message": str(last_error)}
