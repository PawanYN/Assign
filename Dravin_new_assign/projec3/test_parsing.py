# cv_to_json_openrouter.py  (headings‑only version)

from __future__ import annotations
import json, os, sys
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI          # SDK ≥ 1.0


SCHEMA: dict[str, object] = {
    "title": "CV",
    "type": "object",
    "properties": {
        "name":       {"type": "string"},
        "email":      {"type": "string", "format": "email"},
        "phone":      {"type": "string"},
        "summary":    {"type": "string"},

        "skills": {
            "type":  "array",
            "items": {"type": "string"}
        },

        "experience": {
            "type": "array",
            "items": {
                "type":       "object",
                "properties": {
                    "company":  {"type": "string"},
                    "title":    {"type": "string"},
                    "start":    {"type": "string"},         # e.g. "2022‑05"
                    "end":      {"type": ["string", "null"]},
                    "location": {"type": "string"},
                    "bullets":  {
                        "type":  "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["company", "title", "start"]
            }
        },

        "education": {
            "type": "array",
            "items": {
                "type":       "object",
                "properties": {
                    "institution": {"type": "string"},
                    "degree":      {"type": "string"},
                    "start":       {"type": "string"},
                    "end":         {"type": ["string", "null"]},
                    "location":    {"type": "string"}
                },
                "required": ["institution", "degree"]
            }
        }
    },

    # keys that **must** appear in the final JSON
    "required": ["name", "email", "experience", "education"]
}


# 1. load key
load_dotenv(".env")
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    sys.exit("❌  OPENROUTER_API_KEY not found in .env")

# 2. OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# 3. helper: PDF → plain text
def pdf_to_text(pdf_path: str | Path) -> str:
    reader = PdfReader(str(pdf_path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

# 4. main
def main() -> None:
    cv_text = pdf_to_text("data/CV-AKHIL-v2.pdf")

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},   # ← JSON‑mode
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert résumé parser. "
                    "Return a JSON object that looks like this schema:\n"
                    f"{json.dumps(SCHEMA, indent=2)}\n"
                    "Do not output anything else."
                ),
            },
            {"role": "user", "content": cv_text},
        ],
    )

    headings_json = response.choices[0].message.content
    try:
        headings = json.loads(headings_json)
        print("✅ Headings found:")
        print(json.dumps(headings, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️  Model returned invalid JSON — raw output below:\n", headings_json)


if __name__ == "__main__":
    main()


# "You are an expert résumé parser. "
# "Find every SECTION HEADING in the résumé text (e.g. Education, "
# "Work Experience, Projects, Skills, etc.). "
# "Return **only** a JSON Dictonary of the distinct headings as key of dictionary with there corresponding info , "
# "spelled exactly as they appear, e.g.:\n"
# '{"Education":"mathematic and computing", "Work Experience":"11th class", "Technical Skills":"python,webdev"}\n'
# "Respond in JSON — no extra keys, no prose, just the array."