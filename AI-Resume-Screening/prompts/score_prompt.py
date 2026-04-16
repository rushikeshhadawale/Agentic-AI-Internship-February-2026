from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_result"],
    template="""
Assign a score (0-100) based on matching skills.

Rules:
- More matches → higher score
- Missing important skills → reduce score

Return JSON:
{{
  "score": number
}}

Match Result:
{match_result}
"""
)