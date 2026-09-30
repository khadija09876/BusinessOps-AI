import time
import io
import streamlit as st
from groq import Groq

# PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

# Word / DOCX generation
from docx import Document
from docx.shared import Pt


# CrewAI Flow
from crewai.flow import Flow, start, listen


# ============================================================
# BUSINESSOPS AI
# Autonomous Business Process Intelligence Platform
# ============================================================

st.set_page_config(
    page_title="BusinessOps AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIG
# ============================================================

MODEL = "openai/gpt-oss-20b"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 229, 255, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(139, 92, 246, 0.08),
                transparent 30%
            ),
            #070b12;
        color: #f4f7fb;
    }

    section[data-testid="stSidebar"] {
        background: #090e17;
        border-right: 1px solid #1c2635;
    }

    /* HERO */

    .hero {
        padding: 35px 10px 25px 10px;
    }

    .badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 30px;
        border: 1px solid #1e90a8;
        background: rgba(0, 229, 255, 0.08);
        color: #62eaff;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .hero-title {
        font-size: 48px;
        margin: 15px 0 8px 0;
        font-weight: 800;
        color: #ffffff;
    }

    .hero-text {
        color: #9ba8b8;
        font-size: 17px;
        max-width: 850px;
        line-height: 1.6;
    }

    /* WORKFLOW CARDS */

    .stage {
        background: linear-gradient(
            145deg,
            rgba(18, 27, 40, 0.98),
            rgba(9, 15, 24, 0.98)
        );
        border: 1px solid #1d2a3b;
        border-radius: 15px;
        padding: 20px;
        min-height: 155px;
        margin-bottom: 12px;
        box-sizing: border-box;
    }

    .stage-number {
        color: #61eaff;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .stage-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 750;
        margin-top: 10px;
    }

    .stage-text {
        color: #8f9dad;
        font-size: 13px;
        margin-top: 10px;
        line-height: 1.55;
    }

    /* METRIC CARDS */

    .metric-card {
        background: #0c131e;
        border: 1px solid #1c2939;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        min-height: 95px;
    }

    .metric-label {
        color: #7e8b9b;
        font-size: 11px;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* REPORT */

    .report-box {
        background: #0b121c;
        border: 1px solid #203044;
        border-radius: 16px;
        padding: 25px;
        line-height: 1.7;
    }

    /* SIDEBAR */

    .sidebar-title {
        color: #ffffff;
        font-size: 21px;
        font-weight: 800;
    }

    .sidebar-subtitle {
        color: #7f8c9d;
        font-size: 12px;
        line-height: 1.5;
    }

    /* BUTTON */

    div.stButton > button {
        border-radius: 10px;
        font-weight: 700;
    }

    /* FOOTER */

    .footer {
        text-align: center;
        color: #667386;
        font-size: 12px;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# REPORT GENERATION FUNCTIONS
# ============================================================

def create_pdf(report_text):
    """
    Convert the generated BusinessOps report into a PDF.
    """

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
        title="BusinessOps AI Report",
        author="BusinessOps AI",
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_LEFT
    title_style.fontSize = 20
    title_style.leading = 25

    heading_style = styles["Heading2"]
    heading_style.fontSize = 14
    heading_style.leading = 18
    heading_style.spaceBefore = 12
    heading_style.spaceAfter = 7

    body_style = styles["BodyText"]
    body_style.fontSize = 10
    body_style.leading = 15
    body_style.spaceAfter = 7

    story = []

    story.append(
        Paragraph(
            "BusinessOps AI",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Business Operations Intelligence Report",
            heading_style,
        )
    )

    story.append(Spacer(1, 10))

    # Process report line by line
    for line in report_text.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        if line.startswith("## "):

            heading = line.replace("## ", "").strip()

            story.append(
                Paragraph(
                    heading,
                    heading_style,
                )
            )

        elif line.startswith("# "):

            heading = line.replace("# ", "").strip()

            story.append(
                Paragraph(
                    heading,
                    heading_style,
                )
            )

        elif line.startswith("- "):

            bullet = line[2:].strip()

            story.append(
                Paragraph(
                    "• " + bullet,
                    body_style,
                )
            )

        else:

            # Escape special characters for ReportLab
            safe_line = (
                line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    safe_line,
                    body_style,
                )
            )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


def create_docx(report_text):
    """
    Convert the generated BusinessOps report into a Word DOCX file.
    """

    document = Document()

    # Document title
    title = document.add_heading(
        "BusinessOps AI",
        level=0,
    )

    document.add_paragraph(
        "Business Operations Intelligence Report"
    )

    document.add_paragraph("")

    # Process report line by line
    for line in report_text.splitlines():

        line = line.strip()

        if not line:
            document.add_paragraph("")
            continue

        if line.startswith("## "):

            heading = line.replace("## ", "").strip()

            document.add_heading(
                heading,
                level=1,
            )

        elif line.startswith("# "):

            heading = line.replace("# ", "").strip()

            document.add_heading(
                heading,
                level=1,
            )

        elif line.startswith("- "):

            bullet = line[2:].strip()

            paragraph = document.add_paragraph(
                style="List Bullet"
            )

            paragraph.add_run(bullet)

        else:

            paragraph = document.add_paragraph()

            run = paragraph.add_run(line)

            run.font.size = Pt(10.5)

    # Save DOCX to memory
    buffer = io.BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# CREWAI FLOW
# ============================================================

class BusinessOpsFlow(Flow):

    # --------------------------------------------------------
    # 01 — INTAKE
    # --------------------------------------------------------

    @start()
    def intake(self):

        return {
            "request": self.state.get("request", "").strip()
        }

    # --------------------------------------------------------
    # 02 — BUSINESS ANALYSIS
    # --------------------------------------------------------

    @listen(intake)
    def business_analysis(self, data):

        request = data["request"]

        return {
            "request": request,

            "analysis": (
                "Identify the business objective, stakeholders, "
                "current situation, constraints, and expected outcome."
            ),
        }

    # --------------------------------------------------------
    # 03 — OPERATIONS PLANNING
    # --------------------------------------------------------

    @listen(business_analysis)
    def operations_planning(self, data):

        return {
            **data,

            "operations": (
                "Design practical operational steps, responsible roles, "
                "dependencies, resources, and measurable outcomes."
            ),
        }

    # --------------------------------------------------------
    # 04 — RISK MANAGEMENT
    # --------------------------------------------------------

    @listen(operations_planning)
    def risk_management(self, data):

        return {
            **data,

            "risk": (
                "Identify operational, people, technology, communication, "
                "timeline, and implementation risks."
            ),
        }

    # --------------------------------------------------------
    # 05 — ACTION PLANNING
    # --------------------------------------------------------

    @listen(risk_management)
    def action_planning(self, data):

        return {
            **data,

            "actions": (
                "Create prioritized next actions and define what should "
                "happen immediately, next, and later."
            ),
        }

    # --------------------------------------------------------
    # 06 — QUALITY CONTROL
    # --------------------------------------------------------

    @listen(action_planning)
    def quality_control(self, data):

        return {
            **data,

            "qa": (
                "Check whether the proposed workflow is practical, "
                "complete, consistent, and measurable."
            ),
        }

    # --------------------------------------------------------
    # FINAL GROQ GENERATION
    # --------------------------------------------------------

    @listen(quality_control)
    def final_report(self, data):

        if not data["request"]:
            return "Please enter a business request."

        # --------------------------------------------
        # GET GROQ API KEY
        # --------------------------------------------

        try:
            api_key = st.secrets["GROQ_API_KEY"]

        except Exception:
            api_key = None

        if not api_key:

            return (
                "GROQ_API_KEY is missing.\n\n"
                "Please add your Groq API key in:\n"
                "Streamlit Cloud → Manage App → Settings → Secrets"
            )

        # --------------------------------------------
        # GROQ CLIENT
        # --------------------------------------------

        client = Groq(api_key=api_key)

        # --------------------------------------------
        # COMPACT PROMPT
        # --------------------------------------------

        prompt = f"""
You are BusinessOps AI, an autonomous business process
intelligence assistant.

Analyze the following business request:

{data["request"][:2200]}

Internal workflow analysis:

BUSINESS ANALYSIS:
{data["analysis"]}

OPERATIONS:
{data["operations"]}

RISK MANAGEMENT:
{data["risk"]}

ACTION PLANNING:
{data["actions"]}

QUALITY CONTROL:
{data["qa"]}

Create a professional Business Operations Report.

Use these sections:

## Executive Summary

## Business Analysis

## Recommended Workflow

## Risks & Mitigations

## Priority Actions

## KPIs / Success Metrics

## QA Check

Requirements:

- Be practical.
- Be specific.
- Do not invent company-specific facts.
- Use professional language.
- Give actionable recommendations.
- Keep the report concise.
- Maximum approximately 450 words.
"""

        # --------------------------------------------
        # GROQ REQUEST
        # --------------------------------------------

        try:

            response = client.chat.completions.create(
                model=MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional business operations "
                            "intelligence assistant. Produce concise, "
                            "structured and actionable business reports."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],

                temperature=0.1,

                max_completion_tokens=600,

                reasoning_effort="low",
            )

            result = response.choices[0].message.content

            if not result or not result.strip():

                return (
                    "The AI returned an empty response. "
                    "Please try again."
                )

            return result.strip()

        # --------------------------------------------
        # ERROR HANDLING
        # --------------------------------------------

        except Exception as e:

            error_text = str(e).lower()

            # Rate limit retry
            if "rate limit" in error_text or "429" in error_text:

                time.sleep(3)

                try:

                    retry = client.chat.completions.create(
                        model=MODEL,

                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],

                        temperature=0.1,

                        max_completion_tokens=600,

                        reasoning_effort="low",
                    )

                    retry_result = (
                        retry
                        .choices[0]
                        .message
                        .content
                    )

                    if retry_result and retry_result.strip():

                        return retry_result.strip()

                    return (
                        "Groq returned an empty response "
                        "after the retry."
                    )

                except Exception as retry_error:

                    return (
                        "Groq rate limit is temporarily active.\n\n"
                        "Please wait a few seconds and run the "
                        "business analysis again.\n\n"
                        f"Technical detail: {retry_error}"
                    )

            return (
                "BusinessOps AI could not complete the analysis.\n\n"
                f"Technical detail: {e}"
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-title">
            ⚡ BusinessOps AI
        </div>

        <div class="sidebar-subtitle">
            Autonomous Business Process Intelligence Platform
        </div>
        """
    )

    st.divider()

    st.markdown("### Technology")

    st.write("🐍 Python 3.12")
    st.write("🎨 Streamlit")
    st.write("🤖 CrewAI Flow")
    st.write("⚡ Groq API")
    st.write("🧠 GPT-OSS 20B")
    st.write("☁️ Streamlit Cloud")

    st.divider()

    st.markdown("### Architecture")

    st.markdown(
        """
        **Single Groq generation + multi-stage CrewAI Flow**

        The workflow contains multiple business intelligence
        stages while keeping the actual LLM generation to
        one primary request per run.
        """
    )

    st.divider()

    st.caption("Free-tier friendly architecture")
    st.caption("No Ollama • No local model • No paid database")


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <span class="badge">
            AUTONOMOUS BUSINESS INTELLIGENCE
        </span>

        <div class="hero-title">
            BusinessOps AI
        </div>

        <div class="hero-text">
            Transform complex business requests into structured
            operational plans, risk controls, priority actions,
            and measurable outcomes using an agentic AI workflow.
        </div>

    </div>
    """
)


# ============================================================
# WORKFLOW STAGES
# ============================================================

st.markdown("### Agentic Workflow")

stages = [
    (
        "01",
        "Business Analyst",
        "Understands the business problem, objective, stakeholders and constraints.",
    ),
    (
        "02",
        "Operations Planner",
        "Converts the problem into an executable operational workflow.",
    ),
    (
        "03",
        "Risk Manager",
        "Identifies implementation risks and practical mitigation strategies.",
    ),
    (
        "04",
        "Action Planner",
        "Converts recommendations into prioritized next actions.",
    ),
    (
        "05",
        "KPI Designer",
        "Defines measurable outcomes and success indicators.",
    ),
    (
        "06",
        "QA Auditor",
        "Performs a final quality and consistency review.",
    ),
]


cols = st.columns(3)


for i, (number, title, description) in enumerate(stages):

    with cols[i % 3]:

        st.html(
            f"""
            <div class="stage">

                <div class="stage-number">
                    {number} / 06
                </div>

                <div class="stage-title">
                    {title}
                </div>

                <div class="stage-text">
                    {description}
                </div>

            </div>
            """
        )


# ============================================================
# METRICS
# ============================================================

st.write("")

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.html(
        """
        <div class="metric-card">

            <div class="metric-label">
                WORKFLOW STAGES
            </div>

            <div class="metric-value">
                06
            </div>

        </div>
        """
    )


with m2:

    st.html(
        """
        <div class="metric-card">

            <div class="metric-label">
                LLM CALLS / RUN
            </div>

            <div class="metric-value">
                01
            </div>

        </div>
        """
    )


with m3:

    st.html(
        """
        <div class="metric-card">

            <div class="metric-label">
                MODEL
            </div>

            <div class="metric-value">
                20B
            </div>

        </div>
        """
    )


with m4:

    st.html(
        """
        <div class="metric-card">

            <div class="metric-label">
                DEPLOYMENT
            </div>

            <div class="metric-value">
                CLOUD
            </div>

        </div>
        """
    )


# ============================================================
# BUSINESS REQUEST
# ============================================================

st.write("")

st.markdown("### Business Request")


sample = st.selectbox(
    "Quick scenario",

    [
        "Custom request",
        "Employee Onboarding",
        "Software Rollout",
        "Office Relocation",
        "Customer Support Improvement",
    ],
)


# ============================================================
# SAMPLE SCENARIOS
# ============================================================

default_text = ""


if sample == "Employee Onboarding":

    default_text = (
        "Our company is growing quickly and new employees are having "
        "difficulty completing HR, IT, security and department onboarding. "
        "Design a better onboarding process."
    )


elif sample == "Software Rollout":

    default_text = (
        "A company is introducing a new internal software platform. "
        "Employees need training, communication, migration support and "
        "a controlled rollout plan."
    )


elif sample == "Office Relocation":

    default_text = (
        "Our organization is moving to a new office. We need a plan "
        "covering employees, IT infrastructure, vendors, communication, "
        "facilities and business continuity."
    )


elif sample == "Customer Support Improvement":

    default_text = (
        "Customer support response times are increasing and customers "
        "are complaining about inconsistent answers. Create an improved "
        "support operations workflow."
    )


# ============================================================
# REQUEST INPUT
# ============================================================

request = st.text_area(
    "Describe your business problem or process",

    value=default_text,

    height=170,

    placeholder=(
        "Example: Our company wants to improve "
        "employee onboarding..."
    ),
)


# ============================================================
# EXECUTE BUSINESSOPS AI
# ============================================================

if st.button(
    "⚡ RUN BUSINESSOPS AI",

    type="primary",

    use_container_width=True,
):

    if not request.strip():

        st.warning(
            "Please enter a business request first."
        )

    else:

        with st.spinner(
            "BusinessOps AI is analyzing the request "
            "and generating the report..."
        ):

            try:

                flow = BusinessOpsFlow()

                flow.state["request"] = request

                result = flow.kickoff()

            except Exception as flow_error:

                result = (
                    "BusinessOps AI encountered an error.\n\n"
                    f"{flow_error}"
                )

        st.success(
            "Business workflow completed."
        )

        st.markdown(
            "### Intelligence Report"
        )

        # ====================================================
        # REPORT DISPLAY
        # ====================================================

        st.markdown(
            f"""
            <div class="report-box">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(result)

        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # REPORT DOWNLOADS
        # ====================================================

        st.markdown("### Download Report")

        # Create all formats
        pdf_file = create_pdf(result)
        docx_file = create_docx(result)

        download_col1, download_col2, download_col3 = st.columns(3)


        # ----------------------------------------------------
        # TXT
        # ----------------------------------------------------

        with download_col1:

            st.download_button(
                "📄 Download TXT",

                data=str(result),

                file_name="businessops_report.txt",

                mime="text/plain",

                use_container_width=True,

            )


        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        with download_col2:

            st.download_button(
                "📕 Download PDF",

                data=pdf_file,

                file_name="businessops_report.pdf",

                mime="application/pdf",

                use_container_width=True,

            )


        # ----------------------------------------------------
        # WORD / DOCX
        # ----------------------------------------------------

        with download_col3:

            st.download_button(
                "📝 Download Word",

                data=docx_file,

                file_name="businessops_report.docx",

                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),

                use_container_width=True,

            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.html(
    """
    <div class="footer">
        BusinessOps AI • Autonomous Business Process Intelligence
        • CrewAI + Groq • Free-tier deployment architecture
    </div>
    """
)
