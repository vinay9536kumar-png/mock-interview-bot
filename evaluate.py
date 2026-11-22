import json
from questions import call_gemini


def evaluate_answer(question, answer, jd):
    prompt = f"""You are a fair technical interviewer evaluating a fresher.

QUESTION: {question}
CANDIDATE ANSWER: {answer}
JOB DESCRIPTION (for context): {jd}

Return ONLY JSON in this format:
{{
  "score": <integer 0-10>,
  "strengths": ["..."],
  "improvements": ["..."],
  "ideal_answer": "a short model answer in 3-4 lines"
}}
"""
    text = call_gemini(prompt).strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)


if __name__ == "__main__":
    from questions import read_pdf, generate_questions

    resume = read_pdf("resume.pdf")
    jd = open("jd.txt", encoding="utf-8").read()
    questions = generate_questions(resume, jd, n=3)

    total = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i} [{q['type']}]: {q['question']}")
        ans = input("Your answer: ")
        res = evaluate_answer(q["question"], ans, jd)
        total += res["score"]
        print(f"\nScore: {res['score']}/10")
        print("Strengths:", "; ".join(res["strengths"]))
        print("Improve:", "; ".join(res["improvements"]))
        print("Ideal:", res["ideal_answer"])

    print(f"\nFinal Score: {total}/{len(questions) * 10}")