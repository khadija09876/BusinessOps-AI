import time
import io
import re
import streamlit as st
from groq import Groq

# ============================================================
# PDF GENERATION
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

# ============================================================
# WORD / DOCX GENERATION
# ============================================================

from docx import Document
from docx.shared import Pt

# ============================================================
# CREWAI FLOW
# ============================================================

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
        max-width: 900px;
        line-height: 1.6;
    }

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

    .report-box {
        background: #0b121c;
        border: 1px solid #203044;
        border-radius: 16px;
        padding: 25px;
        line-height: 1.7;
    }

    .feature-card {
        background: linear-gradient(
            145deg,
            #0d1622,
            #09111b
        );
        border: 1px solid #1e3044;
        border-radius: 14px;
        padding: 18px;
        min-height: 125px;
    }

    .feature-title {
        color: #ffffff;
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .feature-text {
        color: #8493a5;
        font-size: 12px;
        line-height: 1.5;
    }

    .status-card {
        background: #0c131e;
        border: 1px solid #1d2b3d;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }

    .status-title {
        color: #7d8b9d;
        font-size: 10px;
        letter-spacing: 1px;
    }

    .status-value {
        color: #61eaff;
        font-size: 15px;
        font-weight: 700;
        margin-top: 5px;
    }

    .roadmap-card {
        background: #0c131e;
        border-left: 3px solid #61eaff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }

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

    div.stButton > button {
        border-radius: 10px;
        font-weight: 700;
    }

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
# HELPER FUNCTIONS
# ============================================================

def clean_markdown(text):
    """
    Remove markdown formatting for simple PDF/DOCX content.
    """

    if not text:
        return ""

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = text.replace("`", "")

    return text.strip()


def split_report_sections(report_text):
    """
    Split AI report into markdown-style sections.
    """

    sections = {}

    current_title = "Executive Summary"
    current_content = []

    for line in report_text.splitlines():

        line = line.strip()

        if line.startswith("## "):

            if current_content:
                sections[current_title] = "\n".join(
                    current_content
                ).strip()

            current_title = line.replace(
                "## ", ""
            ).strip()

            current_content = []

        elif line.startswith("# "):

            if current_content:
                sections[current_title] = "\n".join(
                    current_content
                ).strip()

            current_title = line.replace(
                "# ", ""
            ).strip()

            current_content = []

        else:

            current_content.append(line)

    if current_content:
        sections[current_title] = "\n".join(
            current_content
        ).strip()

    return sections


def count_bullets(text):
    """
    Count bullet-style action/risk items.
    """

    if not text:
        return 0

    return len(
        [
            line
            for line in text.splitlines()
            if line.strip().startswith(("-", "•", "*"))
        ]
    )


# ============================================================
# PDF GENERATION
# ============================================================

def create_pdf(report_text):

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

    for line in report_text.splitlines():

        line = clean_markdown(line)

        if not line:

            story.append(Spacer(1, 6))
            continue

        if line.startswith("## "):

            heading = line.replace(
                "## ",
                ""
            ).strip()

            story.append(
                Paragraph(
                    heading,
                    heading_style,
                )
            )

        elif line.startswith("# "):

            heading = line.replace(
                "# ",
                ""
            ).strip()

            story.append(
                Paragraph(
                    heading,
                    heading_style,
                )
            )

        elif line.startswith("- "):

            bullet = line[2:].strip()

            safe_bullet = (
                bullet
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    "• " + safe_bullet,
                    body_style,
                )
            )

        else:

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


# ============================================================
# DOCX GENERATION
# ============================================================

def create_docx(report_text):

    document = Document()

    document.add_heading(
        "BusinessOps AI",
        level=0,
    )

    document.add_paragraph(
        "Business Operations Intelligence Report"
    )

    document.add_paragraph("")

    for line in report_text.splitlines():

        line = line.strip()

        if not line:

            document.add_paragraph("")
            continue

        if line.startswith("## "):

            heading = line.replace(
                "## ",
                ""
            ).strip()

            document.add_heading(
                heading,
                level=1,
            )

        elif line.startswith("# "):

            heading = line.replace(
                "# ",
                ""
            ).strip()

            document.add_heading(
                heading,
                level=1,
            )

        elif line.startswith("- "):

            bullet = line[2:].strip()

            paragraph = document.add_paragraph(
                style="List Bullet"
            )

            paragraph.add_run(
                clean_markdown(bullet)
            )

        else:

            paragraph = document.add_paragraph()

            run = paragraph.add_run(
                clean_markdown(line)
            )

            run.font.size = Pt(10.5)

    buffer = io.BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# CREWAI FLOW
# ============================================================

class BusinessOpsFlow(Flow):

    # ========================================================
    # 01 — INTAKE
    # ========================================================

    @start()
    def intake(self):

        return {
            "request": self.state.get(
                "request",
                ""
            ).strip()
        }

    # ========================================================
    # 02 — BUSINESS ANALYSIS
    # ========================================================

    @listen(intake)
    def business_analysis(self, data):

        request = data["request"]

        return {
            "request": request,

            "analysis": (
                "Identify the business objective, stakeholders, "
                "current situation, constraints, business impact, "
                "and expected outcome."
            ),
        }

    # ========================================================
    # 03 — OPERATIONS PLANNING
    # ========================================================

    @listen(business_analysis)
    def operations_planning(self, data):

        return {
            **data,

            "operations": (
                "Design practical operational steps, responsible "
                "roles, dependencies, resources, department impact, "
                "and measurable outcomes."
            ),
        }

    # ========================================================
    # 04 — RISK MANAGEMENT
    # ========================================================

    @listen(operations_planning)
    def risk_management(self, data):

        return {
            **data,

            "risk": (
                "Identify operational, people, technology, "
                "communication, timeline, implementation risks, "
                "and appropriate mitigation strategies."
            ),
        }

    # ========================================================
    # 05 — ACTION PLANNING
    # ========================================================

    @listen(risk_management)
    def action_planning(self, data):

        return {
            **data,

            "actions": (
                "Create prioritized next actions, ownership, "
                "dependencies, implementation phases, KPIs, "
                "and short-term and long-term roadmap items."
            ),
        }

    # ========================================================
    # 06 — QUALITY CONTROL
    # ========================================================

    @listen(action_planning)
    def quality_control(self, data):

        return {
            **data,

            "qa": (
                "Check whether the proposed workflow is practical, "
                "complete, consistent, actionable, measurable, "
                "and clear about missing information and assumptions."
            ),
        }

    # ========================================================
    # FINAL GROQ GENERATION
    # ========================================================

    @listen(quality_control)
    def final_report(self, data):

        if not data["request"]:

            return (
                "Please enter a business request."
            )

        # ----------------------------------------------------
        # GROQ API KEY
        # ----------------------------------------------------

        try:

            api_key = st.secrets[
                "GROQ_API_KEY"
            ]

        except Exception:

            api_key = None

        if not api_key:

            return (
                "GROQ_API_KEY is missing.\n\n"
                "Please add your Groq API key in:\n"
                "Streamlit Cloud → Manage App → Settings → Secrets"
            )

        # ----------------------------------------------------
        # GROQ CLIENT
        # ----------------------------------------------------

        client = Groq(
            api_key=api_key
        )

        # ----------------------------------------------------
        # PROFESSIONAL BUSINESSOPS PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are BusinessOps AI, a professional autonomous
business process intelligence assistant.

Your job is to transform a business problem into
a practical, structured operational plan.

BUSINESS REQUEST:

{data["request"][:2200]}

INTERNAL WORKFLOW:

BUSINESS ANALYSIS:
{data["analysis"]}

OPERATIONS PLANNING:
{data["operations"]}

RISK MANAGEMENT:
{data["risk"]}

ACTION PLANNING:
{data["actions"]}

QUALITY CONTROL:
{data["qa"]}


Generate a professional Business Operations Intelligence Report.

Use EXACTLY these sections:

## Executive Summary

Give a concise overview of the problem, objective,
expected business impact, and recommended direction.

## Business Analysis

Identify:
- Business objective
- Key stakeholders
- Current challenge
- Constraints
- Expected outcome

## Department Impact

Identify relevant departments or business functions
and explain their expected responsibilities or impact.

Do not invent departments if they are not relevant.

## Information Gaps

Identify important information that is missing from
the request.

If there are no critical gaps, write:
"No critical information gaps identified."

Do not invent facts.

## Recommended Workflow

Provide a clear step-by-step operational process.

Use numbered steps where useful.

## Priority Matrix

Classify important actions using:
- Critical
- High
- Medium
- Low

Explain why each important priority matters.

## Risk Register

For the most important risks provide:
- Risk
- Impact
- Likelihood
- Mitigation
- Suggested Owner

Do not create unrealistic risks.

## Priority Actions

Provide practical next actions.

For each action include:
- Action
- Suggested owner
- Priority
- Dependency when relevant

## 30/60/90 Day Roadmap

Organize implementation into:
- First 30 days
- Days 31–60
- Days 61–90

Only include phases appropriate to the business request.

## KPIs / Success Metrics

Provide measurable indicators that could be used
to evaluate whether the process is improving.

Do not invent current performance numbers.

## Process Canvas

Summarize:

Problem:
Objective:
Key Stakeholders:
Main Process:
Key Risks:
Key Outcome:

## QA Audit

Provide an AI quality assessment covering:

- Completeness
- Actionability
- Risk Coverage
- KPI Coverage
- Clarity

Use a score from 1–10 for each dimension.

Give a short reason for each score.

Also identify any remaining assumptions.

GENERAL REQUIREMENTS:

- Be professional and concise.
- Be specific and practical.
- Do not invent company-specific facts.
- Clearly distinguish assumptions from known information.
- Do not claim actions have actually been completed.
- Recommendations should be actionable.
- Avoid unnecessary repetition.
- Keep the complete report approximately 700–850 words maximum.
"""

        # ----------------------------------------------------
        # GROQ REQUEST
        # ----------------------------------------------------

        try:

            response = client.chat.completions.create(

                model=MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are BusinessOps AI, a professional "
                            "business operations intelligence system. "
                            "Return a structured Markdown report using "
                            "the exact requested section headings."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],

                temperature=0.1,

                max_completion_tokens=850,

                reasoning_effort="low",
            )

            result = (
                response
                .choices[0]
                .message
                .content
            )

            if not result or not result.strip():

                return (
                    "The AI returned an empty response. "
                    "Please try again."
                )

            return result.strip()

        # ----------------------------------------------------
        # ERROR HANDLING
        # ----------------------------------------------------

        except Exception as e:

            error_text = str(e).lower()

            if (
                "rate limit" in error_text
                or "429" in error_text
            ):

                time.sleep(3)

                try:

                    retry = client.chat.completions.create(

                        model=MODEL,

                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Generate the requested "
                                    "BusinessOps report concisely."
                                ),
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],

                        temperature=0.1,

                        max_completion_tokens=850,

                        reasoning_effort="low",
                    )

                    retry_result = (
                        retry
                        .choices[0]
                        .message
                        .content
                    )

                    if (
                        retry_result
                        and retry_result.strip()
                    ):

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

    st.write("🐍 Python")
    st.write("🎨 Streamlit")
    st.write("🤖 CrewAI Flow")
    st.write("⚡ Groq API")
    st.write("🧠 GPT-OSS 20B")
    st.write("☁️ Streamlit Cloud")

    st.divider()

    st.markdown("### Intelligence Modules")

    st.write("✓ Business Analysis")
    st.write("✓ Department Impact")
    st.write("✓ Risk Register")
    st.write("✓ Priority Matrix")
    st.write("✓ Action Planning")
    st.write("✓ KPI Design")
    st.write("✓ 30/60/90 Roadmap")
    st.write("✓ QA Audit")

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

    st.caption(
        "Free-tier friendly architecture"
    )

    st.caption(
        "No Ollama • No local model • No paid database"
    )


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
            Transform complex business requests into
            structured operational plans, risk controls,
            priority actions, department responsibilities,
            implementation roadmaps, and measurable outcomes.
        </div>

    </div>
    """
)


# ============================================================
# WORKFLOW STAGES
# ============================================================

st.markdown(
    "### Agentic Workflow"
)

st.caption(
    "Multi-stage CrewAI workflow with one primary Groq generation per run."
)


stages = [

    (
        "01",
        "Business Analyst",
        "Understands the business problem, objective, stakeholders, constraints and expected outcome.",
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
        "Converts recommendations into prioritized next actions and ownership.",
    ),

    (
        "05",
        "KPI Designer",
        "Defines measurable outcomes, KPIs and implementation roadmap.",
    ),

    (
        "06",
        "QA Auditor",
        "Performs final completeness, consistency and quality review.",
    ),
]


cols = st.columns(3)


for i, (
    number,
    title,
    description,
) in enumerate(stages):

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
                AI MODULES
            </div>

            <div class="metric-value">
                08+
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

st.markdown(
    "### Business Request"
)


sample = st.selectbox(

    "Quick scenario",

    [
        "Custom request",
        "Employee Onboarding",
        "Software Rollout",
        "Office Relocation",
        "Customer Support Improvement",
        "Project Management Improvement",
        "Vendor Management",
    ],
)


# ============================================================
# SAMPLE SCENARIOS
# ============================================================

default_text = ""


if sample == "Employee Onboarding":

    default_text = (
        "Our company is growing quickly and new employees are "
        "having difficulty completing HR, IT, security and "
        "department onboarding. Design a better onboarding "
        "process with clear ownership, risk controls and KPIs."
    )


elif sample == "Software Rollout":

    default_text = (
        "A company is introducing a new internal software "
        "platform. Employees need training, communication, "
        "migration support and a controlled rollout plan."
    )


elif sample == "Office Relocation":

    default_text = (
        "Our organization is moving to a new office. We need "
        "a plan covering employees, IT infrastructure, vendors, "
        "communication, facilities and business continuity."
    )


elif sample == "Customer Support Improvement":

    default_text = (
        "Customer support response times are increasing and "
        "customers are complaining about inconsistent answers. "
        "Create an improved support operations workflow."
    )


elif sample == "Project Management Improvement":

    default_text = (
        "Our software projects frequently miss deadlines because "
        "requirements, ownership and dependencies are unclear. "
        "Design an improved project management process."
    )


elif sample == "Vendor Management":

    default_text = (
        "Our company works with multiple external vendors and "
        "has difficulty tracking performance, deadlines, costs "
        "and responsibilities. Create an improved vendor management "
        "process with risks and KPIs."
    )


# ============================================================
# REQUEST INPUT
# ============================================================

request = st.text_area(

    "Describe your business problem or process",

    value=default_text,

    height=180,

    placeholder=(
        "Example: Our company wants to improve employee "
        "onboarding across HR, IT and department teams..."
    ),
)


# ============================================================
# RUN BUSINESSOPS AI
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

        # ----------------------------------------------------
        # WORKFLOW EXECUTION
        # ----------------------------------------------------

        with st.spinner(
            "BusinessOps AI is analyzing the request, "
            "planning operations, evaluating risks and "
            "generating the intelligence report..."
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


        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        st.session_state["businessops_result"] = result
        st.session_state["businessops_request"] = request


# ============================================================
# SHOW REPORT IF AVAILABLE
# ============================================================

if "businessops_result" in st.session_state:

    result = st.session_state[
        "businessops_result"
    ]

    request_used = st.session_state.get(
        "businessops_request",
        ""
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        "Business workflow completed successfully."
    )


    # ========================================================
    # EXECUTION STATUS
    # ========================================================

    st.markdown(
        "### Workflow Status"
    )

    s1, s2, s3, s4, s5, s6 = st.columns(6)

    statuses = [
        ("INTAKE", "COMPLETED"),
        ("ANALYSIS", "COMPLETED"),
        ("OPERATIONS", "COMPLETED"),
        ("RISK", "COMPLETED"),
        ("ACTIONS", "COMPLETED"),
        ("QA", "COMPLETED"),
    ]

    status_cols = [
        s1,
        s2,
        s3,
        s4,
        s5,
        s6,
    ]

    for col, (
        title,
        status,
    ) in zip(
        status_cols,
        statuses
    ):

        with col:

            st.html(
                f"""
                <div class="status-card">

                    <div class="status-title">
                        {title}
                    </div>

                    <div class="status-value">
                        ✓ {status}
                    </div>

                </div>
                """
            )


    # ========================================================
    # PARSE REPORT
    # ========================================================

    sections = split_report_sections(
        result
    )


    # ========================================================
    # DYNAMIC METRICS
    # ========================================================

    risk_count = count_bullets(
        sections.get(
            "Risk Register",
            ""
        )
    )

    action_count = count_bullets(
        sections.get(
            "Priority Actions",
            ""
        )
    )

    gap_count = count_bullets(
        sections.get(
            "Information Gaps",
            ""
        )
    )


    # ========================================================
    # REPORT OVERVIEW
    # ========================================================

    st.markdown(
        "### Intelligence Overview"
    )

    o1, o2, o3, o4 = st.columns(4)


    with o1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    PRIORITY ACTIONS
                </div>

                <div class="metric-value">
                    {action_count if action_count else "—"}
                </div>

            </div>
            """
        )


    with o2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    RISK ITEMS
                </div>

                <div class="metric-value">
                    {risk_count if risk_count else "—"}
                </div>

            </div>
            """
        )


    with o3:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    INFORMATION GAPS
                </div>

                <div class="metric-value">
                    {gap_count if gap_count else "—"}
                </div>

            </div>
            """
        )


    with o4:

        st.html(
            """
            <div class="metric-card">

                <div class="metric-label">
                    LLM GENERATIONS
                </div>

                <div class="metric-value">
                    01
                </div>

            </div>
            """
        )


    # ========================================================
    # REPORT TABS
    # ========================================================

    st.markdown(
        "### Business Intelligence Report"
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📊 Executive View",
            "⚙️ Operations",
            "⚠️ Risk & Priority",
            "🚀 Roadmap",
            "📈 KPIs & QA",
            "📄 Full Report",
        ]
    )


    # ========================================================
    # TAB 1 — EXECUTIVE VIEW
    # ========================================================

    with tab1:

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        executive = sections.get(
            "Executive Summary",
            "Executive summary was not returned."
        )

        st.markdown(
            "#### Executive Summary"
        )

        st.markdown(
            executive
        )

        st.markdown(
            "#### Department Impact"
        )

        st.markdown(
            sections.get(
                "Department Impact",
                "No department impact information returned."
            )
        )

        st.markdown(
            "#### Information Gaps"
        )

        st.markdown(
            sections.get(
                "Information Gaps",
                "No information gaps returned."
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # TAB 2 — OPERATIONS
    # ========================================================

    with tab2:

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        st.markdown(
            "#### Recommended Workflow"
        )

        st.markdown(
            sections.get(
                "Recommended Workflow",
                "No workflow returned."
            )
        )

        st.markdown(
            "#### Process Canvas"
        )

        st.markdown(
            sections.get(
                "Process Canvas",
                "No process canvas returned."
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # TAB 3 — RISK & PRIORITY
    # ========================================================

    with tab3:

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        st.markdown(
            "#### Priority Matrix"
        )

        st.markdown(
            sections.get(
                "Priority Matrix",
                "No priority matrix returned."
            )
        )

        st.divider()

        st.markdown(
            "#### Risk Register"
        )

        st.markdown(
            sections.get(
                "Risk Register",
                "No risk register returned."
            )
        )

        st.markdown(
            "#### Priority Actions"
        )

        st.markdown(
            sections.get(
                "Priority Actions",
                "No priority actions returned."
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # TAB 4 — ROADMAP
    # ========================================================

    with tab4:

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        st.markdown(
            "#### 30 / 60 / 90 Day Roadmap"
        )

        roadmap = sections.get(
            "30/60/90 Day Roadmap",
            "No roadmap returned."
        )

        st.markdown(
            roadmap
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # TAB 5 — KPIs & QA
    # ========================================================

    with tab5:

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        st.markdown(
            "#### KPIs / Success Metrics"
        )

        st.markdown(
            sections.get(
                "KPIs / Success Metrics",
                "No KPI information returned."
            )
        )

        st.divider()

        st.markdown(
            "#### AI QA Audit"
        )

        st.markdown(
            sections.get(
                "QA Audit",
                "No QA audit returned."
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # TAB 6 — FULL REPORT
    # ========================================================

    with tab6:

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        st.markdown(
            result
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # DOWNLOAD REPORTS
    # ========================================================

    st.markdown(
        "### Export Business Report"
    )

    st.caption(
        "Download the generated intelligence report for "
        "sharing, documentation or presentation."
    )


    pdf_file = create_pdf(
        result
    )

    docx_file = create_docx(
        result
    )


    d1, d2, d3 = st.columns(3)


    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    with d1:

        st.download_button(

            "📄 Download TXT",

            data=str(result),

            file_name="businessops_report.txt",

            mime="text/plain",

            use_container_width=True,

        )


    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    with d2:

        st.download_button(

            "📕 Download PDF",

            data=pdf_file,

            file_name="businessops_report.pdf",

            mime="application/pdf",

            use_container_width=True,

        )


    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    with d3:

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


    # ========================================================
    # REQUEST USED
    # ========================================================

    with st.expander(
        "View submitted business request"
    ):

        st.write(
            request_used
        )


# ============================================================
# FEATURE SHOWCASE
# ============================================================

st.write("")

st.markdown(
    "### Business Intelligence Capabilities"
)


feature_data = [

    (
        "🎯",
        "Business Analysis",
        "Transforms an unstructured business problem into objectives, stakeholders, constraints and expected outcomes.",
    ),

    (
        "🏢",
        "Department Impact",
        "Maps relevant business functions and identifies where responsibilities or dependencies exist.",
    ),

    (
        "⚠️",
        "Risk Register",
        "Identifies operational risks with impact, likelihood, mitigation and suggested ownership.",
    ),

    (
        "🔥",
        "Priority Matrix",
        "Organizes important actions according to business urgency and importance.",
    ),

    (
        "🚀",
        "Action Roadmap",
        "Converts recommendations into practical actions and a 30/60/90-day implementation direction.",
    ),

    (
        "📈",
        "KPI Intelligence",
        "Generates measurable success indicators to evaluate whether the process is improving.",
    ),

    (
        "🔎",
        "Information Gaps",
        "Detects missing information and assumptions that could affect implementation quality.",
    ),

    (
        "🛡️",
        "AI QA Audit",
        "Reviews completeness, actionability, risk coverage, KPI coverage and clarity.",
    ),

]


feature_cols = st.columns(4)


for i, (
    icon,
    title,
    description,
) in enumerate(feature_data):

    with feature_cols[i % 4]:

        st.html(
            f"""
            <div class="feature-card">

                <div style="font-size:22px;">
                    {icon}
                </div>

                <div class="feature-title">
                    {title}
                </div>

                <div class="feature-text">
                    {description}
                </div>

            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.html(
    """
    <div class="footer">

        BusinessOps AI • Autonomous Business Process Intelligence
        • CrewAI + Groq • Streamlit Cloud

    </div>
    """
)
