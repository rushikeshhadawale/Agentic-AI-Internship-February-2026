from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Extract the following from the resume:

1. Skills
2. Tools
3. Years of Experience

Rules:
- Only include explicitly mentioned skills
- Do NOT assume anything

Return in JSON format:
{{
  "skills": [],
  "tools": [],
  "experience": ""
}}

Resume:
{resume}
"""
)