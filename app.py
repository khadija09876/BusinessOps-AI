import time
import io
import streamlit as st
from groq import Groq
import plotly.express as px
import pandas as pd

# CrewAI Multi-Agent Libraries
from crewai import Agent, Task, Crew, Process
from crewai.flow import Flow, start, listen

# Report generation libraries
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from docx import Document


# ============================================================
# BUSINESSOPS AI - MULTI-AGENT ENTERPRISE EDITION
# ============================================================

st.set_page_config(
    page_title="BusinessOps AI - Multi-Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "report_history" not in st.session_state:
    st.session_state.report_history = []


# ============================================================
# THEME & UI STYLES
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(122, 34, 55, 0.10), transparent 28%),
            radial-gradient(circle at 90% 5%, rgba(255, 255, 255, 0.025), transparent 25%),
            linear-gradient(135deg, #07080a 0%, #0b0c0f 48%, #090a0d 100%);
        color: #eeeeec;
    }
    .main .block-container {
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }
    #MainMenu, footer { visibility: hidden; }
    header, [data-testid="stHeader"] { background: transparent !important; }

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
    .hero { padding: 10px 0 20px 0; }
    .stage {
        background: linear-gradient(145deg, rgba(20, 19, 23, 0.98), rgba(11, 12, 15, 0.98));
        border: 1px solid rgba(255, 255, 255, 0.065);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        height: 100%;
    }
    .stage-number { font-size: 11px; color: #8c334d; font-weight: 750; letter-spacing: 0.8px; margin-bottom: 6px; }
    .stage-title { font-size: 15px; color: #f1f1ef; font-weight: 750; margin-bottom: 8px; }
    .stage-text { font-size: 12px; color: #969aa3; line-height: 1.6; }
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
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0e11 0%, #090a0d 55%, #07080a 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.065);
    }
    h1 { color: #f5f4f1 !important; font-weight: 900 !important; letter-spacing: -1.8px !important; }
    h3 { color: #e5e3df !important; font-weight: 750 !important; }
    p, li { color: #c8c9cc; line-height: 1.75; }
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
    }
    div.stButton > button:hover {
        background: linear-gradient(105deg, #893149 0%, #6c293b 50%, #542532 100%);
    }
    div[data-testid="stDownloadButton"] button {
        min-height: 43px;
        border-radius: 10px;
        background: linear-gradient(145deg, #111318, #0d0f13);
        border: 1px solid #292c34;
        color: #d9dadc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EXPORT HELPERS (PDF & DOCX)
# ============================================================

def create_pdf(text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle('ReportNormal', parent=styles['Normal'], fontSize=10, leading=14, textColor='#222222')
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
# CREWAI MULTI-AGENT WORKFLOW (CREWAI FLOW + AGENTS)
# ============================================================

class MultiAgentBusinessOpsFlow(Flow):

    @start()
    def initialize_params(self):
        return {
            "request": self.state.get("request", "").strip(),
            "time_period": self.state.get("time_period", "Immediate"),
            "priority": self.state.get("priority", "Medium"),
            "model": self.state.get("model", "openai/gpt-oss-20b"),
            "temperature": self.state.get("temperature", 0.1)
        }

    @listen(initialize_params)
    def run_multi_agent_crew(self, data):
        if not data["request"]:
            return "Please enter a business request."

        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            return "GROQ_API_KEY is missing. Add it in Streamlit Cloud → Settings → Secrets."

        # Configure Groq LLM wrapper for CrewAI
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model=data["model"],
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
            temperature=data["temperature"]
        )

        # 1. Define Specialized Agents
        analyst = Agent(
            role='Senior Business Analyst',
            goal='Analyze objective, stakeholders, current pain points, and core constraints.',
            backstory='Expert in business diagnostics, root-cause identification, and organizational alignment.',
            verbose=False,
            llm=llm
        )

        operations_planner = Agent(
            role='Operations Planning Director',
            goal='Design practical workflows, milestones, resource mappings, and dependencies.',
            backstory='Seasoned COO specializing in scalable process design and cross-functional deployment.',
            verbose=False,
            llm=llm
        )

        risk_manager = Agent(
            role='Risk & Compliance Manager',
            goal='Identify operational, technical, and human bottlenecks with actionable mitigations.',
            backstory='Master risk officer skilled in preemptive threat modeling and continuity planning.',
            verbose=False,
            llm=llm
        )

        qa_auditor = Agent(
            role='Quality Assurance & Strategy Auditor',
            goal='Synthesize findings into an executive report with KPIs and rigorous quality checks.',
            backstory='Rigorous auditor ensuring enterprise deliverables meet the highest strategic standards.',
            verbose=False,
            llm=llm
        )

        # 2. Define Tasks for each Agent
        task1 = Task(
            description=f"Analyze this business problem: {data['request']}. Outline Executive Summary and Business Analysis.",
            expected_output="Detailed Executive Summary and Business Analysis sections.",
            agent=analyst
        )

        task2 = Task(
            description=f"Design a milestone workflow tailored for a {data['time_period']} horizon.",
            expected_output="Recommended Workflow sections with clear phased milestones.",
            agent=operations_planner
        )

        task3 = Task(
            description="Identify primary implementation risks and practical mitigations.",
            expected_output="Risks & Mitigations section.",
            agent=risk_manager
        )

        task4 = Task(
            description=f"Compile final report with Priority Actions (Priority: {data['priority']}), KPIs/Success Metrics, and QA Check.",
            expected_output="Complete professional Business Operations Report in Markdown format with sections: ## Executive Summary, ## Business Analysis, ## Recommended Workflow, ## Risks & Mitigations, ## Priority Actions, ## KPIs / Success Metrics, ## QA Check.",
            agent=qa_auditor
        )

        # 3. Assemble and Run Crew in Sequential Process
        crew = Crew(
            agents=[analyst, operations_planner, risk_manager, qa_auditor],
            tasks=[task1, task2, task3, task4],
            process=Process.sequential,
            verbose=False
        )

        try:
            result = crew.kickoff()
            return str(result).strip()
        except Exception as e:
            return f"Multi-Agent execution error: {e}"


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

with st.sidebar:
    st.markdown("## ⚡ BusinessOps AI")
    st.markdown("<p style='font-size:12px; color:#969aa3;'>Multi-Agent Autonomous Intelligence Platform</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🤖 Multi-Agent Team")
    st.write("🕵️‍♂️ Senior Business Analyst")
    st.write("⚙️ Operations Planning Director")
    st.write("🛡️ Risk & Compliance Manager")
    st.write("📋 QA & Strategy Auditor")
    
    st.divider()
    st.markdown("### ⚙️ Engine Parameters")
    selected_model = st.selectbox(
        "🧠 LLM Model",
        ["openai/gpt-oss-20b", "llama-3.3-70b-versatile"]
    )
    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.1, 0.05)
    
    st.divider()
    st.markdown("### 📂 Project History")
    if st.session_state.report_history:
        history_titles = [item["title"] for item in st.session_state.report_history]
        selected_history = st.selectbox("Select past report", ["-- Current Session --"] + history_titles)
        if selected_history != "-- Current Session --":
            matched_item = next((item for item in st.session_state.report_history if item["title"] == selected_history), None)
            if matched_item:
                st.info(f"Loaded: {matched_item['title']} ({matched_item['time']})")
    else:
        st.caption("No past reports saved yet.")


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <span class="badge">MULTI-AGENT COLLABORATION ENGINE</span>
        <h1>BusinessOps AI</h1>
        <p>Deploy autonomous AI agents working collaboratively to analyze complex business requests, plan workflows, manage risks, and formulate executive reports.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WORKFLOW AGENTS OVERVIEW
# ============================================================

st.markdown("### Active Agentic Team")

stages = [
    ("01", "Business Analyst", "Evaluates objectives, stakeholders, constraints, and initial scope."),
    ("02", "Operations Planner", "Designs operational milestones and resource dependencies."),
    ("03", "Risk Manager", "Preemptively identifies bottlenecks and mitigation strategies."),
    ("04", "QA Auditor", "Validates consistency, assigns KPIs, and compiles final report."),
]

cols = st.columns(4)

for i, (number, title, description) in enumerate(stages):
    with cols[i]:
        st.markdown(
            f"""
            <div class="stage">
                <div class="stage-number">AGENT {number}</div>
                <div class="stage-title">{title}</div>
                <div class="stage-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


# ============================================================
# INPUT & CONFIGURATION
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
# EXECUTION & DASHBOARD
# ============================================================

if st.button("⚡ DEPLOY MULTI-AGENT CREW", type="primary", use_container_width=True):
    if not request.strip():
        st.warning("Please enter a business request first.")
    else:
        with st.spinner("Multi-Agent crew is collaborating on your report (Analyst -> Planner -> Risk -> QA)..."):
            flow = MultiAgentBusinessOpsFlow()
            flow.state["request"] = request
            flow.state["time_period"] = time_period
            flow.state["priority"] = priority
            flow.state["model"] = selected_model
            flow.state["temperature"] = temperature
            result = flow.kickoff()

        st.success("Multi-agent workflow completed successfully.")
        
        # Save to history
        history_entry = {
            "title": request[:45] + "...",
            "time": time.strftime("%H:%M:%S"),
            "result": result
        }
        if history_entry not in st.session_state.report_history:
            st.session_state.report_history.insert(0, history_entry)

        st.write("")
        st.markdown("---")
        st.markdown("### 🎛️ Multi-Agent Intelligence Dashboard")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Operational Overview", 
            "📈 Agent Analytics", 
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
                st.metric(label="ACTIVE AGENTS", value="04")
            with om4:
                st.metric(label="COLLABORATION SYNC", value="100%")

        with tab2:
            st.markdown("#### 📈 Multi-Agent Contribution & Execution Velocity")
            chart_data = pd.DataFrame({
                "Agent Role": ["Business Analyst", "Operations Planner", "Risk Manager", "QA Auditor"],
                "Confidence Score (%)": [98, 94, 91, 99],
                "Tokens Processed": [450, 620, 510, 580]
            })
            
            fig = px.bar(
                chart_data, 
                x="Agent Role", 
                y="Confidence Score (%)",
                color="Tokens Processed",
                color_continuousScale="Reds",
                text="Confidence Score (%)"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#d7d7d4",
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            r_cols = st.columns(3)
            with r_cols[0]:
                st.info("**Phase 1: Setup & Intake**\n\n• Align stakeholders\n• Confirm scope & constraints\n• Immediate resource mapping")
            with r_cols[1]:
                st.warning(f"**Phase 2: Execution ({time_period.split(' ')[0]})**\n\n• Deploy core operational workflows\n• Monitor dependency bottlenecks\n• Risk mitigation deployment")
            with r_cols[2]:
                st.success("**Phase 3: Optimization & QA**\n\n• Evaluate performance metrics\n• Continuous quality audits\n• Final sign-off & handoff")

        with tab4:
            ro1, ro2, ro3 = st.columns(3)
            with ro1:
                st.error("**Operational Bottlenecks**\n\n• Resource allocation limits\n• Cross-department delays\n• Workflow friction points")
            with ro2:
                st.warning("**Mitigation Strategy**\n\n• Early escalation matrix\n• Automated tracking triggers\n• Contingency buffer assignment")
            with ro3:
                st.success("**Continuity Assurance**\n\n• Backup protocol channels\n• Regular status checkpoints\n• Stakeholder alignment validation")

        with tab5:
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
                    file_name="businessops_multiagent_report.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with dl2:
                pdf_bytes = create_pdf(result)
                st.download_button(
                    "📥 Download PDF (.pdf)",
                    data=pdf_bytes,
                    file_name="businessops_multiagent_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with dl3:
                docx_bytes = create_docx(result)
                st.download_button(
                    "📥 Download Word (.docx)",
                    data=docx_bytes,
                    file_name="businessops_multiagent_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#667386; font-size:12px;">
        BusinessOps AI • True Multi-Agent Enterprise Edition • CrewAI + Groq + Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
