import tempfile
import streamlit as st
from questions import read_pdf, generate_questions
from evaluate import evaluate_answer

st.set_page_config(page_title="AI Mock Interview Bot", page_icon="🎤")
st.title("🎤 AI Mock Interview Bot")

# Session state
for key, default in {"questions": [], "index": 0, "results": [], "jd": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Setup screen
if not st.session_state.questions:
    resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    jd = st.text_area("Paste the job description", height=200)
    n = st.slider("Number of questions", 3, 8, 5)

    if st.button("Start interview") and resume_file and jd.strip():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume_file.read())
        with st.spinner("Preparing your questions..."):
            resume = read_pdf(tmp.name)
            st.session_state.questions = generate_questions(resume, jd, n)
            st.session_state.jd = jd
        st.rerun()

# Interview screen
else:
    qs = st.session_state.questions
    i = st.session_state.index

    if i < len(qs):
        q = qs[i]
        st.progress(i / len(qs))
        st.subheader(f"Question {i + 1} of {len(qs)}  ({q['type']})")
        st.write(q["question"])
        answer = st.text_area("Your answer", key=f"ans_{i}", height=150)

        if st.button("Submit answer") and answer.strip():
            with st.spinner("Evaluating..."):
                res = evaluate_answer(q["question"], answer, st.session_state.jd)
            st.session_state.results.append({"question": q["question"], "answer": answer, **res})
            st.session_state.index += 1
            st.rerun()

    else:
        results = st.session_state.results
        total = sum(r["score"] for r in results)
        st.success(f"Interview complete! Final score: {total}/{len(results) * 10}")

        for n, r in enumerate(results, 1):
            with st.expander(f"Q{n}: {r['question']}  ({r['score']}/10)"):
                st.markdown("**Your answer:** " + r["answer"])
                st.markdown("**Strengths:** " + "; ".join(r["strengths"]))
                st.markdown("**Improve:** " + "; ".join(r["improvements"]))
                st.markdown("**Ideal answer:** " + r["ideal_answer"])

        if st.button("Start a new interview"):
            for key in ["questions", "index", "results", "jd"]:
                del st.session_state[key]
            st.rerun()