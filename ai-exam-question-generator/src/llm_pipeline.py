import json
import re
from .paper_schema import Paper
from .gemini_client import call_gemini

def _extract_json(text: str) -> str:
    text = text.strip()
    # remove code fences if any
    text = re.sub(r"^```(json)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not locate JSON object in response.")
    return text[start:end+1]

def _looks_truncated(t: str) -> bool:
    # simple heuristic: ends without closing brace
    t = t.strip()
    return not t.endswith("}")

def generate_paper_via_api(prompt: str) -> Paper:
    raw = call_gemini(prompt)

    # ✅ If truncated, ask Gemini to fix it once
    if _looks_truncated(raw):
        repair_prompt = f"""
The following JSON is incomplete/truncated. Return ONLY the corrected FULL valid JSON.
Do not add any new questions. Only complete/close structures properly.

TRUNCATED JSON:
{raw}
""".strip()
        raw = call_gemini(repair_prompt)

    json_text = _extract_json(raw)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        raise ValueError("Gemini did not return valid JSON.\n\nRAW OUTPUT:\n" + raw)

    return Paper.model_validate(data)
