import time
import io
import re
from datetime import datetime

import streamlit as st
from groq import Groq

# ============================================================
# PDF
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

# ============================================================
# DOCX
# ============================================================

from docx import Document
from docx.shared import Pt

# ============================================================
# CREWAI
# ============================================================

from crewai.flow import Flow, start, listen


# ============================================================
# APP CONFIG
# ============================================================

st.set_page_config(
    page_title="BusinessOps AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = "openai/gpt-oss-20b"


# ============================================================
# SESSION STATE
# ============================================================

if "businessops_result" not in st.session_state:
    st.session_state["businessops_result"] = ""

if "businessops_request" not in st.session_state:
    st.session_state["businessops_request"] = ""

if "businessops_report_id" not in st.session_state:
    st.session_state["businessops_report_id"] = ""

if "businessops_timestamp" not in st.session_state:
    st.session_state["businessops_timestamp"] = ""


# ============================================================
# PREMIUM DARK UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       BASE
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(0, 229, 255, 0.075),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(124, 58, 237, 0.10),
                transparent 27%
            ),
            #05070c;

        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1420px;
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    #MainMenu,
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
                #070a10 0%,
                #05070c 100%
            );

        border-right: 1px solid rgba(255,255,255,0.055);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    .brand {
        padding: 12px 10px 18px 10px;
    }

    .brand-mark {
        width: 40px;
        height: 40px;
        border-radius: 12px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                135deg,
                #00cfe8,
                #6941d9
            );

        color: white;
        font-size: 18px;
        font-weight: 900;

        box-shadow:
            0 8px 28px rgba(0,229,255,0.14);
    }

    .brand-name {
        margin-top: 11px;
        color: #ffffff;
        font-size: 18px;
        font-weight: 850;
        letter-spacing: -0.5px;
    }

    .brand-desc {
        margin-top: 4px;
        color: #657286;
        font-size: 10px;
        line-height: 1.55;
    }

    .system-card {
        margin-top: 15px;
        padding: 11px 12px;

        border-radius: 11px;

        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06);
    }

    .system-label {
        color: #58667a;
        font-size: 8px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }

    .system-value {
        margin-top: 5px;
        color: #67e8f9;
        font-size: 11px;
        font-weight: 750;
    }

    .system-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22d3ee;
        margin-right: 5px;
        box-shadow: 0 0 10px rgba(34,211,238,0.8);
    }

    .side-info {
        margin-top: 13px;
        color: #505d70;
        font-size: 9px;
        line-height: 1.6;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 31px 34px 30px 34px;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(13,19,30,0.98),
                rgba(8,12,20,0.98)
            );

        border: 1px solid rgba(255,255,255,0.065);

        box-shadow:
            0 20px 70px rgba(0,0,0,0.25);

        margin-bottom: 18px;
    }

    .hero::after {
        content: "";

        position: absolute;

        right: -90px;
        top: -120px;

        width: 280px;
        height: 280px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(124,58,237,0.15),
                transparent 65%
            );
    }

    .hero-badge {
        display: inline-flex;

        padding: 6px 10px;

        border-radius: 20px;

        background: rgba(0,229,255,0.055);

        border: 1px solid rgba(0,229,255,0.13);

        color: #67e8f9;

        font-size: 8px;
        font-weight: 850;
        letter-spacing: 1.4px;
    }

    .hero-title {
        margin-top: 13px;

        font-size: clamp(38px, 5vw, 58px);

        line-height: 1;

        font-weight: 900;

        letter-spacing: -2.8px;

        color: #f8fafc;
    }

    .hero-title span {
        color: #67e8f9;
    }

    .hero-desc {
        margin-top: 12px;

        max-width: 760px;

        color: #7f8da1;

        font-size: 13px;

        line-height: 1.7;
    }

    .hero-line {
        width: 85px;
        height: 2px;

        margin-top: 19px;

        border-radius: 10px;

        background:
            linear-gradient(
                90deg,
                #00e5ff,
                #7c3aed
            );
    }

    /* ======================================================
       COMPACT SECTION
       ====================================================== */

    .section {
        margin-top: 19px;
        margin-bottom: 10px;
    }

    .section-title {
        color: #f1f5f9;
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -0.25px;
    }

    .section-desc {
        color: #5f6d80;
        font-size: 10px;
        margin-top: 3px;
    }

    /* ======================================================
       WORKFLOW STRIP
       ====================================================== */

    .flow-strip {
        display: flex;
        align-items: center;
        gap: 7px;

        padding: 11px;

        background:
            rgba(9,14,23,0.95);

        border: 1px solid rgba(255,255,255,0.055);

        border-radius: 14px;

        overflow-x: auto;
    }

    .flow-item {
        flex: 1;

        min-width: 135px;

        padding: 10px 11px;

        border-radius: 10px;

        background: rgba(255,255,255,0.022);

        border: 1px solid rgba(255,255,255,0.045);
    }

    .flow-num {
        color: #22d3ee;
        font-size: 8px;
        font-weight: 850;
        letter-spacing: 1px;
    }

    .flow-name {
        margin-top: 4px;
        color: #e5e7eb;
        font-size: 10px;
        font-weight: 750;
    }

    .flow-arrow {
        color: #37465a;
        font-size: 13px;
    }

    /* ======================================================
       CONTROL PANEL
       ====================================================== */

    .control-panel {
        padding: 17px;

        background:
            linear-gradient(
                145deg,
                rgba(11,18,29,0.98),
                rgba(7,11,18,0.98)
            );

        border: 1px solid rgba(255,255,255,0.06);

        border-radius: 17px;
    }

    .control-label {
        color: #64748b;
        font-size: 8px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    /* ======================================================
       METRIC CARDS
       ====================================================== */

    .metrics {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 9px;
        margin-top: 11px;
    }

    .metric {
        padding: 13px 14px;

        border-radius: 12px;

        background: rgba(255,255,255,0.022);

        border: 1px solid rgba(255,255,255,0.05);
    }

    .metric-label {
        color: #59677a;
        font-size: 8px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .metric-value {
        margin-top: 5px;
        color: #e5e7eb;
        font-size: 20px;
        font-weight: 850;
    }

    .metric-value span {
        color: #67e8f9;
    }

    /* ======================================================
       REPORT HEADER
       ====================================================== */

    .report-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 13px 15px;

        border-radius: 12px;

        background: rgba(0,229,255,0.025);

        border: 1px solid rgba(0,229,255,0.08);

        margin-top: 15px;
        margin-bottom: 9px;
    }

    .report-name {
        color: #e2e8f0;
        font-size: 12px;
        font-weight: 800;
    }

    .report-id {
        color: #526176;
        font-size: 9px;
        margin-top: 3px;
    }

    .report-time {
        color: #64748b;
        font-size: 9px;
        text-align: right;
    }

    /* ======================================================
       STATUS STRIP
       ====================================================== */

    .status-strip {
        display: flex;
        gap: 6px;

        margin-bottom: 13px;
    }

    .status {
        flex: 1;

        padding: 7px;

        border-radius: 8px;

        text-align: center;

        background: rgba(34,197,94,0.035);

        border: 1px solid rgba(34,197,94,0.08);
    }

    .status-label {
        color: #526176;
        font-size: 7px;
        font-weight: 800;
        letter-spacing: 0.8px;
    }

    .status-value {
        color: #86efac;
        font-size: 8px;
        font-weight: 800;
        margin-top: 3px;
    }

    /* ======================================================
       REPORT
       ====================================================== */

    .report-card {
        padding: 19px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                rgba(10,16,26,0.98),
                rgba(7,11,18,0.98)
            );

        border: 1px solid rgba(255,255,255,0.055);
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    textarea,
    input {
        background: #090f18 !important;
        color: #f8fafc !important;

        border: 1px solid #1a2737 !important;

        border-radius: 10px !important;
    }

    textarea:focus,
    input:focus {
        border-color: #0891b2 !important;

        box-shadow:
            0 0 0 1px rgba(0,229,255,0.12) !important;
    }

    div[data-baseweb="select"] > div {
        background: #090f18 !important;
        border-color: #1a2737 !important;
        border-radius: 10px !important;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    div.stButton > button {
        min-height: 44px;

        border-radius: 10px;

        border: 1px solid rgba(0,229,255,0.16);

        background:
            linear-gradient(
                100deg,
                #0891b2,
                #5b3bbf
            );

        color: white;

        font-weight: 800;

        box-shadow:
            0 9px 25px rgba(0,0,0,0.20);
    }

    div.stButton > button:hover {
        border-color: rgba(103,232,249,0.35);

        box-shadow:
            0 12px 30px rgba(0,229,255,0.10);
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 9px;
        background: #0b121d;
        border: 1px solid #1a2939;
        color: #dbe5ef;
        font-weight: 700;
    }

    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        color: #637187 !important;
        font-size: 10px !important;
        font-weight: 750 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #67e8f9 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background: #22d3ee !important;
    }

    /* ======================================================
       EXPANDER
       ====================================================== */

    div[data-testid="stExpander"] {
        background: #080e17;
        border: 1px solid #182535;
        border-radius: 11px;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        color: #414d5f;
        font-size: 9px;
        padding: 15px;
    }

    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {

        .hero {
            padding: 25px;
        }

        .hero-title {
            font-size: 40px;
        }

        .metrics {
            grid-template-columns: repeat(2, 1fr);
        }

        .status-strip {
            flex-wrap: wrap;
        }

        .status {
            min-width: 29%;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def clean_markdown(text):
    if not text:
        return ""

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = text.replace("`", "")

    return text.strip()


def split_report_sections(report_text):

    sections = {}

    current_title = "General"
    current_content = []

    for line in report_text.splitlines():

        stripped = line.strip()

        if stripped.startswith("## "):

            if current_content:
                sections[current_title] = "\n".join(
                    current_content
                ).strip()

            current_title = stripped[3:].strip()
            current_content = []

        elif stripped.startswith("# "):

            if current_content:
                sections[current_title] = "\n".join(
                    current_content
                ).strip()

            current_title = stripped[2:].strip()
            current_content = []

        else:

            current_content.append(line)

    if current_content:

        sections[current_title] = "\n".join(
            current_content
        ).strip()

    return sections


def count_bullets(text):

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


def extract_qa_scores(text):

    if not text:
        return []

    pattern = r"(Completeness|Actionability|Risk Coverage|KPI Coverage|Clarity).*?(\d{1,2})\s*/\s*10"

    return re.findall(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


# ============================================================
# PDF
# ============================================================

def create_pdf(report_text, report_id):

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
    heading_style.fontSize = 13
    heading_style.leading = 17
    heading_style.spaceBefore = 12
    heading_style.spaceAfter = 7

    body_style = styles["BodyText"]
    body_style.fontSize = 10
    body_style.leading = 15
    body_style.spaceAfter = 6

    story = []

    story.append(
        Paragraph(
            "BusinessOps AI",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Business Operations Intelligence Report · {report_id}",
            heading_style,
        )
    )

    story.append(Spacer(1, 8))

    for raw_line in report_text.splitlines():

        line = clean_markdown(raw_line)

        if not line:

            story.append(Spacer(1, 5))
            continue

        if line.startswith("## "):

            story.append(
                Paragraph(
                    line[3:].strip(),
                    heading_style,
                )
            )

        elif line.startswith("# "):

            story.append(
                Paragraph(
                    line[2:].strip(),
                    heading_style,
                )
            )

        elif line.startswith("- "):

            bullet = (
                line[2:]
                .strip()
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    "• " + bullet,
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
# DOCX
# ============================================================

def create_docx(report_text, report_id):

    document = Document()

    document.add_heading(
        "BusinessOps AI",
        level=0,
    )

    document.add_paragraph(
        f"Business Operations Intelligence Report · {report_id}"
    )

    document.add_paragraph("")

    for line in report_text.splitlines():

        line = line.strip()

        if not line:

            document.add_paragraph("")
            continue

        if line.startswith("## "):

            document.add_heading(
                line[3:].strip(),
                level=1,
            )

        elif line.startswith("# "):

            document.add_heading(
                line[2:].strip(),
                level=1,
            )

        elif line.startswith("- "):

            paragraph = document.add_paragraph(
                style="List Bullet"
            )

            paragraph.add_run(
                clean_markdown(
                    line[2:].strip()
                )
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

    # --------------------------------------------------------
    # 01 — INTAKE
    # --------------------------------------------------------

    @start()
    def intake(self):

        return {
            "request": self.state.get(
                "request",
                ""
            ).strip(),

            "department": self.state.get(
                "department",
                "All Departments"
            ),

            "priority": self.state.get(
                "priority",
                "Medium"
            ),

            "timeline": self.state.get(
                "timeline",
                "90 Days"
            ),
        }

    # --------------------------------------------------------
    # 02 — BUSINESS ANALYSIS
    # --------------------------------------------------------

    @listen(intake)
    def business_analysis(self, data):

        return {
            **data,

            "analysis": (
                "Identify the business objective, stakeholders, "
                "current situation, constraints, business impact "
                "and expected outcome."
            ),
        }

    # --------------------------------------------------------
    # 03 — OPERATIONS
    # --------------------------------------------------------

    @listen(business_analysis)
    def operations_planning(self, data):

        return {
            **data,

            "operations": (
                "Design practical operational steps, responsible "
                "roles, dependencies, resources, department impact "
                "and measurable outcomes."
            ),
        }

    # --------------------------------------------------------
    # 04 — RISK
    # --------------------------------------------------------

    @listen(operations_planning)
    def risk_management(self, data):

        return {
            **data,

            "risk": (
                "Identify operational, people, technology, "
                "communication, timeline and implementation risks "
                "with practical mitigation."
            ),
        }

    # --------------------------------------------------------
    # 05 — ACTIONS
    # --------------------------------------------------------

    @listen(risk_management)
    def action_planning(self, data):

        return {
            **data,

            "actions": (
                "Create prioritized next actions, ownership, "
                "dependencies, implementation phases and KPIs."
            ),
        }

    # --------------------------------------------------------
    # 06 — QA
    # --------------------------------------------------------

    @listen(action_planning)
    def quality_control(self, data):

        return {
            **data,

            "qa": (
                "Check whether the proposed workflow is practical, "
                "complete, consistent, actionable, measurable and "
                "clear about assumptions."
            ),
        }

    # --------------------------------------------------------
    # FINAL GROQ GENERATION
    # --------------------------------------------------------

    @listen(quality_control)
    def final_report(self, data):

        if not data["request"]:

            return "Please enter a business request."

        try:

            api_key = st.secrets["GROQ_API_KEY"]

        except Exception:

            api_key = None

        if not api_key:

            return (
                "GROQ_API_KEY is missing.\n\n"
                "Add your Groq API key in "
                "Streamlit Cloud → Manage App → Settings → Secrets."
            )

        client = Groq(
            api_key=api_key
        )

        prompt = f"""
You are BusinessOps AI, a professional autonomous
business process intelligence assistant.

Transform the business request into a practical,
structured operational plan.

BUSINESS REQUEST:
{data["request"][:2200]}

BUSINESS CONTEXT:
Department: {data["department"]}
Priority: {data["priority"]}
Implementation Horizon: {data["timeline"]}

INTERNAL BUSINESS ANALYSIS:
{data["analysis"]}

INTERNAL OPERATIONS PLAN:
{data["operations"]}

INTERNAL RISK REVIEW:
{data["risk"]}

INTERNAL ACTION PLAN:
{data["actions"]}

INTERNAL QA REVIEW:
{data["qa"]}

Generate a professional Business Operations Intelligence Report.

Use EXACTLY these headings:

## Executive Summary

Give a concise overview of the problem, objective,
business impact and recommended direction.

## Business Analysis

Cover:
- Business objective
- Stakeholders
- Current challenge
- Constraints
- Expected outcome

## Department Impact

Identify relevant departments/functions and their
responsibilities or impact.

Do not invent irrelevant departments.

## Information Gaps

Identify missing information that could affect
implementation.

If none are critical, state:
"No critical information gaps identified."

## Recommended Workflow

Give a practical step-by-step operational process.

## Priority Matrix

Classify key actions as:
- Critical
- High
- Medium
- Low

Briefly explain the reasoning.

## Risk Register

For important risks include:
- Risk
- Impact
- Likelihood
- Mitigation
- Suggested Owner

Do not invent unrealistic risks.

## Priority Actions

For each important action include:
- Action
- Suggested Owner
- Priority
- Dependency when relevant

## 30/60/90 Day Roadmap

Organize appropriate implementation phases into:
- First 30 days
- Days 31–60
- Days 61–90

## KPIs / Success Metrics

Provide measurable indicators.

Do not invent current performance numbers.

## Process Canvas

Use this structure:

Problem:
Objective:
Key Stakeholders:
Main Process:
Key Risks:
Key Outcome:

## QA Audit

Assess:
- Completeness
- Actionability
- Risk Coverage
- KPI Coverage
- Clarity

Use 1–10 scores with one short reason for each.

Also list remaining assumptions.

RULES:

- Professional business language.
- Concise and practical.
- No invented company facts.
- Clearly identify assumptions.
- Never claim that an action has already been completed.
- Avoid repetition.
- Keep the report concise.
"""

        try:

            response = client.chat.completions.create(

                model=MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are BusinessOps AI. "
                            "Generate a professional structured "
                            "Markdown business operations report "
                            "using the exact headings requested."
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
                        "Please wait a few seconds and run "
                        "the analysis again.\n\n"
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

    st.markdown(
        """
        <div class="brand">

            <div class="brand-mark">
                ⚡
            </div>

            <div class="brand-name">
                BusinessOps AI
            </div>

            <div class="brand-desc">
                Autonomous business process intelligence
                for operational decision support.
            </div>

            <div class="system-card">

                <div class="system-label">
                    SYSTEM
                </div>

                <div class="system-value">
                    <span class="system-dot"></span>
                    AI ENGINE READY
                </div>

            </div>

            <div class="side-info">
                CrewAI Flow · Groq · Streamlit Cloud<br>
                Single-generation architecture
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            AUTONOMOUS BUSINESS INTELLIGENCE
        </div>

        <div class="hero-title">
            BusinessOps <span>AI</span>
        </div>

        <div class="hero-desc">
            Turn an unstructured business problem into a
            practical workflow, risk register, priority actions,
            roadmap and measurable KPIs.
        </div>

        <div class="hero-line"></div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WORKFLOW
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">Workflow</div>
        <div class="section-desc">
            One coordinated CrewAI process from intake to quality audit.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

workflow_html = """
<div class="flow-strip">
"""

workflow_items = [
    ("01", "Intake"),
    ("02", "Analysis"),
    ("03", "Operations"),
    ("04", "Risk"),
    ("05", "Actions"),
    ("06", "QA"),
]

for index, (number, name) in enumerate(workflow_items):

    workflow_html += f"""
        <div class="flow-item">
            <div class="flow-num">{number}</div>
            <div class="flow-name">{name}</div>
        </div>
    """

    if index < len(workflow_items) - 1:

        workflow_html += """
            <div class="flow-arrow">›</div>
        """

workflow_html += "</div>"

st.markdown(
    workflow_html,
    unsafe_allow_html=True,
)


# ============================================================
# BUSINESS REQUEST SECTION
# ============================================================

st.markdown(
    """
    <div class="section">
        <div class="section-title">Analysis Workspace</div>
        <div class="section-desc">
            Configure the context, then describe the business challenge.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTROL PANEL
# ============================================================

st.markdown(
    '<div class="control-panel">',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        '<div class="control-label">SCENARIO</div>',
        unsafe_allow_html=True,
    )

    sample = st.selectbox(
        "Scenario",
        [
            "Custom request",
            "Employee Onboarding",
            "Software Rollout",
            "Office Relocation",
            "Customer Support Improvement",
            "Project Management Improvement",
            "Vendor Management",
        ],
        label_visibility="collapsed",
    )


with c2:

    st.markdown(
        '<div class="control-label">BUSINESS AREA</div>',
        unsafe_allow_html=True,
    )

    department = st.selectbox(
        "Business Area",
        [
            "All Departments",
            "Operations",
            "Human Resources",
            "Information Technology",
            "Finance",
            "Sales & Marketing",
            "Customer Support",
            "Project Management",
            "Procurement",
        ],
        label_visibility="collapsed",
    )


with c3:

    st.markdown(
        '<div class="control-label">PRIORITY</div>',
        unsafe_allow_html=True,
    )

    priority = st.selectbox(
        "Priority",
        [
            "Critical",
            "High",
            "Medium",
            "Low",
        ],
        index=2,
        label_visibility="collapsed",
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SCENARIOS
# ============================================================

default_text = ""

if sample == "Employee Onboarding":

    default_text = (
        "Our company is growing quickly and new employees "
        "are having difficulty completing HR, IT, security "
        "and department onboarding. Design a better onboarding "
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
        "Our software projects frequently miss deadlines "
        "because requirements, ownership and dependencies "
        "are unclear. Design an improved project management process."
    )

elif sample == "Vendor Management":

    default_text = (
        "Our company works with multiple external vendors and "
        "has difficulty tracking performance, deadlines, costs "
        "and responsibilities. Create an improved vendor "
        "management process with risks and KPIs."
    )


# ============================================================
# TIMELINE
# ============================================================

timeline = st.selectbox(
    "Implementation horizon",
    [
        "Immediate",
        "30 Days",
        "60 Days",
        "90 Days",
    ],
    index=3,
)


# ============================================================
# REQUEST
# ============================================================

request = st.text_area(
    "Business challenge",
    value=default_text,
    height=145,
    placeholder=(
        "Example: Our company wants to improve employee "
        "onboarding across HR, IT and department teams..."
    ),
)


# ============================================================
# RUN
# ============================================================

run_col1, run_col2 = st.columns(
    [4, 1]
)

with run_col1:

    run_clicked = st.button(
        "⚡ Analyze Business Process",
        type="primary",
        use_container_width=True,
    )

with run_col2:

    if st.session_state.get(
        "businessops_result"
    ):

        if st.button(
            "Clear",
            use_container_width=True,
        ):

            st.session_state["businessops_result"] = ""
            st.session_state["businessops_request"] = ""
            st.session_state["businessops_report_id"] = ""
            st.session_state["businessops_timestamp"] = ""

            st.rerun()


# ============================================================
# EXECUTE
# ============================================================

if run_clicked:

    if not request.strip():

        st.warning(
            "Please describe a business challenge first."
        )

    else:

        with st.spinner(
            "BusinessOps AI is running the workflow..."
        ):

            try:

                flow = BusinessOpsFlow()

                flow.state["request"] = request
                flow.state["department"] = department
                flow.state["priority"] = priority
                flow.state["timeline"] = timeline

                result = flow.kickoff()

            except Exception as flow_error:

                result = (
                    "BusinessOps AI encountered an error.\n\n"
                    f"{flow_error}"
                )

        now = datetime.now()

        report_id = (
            "BO-"
            + now.strftime("%Y%m%d-%H%M%S")
        )

        st.session_state["businessops_result"] = result
        st.session_state["businessops_request"] = request
        st.session_state["businessops_report_id"] = report_id
        st.session_state["businessops_timestamp"] = (
            now.strftime("%d %b %Y · %I:%M %p")
        )

        st.rerun()


# ============================================================
# RESULT
# ============================================================

result = st.session_state.get(
    "businessops_result",
    "",
)


if result:

    report_id = st.session_state.get(
        "businessops_report_id",
        "BusinessOps Report",
    )

    report_time = st.session_state.get(
        "businessops_timestamp",
        "",
    )

    request_used = st.session_state.get(
        "businessops_request",
        "",
    )

    sections = split_report_sections(
        result
    )

    # ========================================================
    # REPORT META
    # ========================================================

    st.markdown(
        f"""
        <div class="report-meta">

            <div>
                <div class="report-name">
                    Business Intelligence Report
                </div>

                <div class="report-id">
                    {report_id} · CrewAI workflow
                </div>
            </div>

            <div class="report-time">
                {report_time}<br>
                01 AI generation
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # STATUS
    # ========================================================

    statuses = [
        "INTAKE",
        "ANALYSIS",
        "OPERATIONS",
        "RISK",
        "ACTIONS",
        "QA",
    ]

    status_html = """
    <div class="status-strip">
    """

    for status in statuses:

        status_html += f"""
            <div class="status">
                <div class="status-label">
                    {status}
                </div>
                <div class="status-value">
                    ✓ READY
                </div>
            </div>
        """

    status_html += "</div>"

    st.markdown(
        status_html,
        unsafe_allow_html=True,
    )

    # ========================================================
    # REPORT METRICS
    # ========================================================

    risk_count = count_bullets(
        sections.get(
            "Risk Register",
            "",
        )
    )

    action_count = count_bullets(
        sections.get(
            "Priority Actions",
            "",
        )
    )

    gap_count = count_bullets(
        sections.get(
            "Information Gaps",
            "",
        )
    )

    section_count = len(
        sections
    )

    st.markdown(
        f"""
        <div class="metrics">

            <div class="metric">
                <div class="metric-label">
                    ACTION ITEMS
                </div>
                <div class="metric-value">
                    <span>{action_count}</span>
                </div>
            </div>

            <div class="metric">
                <div class="metric-label">
                    RISK ITEMS
                </div>
                <div class="metric-value">
                    <span>{risk_count}</span>
                </div>
            </div>

            <div class="metric">
                <div class="metric-label">
                    INFO GAPS
                </div>
                <div class="metric-value">
                    <span>{gap_count}</span>
                </div>
            </div>

            <div class="metric">
                <div class="metric-label">
                    REPORT SECTIONS
                </div>
                <div class="metric-value">
                    <span>{section_count}</span>
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # TABS
    # ========================================================

    st.write("")

    tabs = st.tabs(
        [
            "Overview",
            "Operations",
            "Risk",
            "Roadmap",
            "KPIs",
            "Full Report",
        ]
    )

    # ========================================================
    # OVERVIEW
    # ========================================================

    with tabs[0]:

        st.markdown(
            "### Executive Summary"
        )

        st.markdown(
            sections.get(
                "Executive Summary",
                "No executive summary returned.",
            )
        )

        st.divider()

        st.markdown(
            "### Business Analysis"
        )

        st.markdown(
            sections.get(
                "Business Analysis",
                "No business analysis returned.",
            )
        )

        st.divider()

        st.markdown(
            "### Department Impact"
        )

        st.markdown(
            sections.get(
                "Department Impact",
                "No department impact returned.",
            )
        )

        st.divider()

        st.markdown(
            "### Information Gaps"
        )

        st.markdown(
            sections.get(
                "Information Gaps",
                "No information gaps returned.",
            )
        )

    # ========================================================
    # OPERATIONS
    # ========================================================

    with tabs[1]:

        st.markdown(
            "### Recommended Workflow"
        )

        st.markdown(
            sections.get(
                "Recommended Workflow",
                "No workflow returned.",
            )
        )

        st.divider()

        st.markdown(
            "### Process Canvas"
        )

        st.markdown(
            sections.get(
                "Process Canvas",
                "No process canvas returned.",
            )
        )

        st.divider()

        st.markdown(
            "### Priority Matrix"
        )

        st.markdown(
            sections.get(
                "Priority Matrix",
                "No priority matrix returned.",
            )
        )

    # ========================================================
    # RISK
    # ========================================================

    with tabs[2]:

        st.markdown(
            "### Risk Register"
        )

        st.markdown(
            sections.get(
                "Risk Register",
                "No risk register returned.",
            )
        )

        st.divider()

        st.markdown(
            "### Priority Actions"
        )

        st.markdown(
            sections.get(
                "Priority Actions",
                "No priority actions returned.",
            )
        )

    # ========================================================
    # ROADMAP
    # ========================================================

    with tabs[3]:

        st.markdown(
            "### 30 / 60 / 90 Day Roadmap"
        )

        st.markdown(
            sections.get(
                "30/60/90 Day Roadmap",
                "No roadmap returned.",
            )
        )

    # ========================================================
    # KPI + QA
    # ========================================================

    with tabs[4]:

        st.markdown(
            "### KPIs / Success Metrics"
        )

        st.markdown(
            sections.get(
                "KPIs / Success Metrics",
                "No KPI information returned.",
            )
        )

        st.divider()

        st.markdown(
            "### AI QA Audit"
        )

        qa_text = sections.get(
            "QA Audit",
            "No QA audit returned.",
        )

        st.markdown(
            qa_text
        )

        qa_scores = extract_qa_scores(
            qa_text
        )

        if qa_scores:

            st.divider()

            score_cols = st.columns(
                len(qa_scores)
            )

            for col, (
                label,
                score,
            ) in zip(
                score_cols,
                qa_scores,
            ):

                with col:

                    try:
                        numeric_score = int(score)
                    except Exception:
                        numeric_score = 0

                    st.metric(
                        label,
                        f"{numeric_score}/10",
                    )

    # ========================================================
    # FULL REPORT
    # ========================================================

    with tabs[5]:

        with st.container(
            border=True
        ):

            st.markdown(
                result
            )

    # ========================================================
    # EXPORT
    # ========================================================

    st.write("")

    st.markdown(
        """
        <div class="section">
            <div class="section-title">Export</div>
            <div class="section-desc">
                Save the generated report for documentation or presentation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf_file = create_pdf(
        result,
        report_id,
    )

    docx_file = create_docx(
        result,
        report_id,
    )

    d1, d2, d3 = st.columns(3)

    with d1:

        st.download_button(
            "Download TXT",
            data=str(result),
            file_name=f"{report_id}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with d2:

        st.download_button(
            "Download PDF",
            data=pdf_file,
            file_name=f"{report_id}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with d3:

        st.download_button(
            "Download Word",
            data=docx_file,
            file_name=f"{report_id}.docx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            use_container_width=True,
        )

    # ========================================================
    # REQUEST
    # ========================================================

    with st.expander(
        "View submitted request"
    ):

        st.write(
            request_used
        )


# ============================================================
# SMALL CAPABILITY LINE
# ============================================================

st.write("")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:9px;
        color:#4b596c;
        font-size:9px;
    ">
        Business Analysis · Operations · Risk · Actions · Roadmap · KPIs · QA
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        BusinessOps AI · CrewAI + Groq · Streamlit Cloud
    </div>
    """,
    unsafe_allow_html=True,
)
