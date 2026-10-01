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

            background:
                linear-gradient(
                    135deg,
                    #8f3048,
                    #5b2633
                );

            color: white;
            font-size: 20px;
            font-weight: 900;

            box-shadow:
                0 8px 28px rgba(128,38,57,0.18);
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
            padding: 13px 13px;

            border-radius: 11px;

            background: rgba(255,255,255,0.025);
            border: 1px solid rgba(255,255,255,0.06);
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
                0 0 10px rgba(185,91,115,0.65);
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

            background:
                linear-gradient(
                    135deg,
                    rgba(21,20,24,0.98),
                    rgba(12,13,17,0.98)
                );

            border: 1px solid rgba(255,255,255,0.065);

            box-shadow:
                0 20px 65px rgba(0,0,0,0.24);

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

            background:
                radial-gradient(
                    circle,
                    rgba(128,38,57,0.13),
                    transparent 65%
                );

            pointer-events: none;
        }

        .hero-badge {
            display: inline-flex;

            padding: 6px 10px;

            border-radius: 20px;

            background: rgba(128,38,57,0.065);

            border: 1px solid rgba(185,91,115,0.16);

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

            background:
                linear-gradient(
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

            background: rgba(14,15,19,0.95);

            border: 1px solid rgba(255,255,255,0.055);

            border-radius: 14px;

            overflow-x: auto;
        }

        .flow-item {
            flex: 1;

            min-width: 125px;

            padding: 12px 12px;

            border-radius: 9px;

            background: rgba(255,255,255,0.022);

            border: 1px solid rgba(255,255,255,0.045);

            transition: 0.2s ease;
        }

        .flow-item:hover {
            border-color: rgba(185,91,115,0.24);

            background:
                rgba(128,38,57,0.045);
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

            background:
                linear-gradient(
                    145deg,
                    rgba(19,18,22,0.98),
                    rgba(11,12,16,0.98)
                );

            border: 1px solid rgba(255,255,255,0.06);

            border-radius: 16px;
        }

        .control-label {
            color: #7d838e;

            font-size: 9px;
            font-weight: 800;

            letter-spacing: 1px;

            margin-bottom: 6px;
        }


        /* ======================================================
           STREAMLIT INPUT TEXT
        ====================================================== */

        textarea,
        input {
            background: #0c0e13 !important;

            color: #f5f5f4 !important;

            border:
                1px solid #272a32 !important;

            border-radius:
                9px !important;

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
            border-color:
                #8f3048 !important;

            box-shadow:
                0 0 0 1px
                rgba(185,91,115,0.15) !important;
        }

        div[data-baseweb="select"] > div {
            background:
                #0c0e13 !important;

            border-color:
                #272a32 !important;

            border-radius:
                9px !important;

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

            border:
                1px solid rgba(185,91,115,0.22);

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

            border:
                1px solid #292c34;

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
                rgba(255,255,255,0.022);

            border:
                1px solid rgba(255,255,255,0.05);

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
                rgba(128,38,57,0.035);

            border:
                1px solid rgba(185,91,115,0.10);

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
                rgba(100,116,139,0.035);

            border:
                1px solid rgba(100,116,139,0.09);
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

            background:
                linear-gradient(
                    145deg,
                    rgba(17,17,21,0.98),
                    rgba(10,11,15,0.98)
                );

            border:
                1px solid rgba(255,255,255,0.055);
        }


        /* ======================================================
           REPORT MARKDOWN
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
            background:
                #0d0f14;

            border:
                1px solid #272a32;

            border-radius:
                11px;
        }

        div[data-testid="stExpander"] summary {
            font-size: 12px !important;
        }


        /* ======================================================
           STREAMLIT METRIC
        ====================================================== */

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.018);
            border: 1px solid rgba(255,255,255,0.05);
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
