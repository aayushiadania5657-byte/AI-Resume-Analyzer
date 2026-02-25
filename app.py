import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>
.main {background-color: #0f172a;}
h1, h2, h3 {color: #e2e8f0;}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI Resume Analyzer & Job Match System</h1>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# -------------------------
# SKILL DATABASE
# -------------------------
skills_db = {
    "Data Analyst": ["python", "sql", "excel", "power bi", "statistics", "tableau"],
    "Web Developer": ["html", "css", "javascript", "react", "node", "bootstrap"],
    "Java Developer": ["java", "spring", "hibernate", "jdbc", "oop", "mysql"],
    "Python Developer": ["python", "django", "flask", "pandas", "numpy"],
    "Software Engineer": ["data structures", "algorithms", "oop", "git", "problem solving"],
    "HR Manager": ["recruitment", "communication", "interviewing", "payroll", "hr policies"],
    "Marketing Executive": ["seo", "digital marketing", "social media", "branding", "sales"],
    "Graphic Designer": ["photoshop", "illustrator", "figma", "creativity", "canva"]
}

selected_role = st.sidebar.selectbox("🎯 Select Job Role", list(skills_db.keys()))
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
st.markdown("""
<div style="
    background-color:#1e293b;
    padding:12px;
    border-radius:10px;
    border:1px solid #2563eb;
    text-align:center;
    font-size:14px;
    color:#e2e8f0;
">
📄 <b>Upload PDF under 50 MB</b> <br>
For best results, use ATS-friendly resume format.
</div>
""", unsafe_allow_html=True)


# -------------------------
# MAIN LOGIC
# -------------------------
if uploaded_file is not None:

    # Extract Text
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""

    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text.lower()

    selected_skills = skills_db[selected_role]

    # Skill Detection
    found_skills = []
    for skill in selected_skills:
        if skill in resume_text:
            found_skills.append(skill)

    missing_skills = list(set(selected_skills) - set(found_skills))
    match_percentage = (len(found_skills) / len(selected_skills)) * 100
    # -------------------------
    # AUTOMATIC ROLE RECOMMENDATION
    # -------------------------
    role_scores = {}

    for role, skills in skills_db.items():
        matched = 0
        for skill in skills:
            if skill in resume_text:
                matched += 1
        score = (matched / len(skills)) * 100
        role_scores[role] = score

    best_role = max(role_scores, key=role_scores.get)
    best_score = role_scores[best_role]

    st.subheader("🤖 Recommended Job Role")
    st.success(f"Best Matched Role: {best_role} ({round(best_score,2)}%)")
    # -------------------------
    # RESUME WRITING QUALITY SCORE
    # -------------------------
    action_verbs = ["developed", "implemented", "designed", "built", "created", "improved"]
    weak_words = ["hardworking", "team player", "dedicated", "passionate"]

    verb_count = sum(resume_text.count(word) for word in action_verbs)
    weak_count = sum(resume_text.count(word) for word in weak_words)

    numbers_found = len(re.findall(r'\d+%', resume_text))

    writing_score = (verb_count * 5) + (numbers_found * 5) - (weak_count * 3)
    writing_score = max(0, min(writing_score, 100))

    st.subheader("✍ Resume Writing Quality Score")
    st.progress(writing_score)
    st.write(f"Score: {writing_score} / 100")

    if writing_score >= 70:
        st.success("Strong and Impactful Resume Writing!")
    elif writing_score >= 40:
        st.info("Good Resume but can be improved with quantified achievements.")
    else:
        st.warning("Add more action verbs and measurable achievements.")



    # Experience Detection
    experience_pattern = r'(\d+)\s*(years|year)'
    experience_matches = re.findall(experience_pattern, resume_text)
    total_exp = sum(int(match[0]) for match in experience_matches) if experience_matches else 0

    # Education Detection
    education_keywords = ["b.tech", "m.tech", "bachelor", "master", "mba", "bca", "mca"]
    education_found = [edu.upper() for edu in education_keywords if edu in resume_text]

    # -------------------------
    # DISPLAY METRICS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric("📊 Match Percentage", f"{round(match_percentage,2)} %")

    with col2:
        st.metric("⏳ Experience", f"{total_exp} Years")

    st.subheader("🎓 Education Detected")
    for edu in education_found:
        st.success(edu)

    # -------------------------
    # ATS SCORE
    # -------------------------
    skill_component = (len(found_skills) / len(selected_skills)) * 40
    job_component = (match_percentage / 100) * 30
    experience_component = 20 if total_exp > 0 else 0
    education_component = 10 if education_found else 0

    ats_score = skill_component + job_component + experience_component + education_component
    # -------------------------
    # SCORE BREAKDOWN
    # -------------------------
    st.subheader("📊 Detailed Score Breakdown")

    colA, colB, colC, colD = st.columns(4)

    with colA:
        st.metric("Skills Score", f"{round(skill_component,2)} / 40")

    with colB:
        st.metric("Job Match Score", f"{round(job_component,2)} / 30")

    with colC:
        st.metric("Experience Score", f"{experience_component} / 20")

    with colD:
        st.metric("Education Score", f"{education_component} / 10")

    # -------------------------
    # RESUME SUMMARY
    # -------------------------
    st.subheader("📋 Resume Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎯 Selected Role", selected_role)

    with col2:
        st.metric("✅ Skills Matched", f"{len(found_skills)} / {len(selected_skills)}")

    with col3:
        st.metric("🤖 ATS Score", f"{round(ats_score,2)} / 100")

    # -------------------------
    # ATS DISPLAY
    # -------------------------
    st.subheader("🤖 ATS Compatibility Score")
    st.progress(int(ats_score))
    st.write(f"### {round(ats_score,2)} / 100")

    # Badge
    if ats_score >= 85:
        st.success("🏆 Elite Candidate")
    elif ats_score >= 70:
        st.info("🥇 Strong Profile")
    elif ats_score >= 50:
        st.warning("🛠 Improving Candidate")
    else:
        st.error("⚠ Needs Major Improvement")

    # -------------------------
    # SKILL LIST
    # -------------------------
    st.subheader("✅ Matched Skills")
    st.write(found_skills)

    st.subheader("❌ Missing Skills")
    st.write(missing_skills)
    # -------------------------
    # PROJECTED IMPROVEMENT
    # -------------------------
    if missing_skills:
        potential_skill_score = 40
        potential_job_score = 30

        projected_score = potential_skill_score + potential_job_score + experience_component + education_component
        projected_score = min(projected_score, 100)

        st.subheader("🚀 Projected ATS Score After Improvements")

        st.info(
            f"If you add the missing skills, your ATS score can improve "
            f"from {round(ats_score,2)} → {round(projected_score,2)}"
        )

    # -------------------------
    # IMPROVEMENT SUGGESTIONS
    # -------------------------
    st.subheader("💡 Improvement Suggestions")

    if missing_skills:
        for skill in missing_skills:
            st.info(f"Consider adding {skill.upper()} to improve your profile.")
    else:
        st.success("Your resume matches all required skills for this role!")

    # -------------------------
    # PIE CHART
    # -------------------------
    st.subheader("📈 Skill Distribution")
    labels = ["Matched", "Missing"]
    sizes = [len(found_skills), len(missing_skills)]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)

    # -------------------------
    # PDF REPORT
    # -------------------------
    if st.button("📥 Download Analysis Report"):

        file_path = "Resume_Report.pdf"
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("AI Resume Analysis Report", styles['Title']))
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph(f"Selected Role: {selected_role}", styles['Normal']))
        elements.append(Paragraph(f"Match Percentage: {round(match_percentage,2)} %", styles['Normal']))
        elements.append(Paragraph(f"ATS Score: {round(ats_score,2)} / 100", styles['Normal']))
        elements.append(Paragraph(f"Total Experience: {total_exp} Years", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("Matched Skills:", styles['Heading2']))
        for skill in found_skills:
            elements.append(Paragraph(f"- {skill.upper()}", styles['Normal']))

        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph("Missing Skills:", styles['Heading2']))
        for skill in missing_skills:
            elements.append(Paragraph(f"- {skill.upper()}", styles['Normal']))

        doc.build(elements)

        with open(file_path, "rb") as f:
            st.download_button("Click Here to Download", f, file_name="Resume_Report.pdf")
            st.markdown("""
---
### 🧠 How This System Works

This AI Resume Analyzer uses structured scoring logic based on:

• Skill relevance matching  
• Experience detection  
• Education qualification parsing  
• Weighted ATS compatibility scoring  
• Predictive improvement modeling  

The system evaluates resume strength and estimates potential score improvements
based on missing skill additions.
""")

    st.markdown("---")
    st.caption("⚠ Note: This system provides automated analysis based on keyword matching. It may not fully represent the candidate's complete capability or experience.")