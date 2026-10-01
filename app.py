import time
import streamlit as st
from groq import Groq

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
# PREMIUM CHARCOAL + DEEP MAROON THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL APPLICATION
       ====================================================== */

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


    /* ======================================================
       SIDEBAR
       ====================================================== */

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

    section[data-testid="stSidebar"] p {
        color: #969aa3;
        line-height: 1.65;
    }

    section[data-testid="stSidebar"] h3 {
        color: #f1f1ef !important;
        letter-spacing: -0.4px;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    h1 {
        color: #f5f4f1 !important;
        font-weight: 900 !important;
        letter-spacing: -1.8px !important;
    }

    h2 {
        color: #eeeDEA !important;
        font-weight: 850 !important;
        letter-spacing: -0.8px !important;
    }

    h3 {
        color: #e5e3df !important;
        font-weight: 750 !important;
        letter-spacing: -0.3px !important;
    }

    p {
        color: #c8c9cc;
        line-height: 1.75;
    }

    li {
        color: #c8c9cc;
        line-height: 1.7;
    }

    strong {
        color: #f0efec;
    }

    small {
        color: #858992;
    }


    /* ======================================================
       CAPTIONS / LABELS
       ====================================================== */

    [data-testid="stCaptionContainer"] {
        color: #858a94 !important;
    }

    label {
        color: #a9adb5 !important;
        font-size: 11px !important;
        font-weight: 650 !important;
    }


    /* ======================================================
       CARDS / CONTAINERS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(20, 19, 23, 0.98),
                rgba(11, 12, 15, 0.98)
            ) !important;

        border: 1px solid rgba(255, 255, 255, 0.065) !important;
        border-radius: 16px !important;

        box-shadow:
            0 14px 38px rgba(0, 0, 0, 0.20);
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    textarea,
    input {
        background: #0c0e12 !important;
        color: #f2f1ee !important;
        border: 1px solid #292c33 !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        line-height: 1.65 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #6f747d !important;
        font-size: 12px !important;
    }

    textarea:focus,
    input:focus {
        border-color: #823249 !important;

        box-shadow:
            0 0 0 1px rgba(157, 58, 84, 0.18),
            0 0 20px rgba(122, 34, 55, 0.08) !important;
    }


    /* ======================================================
       SELECTBOX
       ====================================================== */

    div[data-baseweb="select"] > div {
        background: #0c0e12 !important;
        border-color: #292c33 !important;
        border-radius: 10px !important;
        min-height: 43px !important;
    }

    div[data-baseweb="select"] span {
        font-size: 12px !important;
        color: #ddddda !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

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
        letter-spacing: 0.1px;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.22);

        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: rgba(210, 145, 160, 0.45);

        background:
            linear-gradient(
                105deg,
                #893149 0%,
                #6c293b 50%,
                #542532 100%
            );

        box-shadow:
            0 12px 32px rgba(116, 34, 55, 0.20);

        transform: translateY(-1px);
    }


    /* ======================================================
       DOWNLOAD BUTTONS
       ====================================================== */

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

    div[data-testid="stDownloadButton"] button:hover {
        border-color: #743047;
        color: #eeeeee;
        background: #13151a;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.030),
                rgba(255, 255, 255, 0.012)
            );

        border: 1px solid rgba(255, 255, 255, 0.055);
        border-radius: 12px;
        padding: 14px 15px;

        box-shadow:
            0 7px 20px rgba(0, 0, 0, 0.12);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 9px !important;
        color: #777d87 !important;
        font-weight: 750 !important;
        letter-spacing: 0.6px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        color: #e5e4e1 !important;
        font-weight: 800 !important;
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        color: #777d87 !important;
        font-size: 11px !important;
        font-weight: 750 !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #b76a7f !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #c98294 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background: #8c334d !important;
    }


    /* ======================================================
       EXPANDER
       ====================================================== */

    div[data-testid="stExpander"] {
        background:
            linear-gradient(
                145deg,
                #0e1014,
                #0b0c10
            );

        border: 1px solid #282b32;
        border-radius: 11px;
    }

    div[data-testid="stExpander"] summary {
        color: #d7d7d4 !important;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: rgba(255, 255, 255, 0.055) !important;
    }


    /* ======================================================
       SCROLLBAR
       ====================================================== */

    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #08090c;
    }

    ::-webkit-scrollbar-thumb {
        background: #30252b;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #663044;
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

        h2 {
            font-size: 25px !important;
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
# CREWAI FLOW
# ============================================================

class BusinessOpsFlow(Flow):

    @start()
    def intake(self):
        return {
            "request": self.state.get("request", "").strip()
        }

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

    @listen(business_analysis)
    def operations_planning(self, data):
        return {
            **data,
            "operations": (
                "Design practical operational steps, responsible roles, "
                "dependencies, resources, and measurable outcomes."
            ),
        }

    @listen(operations_planning)
    def risk_management(self, data):
        return {
            **data,
            "risk": (
                "Identify operational, people, technology, communication, "
                "timeline, and implementation risks."
            ),
        }

    @listen(risk_management)
    def action_planning(self, data):
        return {
            **data,
            "actions": (
                "Create prioritized next actions and define what should "
                "happen immediately, next, and later."
            ),
        }

    @listen(action_planning)
    def quality_control(self, data):
        return {
            **data,
            "qa": (
                "Check whether the proposed workflow is practical, "
                "complete, consistent, and measurable."
            ),
        }

    @listen(quality_control)
    def final_report(self, data):

        if not data["request"]:
            return "Please enter a business request."

        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return (
                "GROQ_API_KEY is missing. "
                "Add it in Streamlit Cloud → Settings → Secrets."
            )

        client = Groq(api_key=api_key)

        prompt = f"""
You are BusinessOps AI, an autonomous business process intelligence
assistant.

Analyze this business request:

{data["request"][:2500]}

Internal workflow stages:

1. Business Analysis
{data["analysis"]}

2. Operations Planning
{data["operations"]}

3. Risk Management
{data["risk"]}

4. Action Planning
{data["actions"]}

5. Quality Control
{data["qa"]}

Generate a professional Business Operations Report.

Use exactly these sections:

## Executive Summary
## Business Analysis
## Recommended Workflow
## Risks & Mitigations
## Priority Actions
## KPIs / Success Metrics
## QA Check

Requirements:
- Be practical and specific.
- Do not invent company-specific facts.
- Use concise professional language.
- Give actionable recommendations.
- Maximum approximately 450 words.
"""

        try:

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional business operations "
                            "intelligence assistant. Produce concise, "
                            "structured and actionable reports."
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
                return "The AI returned an empty response. Please try again."

            return result.strip()

        except Exception as e:

            error_text = str(e).lower()

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

                    retry_result = retry.choices[0].message.content

                    if retry_result and retry_result.strip():
                        return retry_result.strip()

                    return "Groq returned an empty response after retry."

                except Exception as retry_error:

                    return (
                        "Groq rate limit is temporarily active. "
                        "Please wait a few seconds and run again.\n\n"
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

    st.markdown("## ⚡ BusinessOps AI")

    st.markdown(
        """
        <div class="small-muted">
        Autonomous Business Process Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True,
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

st.markdown(
    """
    <div class="hero">

        <span class="badge">
            AUTONOMOUS BUSINESS INTELLIGENCE
        </span>

        <h1>BusinessOps AI</h1>

        <p>
        Transform complex business requests into structured
        operational plans, risk controls, priority actions,
        and measurable outcomes using an agentic AI workflow.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
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

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">WORKFLOW STAGES</div>
            <div class="metric-value">06</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">LLM CALLS / RUN</div>
            <div class="metric-value">01</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">MODEL</div>
            <div class="metric-value">20B</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">DEPLOYMENT</div>
            <div class="metric-value">CLOUD</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ============================================================
# BUSINESS REQUEST
# ============================================================

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


request = st.text_area(
    "Describe your business problem or process",
    value=default_text,
    height=170,
    placeholder=(
        "Example: Our company wants to improve employee onboarding..."
    ),
)


# ============================================================
# EXECUTE
# ============================================================

if st.button(
    "⚡ RUN BUSINESSOPS AI",
    type="primary",
    use_container_width=True,
):

    if not request.strip():

        st.warning("Please enter a business request first.")

    else:

        with st.spinner(
            "BusinessOps AI is analyzing the request and generating the report..."
        ):

            flow = BusinessOpsFlow()
            flow.state["request"] = request

            result = flow.kickoff()

        st.success("Business workflow completed.")

        st.markdown("### Intelligence Report")

        st.markdown(
            f"""
            <div class="report">
            {result.replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.download_button(
            "Download Report",
            data=str(result),
            file_name="businessops_report.txt",
            mime="text/plain",
            use_container_width=True,
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
        • CrewAI + Groq • Free-tier deployment architecture
    </div>
    """,
    unsafe_allow_html=True,
)
