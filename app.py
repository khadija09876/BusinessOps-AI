import io
import re
from datetime import datetime
from html import escape

import streamlit as st
from groq import Groq

from crewai.flow import Flow, start, listen
from pydantic import BaseModel, Field

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

from docx import Document


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BusinessOps AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "openai/gpt-oss-20b"


# ============================================================
# SESSION STATE
# ============================================================

if "businessops_result" not in st.session_state:
    st.session_state.businessops_result = ""

if "businessops_request" not in st.session_state:
    st.session_state.businessops_request = ""

if "businessops_report_id" not in st.session_state:
    st.session_state.businessops_report_id = ""

if "businessops_timestamp" not in st.session_state:
    st.session_state.businessops_timestamp = ""

if "businessops_meta" not in st.session_state:
    st.session_state.businessops_meta = {}


# ============================================================
# PREMIUM CHARCOAL + MAROON THEME
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
                circle at 8% 0%,
                rgba(128, 38, 57, 0.075),
                transparent 25%
            ),
            radial-gradient(
                circle at 92% 2%,
                rgba(148, 163, 184, 0.055),
                transparent 27%
            ),
            #08090c;

        color: #f5f5f4;
    }

    .main .block-container {
        max-width: 1380px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

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
                #0c0d10 0%,
                #08090c 100%
            );

        border-right: 1px solid rgba(255,255,255,0.055);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.8rem;
    }

    section[data-testid="stSidebar"] p {
        color: #9298a3;
    }


    /* ======================================================
       TEXT
    ====================================================== */

    h1 {
        color: #f5f5f4 !important;
        font-weight: 900 !important;
        letter-spacing: -1.5px !important;
    }

    h2 {
        color: #eeeeec !important;
        font-weight: 800 !important;
    }

    h3 {
        color: #e2e2df !important;
        font-weight: 750 !important;
    }

    p {
        color: #cdd0d5;
        line-height: 1.75;
    }

    li {
        color: #cdd0d5;
        line-height: 1.7;
    }

    strong {
        color: #f0f0ee;
    }


    /* ======================================================
       NATIVE STREAMLIT STATUS
    ====================================================== */

    section[data-testid="stSidebar"] [data-testid="stAlert"] {
        background: rgba(128, 38, 57, 0.08) !important;
        border: 1px solid rgba(185, 91, 115, 0.18) !important;
        border-radius: 11px !important;
    }


    /* ======================================================
       CARDS
    ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(19,18,22,0.98),
                rgba(11,12,16,0.98)
            );

        border-color: rgba(255,255,255,0.06) !important;
        border-radius: 16px !important;
    }


    /* ======================================================
       INPUTS
    ====================================================== */

    textarea,
    input {
        background: #0c0e13 !important;
        color: #f5f5f4 !important;

        border: 1px solid #272a32 !important;

        border-radius: 9px !important;

        font-size: 13px !important;
        line-height: 1.65 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #707680 !important;
        font-size: 12px !important;
    }

    textarea:focus,
    input:focus {
        border-color: #8f3048 !important;

        box-shadow:
            0 0 0 1px
            rgba(185,91,115,0.15) !important;
    }

    div[data-baseweb="select"] > div {
        background: #0c0e13 !important;
        border-color: #272a32 !important;
        border-radius: 9px !important;
        min-height: 43px !important;
    }

    div[data-baseweb="select"] span {
        font-size: 12px !important;
    }

    label {
        color: #a0a4ac !important;
        font-size: 11px !important;
    }


    /* ======================================================
       BUTTONS
    ====================================================== */

    div.stButton > button {
        min-height: 45px;

        border-radius: 9px;

        border: 1px solid
            rgba(185,91,115,0.22);

        background:
            linear-gradient(
                100deg,
                #7c2940,
                #542733
            );

        color: white;

        font-size: 12px;
        font-weight: 800;

        box-shadow:
            0 9px 25px
            rgba(0,0,0,0.20);
    }

    div.stButton > button:hover {
        border-color:
            rgba(215,154,170,0.38);

        box-shadow:
            0 12px 30px
            rgba(128,38,57,0.14);
    }

    div[data-testid="stDownloadButton"] button {
        min-height: 43px;
        border-radius: 9px;

        background: #101116;

        border: 1px solid #292c34;

        color: #d8d9dc;

        font-size: 11px;
        font-weight: 700;
    }


    /* ======================================================
       METRICS
    ====================================================== */

    div[data-testid="stMetric"] {
        background:
            rgba(255,255,255,0.022);

        border:
            1px solid rgba(255,255,255,0.05);

        border-radius: 11px;

        padding: 13px 14px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 9px !important;
        color: #777d88 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 21px !important;
        color: #e4e4e2 !important;
    }


    /* ======================================================
       TABS
    ====================================================== */

    button[data-baseweb="tab"] {
        color: #7b818b !important;
        font-size: 11px !important;
        font-weight: 750 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #c98294 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background: #9a3b55 !important;
    }


    /* ======================================================
       EXPANDER
    ====================================================== */

    div[data-testid="stExpander"] {
        background: #0d0f14;
        border: 1px solid #272a32;
        border-radius: 11px;
    }


    /* ======================================================
       SIDEBAR CAPTION
    ====================================================== */

    section[data-testid="stSidebar"] small {
        color: #777d88 !important;
    }


    /* ======================================================
       DIVIDER
    ====================================================== */

    hr {
        border-color:
            rgba(255,255,255,0.055) !important;
    }


    /* ======================================================
       MOBILE
    ====================================================== */

    @media (max-width: 900px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 38px !important;
        }

        p,
        li {
            font-size: 13px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_markdown(text: str) -> str:
    """Convert basic markdown into readable plain text."""

    if not text:
        return ""

    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"[*_`#]", "", text)

    return text.strip()


def split_report_sections(report: str) -> dict:
    """Split report using ## headings."""

    sections = {}

    pattern = re.compile(
        r"^##\s+(.+?)\s*$",
        flags=re.MULTILINE,
    )

    matches = list(pattern.finditer(report))

    if not matches:
        return {
            "Full Report": report
        }

    for index, match in enumerate(matches):

        title = match.group(1).strip()

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(report)

        content = report[start:end].strip()

        sections[title] = content

    return sections


def count_bullets(text: str) -> int:
    """Count markdown bullet/numbered lines."""

    if not text:
        return 0

    count = 0

    for line in text.splitlines():

        line = line.strip()

        if re.match(r"^[-*•]\s+", line):
            count += 1

        elif re.match(r"^\d+\.\s+", line):
            count += 1

    return count


def create_txt(report: str) -> bytes:
    return report.encode("utf-8")


def create_pdf(report: str, report_id: str) -> bytes:

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "BusinessOpsTitle",
        parent=styles["Title"],
        fontSize=18,
        leading=23,
        textColor=HexColor("#7c2940"),
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "BusinessOpsHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        textColor=HexColor("#542733"),
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BusinessOpsBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        textColor=HexColor("#222222"),
        spaceAfter=6,
    )

    story = []

    story.append(
        Paragraph(
            "BusinessOps AI — Analysis Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Report ID: {escape(report_id)}",
            body_style,
        )
    )

    story.append(Spacer(1, 10))

    sections = split_report_sections(report)

    for title, content in sections.items():

        if title == "Full Report":

            paragraphs = content.split("\n")

        else:

            story.append(
                Paragraph(
                    escape(title),
                    heading_style,
                )
            )

            paragraphs = content.split("\n")

        for line in paragraphs:

            line = line.strip()

            if not line:
                continue

            if line.startswith("- "):
                line = "• " + line[2:]

            line = clean_markdown(line)

            if line:

                story.append(
                    Paragraph(
                        escape(line),
                        body_style,
                    )
                )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


def create_docx(report: str, report_id: str) -> bytes:

    document = Document()

    document.add_heading(
        "BusinessOps AI — Analysis Report",
        level=0,
    )

    document.add_paragraph(
        f"Report ID: {report_id}"
    )

    document.add_paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    sections = split_report_sections(report)

    for title, content in sections.items():

        if title == "Full Report":

            for line in content.splitlines():

                line = line.strip()

                if line:

                    document.add_paragraph(
                        clean_markdown(line)
                    )

            continue

        document.add_heading(
            title,
            level=1,
        )

        for line in content.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("- "):

                document.add_paragraph(
                    clean_markdown(line[2:]),
                    style="List Bullet",
                )

            elif re.match(r"^\d+\.\s+", line):

                cleaned = re.sub(
                    r"^\d+\.\s+",
                    "",
                    line,
                )

                document.add_paragraph(
                    clean_markdown(cleaned),
                    style="List Number",
                )

            else:

                document.add_paragraph(
                    clean_markdown(line)
                )

    buffer = io.BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# CREWAI FLOW STATE
# ============================================================

class BusinessOpsState(BaseModel):

    request: str = ""

    scenario: str = ""

    department: str = ""

    priority: str = ""

    timeline: str = ""

    intake_status: str = "Pending"

    analysis_status: str = "Pending"

    operations_status: str = "Pending"

    risk_status: str = "Pending"

    actions_status: str = "Pending"

    qa_status: str = "Pending"

    workflow_notes: list[str] = Field(
        default_factory=list
    )

    report: str = ""


# ============================================================
# CREWAI BUSINESSOPS FLOW
# ============================================================

class BusinessOpsFlow(Flow[BusinessOpsState]):

    @start()
    def intake(self):

        self.state.intake_status = "Completed"

        self.state.workflow_notes.append(
            "Business request received and classified."
        )

        return "intake_complete"


    @listen(intake)
    def business_analysis(self, previous):

        self.state.analysis_status = "Completed"

        self.state.workflow_notes.append(
            "Business context and improvement objective identified."
        )

        return "analysis_complete"


    @listen(business_analysis)
    def operations_planning(self, previous):

        self.state.operations_status = "Completed"

        self.state.workflow_notes.append(
            "Operational workflow and process improvement areas mapped."
        )

        return "operations_complete"


    @listen(operations_planning)
    def risk_management(self, previous):

        self.state.risk_status = "Completed"

        self.state.workflow_notes.append(
            "Potential operational risk categories prepared."
        )

        return "risk_complete"


    @listen(risk_management)
    def action_planning(self, previous):

        self.state.actions_status = "Completed"

        self.state.workflow_notes.append(
            "Priority actions and implementation roadmap prepared."
        )

        return "actions_complete"


    @listen(action_planning)
    def quality_control(self, previous):

        self.state.qa_status = "Completed"

        self.state.workflow_notes.append(
            "Report structure and quality requirements prepared."
        )

        return "qa_complete"


    @listen(quality_control)
    def final_report(self, previous):

        if "GROQ_API_KEY" not in st.secrets:

            raise RuntimeError(
                "GROQ_API_KEY is missing from Streamlit Secrets."
            )

        api_key = st.secrets["GROQ_API_KEY"]

        if not api_key:

            raise RuntimeError(
                "GROQ_API_KEY is empty in Streamlit Secrets."
            )

        client = Groq(
            api_key=api_key
        )

        prompt = f"""
You are BusinessOps AI, an autonomous business process
intelligence analyst.

Analyze the following business request.

BUSINESS REQUEST:
{self.state.request}

SCENARIO:
{self.state.scenario}

BUSINESS AREA:
{self.state.department}

PRIORITY:
{self.state.priority}

TIMELINE:
{self.state.timeline}

Your task is to produce a professional operational
intelligence report.

IMPORTANT RULES:

1. Do not invent company-specific facts.
2. Clearly distinguish assumptions from known information.
3. Keep recommendations practical.
4. Focus on business operations and process improvement.
5. Identify risks without exaggeration.
6. Provide measurable KPIs.
7. Provide clear priority actions.
8. Keep the report concise but useful.
9. Do not mention that you are an AI.
10. Do not include unnecessary introductions.
11. Use exactly the section headings below.

REQUIRED REPORT STRUCTURE:

## Executive Summary

## Business Analysis

## Department Impact

## Information Gaps

## Recommended Workflow

## Priority Matrix

## Risk Register

## Priority Actions

## 30/60/90 Day Roadmap

## KPIs / Success Metrics

## Process Canvas

## QA Audit

For the Priority Matrix, Risk Register, Roadmap,
KPIs and Process Canvas, use concise bullet points
or simple markdown tables where useful.

For the QA Audit, evaluate:
- completeness
- clarity
- operational practicality
- measurable outcomes
- assumptions/gaps

Do not create fake numerical business results.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional business "
                        "operations intelligence analyst."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            max_completion_tokens=2200,
        )

        report = response.choices[0].message.content

        if not report or not report.strip():

            raise RuntimeError(
                "Groq returned an empty report."
            )

        self.state.report = report.strip()

        return self.state.report


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("### ◈")

    st.subheader("BusinessOps AI")

    st.caption(
        "Autonomous Business Process "
        "Intelligence Platform"
    )

    st.caption("SYSTEM STATUS")

    st.success("● Operational")

    st.caption(
        "AI-powered workflow analysis, risk identification, "
        "action planning and business performance intelligence."
    )

    st.divider()

    st.caption("TECH STACK")

    st.write("Python")
    st.write("Streamlit")
    st.write("CrewAI Flow")
    st.write("Groq API")
    st.write("GPT-OSS 20B")

    st.divider()

    st.caption(
        "One LLM generation is used per complete workflow "
        "to remain suitable for free-tier experimentation."
    )


# ============================================================
# HERO
# ============================================================

st.caption(
    "AUTONOMOUS BUSINESS INTELLIGENCE"
)

st.title("BusinessOps AI")

st.write(
    "Transform business requests into structured operational "
    "plans, risk insights, prioritized actions and measurable "
    "performance outcomes."
)

st.divider()


# ============================================================
# WORKFLOW
# ============================================================

st.caption("AI WORKFLOW")

st.subheader(
    "Autonomous Process Intelligence"
)

st.caption(
    "A six-stage CrewAI Flow organizes the request before "
    "the final intelligence report is generated."
)

workflow_cols = st.columns(6)

workflow_steps = [
    ("01", "Business Intake"),
    ("02", "Analysis"),
    ("03", "Operations"),
    ("04", "Risk Review"),
    ("05", "Action Plan"),
    ("06", "QA Audit"),
]

for column, (number, name) in zip(
    workflow_cols,
    workflow_steps,
):

    with column:

        st.metric(
            label=number,
            value=name,
        )


# ============================================================
# CONTROL PANEL
# ============================================================

st.divider()

st.caption("ANALYSIS WORKSPACE")

st.subheader("Business Request")

st.caption(
    "Describe the business process, operational problem "
    "or improvement requirement."
)


with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:

        scenario = st.selectbox(
            "Scenario",
            [
                "Operational Improvement",
                "Process Optimization",
                "Cost Reduction",
                "Customer Experience",
                "Risk Management",
                "Performance Improvement",
            ],
        )

        department = st.selectbox(
            "Business Area",
            [
                "Operations",
                "Human Resources",
                "Finance",
                "Sales",
                "Marketing",
                "Customer Support",
                "IT",
                "Management",
            ],
        )

    with col2:

        priority = st.selectbox(
            "Priority",
            [
                "Critical",
                "High",
                "Medium",
                "Low",
            ],
        )

        timeline = st.selectbox(
            "Timeline",
            [
                "Immediate",
                "7 Days",
                "30 Days",
                "60 Days",
                "90 Days",
            ],
        )

    request = st.text_area(
        "Business Request",
        placeholder=(
            "Example: Our customer support response time "
            "has increased. Analyze the process, identify "
            "operational bottlenecks, assess risks and "
            "propose an improvement plan."
        ),
        height=180,
    )

    run_col, clear_col = st.columns([3, 1])

    with run_col:

        run = st.button(
            "Run BusinessOps Analysis",
            use_container_width=True,
        )

    with clear_col:

        clear = st.button(
            "Clear",
            use_container_width=True,
        )


# ============================================================
# CLEAR
# ============================================================

if clear:

    st.session_state.businessops_result = ""

    st.session_state.businessops_request = ""

    st.session_state.businessops_report_id = ""

    st.session_state.businessops_timestamp = ""

    st.session_state.businessops_meta = {}

    st.rerun()


# ============================================================
# RUN ANALYSIS
# ============================================================

if run:

    if not request.strip():

        st.warning(
            "Please enter a business request before running "
            "the analysis."
        )

    else:

        try:

            report_id = (
                "BO-"
                + datetime.now().strftime(
                    "%Y%m%d-%H%M%S"
                )
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            st.session_state.businessops_request = request

            st.session_state.businessops_report_id = report_id

            st.session_state.businessops_timestamp = timestamp

            with st.spinner(
                "BusinessOps AI is running the autonomous workflow..."
            ):

                flow = BusinessOpsFlow()

                result = flow.kickoff(
                    inputs={
                        "request": request,
                        "scenario": scenario,
                        "department": department,
                        "priority": priority,
                        "timeline": timeline,
                    }
                )

                if hasattr(result, "raw"):

                    result = result.raw

                if not result:

                    result = flow.state.report

                if not result:

                    raise RuntimeError(
                        "The workflow returned an empty report."
                    )

                st.session_state.businessops_result = str(
                    result
                )

                st.session_state.businessops_meta = {
                    "scenario": scenario,
                    "department": department,
                    "priority": priority,
                    "timeline": timeline,
                }

            st.success(
                "BusinessOps analysis completed successfully."
            )

        except Exception as error:

            st.error(
                f"Analysis failed: {error}"
            )


# ============================================================
# RESULTS
# ============================================================

report = st.session_state.businessops_result


if report:

    st.divider()

    st.caption("INTELLIGENCE REPORT")

    st.subheader("Operational Assessment")

    with st.container(border=True):

        st.write(
            "BusinessOps Analysis Report"
        )

        st.caption(
            f"{st.session_state.businessops_report_id} "
            f"· "
            f"{st.session_state.businessops_timestamp}"
        )


    # ========================================================
    # WORKFLOW STATUS
    # ========================================================

    status_cols = st.columns(6)

    statuses = [
        "INTAKE",
        "ANALYSIS",
        "OPERATIONS",
        "RISK",
        "ACTIONS",
        "QA",
    ]

    for column, label in zip(
        status_cols,
        statuses,
    ):

        with column:

            st.metric(
                label=label,
                value="READY",
            )


    # ========================================================
    # DYNAMIC METRICS
    # ========================================================

    sections = split_report_sections(report)

    risk_count = count_bullets(
        sections.get("Risk Register", "")
    )

    action_count = count_bullets(
        sections.get("Priority Actions", "")
    )

    kpi_count = count_bullets(
        sections.get("KPIs / Success Metrics", "")
    )

    if risk_count == 0:
        risk_count = "—"

    if action_count == 0:
        action_count = "—"

    if kpi_count == 0:
        kpi_count = "—"


    st.write("")

    metric_cols = st.columns(4)

    with metric_cols[0]:

        st.metric(
            "PRIORITY",
            st.session_state.businessops_meta.get(
                "priority",
                "—",
            ),
        )

    with metric_cols[1]:

        st.metric(
            "RISK AREAS",
            risk_count,
        )

    with metric_cols[2]:

        st.metric(
            "ACTIONS",
            action_count,
        )

    with metric_cols[3]:

        st.metric(
            "KPIs",
            kpi_count,
        )


    # ========================================================
    # REPORT TABS
    # ========================================================

    st.write("")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
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

    with tab1:

        overview_sections = [
            "Executive Summary",
            "Business Analysis",
            "Department Impact",
            "Information Gaps",
        ]

        for title in overview_sections:

            if title in sections:

                st.markdown(
                    f"### {title}"
                )

                st.markdown(
                    sections[title]
                )

                st.divider()


    # ========================================================
    # OPERATIONS
    # ========================================================

    with tab2:

        for title in [
            "Recommended Workflow",
            "Process Canvas",
        ]:

            if title in sections:

                st.markdown(
                    f"### {title}"
                )

                st.markdown(
                    sections[title]
                )

                st.divider()


    # ========================================================
    # RISK
    # ========================================================

    with tab3:

        if "Risk Register" in sections:

            st.markdown("### Risk Register")

            st.markdown(
                sections["Risk Register"]
            )

        else:

            st.info(
                "Risk Register was not returned in the report."
            )

        if "Priority Matrix" in sections:

            st.markdown("### Priority Matrix")

            st.markdown(
                sections["Priority Matrix"]
            )


    # ========================================================
    # ROADMAP
    # ========================================================

    with tab4:

        if "Priority Actions" in sections:

            st.markdown("### Priority Actions")

            st.markdown(
                sections["Priority Actions"]
            )

        if "30/60/90 Day Roadmap" in sections:

            st.markdown("### 30/60/90 Day Roadmap")

            st.markdown(
                sections["30/60/90 Day Roadmap"]
            )


    # ========================================================
    # KPIs
    # ========================================================

    with tab5:

        if "KPIs / Success Metrics" in sections:

            st.markdown(
                "### KPIs / Success Metrics"
            )

            st.markdown(
                sections["KPIs / Success Metrics"]
            )

        else:

            st.info(
                "No KPI section was returned."
            )


    # ========================================================
    # FULL REPORT
    # ========================================================

    with tab6:

        st.markdown(report)


    # ========================================================
    # EXPORTS
    # ========================================================

    st.divider()

    st.caption("EXPORT REPORT")

    export_cols = st.columns(3)

    with export_cols[0]:

        st.download_button(
            label="Download TXT",
            data=create_txt(report),
            file_name=(
                f"{st.session_state.businessops_report_id}.txt"
            ),
            mime="text/plain",
            use_container_width=True,
        )

    with export_cols[1]:

        st.download_button(
            label="Download PDF",
            data=create_pdf(
                report,
                st.session_state.businessops_report_id,
            ),
            file_name=(
                f"{st.session_state.businessops_report_id}.pdf"
            ),
            mime="application/pdf",
            use_container_width=True,
        )

    with export_cols[2]:

        st.download_button(
            label="Download Word",
            data=create_docx(
                report,
                st.session_state.businessops_report_id,
            ),
            file_name=(
                f"{st.session_state.businessops_report_id}.docx"
            ),
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            use_container_width=True,
        )


    # ========================================================
    # REQUEST DETAILS
    # ========================================================

    with st.expander(
        "View Submitted Business Request"
    ):

        st.write(
            st.session_state.businessops_request
        )

        metadata = st.session_state.businessops_meta

        st.write(
            f"**Scenario:** {metadata.get('scenario', '—')}"
        )

        st.write(
            f"**Business Area:** {metadata.get('department', '—')}"
        )

        st.write(
            f"**Priority:** {metadata.get('priority', '—')}"
        )

        st.write(
            f"**Timeline:** {metadata.get('timeline', '—')}"
        )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.divider()

    st.caption("READY")

    st.subheader(
        "Waiting for Business Request"
    )

    st.caption(
        "Enter a business problem above to begin the "
        "BusinessOps intelligence workflow."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "BusinessOps AI · Autonomous Business Process Intelligence "
    "Platform · Python · Streamlit · CrewAI · Groq"
)
