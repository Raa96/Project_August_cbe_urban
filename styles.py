import streamlit as st

def inject_custom_css():
    """
    Injects the Urban Intel OLED dark theme — Fira Code/Fira Sans typography,
    cyan + amber accent system, glassmorphic cards, glowing borders, monospace labels.
    Mirrors the visual language of urban-intel-main/frontend/index.html.
    """
    st.markdown("""
        <style>
        /* ── Fonts ─────────────────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"], .stMarkdown, p, li, label, span, div {
            font-family: 'Fira Sans', sans-serif;
        }

        /* ── OLED Background ────────────────────────────────────────────────── */
        .stApp {
            background-color: #020617;
            color: #cbd5e1;
        }
        .stApp::before {
            content: '';
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background:
                radial-gradient(ellipse 80% 50% at 50% -10%, rgba(34,211,238,0.06), transparent 60%),
                radial-gradient(ellipse 60% 40% at 90% 110%, rgba(168,85,247,0.05), transparent 60%);
            animation: bgDrift 18s ease-in-out infinite alternate;
        }
        @keyframes bgDrift {
            0% { transform: translateY(0) scale(1); }
            100% { transform: translateY(-20px) scale(1.03); }
        }
        .stMainBlockContainer { position: relative; z-index: 1; }

        /* ── Sidebar ────────────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #1e293b;
        }
        [data-testid="stSidebar"] * {
            font-family: 'Fira Code', monospace !important;
        }
        [data-testid="stSidebar"] .st-emotion-cache-pkbazv {
            color: #94a3b8 !important;
        }
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        [data-testid="stSidebarHeader"] {
            padding: 0.5rem 1rem 0 1rem !important;
        }
        [data-testid="stSidebarNavLink"] {
            transition: background 0.2s ease, border-color 0.2s ease;
        }
        [data-testid="stSidebarNavLink"]:hover {
            background: rgba(34, 211, 238, 0.06) !important;
        }
        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background: rgba(34, 211, 238, 0.1) !important;
            border-left: 2px solid #22d3ee !important;
        }

        /* ── Page Header Banner ─────────────────────────────────────────────── */
        .header-banner {
            padding: 2rem 2.5rem;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid #1e293b;
            border-radius: 12px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            animation: bannerIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        @keyframes bannerIn {
            0% { opacity: 0; transform: translateY(-12px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .header-banner::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, rgba(30,41,59,1) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(30,41,59,1) 1px, transparent 1px);
            background-size: 14px 24px;
            mask-image: radial-gradient(ellipse 60% 50% at 50% 0%, #000 70%, transparent 100%);
            opacity: 0.15;
        }
        .header-banner::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent 20%, rgba(34,211,238,0.08) 40%, transparent 60%);
            background-size: 200% 100%;
            animation: sheen 6s linear infinite;
        }
        @keyframes sheen {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        .header-banner > * { position: relative; z-index: 1; }
        .sys-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 10px;
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 4px;
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            color: #f59e0b;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .sys-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: #f59e0b;
            display: inline-block;
            animation: pulse 2s cubic-bezier(0.4,0,0.6,1) infinite;
            box-shadow: 0 0 8px #f59e0b;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        .header-title {
            font-family: 'Fira Code', monospace;
            font-size: 2.4rem;
            font-weight: 600;
            color: #f8fafc;
            margin: 0;
            letter-spacing: -0.02em;
        }
        .header-title span { color: #22d3ee; }
        .header-subtitle {
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 0.5rem;
            letter-spacing: 0.04em;
        }

        /* ── Live Ticker ────────────────────────────────────────────────────── */
        .ticker-wrap {
            width: 100%;
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 8px 12px;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1.5rem;
        }
        .ticker-label {
            font-family: 'Fira Code', monospace;
            font-size: 9px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            background: #020617;
            padding: 2px 6px;
            border-radius: 3px;
            white-space: nowrap;
        }
        .ticker-text {
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            color: #22d3ee;
            white-space: nowrap;
            overflow: hidden;
            position: relative;
            flex: 1;
            height: 16px;
        }
        .ticker-inner {
            position: absolute;
            white-space: nowrap;
            animation: marquee 25s linear infinite;
        }
        @keyframes marquee {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        /* ── KPI Cards ──────────────────────────────────────────────────────── */
        .kpi-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .kpi-card {
            flex: 1;
            min-width: 180px;
            padding: 1.5rem;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid #1e293b;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
            transition: box-shadow 0.25s ease, border-color 0.25s ease, transform 0.25s ease;
            cursor: default;
            animation: cardIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        .kpi-container .kpi-card:nth-child(1) { animation-delay: 0.05s; }
        .kpi-container .kpi-card:nth-child(2) { animation-delay: 0.12s; }
        .kpi-container .kpi-card:nth-child(3) { animation-delay: 0.19s; }
        .kpi-container .kpi-card:nth-child(4) { animation-delay: 0.26s; }
        .kpi-container .kpi-card:nth-child(5) { animation-delay: 0.33s; }
        .kpi-container .kpi-card:nth-child(6) { animation-delay: 0.40s; }
        .kpi-container .kpi-card:nth-child(7) { animation-delay: 0.47s; }
        @keyframes cardIn {
            0% { opacity: 0; transform: translateY(14px) scale(0.98); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: -16px; right: -16px;
            width: 96px; height: 96px;
            border-radius: 50%;
            background: rgba(34, 211, 238, 0.08);
            filter: blur(24px);
            transition: background 0.25s ease;
        }
        .kpi-card::after {
            content: '';
            position: absolute;
            left: 0; bottom: 0;
            height: 2px; width: 0%;
            background: linear-gradient(to right, #22d3ee, transparent);
            transition: width 0.35s ease;
        }
        .kpi-card:hover {
            border-color: rgba(34, 211, 238, 0.35);
            box-shadow: 0 0 24px rgba(34, 211, 238, 0.12);
            transform: translateY(-3px);
        }
        .kpi-card:hover::before {
            background: rgba(34, 211, 238, 0.18);
        }
        .kpi-card:hover::after { width: 100%; }
        .kpi-card.amber::before { background: rgba(245, 158, 11, 0.08); }
        .kpi-card.amber::after { background: linear-gradient(to right, #f59e0b, transparent); }
        .kpi-card.amber:hover { border-color: rgba(245, 158, 11, 0.45); box-shadow: 0 0 24px rgba(245, 158, 11, 0.14); }
        .kpi-card.amber:hover::before { background: rgba(245, 158, 11, 0.18); }
        .kpi-card.rose::before { background: rgba(244, 63, 94, 0.08); }
        .kpi-card.rose::after { background: linear-gradient(to right, #f43f5e, transparent); }
        .kpi-card.rose:hover { border-color: rgba(244, 63, 94, 0.35); box-shadow: 0 0 24px rgba(244, 63, 94, 0.12); }
        .kpi-card.lime::before { background: rgba(163, 230, 53, 0.08); }
        .kpi-card.lime::after { background: linear-gradient(to right, #a3e635, transparent); }
        .kpi-card.lime:hover { border-color: rgba(163, 230, 53, 0.45); box-shadow: 0 0 24px rgba(163, 230, 53, 0.14); }
        .kpi-card.lime:hover::before { background: rgba(163, 230, 53, 0.18); }

        .kpi-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #334155;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .kpi-value {
            font-family: 'Fira Code', monospace;
            font-size: 2.2rem;
            font-weight: 600;
            color: #f8fafc;
            line-height: 1;
        }
        .kpi-value.cyan { color: #22d3ee; }
        .kpi-value.amber { color: #f59e0b; }
        .kpi-value.rose { color: #f43f5e; }
        .kpi-value.lime { color: #a3e635; }
        .kpi-value.violet { color: #c084fc; }
        .text-lime { color: #a3e635; }
        .text-violet { color: #c084fc; }
        .text-bright { color: #f8fafc; }
        .kpi-label {
            font-family: 'Fira Code', monospace;
            font-size: 9px;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-top: 0.5rem;
        }
        .kpi-trend {
            font-family: 'Fira Code', monospace;
            font-size: 9px;
            padding: 1px 6px;
            border-radius: 3px;
            margin-top: 0.5rem;
            display: inline-block;
        }
        .kpi-trend.up { background: rgba(52, 211, 153, 0.1); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.2); }
        .kpi-trend.warn { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
        .kpi-trend.critical { background: rgba(244, 63, 94, 0.1); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.2); animation: pulse 2s infinite; }

        /* ── Info / Insight Cards ───────────────────────────────────────────── */
        .info-card {
            padding: 1.25rem 1.5rem;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid #1e293b;
            border-left: 3px solid #22d3ee;
            border-radius: 10px;
            margin-bottom: 1rem;
            transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
        }
        .info-card:hover { border-color: #334155; transform: translateX(3px); box-shadow: 0 0 16px rgba(34,211,238,0.08); }
        .info-card h4, .info-card h5 {
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
            font-weight: 600;
            color: #e2e8f0;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0 0 0.4rem 0;
        }
        .info-card p {
            font-size: 0.875rem;
            color: #94a3b8;
            margin: 0;
            line-height: 1.5;
        }

        /* ── Section Headers ────────────────────────────────────────────────── */
        h2, h3 { 
            font-family: 'Fira Code', monospace !important; 
            color: #f8fafc !important;
        }
        .section-label {
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: #475569;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-label::before {
            content: '';
            display: inline-block;
            width: 3px; height: 12px;
            background: #22d3ee;
            border-radius: 2px;
        }

        /* ── Tabs ────────────────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            border-bottom: 1px solid #1e293b;
            margin-bottom: 1.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Fira Code', monospace !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            color: #64748b !important;
            background: transparent !important;
            padding: 10px 18px !important;
            border-radius: 6px 6px 0 0 !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #22d3ee !important;
            background: rgba(34, 211, 238, 0.06) !important;
        }
        .stTabs [aria-selected="true"] {
            color: #22d3ee !important;
            background: rgba(34, 211, 238, 0.1) !important;
            border-color: rgba(34, 211, 238, 0.3) !important;
            box-shadow: 0 -2px 0 #22d3ee inset !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #22d3ee !important;
        }

        /* ── Scrollbar ──────────────────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #020617; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }

        /* ── Metric widget override ─────────────────────────────────────────── */
        [data-testid="stMetricValue"] {
            font-family: 'Fira Code', monospace !important;
            font-size: 2rem !important;
            color: #22d3ee !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: 'Fira Code', monospace !important;
            font-size: 9px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            color: #64748b !important;
        }

        /* ── Buttons & Inputs ───────────────────────────────────────────────── */
        .stButton > button {
            font-family: 'Fira Code', monospace !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            background: rgba(34, 211, 238, 0.1) !important;
            color: #22d3ee !important;
            border: 1px solid rgba(34, 211, 238, 0.3) !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: rgba(34, 211, 238, 0.2) !important;
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2) !important;
        }
        .stSelectbox label, .stDateInput label, .stTextInput label, .stMultiSelect label {
            font-family: 'Fira Code', monospace !important;
            font-size: 10px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            color: #64748b !important;
        }

        /* ── Footer ─────────────────────────────────────────────────────────── */
        .footer-text {
            text-align: center;
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            color: #334155;
            margin-top: 4rem;
            border-top: 1px solid #0f172a;
            padding-top: 1.5rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)


def ticker(messages: list[str] = None):
    """Renders the live data ticker, matching urban-intel-main live feed bar."""
    default = [
        "> Initializing Telemetry Stream...",
        "> Syncing Coimbatore data nodes...",
        "> Traffic matrix loaded.",
        "> AQI vectors nominal.",
        "> Civic grid synchronized.",
        "> System Nominal. All modules online.",
    ]
    msgs = " &nbsp;&nbsp;&nbsp;&nbsp; ".join(messages or default)
    st.markdown(f"""
        <div class="ticker-wrap">
            <span class="ticker-label">Live Feed</span>
            <div class="ticker-text">
                <div class="ticker-inner">{msgs}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, badge: str = "SYSTEM ONLINE"):
    """Renders the top-of-page header banner with sys badge + grid overlay."""
    st.markdown(f"""
        <div class="header-banner">
            <div class="sys-badge">
                <span class="sys-dot"></span>{badge}
            </div>
            <h1 class="header-title">{title}</h1>
            <p class="header-subtitle">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("""
        <div class="footer-text">
            Coimbatore Urban Intelligence Platform &nbsp;// &nbsp;
            Sys.Grid v1.0 &nbsp;// &nbsp; 2026
        </div>
    """, unsafe_allow_html=True)
