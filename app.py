import streamlit as st
from textwrap import dedent


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
# PREMIUM CHARCOAL + MAROON UI
# ============================================================

st.markdown(
    dedent(
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
            background: linear-gradient(
                180deg,
                #0c0d10 0%,
                #08090c 100%
            );

            border-right: 1px solid rgba(255, 255, 255, 0.055);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 0.8rem;
        }

        .brand {
            padding: 12px 9px 18px 9px;
        }

        .brand-mark {
            width: 42px;
            height: 42px;
            border-radius: 11px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: linear-gradient(
                135deg,
                #8f3048,
                #5b2633
            );

            color: white;
            font-size: 20px;
            font-weight: 900;

            box-shadow:
                0 8px 28px rgba(128, 38, 57, 0.18);
        }

        .brand-name {
            margin-top: 11px;
            color: #fafafa;
            font-size: 19px;
            font-weight: 850;
            letter-spacing: -0.4px;
        }

        .brand-desc {
            margin-top: 5px;
            color: #9298a3;
            font-size: 11px;
            line-height: 1.65;
        }

        .system-card {
            margin-top: 16px;
            padding: 13px;
            border-radius: 11px;

            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .system-label {
            color: #777d88;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 1.2px;
        }

        .system-value {
            margin-top: 6px;
            color: #d79aaa;
            font-size: 11px;
            font-weight: 750;
        }

        .system-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;

            background: #b95b73;

            margin-right: 6px;

            box-shadow:
                0 0 10px rgba(185, 91, 115, 0.65);
        }

        .side-info {
            margin-top: 14px;
            color: #656b76;
            font-size: 10px;
            line-height: 1.7;
        }


        /* ======================================================
           HERO
        ====================================================== */

        .hero {
            position: relative;
            overflow: hidden;

            padding: 30px 34px 29px 34px;

            border-radius: 20px;

            background: linear-gradient(
                135deg,
                rgba(21, 20, 24, 0.98),
                rgba(12, 13, 17, 0.98)
            );

            border: 1px solid rgba(255, 255, 255, 0.065);

            box-shadow:
                0 20px 65px rgba(0, 0, 0, 0.24);

            margin-bottom: 16px;
        }

        .hero::after {
            content: "";

            position: absolute;

            right: -100px;
            top: -130px;

            width: 300px;
            height: 300px;

            border-radius: 50%;

            background: radial-gradient(
                circle,
                rgba(128, 38, 57, 0.13),
                transparent 65%
            );

            pointer-events: none;
        }

        .hero-badge {
            display: inline-flex;

            padding: 6px 10px;

            border-radius: 20px;

            background: rgba(128, 38, 57, 0.065);

            border: 1px solid rgba(185, 91, 115, 0.16);

            color: #d79aaa;

            font-size: 9px;
            font-weight: 850;
            letter-spacing: 1.35px;
        }

        .hero-title {
            margin-top: 13px;

            font-size: clamp(38px, 5vw, 58px);

            line-height: 1;

            font-weight: 900;

            letter-spacing: -2.6px;

            color: #f5f5f4;
        }

        .hero-title span {
            color: #c98294;
        }

        .hero-desc {
            margin-top: 12px;

            max-width: 760px;

            color: #989da7;

            font-size: 14px;
            line-height: 1.75;
        }

        .hero-line {
            width: 82px;
            height: 2px;

            margin-top: 18px;

            border-radius: 10px;

            background: linear-gradient(
                90deg,
                #8f3048,
                #a7adb7
            );
        }


        /* ======================================================
           SECTION LABELS
        ====================================================== */

        .section {
            margin-top: 19px;
            margin-bottom: 10px;
        }

        .eyebrow {
            color: #b95b73;
            font-size: 9px;
            font-weight: 850;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .section-title {
            margin-top: 4px;

            color: #eeeeec;

            font-size: 18px;
            font-weight: 800;

            letter-spacing: -0.25px;
        }

        .section-desc {
            color: #737984;

            font-size: 11px;

            margin-top: 4px;

            line-height: 1.6;
        }


        /* ======================================================
           WORKFLOW
        ====================================================== */

        .flow-strip {
            display: flex;
            align-items: center;
            gap: 7px;

            padding: 10px;

            background: rgba(14, 15, 19, 0.95);

            border: 1px solid rgba(255, 255, 255, 0.055);

            border-radius: 14px;

            overflow-x: auto;
        }

        .flow-item {
            flex: 1;

            min-width: 125px;

            padding: 12px;

            border-radius: 9px;

            background: rgba(255, 255, 255, 0.022);

            border: 1px solid rgba(255, 255, 255, 0.045);

            transition: 0.2s ease;
        }

        .flow-item:hover {
            border-color: rgba(185, 91, 115, 0.24);

            background:
                rgba(128, 38, 57, 0.045);
        }

        .flow-num {
            color: #b95b73;

            font-size: 9px;
            font-weight: 850;

            letter-spacing: 1px;
        }

        .flow-name {
            margin-top: 5px;

            color: #e4e4e2;

            font-size: 12px;
            font-weight: 750;
        }

        .flow-arrow {
            color: #555b66;
            font-size: 15px;
        }


        /* ======================================================
           CONTROL PANEL
        ====================================================== */

        .control-panel {
            padding: 18px;

            background: linear-gradient(
                145deg,
                rgba(19, 18, 22, 0.98),
                rgba(11, 12, 16, 0.98)
            );

            border: 1px solid rgba(255, 255, 255, 0.06);

            border-radius: 16px;
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
                0 0 0 1px rgba(185, 91, 115, 0.15) !important;
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

            border: 1px solid rgba(185, 91, 115, 0.22);

            background: linear-gradient(
                100deg,
                #7c2940,
                #542733
            );

            color: white;

            font-size: 12px;

            font-weight: 800;

            box-shadow:
                0 9px 25px rgba(0, 0, 0, 0.20);
        }

        div.stButton > button:hover {
            border-color:
                rgba(215, 154, 170, 0.38);

            box-shadow:
                0 12px 30px rgba(128, 38, 57, 0.14);
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

        .metrics {
            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 9px;

            margin-top: 11px;
        }

        .metric {
            padding: 13px 14px;

            border-radius: 11px;

            background:
                rgba(255, 255, 255, 0.022);

            border:
                1px solid rgba(255, 255, 255, 0.05);

            text-align: left;
        }

        .metric-label {
            color: #777d88;

            font-size: 9px;
            font-weight: 800;

            letter-spacing: 1px;
        }

        .metric-value {
            margin-top: 5px;

            color: #e4e4e2;

            font-size: 21px;
            font-weight: 850;

            line-height: 1.2;
        }

        .metric-value span {
            color: #c98294;
        }


        /* ======================================================
           REPORT META
        ====================================================== */

        .report-meta {
            display: flex;

            justify-content: space-between;
            align-items: center;

            padding: 13px 15px;

            border-radius: 11px;

            background:
                rgba(128, 38, 57, 0.035);

            border:
                1px solid rgba(185, 91, 115, 0.10);

            margin-top: 15px;
            margin-bottom: 9px;
        }

        .report-name {
            color: #e2e2df;

            font-size: 13px;
            font-weight: 800;
        }

        .report-id {
            color: #737985;

            font-size: 9px;

            margin-top: 4px;
        }

        .report-time {
            color: #7b818b;

            font-size: 9px;

            text-align: right;

            line-height: 1.6;
        }


        /* ======================================================
           STATUS
        ====================================================== */

        .status-strip {
            display: flex;

            gap: 6px;

            margin-bottom: 12px;
        }

        .status {
            flex: 1;

            padding: 8px 6px;

            border-radius: 8px;

            text-align: center;

            background:
                rgba(100, 116, 139, 0.035);

            border:
                1px solid rgba(100, 116, 139, 0.09);
        }

        .status-label {
            color: #707680;

            font-size: 8px;
            font-weight: 800;

            letter-spacing: 0.8px;
        }

        .status-value {
            color: #bfc4cc;

            font-size: 9px;
            font-weight: 800;

            margin-top: 4px;
        }


        /* ======================================================
           REPORT
        ====================================================== */

        .report-card {
            padding: 20px;

            border-radius: 14px;

            background: linear-gradient(
                145deg,
                rgba(17, 17, 21, 0.98),
                rgba(10, 11, 15, 0.98)
            );

            border:
                1px solid rgba(255, 255, 255, 0.055);
        }


        /* ======================================================
           MARKDOWN
        ====================================================== */

        div[data-testid="stMarkdownContainer"] {
            font-size: 13px;
            line-height: 1.75;
        }

        div[data-testid="stMarkdownContainer"] p {
            color: #cdd0d5;
            font-size: 13px;
            line-height: 1.75;
        }

        div[data-testid="stMarkdownContainer"] li {
            color: #cdd0d5;
            font-size: 13px;
            line-height: 1.7;
            margin-bottom: 3px;
        }

        div[data-testid="stMarkdownContainer"] h1 {
            color: #f5f5f4;
            font-size: 27px;
            line-height: 1.25;
        }

        div[data-testid="stMarkdownContainer"] h2 {
            color: #eeeeec;
            font-size: 20px;
            line-height: 1.3;
            margin-top: 12px;
        }

        div[data-testid="stMarkdownContainer"] h3 {
            color: #e2e2df;
            font-size: 17px;
            line-height: 1.35;
            margin-top: 10px;
        }

        div[data-testid="stMarkdownContainer"] strong {
            color: #f0f0ee;
        }


        /* ======================================================
           TABS
        ====================================================== */

        button[data-baseweb="tab"] {
            color: #7b818b !important;

            font-size: 11px !important;

            font-weight: 750 !important;

            padding-left: 12px !important;
            padding-right: 12px !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #c98294 !important;
        }

        div[data-baseweb="tab-highlight"] {
            background:
                #9a3b55 !important;
        }


        /* ======================================================
           EXPANDER
        ====================================================== */

        div[data-testid="stExpander"] {
            background: #0d0f14;

            border:
                1px solid #272a32;

            border-radius: 11px;
        }

        div[data-testid="stExpander"] summary {
            font-size: 12px !important;
        }


        /* ======================================================
           STREAMLIT METRIC
        ====================================================== */

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.018);

            border:
                1px solid rgba(255, 255, 255, 0.05);

            border-radius: 10px;

            padding: 10px 12px;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 9px !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 20px !important;
        }


        /* ======================================================
           FOOTER
        ====================================================== */

        .footer {
            text-align: center;

            color: #555b65;

            font-size: 10px;

            padding: 14px;

            line-height: 1.6;
        }


        /* ======================================================
           MOBILE
        ====================================================== */

        @media (max-width: 900px) {

            .hero {
                padding: 25px;
            }

            .hero-title {
                font-size: 41px;
            }

            .hero-desc {
                font-size: 13px;
            }

            .metrics {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .status-strip {
                flex-wrap: wrap;
            }

            .status {
                min-width: 29%;
            }

            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] li {
                font-size: 13px;
            }
        }

        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-mark">
                ◈
            </div>

            <div class="brand-name">
                BusinessOps AI
            </div>

            <div class="brand-desc">
                Autonomous Business Process
                Intelligence Platform
            </div>

            <div class="system-card">

                <div class="system-label">
                    SYSTEM STATUS
                </div>

                <div class="system-value">
                    <span class="system-dot"></span>
                    Operational
                </div>

            </div>

            <div class="side-info">
                AI-powered workflow analysis,
                risk identification, action planning
                and business performance intelligence.
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
            Transform business requests into structured operational
            plans, risk insights, prioritized actions and measurable
            performance outcomes.
        </div>

        <div class="hero-line"></div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WORKFLOW SECTION
# ============================================================

st.markdown(
    """
    <div class="section">

        <div class="eyebrow">
            AI WORKFLOW
        </div>

        <div class="section-title">
            Autonomous Process Intelligence
        </div>

        <div class="section-desc">
            A structured workflow transforms the business request
            into an actionable operational intelligence report.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="flow-strip">

        <div class="flow-item">
            <div class="flow-num">01</div>
            <div class="flow-name">Business Intake</div>
        </div>

        <div class="flow-arrow">→</div>

        <div class="flow-item">
            <div class="flow-num">02</div>
            <div class="flow-name">Analysis</div>
        </div>

        <div class="flow-arrow">→</div>

        <div class="flow-item">
            <div class="flow-num">03</div>
            <div class="flow-name">Operations</div>
        </div>

        <div class="flow-arrow">→</div>

        <div class="flow-item">
            <div class="flow-num">04</div>
            <div class="flow-name">Risk Review</div>
        </div>

        <div class="flow-arrow">→</div>

        <div class="flow-item">
            <div class="flow-num">05</div>
            <div class="flow-name">Action Plan</div>
        </div>

        <div class="flow-arrow">→</div>

        <div class="flow-item">
            <div class="flow-num">06</div>
            <div class="flow-name">QA Audit</div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTROL PANEL
# ============================================================

st.markdown(
    """
    <div class="section">

        <div class="eyebrow">
            ANALYSIS WORKSPACE
        </div>

        <div class="section-title">
            Business Request
        </div>

        <div class="section-desc">
            Describe the business process, operational problem
            or improvement requirement.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="control-panel">',
    unsafe_allow_html=True,
)


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
        "Example: Our customer support response time has increased. "
        "Analyze the process, identify operational bottlenecks, "
        "assess risks and propose an improvement plan."
    ),
    height=180,
)


col_run, col_clear = st.columns([3, 1])


with col_run:

    run = st.button(
        "Run BusinessOps Analysis",
        use_container_width=True,
    )


with col_clear:

    clear = st.button(
        "Clear",
        use_container_width=True,
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# CLEAR
# ============================================================

if clear:
    st.rerun()


# ============================================================
# EMPTY STATE
# ============================================================

if not run:

    st.markdown(
        """
        <div class="section">

            <div class="eyebrow">
                READY
            </div>

            <div class="section-title">
                Waiting for Business Request
            </div>

            <div class="section-desc">
                Enter a business problem above to begin the
                BusinessOps intelligence workflow.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DEMO RESULT
# ============================================================

if run:

    if not request.strip():

        st.warning(
            "Please enter a business request before running the analysis."
        )

    else:

        st.markdown(
            """
            <div class="report-meta">

                <div>

                    <div class="report-name">
                        BusinessOps Analysis Report
                    </div>

                    <div class="report-id">
                        BO-DEMO-001
                    </div>

                </div>

                <div class="report-time">
                    Analysis Ready
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # STATUS STRIP
        # ====================================================

        st.markdown(
            """
            <div class="status-strip">

                <div class="status">
                    <div class="status-label">INTAKE</div>
                    <div class="status-value">READY</div>
                </div>

                <div class="status">
                    <div class="status-label">ANALYSIS</div>
                    <div class="status-value">READY</div>
                </div>

                <div class="status">
                    <div class="status-label">OPERATIONS</div>
                    <div class="status-value">READY</div>
                </div>

                <div class="status">
                    <div class="status-label">RISK</div>
                    <div class="status-value">READY</div>
                </div>

                <div class="status">
                    <div class="status-label">ACTIONS</div>
                    <div class="status-value">READY</div>
                </div>

                <div class="status">
                    <div class="status-label">QA</div>
                    <div class="status-value">READY</div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # METRICS
        # ====================================================

        st.markdown(
            """
            <div class="metrics">

                <div class="metric">

                    <div class="metric-label">
                        PRIORITY
                    </div>

                    <div class="metric-value">
                        <span>HIGH</span>
                    </div>

                </div>


                <div class="metric">

                    <div class="metric-label">
                        RISK AREAS
                    </div>

                    <div class="metric-value">
                        04
                    </div>

                </div>


                <div class="metric">

                    <div class="metric-label">
                        ACTIONS
                    </div>

                    <div class="metric-value">
                        08
                    </div>

                </div>


                <div class="metric">

                    <div class="metric-label">
                        KPIs
                    </div>

                    <div class="metric-value">
                        06
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # REPORT HEADER
        # ====================================================

        st.markdown(
            """
            <div class="section">

                <div class="eyebrow">
                    INTELLIGENCE REPORT
                </div>

                <div class="section-title">
                    Operational Assessment
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # REPORT CARD
        # ====================================================

        st.markdown(
            '<div class="report-card">',
            unsafe_allow_html=True,
        )


        st.markdown("## Executive Summary")

        st.write(
            "The submitted business request has been structured "
            "for operational analysis. The workflow focuses on "
            "process improvement, risk visibility, prioritized "
            "actions and measurable outcomes."
        )


        st.markdown("## Business Analysis")

        st.write(
            "The current requirement indicates an operational "
            "improvement opportunity. The primary focus should "
            "be placed on identifying process bottlenecks, "
            "clarifying ownership and establishing measurable "
            "performance indicators."
        )


        st.markdown("## Recommended Workflow")

        st.markdown(
            """
            - Map the current business process.
            - Identify major operational bottlenecks.
            - Define ownership for each critical activity.
            - Prioritize improvement opportunities.
            - Establish measurable KPIs.
            - Review results and continuously improve the process.
            """
        )


        st.markdown("## Priority Actions")

        st.markdown(
            """
            1. Document the current process.
            2. Identify the highest-impact bottlenecks.
            3. Assign responsible owners.
            4. Define measurable improvement targets.
            5. Monitor performance against KPIs.
            """
        )


        st.markdown("## KPIs / Success Metrics")

        st.markdown(
            """
            - Process completion time
            - Operational efficiency
            - Error rate
            - Customer satisfaction
            - SLA compliance
            - Task completion rate
            """
        )


        # Close report-card div
        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        BusinessOps AI · Autonomous Business Process Intelligence
    </div>
    """,
    unsafe_allow_html=True,
)
