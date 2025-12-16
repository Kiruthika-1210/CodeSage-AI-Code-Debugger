import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-flash-latest")


def call_gemini(prompt: str):
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Remove markdown code fences if present
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?|```$", "", text).strip()

        return json.loads(text)

    except Exception as e:
        msg = str(e)
        if "429" in msg:
            return {
                "error": "AI quota exceeded. Please retry shortly."
            }
        return {
            "error": msg
        }
