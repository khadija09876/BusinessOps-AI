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
# PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 5%,
                rgba(0, 229, 255, 0.13),
                transparent 27%
            ),
            radial-gradient(
                circle at 92% 8%,
                rgba(139, 92, 246, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(236, 72, 153, 0.07),
                transparent 32%
            ),
            #05080f;

        color: #f7f9fc;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* ======================================================
       REMOVE DEFAULT STREAMLIT UI
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #080d17 0%,
                #060a12 100%
            );

        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .side-brand {
        padding: 16px 14px 20px 14px;
    }

    .side-logo {
        width: 44px;
        height: 44px;
        border-radius: 13px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 21px;
        font-weight: 900;

        color: #ffffff;

        background:
            linear-gradient(
                135deg,
                #00e5ff,
                #7c3aed 55%,
                #ec4899
            );

        box-shadow:
            0 10px 35px rgba(0,229,255,0.18);
    }

    .side-title {
        margin-top: 13px;
        font-size: 21px;
        font-weight: 850;
        color: #ffffff;
        letter-spacing: -0.4px;
    }

    .side-subtitle {
        margin-top: 5px;
        color: #7f8da1;
        font-size: 11px;
        line-height: 1.6;
    }

    .side-status {
        margin-top: 18px;
        padding: 12px 13px;
        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                rgba(0,229,255,0.07),
                rgba(124,58,237,0.08)
            );

        border: 1px solid rgba(0,229,255,0.14);
    }

    .side-status-label {
        color: #718096;
        font-size: 9px;
        letter-spacing: 1.3px;
        font-weight: 800;
    }

    .side-status-value {
        color: #67e8f9;
        font-size: 13px;
        font-weight: 750;
        margin-top: 5px;
    }

    .side-mini {
        color: #64748b;
        font-size: 10px;
        margin-top: 14px;
        line-height: 1.6;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero-wrap {
        position: relative;
        overflow: hidden;

        padding: 48px 48px 44px 48px;

        border-radius: 28px;

        background:
            radial-gradient(
                circle at 80% 10%,
                rgba(124,58,237,0.24),
                transparent 35%
            ),
            radial-gradient(
                circle at 15% 80%,
                rgba(0,229,255,0.13),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                rgba(13,22,37,0.97),
                rgba(8,13,24,0.97)
            );

        border: 1px solid rgba(255,255,255,0.08);

        box-shadow:
            0 25px 80px rgba(0,0,0,0.32);

        margin-bottom: 30px;
    }

    .hero-wrap::after {
        content: "";

        position: absolute;

        width: 260px;
        height: 260px;

        right: -100px;
        bottom: -130px;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                rgba(0,229,255,0.12),
                rgba(236,72,153,0.12)
            );

        filter: blur(20px);
    }

    .hero-top {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        padding: 7px 12px;

        border-radius: 30px;

        background:
            linear-gradient(
                90deg,
                rgba(0,229,255,0.09),
                rgba(124,58,237,0.10)
            );

        border: 1px solid rgba(0,229,255,0.20);

        color: #67e8f9;

        font-size: 10px;
        font-weight: 850;
        letter-spacing: 1.5px;
    }

    .hero-title {
        margin-top: 17px;

        font-size: clamp(42px, 6vw, 72px);

        line-height: 0.98;

        font-weight: 900;

        letter-spacing: -3px;

        background:
            linear-gradient(
                100deg,
                #ffffff 5%,
                #dffaff 38%,
                #8be9ff 62%,
                #b9a3ff 88%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        margin-top: 17px;

        max-width: 850px;

        color: #9aa8ba;

        font-size: 16px;

        line-height: 1.75;
    }

    .hero-line {
        width: 125px;
        height: 3px;

        margin-top: 25px;

        border-radius: 20px;

        background:
            linear-gradient(
                90deg,
                #00e5ff,
                #7c3aed,
                #ec4899
            );
    }

    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-title {
        color: #f8fafc;
        font-size: 23px;
        font-weight: 850;
        letter-spacing: -0.5px;
        margin-top: 25px;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #718096;
        font-size: 12px;
        margin-bottom: 18px;
    }

    /* ======================================================
       WORKFLOW CARDS
       ====================================================== */

    .stage {
        position: relative;

        background:
            linear-gradient(
                145deg,
                rgba(16,25,40,0.98),
                rgba(8,14,24,0.98)
            );

        border: 1px solid rgba(255,255,255,0.075);

        border-radius: 18px;

        padding: 21px;

        min-height: 176px;

        margin-bottom: 12px;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stage:hover {
        transform: translateY(-3px);

        border-color:
            rgba(0,229,255,0.28);

        box-shadow:
            0 18px 45px rgba(0,0,0,0.22);
    }

    .stage-number {
        color: #67e8f9;

        font-size: 10px;

        font-weight: 850;

        letter-spacing: 1.4px;
    }

    .stage-title {
        color: #ffffff;

        font-size: 17px;

        font-weight: 800;

        margin-top: 11px;

        letter-spacing: -0.2px;
    }

    .stage-text {
        color: #7f8da1;

        font-size: 12px;

        margin-top: 9px;

        line-height: 1.65;
    }

    .stage-dot {
        position: absolute;

        top: 20px;
        right: 20px;

        width: 8px;
        height: 8px;

        border-radius: 50%;

        background: #00e5ff;

        box-shadow:
            0 0 15px rgba(0,229,255,0.8);
    }

    /* ======================================================
       METRICS
       ====================================================== */

    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(14,22,35,0.96),
                rgba(8,13,23,0.96)
            );

        border: 1px solid rgba(255,255,255,0.065);

        border-radius: 16px;

        padding: 18px;

        min-height: 105px;

        box-shadow:
            0 12px 30px rgba(0,0,0,0.12);
    }

    .metric-label {
        color: #6f7d90;

        font-size: 9px;

        font-weight: 800;

        letter-spacing: 1.4px;
    }

    .metric-value {
        color: #ffffff;

        font-size: 27px;

        font-weight: 850;

        margin-top: 8px;

        letter-spacing: -0.7px;
    }

    .metric-accent {
        color: #67e8f9;
    }

    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-card {
        position: relative;

        background:
            linear-gradient(
                145deg,
                rgba(14,23,38,0.98),
                rgba(8,14,24,0.98)
            );

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 18px;

        padding: 21px;

        min-height: 160px;

        margin-bottom: 14px;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(139,92,246,0.32);

        box-shadow:
            0 18px 45px rgba(0,0,0,0.22);
    }

    .feature-icon {
        width: 38px;
        height: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                rgba(0,229,255,0.12),
                rgba(124,58,237,0.15)
            );

        border: 1px solid rgba(0,229,255,0.13);

        font-size: 18px;

        margin-bottom: 13px;
    }

    .feature-title {
        color: #ffffff;

        font-size: 14px;

        font-weight: 800;

        margin-bottom: 7px;
    }

    .feature-text {
        color: #7d8b9e;

        font-size: 11px;

        line-height: 1.65;
    }

    /* ======================================================
       REPORT AREA
       ====================================================== */

    .report-header {
        padding: 20px 22px;

        border-radius: 16px;

        background:
            linear-gradient(
                100deg,
                rgba(0,229,255,0.07),
                rgba(124,58,237,0.08)
            );

        border: 1px solid rgba(255,255,255,0.07);

        margin-bottom: 16px;
    }

    .report-header-title {
        color: #ffffff;

        font-size: 17px;

        font-weight: 800;
    }

    .report-header-subtitle {
        color: #718096;

        font-size: 11px;

        margin-top: 5px;
    }

    .report-box {
        background:
            linear-gradient(
                145deg,
                rgba(10,17,29,0.98),
                rgba(7,12,21,0.98)
            );

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 18px;

        padding: 24px;

        line-height: 1.75;
    }

    /* ======================================================
       STATUS
       ====================================================== */

    .status-card {
        background:
            rgba(10,18,29,0.96);

        border: 1px solid rgba(0,229,255,0.11);

        border-radius: 12px;

        padding: 13px 9px;

        text-align: center;
    }

    .status-title {
        color: #68778b;

        font-size: 8px;

        letter-spacing: 1.1px;

        font-weight: 800;
    }

    .status-value {
        color: #67e8f9;

        font-size: 11px;

        font-weight: 750;

        margin-top: 6px;
    }

    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        color: #718096 !important;
        font-weight: 700 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #67e8f9 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background:
            linear-gradient(
                90deg,
                #00e5ff,
                #7c3aed
            ) !important;
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    textarea,
    input {
        background: #0a111c !important;
        color: #f8fafc !important;

        border: 1px solid #1d2b3c !important;

        border-radius: 12px !important;
    }

    textarea:focus,
    input:focus {
        border-color: #00e5ff !important;

        box-shadow:
            0 0 0 1px rgba(0,229,255,0.18) !important;
    }

    div[data-baseweb="select"] > div {
        background: #0a111c !important;

        border-color: #1d2b3c !important;

        border-radius: 11px !important;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    div.stButton > button {
        border-radius: 12px;

        min-height: 46px;

        font-weight: 800;

        border: 1px solid rgba(0,229,255,0.18);

        background:
            linear-gradient(
                100deg,
                #00a8c7,
                #6841d9
            );

        color: white;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.20);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 14px 38px rgba(0,229,255,0.16);
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 11px;

        background: #0c1420;

        border: 1px solid #1c2b3d;

        color: #dce5ef;

        font-weight: 700;
    }

    /* ======================================================
       EXPANDER
       ====================================================== */

    div[data-testid="stExpander"] {
        background: #09111b;

        border: 1px solid #1a2939;

        border-radius: 13px;
    }

    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-color: rgba(255,255,255,0.06) !important;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;

        color: #566477;

        font-size: 10px;

        padding: 18px;
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
                "## ",
                ""
            ).strip()

            current_content = []

        elif line.startswith("# "):

            if current_content:

                sections[current_title] = "\n".join(
                    current_content
                ).strip()

            current_title = line.replace(
                "# ",
                ""
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
            if line.strip().startswith(
                ("-", "•", "*")
            )
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
        <div class="side-brand">

            <div class="side-logo">
                ⚡
            </div>

            <div class="side-title">
                BusinessOps AI
            </div>

            <div class="side-subtitle">
                Autonomous Business Process Intelligence
            </div>

            <div class="side-status">

                <div class="side-status-label">
                    SYSTEM STATUS
                </div>

                <div class="side-status-value">
                    ● AI ENGINE READY
                </div>

            </div>

            <div class="side-mini">
                CrewAI Flow · Groq Intelligence ·
                Streamlit Cloud
            </div>

        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero-wrap">

        <div class="hero-top">
            ⚡ AUTONOMOUS BUSINESS INTELLIGENCE
        </div>

        <div class="hero-title">
            BusinessOps AI
        </div>

        <div class="hero-subtitle">
            Transform complex business requests into
            structured operational plans, risk controls,
            priority actions, implementation roadmaps,
            and measurable business outcomes.
        </div>

        <div class="hero-line"></div>

    </div>
    """
)


# ============================================================
# WORKFLOW STAGES
# ============================================================

st.markdown(
    '<div class="section-title">Agentic Workflow</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Six coordinated intelligence stages powering every business analysis.</div>',
    unsafe_allow_html=True,
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

                <div class="stage-dot"></div>

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
                WORKFLOW
            </div>

            <div class="metric-value">
                <span class="metric-accent">06</span>
                stages
            </div>

        </div>
        """
    )


with m2:

    st.html(
        """
        <div class="metric-card">

            <div class="metric-label">
                AI GENERATION
            </div>

            <div class="metric-value">
                <span class="metric-accent">01</span>
                call
            </div>

        </div>
        """
    )


with m3:

    st.html(
        """
        <div class="metric-card">

            <div class="metric-label">
                INTELLIGENCE
            </div>

            <div class="metric-value">
                <span class="metric-accent">08+</span>
                modules
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
                <span class="metric-accent">CLOUD</span>
            </div>

        </div>
        """
    )


# ============================================================
# BUSINESS REQUEST
# ============================================================

st.write("")

st.markdown(
    '<div class="section-title">Business Request</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Describe a real operational challenge and let the intelligence workflow structure it.</div>',
    unsafe_allow_html=True,
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
    # REPORT HEADER
    # ========================================================

    st.write("")

    st.html(
        """
        <div class="report-header">

            <div class="report-header-title">
                Business Intelligence Report
            </div>

            <div class="report-header-subtitle">
                AI-generated operational analysis, risk intelligence,
                action planning and implementation guidance.
            </div>

        </div>
        """
    )


    # ========================================================
    # EXECUTION STATUS
    # ========================================================

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
    # REPORT METRICS
    # ========================================================

    st.write("")

    o1, o2, o3, o4 = st.columns(4)


    with o1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    PRIORITY ACTIONS
                </div>

                <div class="metric-value">
                    <span class="metric-accent">
                        {action_count if action_count else "—"}
                    </span>
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
                    <span class="metric-accent">
                        {risk_count if risk_count else "—"}
                    </span>
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
                    <span class="metric-accent">
                        {gap_count if gap_count else "—"}
                    </span>
                </div>

            </div>
            """
        )


    with o4:

        st.html(
            """
            <div class="metric-card">

                <div class="metric-label">
                    AI GENERATIONS
                </div>

                <div class="metric-value">
                    <span class="metric-accent">
                        01
                    </span>
                </div>

            </div>
            """
        )


    # ========================================================
    # REPORT TABS
    # ========================================================

    st.write("")

    st.markdown(
        '<div class="section-title">Intelligence Report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Explore the generated analysis by operational area.</div>',
        unsafe_allow_html=True,
    )


    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📊 Executive",
            "⚙️ Operations",
            "⚠️ Risk & Priority",
            "🚀 Roadmap",
            "📈 KPIs & QA",
            "📄 Full Report",
        ]
    )


    # ========================================================
    # TAB 1 — EXECUTIVE
    # ========================================================

    with tab1:

        with st.container(border=True):

            st.markdown(
                "#### Executive Summary"
            )

            st.markdown(
                sections.get(
                    "Executive Summary",
                    "Executive summary was not returned."
                )
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


    # ========================================================
    # TAB 2 — OPERATIONS
    # ========================================================

    with tab2:

        with st.container(border=True):

            st.markdown(
                "#### Recommended Workflow"
            )

            st.markdown(
                sections.get(
                    "Recommended Workflow",
                    "No workflow returned."
                )
            )

            st.divider()

            st.markdown(
                "#### Process Canvas"
            )

            st.markdown(
                sections.get(
                    "Process Canvas",
                    "No process canvas returned."
                )
            )


    # ========================================================
    # TAB 3 — RISK & PRIORITY
    # ========================================================

    with tab3:

        with st.container(border=True):

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

            st.divider()

            st.markdown(
                "#### Priority Actions"
            )

            st.markdown(
                sections.get(
                    "Priority Actions",
                    "No priority actions returned."
                )
            )


    # ========================================================
    # TAB 4 — ROADMAP
    # ========================================================

    with tab4:

        with st.container(border=True):

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


    # ========================================================
    # TAB 5 — KPIs & QA
    # ========================================================

    with tab5:

        with st.container(border=True):

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


    # ========================================================
    # TAB 6 — FULL REPORT
    # ========================================================

    with tab6:

        with st.container(border=True):

            st.markdown(
                result
            )


    # ========================================================
    # DOWNLOAD REPORTS
    # ========================================================

    st.write("")

    st.markdown(
        '<div class="section-title">Export</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Save the generated intelligence report for documentation or presentation.</div>',
        unsafe_allow_html=True,
    )


    pdf_file = create_pdf(
        result
    )

    docx_file = create_docx(
        result
    )


    d1, d2, d3 = st.columns(3)


    with d1:

        st.download_button(

            "📄 Download TXT",

            data=str(result),

            file_name="businessops_report.txt",

            mime="text/plain",

            use_container_width=True,

        )


    with d2:

        st.download_button(

            "📕 Download PDF",

            data=pdf_file,

            file_name="businessops_report.pdf",

            mime="application/pdf",

            use_container_width=True,

        )


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
    '<div class="section-title">Business Intelligence Capabilities</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Core intelligence capabilities available in the BusinessOps workflow.</div>',
    unsafe_allow_html=True,
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

                <div class="feature-icon">
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

        BusinessOps AI
        · Autonomous Business Process Intelligence
        · CrewAI + Groq
        · Streamlit Cloud

    </div>
    """
)
