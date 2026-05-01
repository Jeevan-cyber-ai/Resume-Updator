# backend/services/comparator.py
import os
import json
from dotenv import load_dotenv
from google import genai
from prompts.compare import COMPARE_PROMPT

load_dotenv()

def compare_resume_with_job(resume_data: dict, job_title: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY is not set."}

    api_key = api_key.strip('"').strip("'")

    # Extract only the relevant sections for comparison
    relevant_data = {
        "skills": resume_data.get("skills", []),
        "projects": resume_data.get("projects", []),
        "summary": resume_data.get("summary") or resume_data.get("objectives", ""),
        "experience": resume_data.get("experience", []),
    }

    prompt = COMPARE_PROMPT.format(
        job_title=job_title,
        resume_json=json.dumps(relevant_data, indent=2)
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        result_text = response.text.strip()

        # Strip markdown if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        elif result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        return json.loads(result_text.strip())

    except json.JSONDecodeError:
        return {"error": "Model did not return valid JSON.", "raw": response.text}
    except Exception as e:
        return {"error": str(e)}
