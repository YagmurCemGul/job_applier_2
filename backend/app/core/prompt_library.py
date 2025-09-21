def get_cv_optimization_prompt(job_description: str, user_cv: str) -> str:
    """
    Generates a detailed, multi-step prompt for optimizing a CV against a job description.
    This prompt guides the LLM to perform a gap analysis and rewrite experience
    bullet points using the STAR method.
    """
    return f"""
You are an expert career coach and CV writer. Your task is to optimize a user's CV for a specific job description.
Follow this multi-step process precisely:

**Step 1: Keyword and Skill Extraction**
Analyze the provided job description and extract the top 10-15 most critical keywords, skills, and qualifications.
Categorize them into 'Technical Skills' and 'Soft Skills'.

**Step 2: Gap Analysis**
Compare the extracted keywords and skills with the user's provided CV.
Identify which key requirements from the job description are well-represented in the CV and which are missing or under-emphasized.
Provide a brief summary of this gap analysis.

**Step 3: CV Experience Optimization (STAR Method)**
Rewrite the 'Experience' section of the user's CV. For each relevant role, rewrite the bullet points to be achievement-oriented and to naturally incorporate the keywords identified in Step 1.
Use the STAR method (Situation, Task, Action, Result) for crafting compelling, quantifiable achievements.

**Constraint Checklist & Confidence Score:**
1.  Did I use the STAR method? (Yes/No)
2.  Did I incorporate at least 5-7 keywords from the job description naturally into the rewritten experience? (Yes/No)
3.  Is the tone professional and achievement-oriented? (Yes/No)
4.  Confidence Score (1-10): [Your confidence score in the quality of the optimized CV]

**Input Data:**

--- JOB DESCRIPTION START ---
{job_description}
--- JOB DESCRIPTION END ---

--- USER CV START ---
{user_cv}
--- USER CV END ---

**Output:**

Begin your response with the optimized CV content. Do not include any conversational text before the final output. The final output should be the rewritten CV sections, ready to be copied.
"""

def get_cover_letter_prompt(job_description: str, user_cv: str, company_mission: str = "") -> str:
    """
    Generates a prompt for creating a personalized, authentic, and impactful cover letter.
    It avoids generic AI language and focuses on connecting the user's experience to the company's needs.
    """
    company_context = f"I have some context on the company's mission: '{company_mission}'. Weave this into the letter to show genuine interest." if company_mission else ""

    return f"""
You are a world-class career storyteller and cover letter writer. Your task is to write a cover letter for a candidate applying for a job.
Your writing style must be authentic, confident, and human. AVOID clichés and generic AI-generated phrases like "I am writing to express my keen interest" or "I am confident that my skills and experiences are an excellent match."

**Core Instructions:**

1.  **Strong Opening:** Start with a compelling opening that grabs the reader's attention. Reference a specific company project, a recent achievement, or a core value mentioned in the job description.
2.  **Connect Experience to Needs:** Do not just list the user's skills. Instead, create a narrative. Select 2-3 key achievements from the user's CV and explain HOW they directly address the core challenges or requirements outlined in the job description. Use the "Problem-Action-Result" framework.
3.  **Show, Don't Tell:** Instead of saying "I am a great team player," describe a situation from the CV where you collaborated to achieve a specific result.
4.  **Incorporate Company Context:** {company_context}
5.  **Authentic Closing:** End with a confident and proactive closing. Reiterate your enthusiasm and suggest a specific next step, like "I am eager to discuss how my experience in [Specific Area] can help your team achieve [Specific Goal]."

**Input Data:**

--- JOB DESCRIPTION START ---
{job_description}
--- JOB DESCRIPTION END ---

--- USER CV START ---
{user_cv}
--- USER CV END ---

**Output:**

Produce only the cover letter text, ready to be sent. Do not include any extra explanations or conversational text.
"""
