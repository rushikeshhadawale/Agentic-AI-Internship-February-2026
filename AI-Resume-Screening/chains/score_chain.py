from utils.config import get_llm
from prompts.score_prompt import score_prompt

llm = get_llm()

score_chain = score_prompt | llm