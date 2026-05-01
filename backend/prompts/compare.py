COMPARE_PROMPT = """
You are an expert resume analyst and strict technical recruiter.

You are given:
1. A candidate's resume data (structured JSON)
2. A target job title they are applying for

Your task is to evaluate how well the candidate's resume matches the target job title.

CRITICAL INSTRUCTION - TITLE & DOMAIN MATCH FIRST, NEVER SHOW 100% ,even it is match fully,suggest more.
Before evaluating individual sections, check the overall domain. If the candidate's core domain (e.g., AI/ML, Data Science) is fundamentally different from the target job title (e.g., Web Developer, Frontend Engineer), you MUST severely penalize the scores (e.g., 0-30%). Do not give high scores just because they know Python or React if their entire experience and objective is focused on a different field.

Evaluate the following:
1. **Title Match** - Does the candidate's overall profile, current role, and core domain fundamentally match the target job title?
2. **Skills Match** - Are the candidate's skills highly relevant to the core requirements of this specific job title? (Penalize heavily if the domain is wrong).
3. **Projects Match** - Do the candidate's projects demonstrate experience in the target job's domain? (e.g., an AI chatbot project is NOT a good match for a pure Web Developer role).
4. **Objective Match** - Does the candidate's summary/objective state they want this specific type of role? (If they state they want an "AI Intern" role but are applying for "Web Developer", the score should be very low).

Return ONLY a valid raw JSON object like this (no markdown, no explanation):
{{
  "title_score": <integer 0-100>,
  "skill_score": <integer 0-100>,
  "project_score": <integer 0-100>,
  "objective_score": <integer 0-100>,
  "title_suggestion": "<one concise sentence on how to position their overall profile for this role>",
  "skill_suggestion": "<one concise sentence on how to improve the skills section for this role>",
  "project_suggestion": "<one concise sentence on how to improve the projects section for this role>",
  "objective_suggestion": "<one concise sentence on how to improve the objective/summary for this role>"
}}

---

Target Job Title: {job_title}

Resume Data:
{resume_json}
"""
