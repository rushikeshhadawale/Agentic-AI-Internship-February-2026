from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def get_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",   # ✅ works locally
        max_length=512
    )

    return HuggingFacePipeline(pipeline=pipe)