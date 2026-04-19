import os
import google.generativeai as genai

def call_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Put it in your .env file.")

    genai.configure(api_key=api_key)

    # ✅ Stable & fast
    model = genai.GenerativeModel("models/gemini-flash-lite-latest")

    resp = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 8192,   # ✅ bigger output so JSON doesn't cut
            "response_mime_type": "application/json",
        },
    )

    # robust extraction
    try:
        if getattr(resp, "text", None):
            return resp.text
    except Exception:
        pass

    candidates = getattr(resp, "candidates", None) or []
    if not candidates:
        raise ValueError("Gemini returned no candidates.")

    cand = candidates[0]
    content = getattr(cand, "content", None)
    parts = getattr(content, "parts", None) if content else None

    out = ""
    if parts:
        for p in parts:
            t = getattr(p, "text", None)
            if t:
                out += t

    if out.strip():
        return out.strip()

    finish = getattr(cand, "finish_reason", None)
    raise ValueError(f"Gemini returned empty output. finish_reason={finish}")
