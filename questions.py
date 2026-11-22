import os, json, time
import pymupdf as fitz
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]


def call_gemini(prompt, retries=4):
    for attempt in range(retries):
        for model in MODELS:
            try:
                return client.models.generate_content(
                    model=model, contents=prompt
                ).text
            except errors.ServerError:
                continue
        time.sleep(2 ** attempt)
    raise RuntimeError("Gemini is busy right now, please try again later")


def read_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def generate_questions(resume, jd, n=5):
    prompt = f"""You are a strict but friendly technical interviewer.
Based on the RESUME and JOB DESCRIPTION below, create {n} interview
questions for a fresher candidate: a mix of technical, project-based
and one HR question.

Return ONLY a JSON list like:
[{{"type": "technical", "question": "..."}}]

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    text = call_gemini(prompt).strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)


if __name__ == "__main__":
    resume = read_pdf("resume.pdf")
    jd = open("jd.txt", encoding="utf-8").read()
    for i, q in enumerate(generate_questions(resume, jd), 1):
        print(f"{i}. [{q['type']}] {q['question']}\n")