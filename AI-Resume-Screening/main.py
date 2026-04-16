import os
from chains.extract_chain import extract_chain
from chains.match_chain import match_chain
from chains.score_chain import score_chain
from chains.explain_chain import explain_chain

def process_resume(resume_path, job_desc):
    with open(resume_path, "r") as f:
        resume = f.read()

    print("\n==============================")
    print(f"Processing: {resume_path}")
    print("HF KEY:", os.getenv("HUGGINGFACEHUB_API_TOKEN"))

    # Step 1: Extract
    extracted = extract_chain.invoke({"resume": resume})
    print("\nExtracted:", extracted)

    # Step 2: Match
    matched = match_chain.invoke({
        "resume_data": extracted.content,
        "job_description": job_desc
    })
    print("\nMatched:", matched)

    # Step 3: Score
    score = score_chain.invoke({
        "match_result": matched.content
    })
    print("\nScore:", score)

    # Step 4: Explain
    explanation = explain_chain.invoke({
        "score": score.content,
        "match_result": matched.content
    })
    print("\nExplanation:", explanation)


if __name__ == "__main__":
    with open("data/job_description.txt", "r") as f:
        job_desc = f.read()

    resumes = [
        "data/resumes/strong.txt",
        "data/resumes/average.txt",
        "data/resumes/weak.txt"
    ]

    for resume in resumes:
        process_resume(resume, job_desc)