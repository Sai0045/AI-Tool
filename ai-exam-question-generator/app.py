import os
from dotenv import load_dotenv

# 🔥 FORCE load .env from the same folder as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

import streamlit as st
from src.syllabus_parser import parse_syllabus
from src.generator import generate_paper
from src.validators import validate_total_marks, validate_unit_coverage
from src.exporters import (
    export_markdown_paper,
    export_markdown_marking,
    export_json,
    save_outputs
)

# ✅ NEW helper (you must create this file: src/bloom_assigner.py)
from src.bloom_assigner import build_bloom_sequence

st.set_page_config(page_title="AI Exam Question Generator", layout="wide")

st.title("🎓 AI Exam Question Generator (From Syllabus)")
st.write("Generate exam-oriented question papers with **marks, Bloom’s level, model answers, and marking scheme**.")

with st.sidebar:
    st.header("⚙️ Settings")
    title = st.text_input("Paper Title", value="End-Semester Examination")
    seed = st.number_input("Random Seed (optional)", min_value=0, value=7, step=1)

    # ✅ Toggle to use real AI via API
    use_api = st.checkbox("Use API (Real AI)", value=True)

    # ✅ Debug indicator: key loaded or not
    key_loaded = "YES" if os.getenv("GEMINI_API_KEY") else "NO"
    st.caption(f"🔑 GEMINI_API_KEY loaded: **{key_loaded}**")

    st.subheader("🧠 Bloom Level Mix (%)")
    st.caption("Total must be exactly 100%")

    r = st.slider("Remember %", 0, 100, 20, step=5)
    u = st.slider("Understand %", 0, 100, 40, step=5)
    ap = st.slider("Apply %", 0, 100, 20, step=5)
    an = st.slider("Analyze %", 0, 100, 20, step=5)
    ev = st.slider("Evaluate %", 0, 100, 0, step=5)
    cr = st.slider("Create %", 0, 100, 0, step=5)

    bloom_mix = {
        "Remember": r,
        "Understand": u,
        "Apply": ap,
        "Analyze": an,
        "Evaluate": ev,
        "Create": cr
    }

    total_pct = sum(bloom_mix.values())
    if total_pct != 100:
        st.warning(f"⚠️ Bloom mix must total 100%. Current: {total_pct}%")

    st.subheader("🧾 Exam Pattern")
    st.caption("Example: 2 marks x 10, 5 marks x 4, 10 marks x 2")
    n2 = st.number_input("No. of 2-mark questions", min_value=0, value=10, step=1)
    n5 = st.number_input("No. of 5-mark questions", min_value=0, value=4, step=1)
    n10 = st.number_input("No. of 10-mark questions", min_value=0, value=2, step=1)

pattern = ([2] * int(n2)) + ([5] * int(n5)) + ([10] * int(n10))
total_marks = sum(pattern)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📘 Paste Syllabus (Unit-wise)")

    uploaded = st.file_uploader(
        "Upload Syllabus (PDF or TXT)",
        type=["pdf", "txt"]
    )

    default_text = ""

    if uploaded is not None:
        filename = uploaded.name.lower()

        if filename.endswith(".txt"):
            default_text = uploaded.read().decode("utf-8", errors="ignore")

        elif filename.endswith(".pdf"):
            try:
                from src.pdf_utils import extract_text_from_pdf
                file_bytes = uploaded.read()
                extracted = extract_text_from_pdf(file_bytes)

                if not extracted.strip():
                    st.warning(
                        "Could not extract text from this PDF. "
                        "It may be a scanned PDF (image). Please paste syllabus text manually "
                        "or upload a text-based PDF."
                    )
                else:
                    default_text = extracted

            except Exception as e:
                st.error("Failed to read PDF.")
                st.code(str(e))

    syllabus_text = st.text_area(
        "Format example:\nUnit 1: Neural Networks, Activation functions\nUnit 2: Keras APIs, callbacks\n(or bullet list under UNIT headings)",
        value=default_text,
        height=280
    )

with col2:
    st.subheader("📌 Quick Summary")
    st.write(f"**Total Questions:** {len(pattern)}")
    st.write(f"**Total Marks:** {total_marks}")
    st.write(f"**Mode:** {'API (Real AI)' if use_api else 'Offline (Template)'}")

    bloom_mix_str = ", ".join([f"{k}:{v}%" for k, v in bloom_mix.items() if v > 0])
    st.write(f"**Bloom Mix:** {bloom_mix_str}")

if st.button("🚀 Generate Question Paper"):
    if not syllabus_text.strip():
        st.error("Please paste or upload the syllabus first.")
        st.stop()

    if sum(bloom_mix.values()) != 100:
        st.error("Bloom mix must total exactly 100%. Please adjust sliders.")
        st.stop()

    units = parse_syllabus(syllabus_text)

    if not units:
        st.error("Could not detect units/topics. Use 'Unit 1:' format or bullet list under UNIT heading.")
        st.stop()

    # ✅ Create Bloom level list for each question
    bloom_levels = build_bloom_sequence(len(pattern), bloom_mix, seed=int(seed))

    try:
        if use_api:
            if not os.getenv("GEMINI_API_KEY"):
                st.error("GEMINI_API_KEY not found. Put it in your .env file.")
                st.stop()

            from src.prompt_builder import build_prompt
            from src.llm_pipeline import generate_paper_via_api

            prompt = build_prompt(
                title=f"{title} ({total_marks} Marks)",
                total_marks=total_marks,
                units=units,
                pattern=pattern,
                bloom_levels=bloom_levels  # ✅ NEW
            )
            paper = generate_paper_via_api(prompt)

        else:
            # Offline generator still needs a single level, so we pick the most common
            most_common_level = max(bloom_mix, key=bloom_mix.get)

            paper = generate_paper(
                title=f"{title} ({total_marks} Marks)",
                units=units,
                pattern=pattern,
                bloom_preference=most_common_level,
                seed=int(seed)
            )

    except Exception as e:
        st.error("Failed to generate paper.")
        st.code(str(e))
        st.stop()

    errs = []
    errs += validate_total_marks(paper)
    errs += validate_unit_coverage(paper, min_units=2)

    if errs:
        st.warning("Validation warnings:")
        for e in errs:
            st.write(f"- {e}")

    tab1, tab2, tab3 = st.tabs(["📄 Question Paper", "✅ Marking Scheme", "🧩 JSON Output"])

    with tab1:
        md_paper = export_markdown_paper(paper)
        st.markdown(md_paper)

    with tab2:
        md_mark = export_markdown_marking(paper)
        st.markdown(md_mark)

    with tab3:
        json_out = export_json(paper)
        st.code(json_out, language="json")

    save_outputs(paper, outdir="outputs")

    st.success("Saved files in /outputs ✅")
    st.download_button("⬇️ Download Question Paper (MD)", md_paper, file_name="question_paper.md")
    st.download_button("⬇️ Download Marking Scheme (MD)", md_mark, file_name="marking_scheme.md")
    st.download_button("⬇️ Download Full JSON", json_out, file_name="generated_paper.json")
