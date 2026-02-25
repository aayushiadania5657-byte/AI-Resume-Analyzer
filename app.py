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

    st.markdown("---")
    st.caption("⚠ Note: This system provides automated analysis based on keyword matching. It may not fully represent the candidate's complete capability or experience.")