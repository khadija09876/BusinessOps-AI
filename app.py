import time
import streamlit as st
from groq import Groq
from crewai.flow.flow import Flow, start, listen

# ============================================================
# BUSINESSOPS AI
# Reliable FREE-tier architecture
#
# Python + Streamlit + CrewAI Flow + Groq SDK
#
# IMPORTANT:
# - One Groq request per workflow run
# - No LiteLLM
# - No 6 separate LLM calls
# - No Ollama
# - No local model
# - Uses openai/gpt-oss-20b
#
# The CrewAI Flow contains the business workflow stages.
# The final AI generation is done by ONE Groq request.
# ============================================================

st.set_page_config(
    page_title="BusinessOps AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# UI
# -----------------------------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(0,229,255,.08), transparent 28%),
        radial-gradient(circle at 85% 10%, rgba(124,58,237,.10), transparent 30%),
        #070A10;
    color: #E8EEF7;
}
[data-testid="stSidebar"] {
    background: #0B0F17;
    border-right: 1px solid #202A3A;
}
.hero {
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #273348;
    background: linear-gradient(135deg,#0D1521,#090D15,#111126);
    margin-bottom: 22px;
}
.eyebrow {
    color: #00E5FF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}
.hero h1 {
    color: white;
    font-size: 44px;
    margin: 8px 0;
}
.hero p {
    color: #9AA7BA;
    font-size: 16px;
}
.card {
    background: #0C111A;
    border: 1px solid #222D3E;
    border-radius: 16px;
    padding: 18px;
    min-height: 125px;
}
.card-title {
    color: white;
    font-size: 16px;
    font-weight: 800;
}
.card-text {
    color: #8D9AAF;
    font-size: 13px;
    line-height: 1.5;
    margin-top: 8px;
}
.badge {
    display: inline-block;
    margin-top: 10px;
    padding: 5px 9px;
    border-radius: 20px;
    border: 1px solid rgba(0,229,255,.25);
    color: #00E5FF;
    background: rgba(0,229,255,.08);
    font-size: 10px;
    font-weight: 800;
}
.metric {
    background: #0C111A;
    border: 1px solid #222D3E;
    border-radius: 14px;
    padding: 15px;
}
.metric-label {
    color: #7D8A9E;
    font-size: 10px;
    letter-spacing: 1px;
}
.metric-value {
    color: white;
    font-size: 22px;
    font-weight: 800;
    margin-top: 5px;
}
.section {
    color: white;
    font-size: 22px;
    font-weight: 800;
    margin: 22px 0 12px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SETTINGS
# ============================================================

MODEL = "openai/gpt-oss-20b"


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


# ============================================================
# CREWAI FLOW
# ============================================================
#
# These are workflow stages, not six separate LLM calls.
# This is intentional: Groq's free tier has a combined TPM
# limit, so calling the LLM six times can exceed it.
#
# ============================================================

class BusinessOpsFlow(Flow):

    def __init__(self, business_request):
        super().__init__()
        self.business_request = business_request

    @start()
    def intake(self):
        request = self.business_request.strip()[:2200]

        return {
            "request": request,
            "stage": "Intake",
        }

    @listen(intake)
    def business_analysis(self, data):
        request = data["request"]

        return {
            "request": request,
            "analysis_role": (
                "Business Analyst: identify objective, stakeholders, "
                "requirements and assumptions."
            ),
            "stage": "Business Analysis",
        }

    @listen(business_analysis)
    def operations_planning(self, data):
        return {
            **data,
            "planning_role": (
                "Operations Planner: create practical tasks, owners, "
                "priorities, dependencies, risks and success metrics."
            ),
            "stage": "Operations Planning",
        }

    @listen(operations_planning)
    def qa_definition(self, data):
        return {
            **data,
            "qa_role": (
                "QA Auditor: validate completeness, ownership, "
                "dependencies, risks and operational readiness."
            ),
            "stage": "QA Audit",
        }

    @listen(qa_definition)
    def generate_final_report(self, data):
        api_key = get_api_key()

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing from Streamlit Secrets."
            )

        # ----------------------------------------------------
        # ONE AND ONLY ONE Groq request
        # ----------------------------------------------------
        prompt = f"""
You are BusinessOps AI.

Business request:
{data["request"]}

Execute these internal roles in one response:

1. BUSINESS ANALYST
{data["analysis_role"]}

2. OPERATIONS PLANNER
{data["planning_role"]}

3. QA AUDITOR
{data["qa_role"]}

Return a concise professional report using exactly:

## EXECUTIVE SUMMARY
3 short sentences.

## BUSINESS ANALYSIS
Objective:
Stakeholders:
Requirements:
Assumptions:

## OPERATIONS PLAN
| # | Task | Owner | Priority | Dependency |
|---|---|---|---|---|
Create 5 tasks.

## RISKS & MITIGATIONS
- Risk → Mitigation
- Risk → Mitigation
- Risk → Mitigation

## SUCCESS METRICS
- Metric
- Metric
- Metric

## COMMUNICATION DRAFT
One short internal message.

## NEXT ACTIONS
1.
2.
3.

## QA AUDIT
Status: PASS / PASS WITH NOTES / NEEDS REVIEW
Findings:
- 
- 
Recommendation:
-

Maximum 450 words.
Do not explain your process.
"""

        client = Groq(api_key=api_key)

        # A small retry handles a transient 429.
        # It does NOT make repeated calls when the first call succeeds.
        last_error = None

        for attempt in range(2):

            try:
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a concise enterprise business "
                                "operations analyst. Return useful "
                                "business-ready content."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.1,
                    max_completion_tokens=450,
                    reasoning_effort="low",
                )

                content = completion.choices[0].message.content

                if content and content.strip():
                    return content.strip()

                raise RuntimeError(
                    "Groq returned an empty response."
                )

            except Exception as error:
                last_error = error
                message = str(error).lower()

                if (
                    "rate_limit" not in message
                    and "rate limit" not in message
                    and "429" not in message
                ):
                    raise

                if attempt == 0:
                    time.sleep(3)

        raise RuntimeError(
            "Groq rate limit is still active. "
            "Please wait 30–60 seconds before running again."
        ) from last_error


# ============================================================
# SAMPLE REQUESTS
# ============================================================

examples = {
    "Employee Onboarding":
        "Our company is hiring 20 employees next month. "
        "Create an onboarding workflow covering HR documentation, "
        "IT accounts, laptops, security training and department orientation.",

    "Software Rollout":
        "We need to roll out a new project management platform "
        "to 120 employees. Plan pilot testing, training, account setup, "
        "communication and post-launch support.",

    "Office Relocation":
        "Our 80-person office is moving to a new location in six weeks. "
        "Create a plan covering facilities, IT, employees, vendors, "
        "equipment movement, security and communication.",

    "Customer Support":
        "Our customer support team has too many unresolved tickets. "
        "Create an improvement plan covering ticket ownership, escalation, "
        "response targets, training and quality monitoring.",
}


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">AI OPERATIONS CONTROL CENTER</div>
    <h1>BusinessOps AI</h1>
    <p>
        Transform an unstructured business request into an
        actionable, risk-aware and quality-checked execution plan.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Control Center")

    st.markdown("### Workflow")

    st.markdown("""
    **01 — Intake**  
    Capture business request.

    **02 — Business Analysis**  
    Identify objectives and requirements.

    **03 — Operations Planning**  
    Build tasks and dependencies.

    **04 — QA Audit**  
    Validate the final workflow.

    **05 — AI Report**  
    One Groq generation produces the final result.
    """)

    st.divider()

    st.markdown("### Stack")
    st.caption("Python 3.14")
    st.caption("Streamlit")
    st.caption("CrewAI Flow")
    st.caption("Groq SDK")
    st.caption("GPT-OSS 20B")

    st.divider()

    st.caption("No Ollama")
    st.caption("No local model")
    st.caption("No paid database")


# ============================================================
# WORKFLOW CARDS
# ============================================================

st.markdown(
    '<div class="section">Workflow Pipeline</div>',
    unsafe_allow_html=True
)

cards = [
    ("01", "Business Analyst", "Objective, stakeholders and requirements."),
    ("02", "Operations Planner", "Tasks, owners, priorities and dependencies."),
    ("03", "Risk Manager", "Risks and mitigation planning."),
    ("04", "Communications", "Professional internal communication."),
    ("05", "Next Actions", "Immediate executable actions."),
    ("06", "QA Auditor", "Final completeness and readiness check."),
]

cols = st.columns(3)

for i, (number, title, description) in enumerate(cards):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">
                    {number} · {title}
                </div>
                <div class="card-text">
                    {description}
                </div>
                <div class="badge">WORKFLOW STAGE</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

metric_data = [
    ("AI ENGINE", "Groq"),
    ("MODEL", "GPT-OSS 20B"),
    ("LLM CALLS", "1 / RUN"),
    ("ORCHESTRATION", "CrewAI"),
]

for col, (label, value) in zip(
    [m1, m2, m3, m4],
    metric_data
):
    with col:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# INPUT
# ============================================================

st.markdown(
    '<div class="section">Business Request</div>',
    unsafe_allow_html=True
)

scenario = st.selectbox(
    "Choose a sample scenario",
    ["Custom Request"] + list(examples.keys())
)

default_request = (
    ""
    if scenario == "Custom Request"
    else examples[scenario]
)

business_request = st.text_area(
    "Describe your business problem",
    value=default_request,
    height=170,
    placeholder=(
        "Example: We are onboarding 30 employees and need "
        "HR, IT and department managers to coordinate."
    ),
)

run = st.button(
    "🚀 Run BusinessOps AI",
    type="primary",
    use_container_width=True,
)


# ============================================================
# EXECUTION
# ============================================================

if run:

    if not business_request.strip():
        st.warning("Please enter a business request.")

    elif len(business_request.strip()) < 20:
        st.warning("Please provide more details about the business problem.")

    else:

        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Starting CrewAI workflow...")
            progress.progress(15)

            flow = BusinessOpsFlow(
                business_request
            )

            status.info("Business Analysis...")
            progress.progress(30)

            status.info("Operations Planning...")
            progress.progress(50)

            status.info("QA Audit...")
            progress.progress(70)

            # CrewAI Flow runs the workflow.
            result = flow.kickoff()

            progress.progress(100)

            status.success(
                "Workflow completed — one Groq generation used."
            )

            st.markdown(
                '<div class="section">Business Execution Report</div>',
                unsafe_allow_html=True
            )

            st.markdown(result)

        except Exception as error:

            progress.empty()
            status.empty()

            error_text = str(error)
            lower = error_text.lower()

            if (
                "rate_limit" in lower
                or "rate limit" in lower
                or "429" in lower
                or "tokens per minute" in lower
                or "token-per-minute" in lower
            ):
                st.error("Groq TPM rate limit is currently active.")

                st.warning(
                    "Wait 30–60 seconds and run the workflow ONCE. "
                    "This version sends only one Groq generation per run."
                )

            elif "groq_api_key" in lower:
                st.error("GROQ_API_KEY is missing.")

                st.code(
                    'GROQ_API_KEY = "your_groq_api_key"',
                    language="toml"
                )

            elif "empty response" in lower or "none or empty" in lower:
                st.error(
                    "Groq returned an empty response. "
                    "Please run once again after a short wait."
                )

            else:
                st.error(
                    "BusinessOps workflow failed."
                )
                st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "BusinessOps AI • CrewAI Flow • Groq • GPT-OSS 20B • "
    "One-call free-tier architecture"
)
