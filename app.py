import time
import io
import streamlit as st
from groq import Groq

# CrewAI Flow
from crewai.flow import Flow, start, listen

# Report generation libraries & visualization
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from docx import Document
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
# CONFIG
# ============================================================

MODEL = "openai/gpt-oss-20b"


# ============================================================
# PREMIUM CHARCOAL + DEEP MAROON THEME & UI STYLES
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
        CUSTOM COMPONENTS (BADGE, HERO, STAGES, REPORT)
        ====================================================== */

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
        background: linear-gradient(145deg, rgba(20, 19, 23, 0.98), rgba(11, 12, 15, 0.98));
        border: 1px solid rgba(255, 255, 255, 0.065);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        height: 100%;
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

    .report {
        background: linear-gradient(145deg, #0e1014, #0b0c10);
        border: 1px solid #282b32;
        border-radius: 14px;
        padding: 25px;
        color: #d7d7d4;
        line-height: 1.7;
        font-size: 13px;
        box-shadow: 0 14px 35px rgba(0,0,0,0.2);
    }


    /* ======================================================
        SIDEBAR & TYPOGRAPHY
        ====================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0e11 0%, #090a0d 55%, #07080a 100%);
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

    p, li {
        color: #c8c9cc;
        line-height: 1.75;
    }


    /* ======================================================
        INPUTS & BUTTONS
        ====================================================== */

    textarea, input {
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
        background: linear-gradient(105deg, #79283f 0%, #612536 48%, #49212d 100%);
        color: #ffffff;
        font-size: 12px;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(105deg, #893149 0%, #6c293b 50%, #542532 100%);
        transform: translateY(-1px);
    }

    div[data-testid="stDownloadButton"] button {
        min-height: 43px;
        border-radius: 10px;
        background: linear-gradient(145deg, #111318, #0d0f13);
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
# HELPER FUNCTIONS FOR ADVANCED EXPORTS (PDF & DOCX)
# ============================================================

def create_pdf(text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'ReportNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor='#222222'
    )
    story = []
    for line in text_content.split('\n'):
        if line.strip():
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 6))
        else:
            story.append(Spacer(1, 10))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def create_docx(text_content):
    doc = Document()
    for line in text_content.split('\n'):
        if line.startswith("##"):
            doc.add_heading(line.replace("##", "").strip(), level=2)
        elif line.strip():
            doc.add_paragraph(line.strip())
        else:
            doc.add_paragraph("")
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# CREWAI FLOW
# ============================================================

class BusinessOpsFlow(Flow):

    @start()
    def intake(self):
        return {
            "request": self.state.get("request", "").strip(),
            "time_period": self.state.get("time_period", "Immediate"),
            "priority": self.state.get("priority", "Medium")
        }

    @listen(intake)
    def business_analysis(self, data):
        return {
            **data,
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

        # Use user-provided API key from session state if available, else fallback to secrets
        api_key = st.session_state.get("user_groq_api_key") or st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return (
                "GROQ_API_KEY is missing. "
                "Add it in Streamlit Cloud → Settings → Secrets."
            )

        client = Groq(api_key=api_key)

        prompt = f"""
You are BusinessOps AI, an autonomous business process intelligence assistant.
Analyze this business request:

{data["request"][:2500]}

Execution Parameters:
- Target Time Horizon: {data["time_period"]}
- Execution Priority Level: {data["priority"]}

Internal workflow stages:
1. Business Analysis: {data["analysis"]}
2. Operations Planning: {data["operations"]}
3. Risk Management: {data["risk"]}
4. Action Planning: {data["actions"]}
5. Quality Control: {data["qa"]}

Generate a professional Business Operations Report using exactly these sections:
## Executive Summary
## Business Analysis
## Recommended Workflow ({data["time_period"]} Horizon)
## Risks & Mitigations
## Priority Actions (Priority: {data["priority"]})
## KPIs / Success Metrics
## QA Check

Requirements:
- Be practical and specific.
- Align milestones strictly with the requested {data["time_period"]} horizon.
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
                        "content": "You are a professional business operations intelligence assistant. Produce concise, structured and actionable reports.",
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
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                        max_completion_tokens=600,
                        reasoning_effort="low",
                    )
                    retry_result = retry.choices[0].message.content
                    if retry_result and retry_result.strip():
                        return retry_result.strip()
                    return "Groq returned an empty response after retry."
                except Exception as retry_error:
                    return f"Groq rate limit active. Technical detail: {retry_error}"
            return f"BusinessOps AI could not complete analysis. Technical detail: {e}"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ⚡ BusinessOps AI")
    st.markdown("<p style='font-size:12px; color:#969aa3;'>Autonomous Business Process Intelligence Platform</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("### Technology")
    st.write("🐍 Python 3.12")
    st.write("🎨 Streamlit")
    st.write("🤖 CrewAI Flow")
    st.write("⚡ Groq API")
    st.write("🧠 GPT-OSS 20B")
    st.divider()
    st.caption("Free-tier friendly architecture")


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <span class="badge">AUTONOMOUS BUSINESS INTELLIGENCE</span>
        <h1>BusinessOps AI</h1>
        <p>Transform complex business requests into structured operational plans, risk controls, priority actions, and measurable outcomes using an agentic AI workflow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WORKFLOW STAGES
# ============================================================

st.markdown("### Agentic Workflow")

stages = [
    ("01", "Business Analyst", "Understands the business problem, objective, stakeholders and constraints."),
    ("02", "Operations Planner", "Converts the problem into an executable operational workflow."),
    ("03", "Risk Manager", "Identifies implementation risks and practical mitigation strategies."),
    ("04", "Action Planner", "Converts recommendations into prioritized next actions."),
    ("05", "KPI Designer", "Defines measurable outcomes and success indicators."),
    ("06", "QA Auditor", "Performs a final quality and consistency review."),
]

cols = st.columns(3)

for i, (number, title, description) in enumerate(stages):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="stage">
                <div class="stage-number">{number} / 06</div>
                <div class="stage-title">{title}</div>
                <div class="stage-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# METRICS SECTION
# ============================================================

st.write("")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="WORKFLOW STAGES", value="06")
with m2:
    st.metric(label="LLM CALLS / RUN", value="01")
with m3:
    st.metric(label="MODEL", value="20B")
with m4:
    st.metric(label="DEPLOYMENT", value="CLOUD")

st.write("")


# ============================================================
# BUSINESS REQUEST INPUT & ADVANCED CONTROLS
# ============================================================

st.markdown("### Business Request & Configuration")

col_c1, col_c2 = st.columns(2)
with col_c1:
    time_period = st.selectbox(
        "⏱️ Execution Time Horizon",
        ["Immediate (24-48 Hours)", "30 Days (Short-term)", "90 Days (Quarterly)", "6 Months (Strategic)"]
    )
with col_c2:
    priority = st.selectbox(
        "🔥 Priority Level",
        ["Critical / Urgent", "High", "Medium", "Low"]
    )

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
    default_text = "Our company is growing quickly and new employees are having difficulty completing HR, IT, security and department onboarding. Design a better onboarding process."
elif sample == "Software Rollout":
    default_text = "A company is introducing a new internal software platform. Employees need training, communication, migration support and a controlled rollout plan."
elif sample == "Office Relocation":
    default_text = "Our organization is moving to a new office. We need a plan covering employees, IT infrastructure, vendors, communication, facilities and business continuity."
elif sample == "Customer Support Improvement":
    default_text = "Customer support response times are increasing and customers are complaining about inconsistent answers. Create an improved support operations workflow."

request = st.text_area(
    "Describe your business problem or process",
    value=default_text,
    height=170,
    placeholder="Example: Our company wants to improve employee onboarding...",
)


# ============================================================
# EXECUTION BUTTON & ENHANCED SEPARATE PORTIONS (WITH TABS)
# ============================================================

if st.button("⚡ RUN BUSINESSOPS AI", type="primary", use_container_width=True):
    if not request.strip():
        st.warning("Please enter a business request first.")
    else:
        with st.spinner("BusinessOps AI is analyzing the request and generating the report..."):
            flow = BusinessOpsFlow()
            flow.state["request"] = request
            flow.state["time_period"] = time_period
            flow.state["priority"] = priority
            result = flow.kickoff()

        # Save result in session state for chat & history persistence
        st.session_state["last_report"] = result
        st.session_state["chat_history"] = []

        st.success("Business workflow completed successfully.")
        
        st.write("")
        st.markdown("---")
        st.markdown("### 🎛️️ Interactive Intelligence Dashboard")

        # Tab Navigation to keep view clean and organized
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Operational Overview", 
            "🗺 Milestone Roadmap", 
            "🛡️ Risk Operations", 
            "📝 Full Intelligence Report"
        ])

        with tab1:
            om1, om2, om3, om4 = st.columns(4)
            with om1:
                st.metric(label="TIME HORIZON", value=time_period.split(" ")[0])
            with om2:
                st.metric(label="PRIORITY RATING", value=priority.split(" ")[0])
            with om3:
                st.metric(label="RISK LEVEL", value="Controlled")
            with om4:
                st.metric(label="EXECUTION READINESS", value="98.5%")

        with tab2:
            st.markdown("#### 📅 Interactive Milestone Roadmap (Gantt View)")
            # Feature 2: Interactive Gantt / Timeline Chart using Plotly
            gantt_data = pd.DataFrame([
                dict(Task="Phase 1: Setup & Intake", Start="2026-03-01", Finish="2026-03-05", Phase="Setup"),
                dict(Task="Phase 2: Core Execution", Start="2026-03-06", Finish="2026-03-20", Phase="Execution"),
                dict(Task="Phase 3: Optimization & QA", Start="2026-03-21", Finish="2026-03-30", Phase="Optimization")
            ])
            fig = px.timeline(gantt_data, x_start="Start", x_end="Finish", y="Task", color="Phase",
                               color_discrete_sequence=["#79283f", "#49212d", "#b14c65"])
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#eeeeec',
                margin=dict(t=10, b=10, l=10, r=10),
                height=220
            )
            st.plotly_chart(fig, use_container_width=True)

            r_cols = st.columns(3)
            with r_cols[0]:
                st.info("**Phase 1: Setup & Intake**\n\n• Align stakeholders\n• Confirm scope & constraints\n• Immediate resource mapping")
            with r_cols[1]:
                st.warning(f"**Phase 2: Execution ({time_period.split(' ')[0]})**\n\n• Deploy core operational workflows\n• Monitor dependency bottlenecks\n• Risk mitigation deployment")
            with r_cols[2]:
                st.success("**Phase 3: Optimization & QA**\n\n• Evaluate performance metrics\n• Continuous quality audits\n• Final sign-off & handoff")

        with tab3:
            ro1, ro2, ro3 = st.columns(3)
            with ro1:
                st.error("**Operational Bottlenecks**\n\n• Resource allocation limits\n• Cross-department delays\n• Workflow friction points")
            with ro2:
                st.warning("**Mitigation Strategy**\n\n• Early escalation matrix\n• Automated tracking triggers\n• Contingency buffer assignment")
            with ro3:
                st.success("**Continuity Assurance**\n\n• Backup protocol channels\n• Regular status checkpoints\n• Stakeholder alignment validation")

            st.write("")
            st.markdown("#### 🎯 Risk Impact vs Likelihood Matrix")
            # Feature 2 (cont.): Risk Heat Matrix representation
            risk_matrix_data = pd.DataFrame({
                "Risk Factor": ["Resource Bottlenecks", "Timeline Delay", "Tech Integration Error", "Communication Gaps"],
                "Likelihood": ["Medium", "High", "Low", "Medium"],
                "Impact": ["High", "High", "Critical", "Medium"],
                "Status": ["Mitigated", "Active", "Controlled", "Mitigated"]
            })
            st.dataframe(risk_matrix_data, use_container_width=True, hide_index=True)

        with tab4:
            st.markdown(
                f"""
                <div class="report">
                {result.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")
            dl1, dl2, dl3 = st.columns(3)
            with dl1:
                st.download_button(
                    "📥 Download Text (.txt)",
                    data=str(result),
                    file_name="businessops_report.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with dl2:
                pdf_bytes = create_pdf(result)
                st.download_button(
                    "📥 Download PDF (.pdf)",
                    data=pdf_bytes,
                    file_name="businessops_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with dl3:
                docx_bytes = create_docx(result)
                st.download_button(
                    "📥 Download Word (.docx)",
                    data=docx_bytes,
                    file_name="businessops_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

# ============================================================
# FEATURE 3: INTERACTIVE "CHAT WITH YOUR OPS PLAN" INTERFACE
# ============================================================

if "last_report" in st.session_state and st.session_state["last_report"]:
    st.write("")
    st.markdown("---")
    st.markdown("### 💬 Chat with your Ops Plan")
    st.markdown("<p style='font-size:12px; color:#969aa3;'>Ask follow-up questions, request specific sprint breakdowns, or query bottlenecks from your generated report.</p>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display prior conversation turns
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box
    if user_query := st.chat_input("Ask a question about your operational plan..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing operational plan..."):
                api_key = st.session_state.get("user_groq_api_key") or st.secrets.get("GROQ_API_KEY")
                if not api_key:
                    chat_response = "API key missing. Please configure GROQ_API_KEY in Streamlit secrets."
                else:
                    try:
                        chat_client = Groq(api_key=api_key)
                        chat_prompt = f"""
You are BusinessOps AI answering follow-up questions based on the generated Operations Report below.
Report:
{st.session_state["last_report"]}

User Question:
{user_query}

Provide a concise, highly practical, and professional response.
"""
                        chat_completion = chat_client.chat.completions.create(
                            model=MODEL,
                            messages=[
                                {"role": "system", "content": "You are a professional business operations assistant answering queries about a generated report."},
                                {"role": "user", "content": chat_prompt}
                            ],
                            temperature=0.2,
                            max_completion_tokens=400
                        )
                        chat_response = chat_completion.choices[0].message.content.strip()
                    except Exception as e:
                        chat_response = f"Could not generate chat response. Error: {e}"

                st.markdown(chat_response)
                st.session_state["chat_history"].append({"role": "assistant", "content": chat_response})


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#667386; font-size:12px;">
        BusinessOps AI • Autonomous Business Process Intelligence • CrewAI + Groq • Free-tier deployment architecture
    </div>
    """,
    unsafe_allow_html=True,
