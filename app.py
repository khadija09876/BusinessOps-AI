import io
import json
import re
import time

import streamlit as st
from groq import Groq

# CrewAI Flow
from crewai.flow import Flow, start, listen

# Report generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from docx import Document

# Visualization
import plotly.express as px
import pandas as pd


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
# CONFIGURATION
# ============================================================

MODEL = "openai/gpt-oss-20b"


# ============================================================
# PREMIUM CHARCOAL + DEEP MAROON THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(122, 34, 55, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(255, 255, 255, 0.025),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #07080a 0%,
                #0b0c0f 48%,
                #090a0d 100%
            );
        color: #eeeeec;
    }

    .main .block-container {
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header,
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .badge {
        display: inline-block;
        padding: 4px 10px;
        background: rgba(122, 34, 55, 0.25);
        border: 1px solid rgba(177, 76, 101, 0.4);
        border-radius: 20px;
        color: #d98294;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .hero {
        padding: 10px 0 20px 0;
    }

    .stage {
        background:
            linear-gradient(
                145deg,
                rgba(20, 19, 23, 0.98),
                rgba(11, 12, 15, 0.98)
            );
        border: 1px solid rgba(255, 255, 255, 0.065);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        min-height: 145px;
    }

    .stage-number {
        font-size: 11px;
        color: #8c334d;
        font-weight: 750;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }

    .stage-title {
        font-size: 15px;
        color: #f1f1ef;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .stage-text {
        font-size: 12px;
        color: #969aa3;
        line-height: 1.6;
    }

    .agent-output {
        background:
            linear-gradient(
                145deg,
                #111318,
                #0b0c10
            );
        border: 1px solid #292c34;
        border-radius: 14px;
        padding: 22px;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    .agent-label {
        color: #d98294;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .agent-heading {
        color: #f5f4f1;
        font-size: 22px;
        font-weight: 800;
        margin-top: 5px;
        margin-bottom: 12px;
    }

    .report {
        background:
            linear-gradient(
                145deg,
                #0e1014,
                #0b0c10
            );
        border: 1px solid #282b32;
        border-radius: 14px;
        padding: 25px;
        color: #d7d7d4;
        line-height: 1.7;
        font-size: 13px;
        box-shadow: 0 14px 35px rgba(0,0,0,0.2);
    }

    .status-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        background: rgba(122, 34, 55, 0.20);
        border: 1px solid rgba(177, 76, 101, 0.35);
        color: #d98294;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0d0e11 0%,
                #090a0d 55%,
                #07080a 100%
            );
        border-right: 1px solid rgba(255, 255, 255, 0.065);
        box-shadow: 8px 0 35px rgba(0, 0, 0, 0.18);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.9rem;
    }

    h1 {
        color: #f5f4f1 !important;
        font-weight: 900 !important;
        letter-spacing: -1.8px !important;
    }

    h3 {
        color: #e5e3df !important;
        font-weight: 750 !important;
    }

    p,
    li {
        color: #c8c9cc;
        line-height: 1.75;
    }

    textarea,
    input {
        background: #0c0e12 !important;
        color: #f2f1ee !important;
        border: 1px solid #292c33 !important;
        border-radius: 10px !important;
        font-size: 13px !important;
    }

    div.stButton > button {
        min-height: 45px;
        border-radius: 10px;
        border: 1px solid rgba(177, 76, 101, 0.28);
        background:
            linear-gradient(
                105deg,
                #79283f 0%,
                #612536 48%,
                #49212d 100%
            );
        color: #ffffff;
        font-size: 12px;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background:
            linear-gradient(
                105deg,
                #893149 0%,
                #6c293b 50%,
                #542532 100%
            );
        transform: translateY(-1px);
    }

    div[data-testid="stDownloadButton"] button {
        min-height: 43px;
        border-radius: 10px;
        background:
            linear-gradient(
                145deg,
                #111318,
                #0d0f13
            );
        border: 1px solid #292c34;
        color: #d9dadc;
        font-size: 11px;
        font-weight: 750;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

if "last_report" not in st.session_state:
    st.session_state["last_report"] = ""

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "selected_agent" not in st.session_state:
    st.session_state["selected_agent"] = "Business Analyst"


# ============================================================
# EXPORT FUNCTIONS
# ============================================================

def clean_for_pdf(text_content):
    """
    Convert markdown-ish content into safe ReportLab text.
    """
    text_content = str(text_content)

    text_content = re.sub(r"\*\*(.*?)\*\*", r"\1", text_content)
    text_content = re.sub(r"`(.*?)`", r"\1", text_content)
    text_content = text_content.replace("&", "&amp;")
    text_content = text_content.replace("<", "&lt;")
    text_content = text_content.replace(">", "&gt;")

    return text_content


def create_pdf(text_content):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor="#222222",
    )

    story = []

    for line in str(text_content).split("\n"):

        if line.strip():

            safe_line = clean_for_pdf(line)

            story.append(
                Paragraph(
                    safe_line,
                    normal_style
                )
            )

            story.append(
                Spacer(1, 6)
            )

        else:
            story.append(
                Spacer(1, 10)
            )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


def create_docx(text_content):

    doc = Document()

    for line in str(text_content).split("\n"):

        if line.startswith("##"):

            doc.add_heading(
                line.replace("##", "").strip(),
                level=2
            )

        elif line.startswith("#"):

            doc.add_heading(
                line.replace("#", "").strip(),
                level=1
            )

        elif line.strip():

            doc.add_paragraph(
                line.strip()
            )

        else:

            doc.add_paragraph("")

    buffer = io.BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SAFE JSON PARSER
# ============================================================

def extract_json(text):

    if not text:
        return None

    text = str(text).strip()

    # Remove markdown code fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        candidate = text[start:end + 1]

        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


# ============================================================
# DEFAULT STRUCTURE
# ============================================================

def default_result():

    return {
        "executive_summary": "No structured report was generated.",
        "business_analysis": {
            "objective": "",
            "stakeholders": [],
            "constraints": [],
            "success_definition": "",
        },
        "operations_planner": {
            "workflow": [],
            "dependencies": [],
            "resources": [],
        },
        "risk_manager": {
            "risks": []
        },
        "action_planner": {
            "actions": []
        },
        "kpi_designer": {
            "kpis": []
        },
        "qa_auditor": {
            "verdict": "",
            "checks": [],
            "improvements": [],
        },
        "roadmap": [],
        "final_report": "",
    }


# ============================================================
# NORMALIZE AI RESPONSE
# ============================================================

def normalize_result(data):

    base = default_result()

    if not isinstance(data, dict):
        return base

    base.update(data)

    if not isinstance(
        base.get("business_analysis"),
        dict
    ):
        base["business_analysis"] = {
            "objective": "",
            "stakeholders": [],
            "constraints": [],
            "success_definition": "",
        }

    if not isinstance(
        base.get("operations_planner"),
        dict
    ):
        base["operations_planner"] = {
            "workflow": [],
            "dependencies": [],
            "resources": [],
        }

    if not isinstance(
        base.get("risk_manager"),
        dict
    ):
        base["risk_manager"] = {
            "risks": []
        }

    if not isinstance(
        base.get("action_planner"),
        dict
    ):
        base["action_planner"] = {
            "actions": []
        }

    if not isinstance(
        base.get("kpi_designer"),
        dict
    ):
        base["kpi_designer"] = {
            "kpis": []
        }

    if not isinstance(
        base.get("qa_auditor"),
        dict
    ):
        base["qa_auditor"] = {
            "verdict": "",
            "checks": [],
            "improvements": [],
        }

    if not isinstance(base.get("roadmap"), list):
        base["roadmap"] = []

    return base


# ============================================================
# TEXT REPORT BUILDER
# ============================================================

def build_report(data, time_period, priority):

    ba = data["business_analysis"]
    op = data["operations_planner"]
    rm = data["risk_manager"]
    ap = data["action_planner"]
    kd = data["kpi_designer"]
    qa = data["qa_auditor"]

    lines = []

    lines.append("# BusinessOps AI — Intelligence Report")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append(
        str(
            data.get(
                "executive_summary",
                ""
            )
        )
    )
    lines.append("")

    lines.append("## Business Analysis")
    lines.append(
        f"Objective: {ba.get('objective', '')}"
    )

    stakeholders = ba.get(
        "stakeholders",
        []
    )

    if stakeholders:
        lines.append("Stakeholders:")
        for item in stakeholders:
            lines.append(f"- {item}")

    constraints = ba.get(
        "constraints",
        []
    )

    if constraints:
        lines.append("Constraints:")
        for item in constraints:
            lines.append(f"- {item}")

    lines.append(
        f"Success Definition: {ba.get('success_definition', '')}"
    )

    lines.append("")

    lines.append(
        f"## Recommended Workflow — {time_period}"
    )

    for item in op.get("workflow", []):

        if isinstance(item, dict):

            step = item.get("step", "")
            owner = item.get("owner", "")
            outcome = item.get("outcome", "")

            lines.append(
                f"- {step} | Owner: {owner} | Outcome: {outcome}"
            )

        else:

            lines.append(f"- {item}")

    lines.append("")

    lines.append("## Risks & Mitigations")

    for risk in rm.get("risks", []):

        if isinstance(risk, dict):

            name = risk.get("risk", "")
            likelihood = risk.get("likelihood", "")
            impact = risk.get("impact", "")
            mitigation = risk.get("mitigation", "")

            lines.append(
                f"- {name} | Likelihood: {likelihood} | "
                f"Impact: {impact} | Mitigation: {mitigation}"
            )

        else:

            lines.append(f"- {risk}")

    lines.append("")

    lines.append(
        f"## Priority Actions — {priority}"
    )

    for action in ap.get("actions", []):

        if isinstance(action, dict):

            priority_value = action.get(
                "priority",
                ""
            )

            action_text = action.get(
                "action",
                ""
            )

            owner = action.get(
                "owner",
                ""
            )

            timing = action.get(
                "timing",
                ""
            )

            lines.append(
                f"- {priority_value} | {action_text} | "
                f"Owner: {owner} | Timing: {timing}"
            )

        else:

            lines.append(f"- {action}")

    lines.append("")

    lines.append("## KPIs / Success Metrics")

    for kpi in kd.get("kpis", []):

        if isinstance(kpi, dict):

            name = kpi.get(
                "name",
                ""
            )

            target = kpi.get(
                "target",
                ""
            )

            measurement = kpi.get(
                "measurement",
                ""
            )

            lines.append(
                f"- {name} | Target: {target} | "
                f"Measurement: {measurement}"
            )

        else:

            lines.append(f"- {kpi}")

    lines.append("")

    lines.append("## QA Check")

    lines.append(
        f"Verdict: {qa.get('verdict', '')}"
    )

    for check in qa.get("checks", []):

        lines.append(
            f"- {check}"
        )

    improvements = qa.get(
        "improvements",
        []
    )

    if improvements:

        lines.append("Recommended Improvements:")

        for item in improvements:
            lines.append(
                f"- {item}"
            )

    return "\n".join(lines)


# ============================================================
# CREWAI FLOW
# ============================================================

class BusinessOpsFlow(Flow):

    # --------------------------------------------------------
    # STAGE 01
    # --------------------------------------------------------

    @start()
    def business_analyst(self):

        request = self.state.get(
            "request",
            ""
        ).strip()

        time_period = self.state.get(
            "time_period",
            "Immediate (24-48 Hours)"
        )

        priority = self.state.get(
            "priority",
            "Medium"
        )

        return {
            "request": request,
            "time_period": time_period,
            "priority": priority,
            "business_analyst": {
                "role": "Business Analyst",
                "purpose": (
                    "Understand the business problem, "
                    "objective, stakeholders and constraints."
                )
            }
        }

    # --------------------------------------------------------
    # STAGE 02
    # --------------------------------------------------------

    @listen(business_analyst)
    def operations_planner(self, data):

        data["operations_planner"] = {
            "role": "Operations Planner",
            "purpose": (
                "Convert the business problem into "
                "an executable operational workflow."
            )
        }

        return data

    # --------------------------------------------------------
    # STAGE 03
    # --------------------------------------------------------

    @listen(operations_planner)
    def risk_manager(self, data):

        data["risk_manager"] = {
            "role": "Risk Manager",
            "purpose": (
                "Identify implementation risks and "
                "practical mitigation strategies."
            )
        }

        return data

    # --------------------------------------------------------
    # STAGE 04
    # --------------------------------------------------------

    @listen(risk_manager)
    def action_planner(self, data):

        data["action_planner"] = {
            "role": "Action Planner",
            "purpose": (
                "Convert recommendations into "
                "prioritized next actions."
            )
        }

        return data

    # --------------------------------------------------------
    # STAGE 05
    # --------------------------------------------------------

    @listen(action_planner)
    def kpi_designer(self, data):

        data["kpi_designer"] = {
            "role": "KPI Designer",
            "purpose": (
                "Define measurable outcomes "
                "and success indicators."
            )
        }

        return data

    # --------------------------------------------------------
    # STAGE 06
    # --------------------------------------------------------

    @listen(kpi_designer)
    def qa_auditor(self, data):

        data["qa_auditor"] = {
            "role": "QA Auditor",
            "purpose": (
                "Perform final quality and "
                "consistency review."
            )
        }

        return data

    # --------------------------------------------------------
    # FINAL AI EXECUTION
    # --------------------------------------------------------

    @listen(qa_auditor)
    def final_report(self, data):

        request = data["request"]

        if not request:
            return {
                "error": "Please enter a business request."
            }

        api_key = st.secrets.get(
            "GROQ_API_KEY"
        )

        if not api_key:

            return {
                "error": (
                    "GROQ_API_KEY is missing. "
                    "Add it in Streamlit Cloud → "
                    "Settings → Secrets."
                )
            }

        client = Groq(
            api_key=api_key
        )

        prompt = f"""
You are BusinessOps AI, an autonomous
business process intelligence platform.

You must execute SIX specialized agent roles
in sequence for the same business request.

BUSINESS REQUEST:
{request[:3000]}

EXECUTION TIME HORIZON:
{data["time_period"]}

PRIORITY:
{data["priority"]}

====================================================
AGENT 01 — BUSINESS ANALYST
====================================================

Understand:
- business problem
- objective
- stakeholders
- constraints
- definition of success

====================================================
AGENT 02 — OPERATIONS PLANNER
====================================================

Create:
- executable workflow
- operational steps
- responsible owners
- dependencies
- resources
- expected outcomes

====================================================
AGENT 03 — RISK MANAGER
====================================================

Identify:
- operational risks
- people risks
- technology risks
- communication risks
- timeline risks

For every major risk provide:
- risk
- likelihood
- impact
- mitigation

====================================================
AGENT 04 — ACTION PLANNER
====================================================

Create prioritized actions.

Each action must contain:
- priority
- action
- owner
- timing

====================================================
AGENT 05 — KPI DESIGNER
====================================================

Create measurable KPIs.

Each KPI must contain:
- name
- target
- measurement

====================================================
AGENT 06 — QA AUDITOR
====================================================

Review the complete proposed plan.

Check:
- completeness
- practicality
- consistency
- risk coverage
- measurability
- alignment with requested time horizon

Provide:
- verdict
- checks
- improvements

====================================================
ROADMAP
====================================================

Create 3 to 5 realistic roadmap phases.

Each roadmap item must contain:

{{
    "phase": "Phase 1",
    "task": "Task name",
    "start_day": 1,
    "end_day": 3
}}

Use relative days rather than fixed calendar dates.

====================================================
OUTPUT FORMAT
====================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "executive_summary": "...",

    "business_analysis": {{
        "objective": "...",
        "stakeholders": ["...", "..."],
        "constraints": ["...", "..."],
        "success_definition": "..."
    }},

    "operations_planner": {{
        "workflow": [
            {{
                "step": "...",
                "owner": "...",
                "outcome": "..."
            }}
        ],
        "dependencies": ["...", "..."],
        "resources": ["...", "..."]
    }},

    "risk_manager": {{
        "risks": [
            {{
                "risk": "...",
                "likelihood": "Low/Medium/High",
                "impact": "Low/Medium/High/Critical",
                "mitigation": "..."
            }}
        ]
    }},

    "action_planner": {{
        "actions": [
            {{
                "priority": "P1/P2/P3",
                "action": "...",
                "owner": "...",
                "timing": "..."
            }}
        ]
    }},

    "kpi_designer": {{
        "kpis": [
            {{
                "name": "...",
                "target": "...",
                "measurement": "..."
            }}
        ]
    }},

    "qa_auditor": {{
        "verdict": "PASS / PASS WITH IMPROVEMENTS / REVISE",
        "checks": ["...", "..."],
        "improvements": ["...", "..."]
    }},

    "roadmap": [
        {{
            "phase": "Phase 1",
            "task": "...",
            "start_day": 1,
            "end_day": 3
        }}
    ]
}}

IMPORTANT:
- Do NOT return markdown.
- Do NOT return ```json.
- Do NOT explain the JSON.
- Keep the answer concise.
- Make every section specific to the business request.
- Do not use generic placeholder content.
"""

        try:

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional autonomous "
                            "business operations intelligence "
                            "system. Return valid JSON only."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_completion_tokens=1800,
                reasoning_effort="low",
            )

            raw = response.choices[0].message.content

            parsed = extract_json(raw)

            if parsed:

                parsed = normalize_result(
                    parsed
                )

                parsed["final_report"] = build_report(
                    parsed,
                    data["time_period"],
                    data["priority"]
                )

                return parsed

            # JSON fallback
            fallback = default_result()

            fallback["executive_summary"] = raw

            fallback["final_report"] = (
                "# BusinessOps AI — Intelligence Report\n\n"
                "## Executive Summary\n\n"
                + str(raw)
            )

            return fallback

        except Exception as e:

            error_text = str(e).lower()

            if (
                "rate limit" in error_text
                or "429" in error_text
                or "tokens per minute" in error_text
            ):

                time.sleep(2)

                try:

                    retry = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.1,
                        max_completion_tokens=1200,
                        reasoning_effort="low",
                    )

                    raw_retry = (
                        retry
                        .choices[0]
                        .message
                        .content
                    )

                    parsed_retry = extract_json(
                        raw_retry
                    )

                    if parsed_retry:

                        parsed_retry = normalize_result(
                            parsed_retry
                        )

                        parsed_retry["final_report"] = (
                            build_report(
                                parsed_retry,
                                data["time_period"],
                                data["priority"]
                            )
                        )

                        return parsed_retry

                    fallback = default_result()

                    fallback["executive_summary"] = (
                        raw_retry
                    )

                    fallback["final_report"] = (
                        "# BusinessOps AI — Intelligence Report\n\n"
                        "## Executive Summary\n\n"
                        + str(raw_retry)
                    )

                    return fallback

                except Exception as retry_error:

                    return {
                        "error": (
                            "Groq rate limit is currently active. "
                            "Please wait a short time and run again.\n\n"
                            f"Technical detail: {retry_error}"
                        )
                    }

            return {
                "error": (
                    "BusinessOps AI could not complete "
                    "the analysis.\n\n"
                    f"Technical detail: {e}"
                )
            }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ⚡ BusinessOps AI"
    )

    st.markdown(
        """
        <p style='font-size:12px; color:#969aa3;'>
        Autonomous Business Process Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        "### Technology"
    )

    st.write("🐍 Python")
    st.write("🎨 Streamlit")
    st.write("🤖 CrewAI Flow")
    st.write("⚡ Groq API")
    st.write("🧠 GPT-OSS 20B")

    st.divider()

    st.markdown(
        "### Architecture"
    )

    st.write(
        "06 specialized workflow stages"
    )

    st.write(
        "01 Groq LLM call / run"
    )

    st.write(
        "Cloud deployment ready"
    )

    st.divider()

    st.caption(
        "Free-tier friendly architecture"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <span class="badge">
            AUTONOMOUS BUSINESS INTELLIGENCE
        </span>

        <h1>
            BusinessOps AI
        </h1>

        <p>
            Transform complex business requests into
            structured operational plans, risk controls,
            priority actions, and measurable outcomes
            using an agentic AI workflow.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WORKFLOW STAGES
# ============================================================

st.markdown(
    "### Agentic Workflow"
)

stages = [

    (
        "01",
        "Business Analyst",
        "Understands the business problem, objective, stakeholders and constraints."
    ),

    (
        "02",
        "Operations Planner",
        "Converts the problem into an executable operational workflow."
    ),

    (
        "03",
        "Risk Manager",
        "Identifies implementation risks and practical mitigation strategies."
    ),

    (
        "04",
        "Action Planner",
        "Converts recommendations into prioritized next actions."
    ),

    (
        "05",
        "KPI Designer",
        "Defines measurable outcomes and success indicators."
    ),

    (
        "06",
        "QA Auditor",
        "Performs a final quality and consistency review."
    ),
]


cols = st.columns(3)

for i, (
    number,
    title,
    description
) in enumerate(stages):

    with cols[i % 3]:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# METRICS
# ============================================================

st.write("")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        label="WORKFLOW STAGES",
        value="06"
    )

with m2:
    st.metric(
        label="LLM CALLS / RUN",
        value="01"
    )

with m3:
    st.metric(
        label="MODEL",
        value="20B"
    )

with m4:
    st.metric(
        label="DEPLOYMENT",
        value="CLOUD"
    )

st.write("")


# ============================================================
# BUSINESS REQUEST
# ============================================================

st.markdown(
    "### Business Request & Configuration"
)

col_c1, col_c2 = st.columns(2)

with col_c1:

    time_period = st.selectbox(
        "⏱️ Execution Time Horizon",
        [
            "Immediate (24-48 Hours)",
            "30 Days (Short-term)",
            "90 Days (Quarterly)",
            "6 Months (Strategic)"
        ]
    )

with col_c2:

    priority = st.selectbox(
        "🔥 Priority Level",
        [
            "Critical / Urgent",
            "High",
            "Medium",
            "Low"
        ]
    )


# ============================================================
# QUICK SCENARIOS
# ============================================================

sample = st.selectbox(
    "Quick scenario",
    [
        "Custom request",
        "Employee Onboarding",
        "Software Rollout",
        "Office Relocation",
        "Customer Support Improvement",
        "Inventory Management",
        "Sales Process Improvement",
    ],
)


default_text = ""


if sample == "Employee Onboarding":

    default_text = (
        "Our company is growing quickly and new "
        "employees are having difficulty completing "
        "HR, IT, security and department onboarding. "
        "Design a better onboarding process."
    )


elif sample == "Software Rollout":

    default_text = (
        "A company is introducing a new internal "
        "software platform. Employees need training, "
        "communication, migration support and a "
        "controlled rollout plan."
    )


elif sample == "Office Relocation":

    default_text = (
        "Our organization is moving to a new office. "
        "We need a plan covering employees, IT "
        "infrastructure, vendors, communication, "
        "facilities and business continuity."
    )


elif sample == "Customer Support Improvement":

    default_text = (
        "Customer support response times are increasing "
        "and customers are complaining about inconsistent "
        "answers. Create an improved support operations workflow."
    )


elif sample == "Inventory Management":

    default_text = (
        "Our business frequently experiences stockouts "
        "and excess inventory. Design a better inventory "
        "planning and monitoring process."
    )


elif sample == "Sales Process Improvement":

    default_text = (
        "Our sales team is losing leads because follow-ups "
        "are inconsistent. Create a structured sales "
        "follow-up and pipeline management process."
    )


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
# RUN BUTTON
# ============================================================

if st.button(
    "⚡ RUN BUSINESSOPS AI",
    type="primary",
    use_container_width=True
):

    if not request.strip():

        st.warning(
            "Please enter a business request first."
        )

    else:

        with st.spinner(
            "BusinessOps AI is executing six agentic workflow stages..."
        ):

            flow = BusinessOpsFlow()

            flow.state["request"] = request

            flow.state["time_period"] = (
                time_period
            )

            flow.state["priority"] = (
                priority
            )

            result = flow.kickoff()

        if (
            isinstance(result, dict)
            and result.get("error")
        ):

            st.error(
                result["error"]
            )

        else:

            st.session_state["last_result"] = (
                result
            )

            st.session_state["last_report"] = (
                result.get(
                    "final_report",
                    ""
                )
            )

            st.session_state["chat_history"] = []

            st.success(
                "All six BusinessOps AI workflow stages completed successfully."
            )


# ============================================================
# RESULTS DASHBOARD
# ============================================================

result = st.session_state.get(
    "last_result"
)


if result and not result.get("error"):

    st.write("")
    st.markdown("---")

    st.markdown(
        "### 🎛️ Interactive Intelligence Dashboard"
    )


    # ========================================================
    # AGENT SELECTOR
    # ========================================================

    agent_names = [
        "Business Analyst",
        "Operations Planner",
        "Risk Manager",
        "Action Planner",
        "KPI Designer",
        "QA Auditor",
    ]

    selected_agent = st.radio(
        "Select an agent to inspect its completed output",
        agent_names,
        horizontal=True,
        key="agent_selector",
    )


    # ========================================================
    # AGENT OUTPUT
    # ========================================================

    st.markdown(
        '<div class="agent-output">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="agent-label">ACTIVE WORKFLOW STAGE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="agent-heading">{selected_agent}</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # BUSINESS ANALYST
    # --------------------------------------------------------

    if selected_agent == "Business Analyst":

        ba = result.get(
            "business_analysis",
            {}
        )

        st.markdown(
            "**Business Objective**"
        )

        st.write(
            ba.get(
                "objective",
                "Not available"
            )
        )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                "**Stakeholders**"
            )

            for item in ba.get(
                "stakeholders",
                []
            ):

                st.write(
                    f"• {item}"
                )

        with c2:

            st.markdown(
                "**Constraints**"
            )

            for item in ba.get(
                "constraints",
                []
            ):

                st.write(
                    f"• {item}"
                )

        st.markdown(
            "**Definition of Success**"
        )

        st.info(
            ba.get(
                "success_definition",
                "Not available"
            )
        )


    # --------------------------------------------------------
    # OPERATIONS PLANNER
    # --------------------------------------------------------

    elif selected_agent == "Operations Planner":

        op = result.get(
            "operations_planner",
            {}
        )

        st.markdown(
            "#### Executable Workflow"
        )

        workflow = op.get(
            "workflow",
            []
        )

        for index, item in enumerate(
            workflow,
            start=1
        ):

            if isinstance(item, dict):

                st.markdown(
                    f"**Step {index} — {item.get('step', '')}**"
                )

                st.write(
                    f"Owner: {item.get('owner', '')}"
                )

                st.write(
                    f"Expected Outcome: {item.get('outcome', '')}"
                )

            else:

                st.write(
                    f"{index}. {item}"
                )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                "**Dependencies**"
            )

            for item in op.get(
                "dependencies",
                []
            ):

                st.write(
                    f"• {item}"
                )

        with c2:

            st.markdown(
                "**Resources**"
            )

            for item in op.get(
                "resources",
                []
            ):

                st.write(
                    f"• {item}"
                )


    # --------------------------------------------------------
    # RISK MANAGER
    # --------------------------------------------------------

    elif selected_agent == "Risk Manager":

        rm = result.get(
            "risk_manager",
            {}
        )

        risks = rm.get(
            "risks",
            []
        )

        if risks:

            risk_rows = []

            for risk in risks:

                if isinstance(
                    risk,
                    dict
                ):

                    risk_rows.append(
                        {
                            "Risk": risk.get(
                                "risk",
                                ""
                            ),
                            "Likelihood": risk.get(
                                "likelihood",
                                ""
                            ),
                            "Impact": risk.get(
                                "impact",
                                ""
                            ),
                            "Mitigation": risk.get(
                                "mitigation",
                                ""
                            ),
                        }
                    )

            if risk_rows:

                st.dataframe(
                    pd.DataFrame(risk_rows),
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.info(
                "No structured risks returned."
            )


    # --------------------------------------------------------
    # ACTION PLANNER
    # --------------------------------------------------------

    elif selected_agent == "Action Planner":

        ap = result.get(
            "action_planner",
            {}
        )

        actions = ap.get(
            "actions",
            []
        )

        action_rows = []

        for action in actions:

            if isinstance(
                action,
                dict
            ):

                action_rows.append(
                    {
                        "Priority": action.get(
                            "priority",
                            ""
                        ),
                        "Action": action.get(
                            "action",
                            ""
                        ),
                        "Owner": action.get(
                            "owner",
                            ""
                        ),
                        "Timing": action.get(
                            "timing",
                            ""
                        ),
                    }
                )

        if action_rows:

            st.dataframe(
                pd.DataFrame(action_rows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No structured actions returned."
            )


    # --------------------------------------------------------
    # KPI DESIGNER
    # --------------------------------------------------------

    elif selected_agent == "KPI Designer":

        kd = result.get(
            "kpi_designer",
            {}
        )

        kpis = kd.get(
            "kpis",
            []
        )

        kpi_rows = []

        for kpi in kpis:

            if isinstance(
                kpi,
                dict
            ):

                kpi_rows.append(
                    {
                        "KPI": kpi.get(
                            "name",
                            ""
                        ),
                        "Target": kpi.get(
                            "target",
                            ""
                        ),
                        "Measurement": kpi.get(
                            "measurement",
                            ""
                        ),
                    }
                )

        if kpi_rows:

            st.dataframe(
                pd.DataFrame(kpi_rows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No structured KPIs returned."
            )


    # --------------------------------------------------------
    # QA AUDITOR
    # --------------------------------------------------------

    elif selected_agent == "QA Auditor":

        qa = result.get(
            "qa_auditor",
            {}
        )

        verdict = qa.get(
            "verdict",
            "Not available"
        )

        st.markdown(
            "#### QA Verdict"
        )

        if "PASS" in verdict.upper():

            st.success(
                verdict
            )

        else:

            st.warning(
                verdict
            )

        st.markdown(
            "#### QA Checks"
        )

        for check in qa.get(
            "checks",
            []
        ):

            st.write(
                f"✓ {check}"
            )

        improvements = qa.get(
            "improvements",
            []
        )

        if improvements:

            st.markdown(
                "#### Recommended Improvements"
            )

            for item in improvements:

                st.write(
                    f"• {item}"
                )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Operational Overview",
            "🗺 Milestone Roadmap",
            "🛡️ Risk Operations",
            "🎯 KPI Dashboard",
            "📝 Full Intelligence Report",
        ]
    )


    # ========================================================
    # TAB 1 — OVERVIEW
    # ========================================================

    with tab1:

        om1, om2, om3, om4 = st.columns(4)

        with om1:

            st.metric(
                label="TIME HORIZON",
                value=time_period.split(" ")[0]
            )

        with om2:

            st.metric(
                label="PRIORITY",
                value=priority.split(" ")[0]
            )

        with om3:

            risk_count = len(
                result
                .get("risk_manager", {})
                .get("risks", [])
            )

            st.metric(
                label="RISKS IDENTIFIED",
                value=str(risk_count)
            )

        with om4:

            kpi_count = len(
                result
                .get("kpi_designer", {})
                .get("kpis", [])
            )

            st.metric(
                label="KPIs CREATED",
                value=str(kpi_count)
            )

        st.write("")

        st.markdown(
            "#### Executive Summary"
        )

        st.info(
            result.get(
                "executive_summary",
                "No summary available."
            )
        )

        st.markdown(
            "#### Agent Execution Status"
        )

        status_cols = st.columns(6)

        for i, agent in enumerate(
            agent_names
        ):

            with status_cols[i]:

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        padding:12px 5px;
                        border:1px solid #292c33;
                        border-radius:10px;
                        background:#0d0f13;
                    ">
                        <div style="
                            font-size:10px;
                            color:#d98294;
                            font-weight:800;
                        ">
                            0{i+1}
                        </div>

                        <div style="
                            font-size:10px;
                            color:#d7d7d4;
                            margin-top:5px;
                        ">
                            {agent}
                        </div>

                        <div style="
                            color:#7fd39b;
                            font-size:10px;
                            margin-top:7px;
                        ">
                            ✓ COMPLETED
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # TAB 2 — ROADMAP
    # ========================================================

    with tab2:

        st.markdown(
            "#### 🗺 AI-Generated Milestone Roadmap"
        )

        roadmap = result.get(
            "roadmap",
            []
        )

        gantt_rows = []

        for item in roadmap:

            if not isinstance(
                item,
                dict
            ):
                continue

            try:

                start_day = int(
                    item.get(
                        "start_day",
                        1
                    )
                )

                end_day = int(
                    item.get(
                        "end_day",
                        start_day + 1
                    )
                )

            except Exception:

                start_day = 1
                end_day = 2

            gantt_rows.append(
                {
                    "Task": item.get(
                        "task",
                        item.get(
                            "phase",
                            "Phase"
                        )
                    ),
                    "Start": start_day,
                    "Finish": max(
                        end_day,
                        start_day + 1
                    ),
                    "Phase": item.get(
                        "phase",
                        "Execution"
                    ),
                }
            )

        if gantt_rows:

            gantt_df = pd.DataFrame(
                gantt_rows
            )

            fig = px.timeline(
                gantt_df,
                x_start="Start",
                x_end="Finish",
                y="Task",
                color="Phase",
            )

            fig.update_yaxes(
                autorange="reversed"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#eeeeec",
                margin=dict(
                    t=10,
                    b=10,
                    l=10,
                    r=10
                ),
                height=320,
                xaxis_title="Relative Execution Days",
                yaxis_title="",
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                gantt_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "The AI did not return a roadmap."
            )


    # ========================================================
    # TAB 3 — RISK OPERATIONS
    # ========================================================

    with tab3:

        st.markdown(
            "#### 🛡 AI Risk Operations"
        )

        risks = result.get(
            "risk_manager",
            {}
        ).get(
            "risks",
            []
        )

        risk_rows = []

        for risk in risks:

            if isinstance(
                risk,
                dict
            ):

                risk_rows.append(
                    {
                        "Risk Factor": risk.get(
                            "risk",
                            ""
                        ),
                        "Likelihood": risk.get(
                            "likelihood",
                            ""
                        ),
                        "Impact": risk.get(
                            "impact",
                            ""
                        ),
                        "Mitigation": risk.get(
                            "mitigation",
                            ""
                        ),
                    }
                )

        if risk_rows:

            risk_df = pd.DataFrame(
                risk_rows
            )

            st.dataframe(
                risk_df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown(
                "#### Risk Impact vs Likelihood Matrix"
            )

            matrix = []

            for row in risk_rows:

                matrix.append(
                    {
                        "Risk": row["Risk Factor"],
                        "Likelihood": row["Likelihood"],
                        "Impact": row["Impact"],
                    }
                )

            matrix_df = pd.DataFrame(
                matrix
            )

            st.dataframe(
                matrix_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No risks were generated."
            )


    # ========================================================
    # TAB 4 — KPI DASHBOARD
    # ========================================================

    with tab4:

        st.markdown(
            "#### 🎯 AI-Generated Success Metrics"
        )

        kpis = result.get(
            "kpi_designer",
            {}
        ).get(
            "kpis",
            []
        )

        kpi_rows = []

        for kpi in kpis:

            if isinstance(
                kpi,
                dict
            ):

                kpi_rows.append(
                    {
                        "KPI": kpi.get(
                            "name",
                            ""
                        ),
                        "Target": kpi.get(
                            "target",
                            ""
                        ),
                        "Measurement": kpi.get(
                            "measurement",
                            ""
                        ),
                    }
                )

        if kpi_rows:

            st.dataframe(
                pd.DataFrame(kpi_rows),
                use_container_width=True,
                hide_index=True
            )

            kcols = st.columns(
                min(
                    len(kpi_rows),
                    4
                )
            )

            for i, kpi in enumerate(
                kpi_rows[:4]
            ):

                with kcols[i]:

                    st.metric(
                        label=kpi["KPI"][:28],
                        value=kpi["Target"][:30]
                    )

        else:

            st.info(
                "No KPI data was generated."
            )


    # ========================================================
    # TAB 5 — FULL REPORT
    # ========================================================

    with tab5:

        st.markdown(
            f"""
            <div class="report">
            {result.get(
                "final_report",
                ""
            ).replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        dl1, dl2, dl3 = st.columns(3)

        report_text = result.get(
            "final_report",
            ""
        )

        with dl1:

            st.download_button(
                "📥 Download Text (.txt)",
                data=report_text,
                file_name="businessops_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with dl2:

            pdf_bytes = create_pdf(
                report_text
            )

            st.download_button(
                "📥 Download PDF (.pdf)",
                data=pdf_bytes,
                file_name="businessops_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with dl3:

            docx_bytes = create_docx(
                report_text
            )

            st.download_button(
                "📥 Download Word (.docx)",
                data=docx_bytes,
                file_name="businessops_report.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )


    # ========================================================
    # CHAT WITH OPS PLAN
    # ========================================================

    st.write("")
    st.markdown("---")

    st.markdown(
        "### 💬 Chat with your Ops Plan"
    )

    st.markdown(
        """
        <p style='font-size:12px; color:#969aa3;'>
        Ask follow-up questions about the generated
        operational plan, risks, actions, KPIs or roadmap.
        </p>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state[
        "chat_history"
    ]:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    if user_query := st.chat_input(
        "Ask a question about your operational plan..."
    ):

        st.session_state[
            "chat_history"
        ].append(
            {
                "role": "user",
                "content": user_query
            }
        )

        with st.chat_message("user"):

            st.markdown(
                user_query
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analyzing the operational plan..."
            ):

                api_key = st.secrets.get(
                    "GROQ_API_KEY"
                )

                if not api_key:

                    chat_response = (
                        "GROQ_API_KEY is missing."
                    )

                else:

                    try:

                        chat_client = Groq(
                            api_key=api_key
                        )

                        chat_prompt = f"""
You are BusinessOps AI.

Answer the user's question using
the generated business operations report.

REPORT:
{result.get("final_report", "")[:7000]}

USER QUESTION:
{user_query}

Give a concise, practical,
professional answer.
"""

                        chat_completion = (
                            chat_client
                            .chat
                            .completions
                            .create(
                                model=MODEL,
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are a professional "
                                            "business operations "
                                            "assistant."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": chat_prompt
                                    }
                                ],
                                temperature=0.2,
                                max_completion_tokens=400,
                                reasoning_effort="low",
                            )
                        )

                        chat_response = (
                            chat_completion
                            .choices[0]
                            .message
                            .content
                            .strip()
                        )

                    except Exception as e:

                        chat_response = (
                            f"Could not generate response: {e}"
                        )

            st.markdown(
                chat_response
            )

            st.session_state[
                "chat_history"
            ].append(
                {
                    "role": "assistant",
                    "content": chat_response
                }
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#667386;
        font-size:12px;
    ">
        BusinessOps AI • Autonomous Business Process Intelligence
        • CrewAI + Groq • Cloud Deployment Architecture
    </div>
    """,
    unsafe_allow_html=True,
)
