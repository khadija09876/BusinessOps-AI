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
                #0d0e11 0%,
                #090a0d 55%,
                #07080a 100%
            );

        border-right: 1px solid rgba(255,255,255,0.065);

        box-shadow:
            8px 0 35px rgba(0,0,0,0.18);
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
        color: #eeeDEa !important;
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
            );

        border: 1px solid rgba(255,255,255,0.065) !important;

        border-radius: 16px !important;

        box-shadow:
            0 14px 38px rgba(0,0,0,0.20);
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
            0 0 0 1px rgba(157,58,84,0.18),
            0 0 20px rgba(122,34,55,0.08) !important;
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

        border: 1px solid rgba(177,76,101,0.28);

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
            0 10px 28px rgba(0,0,0,0.22);
    }

    div.stButton > button:hover {
        border-color: rgba(210,145,160,0.45);

        background:
            linear-gradient(
                105deg,
                #893149 0%,
                #6c293b 50%,
                #542532 100%
            );

        box-shadow:
            0 12px 32px rgba(116,34,55,0.20);

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

        color: #eee;

        background: #13151a;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.030),
                rgba(255,255,255,0.012)
            );

        border: 1px solid rgba(255,255,255,0.055);

        border-radius: 12px;

        padding: 14px 15px;

        box-shadow:
            0 7px 20px rgba(0,0,0,0.12);
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
       SUCCESS / WARNING / ERROR / INFO
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    div[data-testid="stAlert"][kind="success"] {
        background: rgba(66, 105, 82, 0.08) !important;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: rgba(255,255,255,0.055) !important;
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
