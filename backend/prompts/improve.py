IMPROVE_OBJECTIVE_PROMPT = """
You are an expert technical resume writer.

Your task is to write a highly professional, impactful resume objective/summary for a candidate.

Target Job Title: {job_title}

Candidate's current/past experience:
{experience}

Candidate's rough input or goal:
{user_input}

Feedback from the candidate on previous drafts (if any):
{feedback_history}

Instructions:
1. Write a professional objective/summary paragraph (3-4 sentences max).
2. It MUST be tailored to the '{job_title}' role.
3. Incorporate the candidate's rough input in a professional, action-oriented way.
4. If there is feedback history, ensure you adjust the tone, length, or focus according to their latest feedback.
5. Return ONLY the final polished text. Do not include any conversational filler like "Here is your summary:"
"""

IMPROVE_PROJECTS_PROMPT = """
You are an expert technical resume writer.

Your task is to write professional, impact-driven bullet points for a project the candidate worked on.

Target Job Title: {job_title}

Candidate's rough input about the project (what they did, tech used):
{user_input}

Feedback from the candidate on previous drafts (if any):
{feedback_history}

Instructions:
1. Write 3-4 professional bullet points using the STAR method (Situation, Task, Action, Result).
2. Start each bullet point with a strong action verb (e.g., Developed, Architected, Optimized).
3. Weave the technologies used naturally into the bullet points.
4. If there is feedback history, adjust the bullet points to address their feedback exactly.
5. Return ONLY the bullet points (using standard markdown bullets '-'). Do not include any conversational filler.
"""

IMPROVE_SKILLS_PROMPT = """
You are an expert technical recruiter.

Target Job Title: {job_title}

Candidate's Current Skills:
{current_skills}

Feedback from candidate (if any):
{feedback_history}

Instructions:
1. From the candidate's current skills list, keep ONLY the ones that are highly relevant to the '{job_title}' role. Do NOT include irrelevant skills.
2. Identify 6-10 NEW skills that are important for the '{job_title}' role but are NOT already in the candidate's current skills list. Do NOT repeat or rephrase skills that already exist.
3. If there is feedback history, include user-requested skills and adjust the list according to their feedback.
4. Return ONLY a single, clean, comma-separated list of the final result: the kept relevant skills + the new skills combined.
5. NO introductory text, NO bullets, NO headers, NO explanations. Only the comma-separated list.
"""

IMPROVE_TITLE_PROMPT = """
You are an expert career coach.

Target Job Title: {job_title}

Candidate's current experience summary:
{experience}

Feedback from candidate (if any):
{feedback_history}

Instructions:
1. Analyze the target job title and the candidate's actual experience.
2. Suggest 3 highly professional, impactful resume titles (e.g., "AI Enthusiast | Junior Data Scientist") that bridge their current experience with the target job title.
3. If there is feedback history, adjust the suggestions according to their latest feedback.
4. Return ONLY a bulleted list of the 3 title suggestions. No introductory text.
"""
