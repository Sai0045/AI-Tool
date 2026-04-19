import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Models that support generateContent:\n")
for m in genai.list_models():
    methods = getattr(m, "supported_generation_methods", []) or []
    if "generateContent" in methods:
        print(m.name)
