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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0, 229, 255, 0.08), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(139, 92, 246, 0.08), transparent 30%),
            #070b12;
        color: #f4f7fb;
    }

    section[data-testid="stSidebar"] {
        background: #090e17;
        border-right: 1px solid #1c2635;
    }

    .hero {
        padding: 35px 10px 20px 10px;
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

    .hero h1 {
        font-size: 48px;
        margin: 15px 0 5px 0;
        font-weight: 800;
    }

    .hero p {
        color: #9ba8b8;
        font-size: 17px;
        max-width: 850px;
    }

    .stage {
        background: linear-gradient(
            145deg,
            rgba(18, 27, 40, 0.95),
            rgba(9, 15, 24, 0.95)
        );
        border: 1px solid #1d2a3b;
        border-radius: 15px;
        padding: 18px;
        min-height: 145px;
        margin-bottom: 12px;
    }

    .stage-number {
        color: #61eaff;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .stage-title {
        font-size: 17px;
        font-weight: 750;
        margin-top: 8px;
    }

    .stage-text {
        color: #8f9dad;
        font-size: 13px;
        margin-top: 8px;
        line-height: 1.5;
    }

    .metric-card {
        background: #0c131e;
        border: 1px solid #1c2939;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
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

    .report {
        background: #0b121c;
        border: 1px solid #203044;
        border-radius: 16px;
        padding: 25px;
        line-height: 1.65;
    }

    .small-muted {
        color: #7f8c9d;
        font-size: 12px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 700;
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

        <span class="badge">AUTONOMOUS BUSINESS INTELLIGENCE</span>

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
    <div style="text-align:center;color:#667386;font-size:12px;">
        BusinessOps AI • Autonomous Business Process Intelligence
        • CrewAI + Groq • Free-tier deployment architecture
    </div>
    """,
    unsafe_allow_html=True,
)
