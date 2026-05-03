import streamlit as st
from scorer import calculate_threat_score
from history import history_log
import time
import random

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="SOC Threat Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- MEGA CYBERPUNK CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ---- GLOBAL ---- */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #020510 !important;
    color: #a0e8ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0,245,255,0.015) 2px,
            rgba(0,245,255,0.015) 4px
        );
    pointer-events: none;
    z-index: 0;
    animation: scanlines 8s linear infinite;
}

@keyframes scanlines {
    0% { background-position: 0 0; }
    100% { background-position: 0 100px; }
}

/* ---- HIDE DEFAULT SIDEBAR & HEADER ---- */
[data-testid="stSidebar"] { display: none !important; }
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }

/* ---- TOP NAV BAR ---- */
.top-nav {
    position: sticky;
    top: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    height: 64px;
    background: rgba(2, 5, 16, 0.92);
    border-bottom: 1px solid #00f5ff44;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 30px #00f5ff22, 0 2px 0 #00f5ff33;
    animation: navGlow 3s ease-in-out infinite alternate;
}

@keyframes navGlow {
    0%  { box-shadow: 0 0 20px #00f5ff22, 0 2px 0 #00f5ff33; }
    100%{ box-shadow: 0 0 50px #00f5ff44, 0 2px 0 #00f5ff66; }
}

.nav-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 900;
    color: #00f5ff;
    text-shadow: 0 0 10px #00f5ff, 0 0 20px #00f5ff88;
    letter-spacing: 3px;
    animation: logoPulse 2s ease-in-out infinite;
}

@keyframes logoPulse {
    0%, 100% { text-shadow: 0 0 10px #00f5ff, 0 0 20px #00f5ff88; }
    50%       { text-shadow: 0 0 20px #00f5ff, 0 0 40px #00f5ffaa, 0 0 60px #00f5ff44; }
}

.nav-links {
    display: flex;
    gap: 0.5rem;
}

.nav-btn {
    background: transparent;
    border: 1px solid #00f5ff44;
    color: #a0e8ff;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    padding: 6px 18px;
    cursor: pointer;
    border-radius: 3px;
    text-transform: uppercase;
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
}

.nav-btn::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.15), transparent);
    transition: left 0.4s;
}

.nav-btn:hover::before { left: 100%; }

.nav-btn:hover {
    border-color: #00f5ff;
    color: #00f5ff;
    box-shadow: 0 0 15px #00f5ff44, inset 0 0 10px #00f5ff11;
    text-shadow: 0 0 8px #00f5ff;
}

.nav-btn.active {
    border-color: #00f5ff;
    color: #00f5ff;
    background: rgba(0,245,255,0.08);
    box-shadow: 0 0 20px #00f5ff55;
    text-shadow: 0 0 8px #00f5ff;
}

.nav-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #00ff88;
    letter-spacing: 1px;
}

.status-dot {
    width: 8px; height: 8px;
    background: #00ff88;
    border-radius: 50%;
    animation: statusPulse 1.5s ease-in-out infinite;
    box-shadow: 0 0 6px #00ff88;
}

@keyframes statusPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.8); }
}

/* ---- PAGE WRAPPER ---- */
.main-content {
    padding: 2rem 2.5rem;
    animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---- SECTION TITLE ---- */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00f5ff;
    text-shadow: 0 0 20px #00f5ff88;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    position: relative;
    display: inline-block;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -6px; left: 0;
    width: 100%; height: 1px;
    background: linear-gradient(90deg, #00f5ff, transparent);
    animation: titleLine 2s ease-in-out infinite alternate;
}

@keyframes titleLine {
    0%  { width: 60%; opacity: 0.6; }
    100%{ width: 100%; opacity: 1; }
}

.section-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #00f5ff66;
    letter-spacing: 3px;
    margin-bottom: 2rem;
}

/* ---- INPUT ---- */
.stTextArea textarea {
    background: rgba(0,245,255,0.04) !important;
    border: 1px solid #00f5ff44 !important;
    border-radius: 4px !important;
    color: #a0e8ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: border 0.3s, box-shadow 0.3s !important;
}

.stTextArea textarea:focus {
    border-color: #00f5ff !important;
    box-shadow: 0 0 20px #00f5ff33 !important;
    outline: none !important;
}

/* ---- SCAN BUTTON ---- */
.stButton > button {
    background: transparent !important;
    border: 1px solid #00f5ff !important;
    color: #00f5ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 3px !important;
    padding: 12px 40px !important;
    border-radius: 3px !important;
    text-transform: uppercase !important;
    transition: all 0.3s !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 0 15px #00f5ff44 !important;
}

.stButton > button:hover {
    background: rgba(0,245,255,0.12) !important;
    box-shadow: 0 0 30px #00f5ff88, inset 0 0 20px #00f5ff11 !important;
    transform: translateY(-2px) !important;
    text-shadow: 0 0 10px #00f5ff !important;
}

/* Stop button red style */
[data-testid="baseButton-secondary"]:has(div:contains("STOP")),
.stButton > button:contains("STOP") {
    border-color: #ff1e3c !important;
    color: #ff4060 !important;
    box-shadow: 0 0 20px #ff1e3c55 !important;
    animation: stopPulse 1s ease-in-out infinite !important;
}
@keyframes stopPulse {
    0%, 100% { box-shadow: 0 0 15px #ff1e3c44; }
    50%       { box-shadow: 0 0 35px #ff1e3c99; }
}

/* ---- METRIC CARDS ---- */
[data-testid="stMetric"] {
    background: rgba(0,245,255,0.04) !important;
    border: 1px solid #00f5ff33 !important;
    border-radius: 6px !important;
    padding: 1rem 1.2rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.3s !important;
    animation: cardSlideIn 0.5s ease-out both !important;
}

[data-testid="stMetric"]:hover {
    border-color: #00f5ff88 !important;
    box-shadow: 0 0 25px #00f5ff22 !important;
    transform: translateY(-3px) !important;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #00f5ff;
    box-shadow: 0 0 10px #00f5ff;
}

@keyframes cardSlideIn {
    from { opacity: 0; transform: translateX(-15px); }
    to   { opacity: 1; transform: translateX(0); }
}

[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    color: #00f5ff88 !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #00f5ff !important;
    text-shadow: 0 0 15px #00f5ff88 !important;
}

/* ---- THREAT LEVEL BADGES ---- */
.threat-safe {
    display: inline-flex; align-items: center; gap: 10px;
    background: rgba(0,255,100,0.08);
    border: 1px solid #00ff6488;
    border-left: 4px solid #00ff64;
    color: #00ff88;
    padding: 10px 20px;
    border-radius: 4px;
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
    animation: safeGlow 2s ease-in-out infinite alternate;
    box-shadow: 0 0 20px rgba(0,255,100,0.1);
}
@keyframes safeGlow {
    0%  { box-shadow: 0 0 10px rgba(0,255,100,0.1); }
    100%{ box-shadow: 0 0 25px rgba(0,255,100,0.3); }
}

.threat-medium {
    display: inline-flex; align-items: center; gap: 10px;
    background: rgba(255,200,0,0.08);
    border: 1px solid #ffc80088;
    border-left: 4px solid #ffc800;
    color: #ffc800;
    padding: 10px 20px;
    border-radius: 4px;
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
    animation: warningFlicker 1.5s ease-in-out infinite;
    box-shadow: 0 0 20px rgba(255,200,0,0.1);
}
@keyframes warningFlicker {
    0%, 100%{ opacity: 1; box-shadow: 0 0 15px rgba(255,200,0,0.2); }
    50%     { opacity: 0.85; box-shadow: 0 0 30px rgba(255,200,0,0.4); }
}

.threat-high {
    display: inline-flex; align-items: center; gap: 10px;
    background: rgba(255,30,60,0.1);
    border: 1px solid #ff1e3c88;
    border-left: 4px solid #ff1e3c;
    color: #ff4060;
    padding: 10px 20px;
    border-radius: 4px;
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
    animation: criticalPulse 0.8s ease-in-out infinite;
    box-shadow: 0 0 20px rgba(255,30,60,0.2);
}
@keyframes criticalPulse {
    0%, 100%{ box-shadow: 0 0 20px rgba(255,30,60,0.2); transform: scale(1); }
    50%     { box-shadow: 0 0 40px rgba(255,30,60,0.5); transform: scale(1.01); }
}

/* ---- REASON CARDS ---- */
.reason-item {
    display: flex; align-items: flex-start; gap: 12px;
    background: rgba(0,245,255,0.03);
    border: 1px solid #00f5ff22;
    border-left: 3px solid #00f5ff66;
    padding: 10px 16px;
    margin: 6px 0;
    border-radius: 3px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: #a0e8ff;
    animation: reasonSlide 0.4s ease-out both;
    transition: all 0.2s;
}
.reason-item:hover {
    background: rgba(0,245,255,0.06);
    border-left-color: #00f5ff;
}
@keyframes reasonSlide {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ---- DASHBOARD LOG ---- */
.log-entry {
    background: rgba(0,245,255,0.03);
    border: 1px solid #00f5ff1a;
    border-left: 3px solid transparent;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    animation: logFadeIn 0.4s ease-out both;
    transition: all 0.2s;
}
.log-entry:hover { background: rgba(0,245,255,0.06); }
.log-entry.safe   { border-left-color: #00ff64; }
.log-entry.medium { border-left-color: #ffc800; }
.log-entry.high   { border-left-color: #ff1e3c; }
@keyframes logFadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.log-score-safe   { color: #00ff88; font-weight: bold; }
.log-score-medium { color: #ffc800; font-weight: bold; }
.log-score-high   { color: #ff4060; font-weight: bold; }

/* ---- LIVE STREAM ---- */
.stream-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 1.5rem;
}

.live-badge {
    background: rgba(255,30,60,0.15);
    border: 1px solid #ff1e3c88;
    color: #ff4060;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    padding: 4px 12px;
    border-radius: 2px;
    animation: liveBlink 1s step-end infinite;
}
@keyframes liveBlink {
    0%, 100%{ opacity: 1; }
    50%     { opacity: 0.3; }
}

.packet-card {
    background: rgba(0,245,255,0.04);
    border: 1px solid #00f5ff33;
    border-radius: 6px;
    padding: 1.5rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
    animation: packetIn 0.3s ease-out;
}
.packet-card::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.06), transparent);
    animation: sweep 2s linear infinite;
}
@keyframes sweep {
    0%  { left: -60%; }
    100%{ left: 140%; }
}
@keyframes packetIn {
    from { opacity: 0; transform: scale(0.97); }
    to   { opacity: 1; transform: scale(1); }
}

.packet-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: #00f5ff88;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* ---- CODE BLOCK ---- */
.stCodeBlock { 
    border: 1px solid #00f5ff22 !important; 
    border-radius: 4px !important; 
}

/* ---- DIVIDER ---- */
hr { border-color: #00f5ff22 !important; }

/* ---- INFO BOX ---- */
.stInfo {
    background: rgba(0,245,255,0.05) !important;
    border: 1px solid #00f5ff33 !important;
    color: #a0e8ff !important;
}

/* ---- SUCCESS BOX ---- */
[data-testid="stSuccess"] {
    background: rgba(0,255,100,0.07) !important;
    border: 1px solid #00ff6444 !important;
    color: #00ff88 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 2px !important;
}

/* ---- GLITCH TITLE ANIM ---- */
@keyframes glitch {
    0%   { text-shadow: 0 0 20px #00f5ff88; }
    20%  { text-shadow: -2px 0 #ff00ff66, 2px 0 #00f5ff88; }
    40%  { text-shadow: 2px 0 #ff00ff66, -2px 0 #00f5ff88; }
    60%  { text-shadow: 0 0 20px #00f5ff88; }
    80%  { text-shadow: -1px 0 #00ff8866, 1px 0 #00f5ff88; }
    100% { text-shadow: 0 0 20px #00f5ff88; }
}

.glitch-text {
    animation: glitch 4s ease-in-out infinite;
}

/* ---- ABOUT GRID ---- */
.about-card {
    background: rgba(0,245,255,0.04);
    border: 1px solid #00f5ff22;
    border-top: 2px solid #00f5ff66;
    border-radius: 6px;
    padding: 1.5rem;
    transition: all 0.3s;
}
.about-card:hover {
    background: rgba(0,245,255,0.08);
    border-color: #00f5ff55;
    box-shadow: 0 0 25px #00f5ff22;
    transform: translateY(-4px);
}
.about-card-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    color: #00f5ff;
    letter-spacing: 2px;
    margin-bottom: 8px;
}
.about-card-body {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem;
    color: #a0e8ff;
    line-height: 1.6;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #020510; }
::-webkit-scrollbar-thumb { background: #00f5ff44; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00f5ff88; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE FOR NAV ----------------
if "page" not in st.session_state:
    st.session_state.page = "Analyzer"

# ---------------- TOP NAV BAR ----------------
pages = ["Analyzer", "SOC Dashboard", "Live Stream", "About"]
page_icons = {"Analyzer": "⬡ SCAN", "SOC Dashboard": "⬡ DASHBOARD", "Live Stream": "⬡ LIVE", "About": "⬡ ABOUT"}

cols = st.columns([3, 1, 1, 1, 1, 2])

with cols[0]:
    st.markdown('<div class="nav-logo">🛡 SOC//MATRIX</div>', unsafe_allow_html=True)

for i, page in enumerate(pages):
    with cols[i + 1]:
        active_class = "active" if st.session_state.page == page else ""
        if st.button(page_icons[page], key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

with cols[5]:
    st.markdown('<div class="nav-status"><div class="status-dot"></div>SYSTEM ONLINE</div>', unsafe_allow_html=True)

st.markdown('<hr style="margin:0; border-color:#00f5ff22;">', unsafe_allow_html=True)

menu = st.session_state.page

# ---- helper: threat color class ----
def level_class(level):
    l = level.lower()
    if "high" in l:   return "high"
    if "medium" in l or "mid" in l: return "medium"
    return "safe"

def threat_badge(level):
    cls = level_class(level)
    icons = {"safe": "✔", "medium": "⚠", "high": "⛔"}
    return f'<div class="threat-{cls}">{icons[cls]} &nbsp; {level.upper()}</div>'

# ---------------- ANALYZER ----------------
if menu == "Analyzer":

    st.markdown("""
    <div class="main-content">
        <div class="section-title glitch-text">⬡ Threat Score Analyzer</div>
        <div class="section-sub">// SUBMIT PAYLOAD · URL · COMMAND FOR ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area("Enter payload / URL / command:", height=120, placeholder="e.g.  ' OR '1'='1  |  <script>alert(1)</script>  |  ; rm -rf /")

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        scan = st.button("⬡  INITIATE SCAN", use_container_width=True)

    if scan and user_input.strip():

        with st.spinner(""):
            time.sleep(0.4)

        score, level, reasons, confidence = calculate_threat_score(user_input)

        history_log.append({"input": user_input, "score": score, "level": level})

        st.markdown("---")
        st.markdown("##### THREAT ANALYSIS RESULT")

        c1, c2, c3 = st.columns(3)
        c1.metric("THREAT SCORE", f"{score}/100")
        c2.metric("RISK LEVEL", level)
        c3.metric("CONFIDENCE", f"{confidence}%")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(threat_badge(level), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("##### DETECTION SIGNATURES")
        if reasons:
            for i, r in enumerate(reasons):
                delay = i * 0.1
                st.markdown(f'<div class="reason-item" style="animation-delay:{delay}s">⚠ &nbsp; {r}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="reason-item" style="border-left-color:#00ff64; color:#00ff88">✔ &nbsp; No threat signatures detected — input appears safe</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
elif menu == "SOC Dashboard":

    st.markdown("""
    <div class="main-content">
        <div class="section-title glitch-text">⬡ SOC Monitoring Dashboard</div>
        <div class="section-sub">// LAST 15 EVENTS · REAL-TIME LOG</div>
    </div>
    """, unsafe_allow_html=True)

    if not history_log:
        st.info("No activity logged yet. Run the Analyzer or Live Stream first.")
    else:
        safe_c = sum(1 for x in history_log if level_class(x["level"]) == "safe")
        med_c  = sum(1 for x in history_log if level_class(x["level"]) == "medium")
        high_c = sum(1 for x in history_log if level_class(x["level"]) == "high")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TOTAL EVENTS", len(history_log))
        m2.metric("🟢 SAFE", safe_c)
        m3.metric("🟡 MEDIUM", med_c)
        m4.metric("🔴 HIGH RISK", high_c)

        st.markdown("---")
        st.markdown("##### EVENT LOG")

        for item in reversed(history_log[-15:]):
            cls = level_class(item["level"])
            score_cls = f"log-score-{cls}"
            st.markdown(f"""
            <div class="log-entry {cls}">
                <span style="color:#00f5ff88; font-size:0.65rem; letter-spacing:2px">PAYLOAD &nbsp;›&nbsp;</span>
                <span style="color:#e0f8ff">{item['input'][:70]}{'...' if len(item['input'])>70 else ''}</span>
                <br>
                <span style="color:#00f5ff55; font-size:0.65rem">SCORE: </span>
                <span class="{score_cls}">{item['score']}/100</span>
                &nbsp;&nbsp;
                <span style="color:#00f5ff55; font-size:0.65rem">LEVEL: </span>
                <span class="{score_cls}">{item['level'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)

# ---------------- LIVE STREAM ----------------
elif menu == "Live Stream":

    st.markdown("""
    <div class="main-content">
        <div class="section-title glitch-text">⬡ Live SOC Attack Stream</div>
        <div class="section-sub">// SIMULATED REAL-TIME PACKET INTERCEPTION</div>
    </div>
    """, unsafe_allow_html=True)

    samples = [
        ("user login request", "safe"), ("fetch homepage", "safe"),
        ("hello world", "safe"), ("normal browsing", "safe"),
        ("' OR '1'='1", "sql"), ("SELECT * FROM users", "sql"),
        ("DROP TABLE users", "sql"), ("admin' --", "sql"),
        ("<script>alert(1)</script>", "xss"), ("<img src=x onerror=alert(1)>", "xss"),
        ("document.cookie", "xss"),
        ("; rm -rf /", "cmd"), ("&& whoami", "cmd"), ("| ls -la", "cmd"),
        ("%3Cscript%3Ealert(1)%3C/script%3E", "enc"), ("c3VicHJvY2Vzcw==", "enc")
    ]

    type_labels = {
        "safe": ("NORMAL TRAFFIC", "#00ff88"),
        "sql":  ("SQL INJECTION",  "#ff4060"),
        "xss":  ("XSS ATTEMPT",    "#ff4060"),
        "cmd":  ("CMD INJECTION",  "#ff4060"),
        "enc":  ("ENCODED PAYLOAD","#ffc800"),
    }

    # ---- session state for stream control ----
    if "stream_running" not in st.session_state:
        st.session_state.stream_running = False

    col_start, _ = st.columns([1, 4])
    with col_start:
        if not st.session_state.stream_running:
            if st.button("⬡  START STREAM", use_container_width=True, key="start_btn"):
                st.session_state.stream_running = True
                st.rerun()
        else:
            if st.button("⬛  STOP STREAM", use_container_width=True, key="stop_btn"):
                st.session_state.stream_running = False
                st.rerun()

    if st.session_state.stream_running:
        placeholder = st.empty()

        for i in range(30):
            # Check stop flag each iteration
            if not st.session_state.stream_running:
                break

            payload, ptype = random.choice(samples)
            score, level, reasons, confidence = calculate_threat_score(payload)

            history_log.append({"input": payload, "score": score, "level": level})

            cls = level_class(level)
            label, label_color = type_labels.get(ptype, ("UNKNOWN", "#a0e8ff"))

            score_color = {"safe": "#00ff88", "medium": "#ffc800", "high": "#ff4060"}.get(cls, "#00f5ff")

            critical_banner = ""
            if cls == "high":
                critical_banner = '<div class="threat-high" style="margin-top:1rem">⛔ &nbsp; CRITICAL THREAT DETECTED — IMMEDIATE ACTION REQUIRED</div>'

            reasons_html = ""
            if reasons:
                reasons_html = "".join(f'<div class="reason-item">⚠ &nbsp; {r}</div>' for r in reasons)

            with placeholder.container():
                st.markdown(f"""
                <div class="packet-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                        <span class="packet-label">📥 INCOMING PACKET #{i+1}/30</span>
                        <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:{label_color}; letter-spacing:2px; border:1px solid {label_color}44; padding:3px 10px; border-radius:2px;">{label}</span>
                        <span class="live-badge">● LIVE</span>
                    </div>
                    <div style="background:rgba(0,0,0,0.4); border:1px solid #00f5ff22; padding:10px 16px; border-radius:3px; font-family:'Share Tech Mono',monospace; font-size:0.9rem; color:#e0f8ff; word-break:break-all;">
                        {payload}
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; margin-top:1rem;">
                        <div style="text-align:center; padding:12px; background:rgba(0,245,255,0.04); border:1px solid #00f5ff22; border-radius:4px;">
                            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#00f5ff66; letter-spacing:2px;">SCORE</div>
                            <div style="font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700; color:{score_color}; text-shadow:0 0 10px {score_color}88;">{score}</div>
                        </div>
                        <div style="text-align:center; padding:12px; background:rgba(0,245,255,0.04); border:1px solid #00f5ff22; border-radius:4px;">
                            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#00f5ff66; letter-spacing:2px;">RISK</div>
                            <div style="font-family:'Orbitron',monospace; font-size:1rem; font-weight:700; color:{score_color}; text-shadow:0 0 10px {score_color}88;">{level.upper()}</div>
                        </div>
                        <div style="text-align:center; padding:12px; background:rgba(0,245,255,0.04); border:1px solid #00f5ff22; border-radius:4px;">
                            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#00f5ff66; letter-spacing:2px;">CONFIDENCE</div>
                            <div style="font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700; color:#00f5ff; text-shadow:0 0 10px #00f5ff88;">{confidence}%</div>
                        </div>
                    </div>
                    {critical_banner}
                    {reasons_html}
                </div>
                """, unsafe_allow_html=True)

            time.sleep(3)

        # Stream ended — either completed or stopped
        st.session_state.stream_running = False
        if i >= 29:
            st.success("✔  STREAM COMPLETE — ALL PACKETS ANALYZED")
        else:
            st.warning("⬛  STREAM TERMINATED BY OPERATOR")

# ---------------- ABOUT ----------------
elif menu == "About":

    st.markdown("""
    <div class="main-content">
        <div class="section-title glitch-text">⬡ About SOC Simulator</div>
        <div class="section-sub">// SECURITY OPERATIONS CENTER · THREAT INTELLIGENCE PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="about-card">
            <div class="about-card-title">🔴 SQL Injection</div>
            <div class="about-card-body">
                Detects malicious SQL syntax used to manipulate databases —
                including OR bypasses, DROP commands, UNION attacks, and comment injections.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="about-card">
            <div class="about-card-title">🟡 XSS Attacks</div>
            <div class="about-card-body">
                Identifies Cross-Site Scripting payloads including inline script tags,
                event handler injections, and encoded variants targeting browser execution.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="about-card">
            <div class="about-card-title">🟠 Command Injection</div>
            <div class="about-card-body">
                Catches shell injection patterns that attempt OS-level command execution —
                pipe operators, shell separators, and dangerous system commands.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_info, _ = st.columns([2, 1])
    with col_info:
        st.markdown("""
        <div class="about-card">
            <div class="about-card-title">⬡ System Architecture</div>
            <div class="about-card-body">
                This platform simulates a real-time Security Operations Center workflow.<br><br>
                • <b>Analyzer</b> — manual payload inspection with confidence scoring<br>
                • <b>Dashboard</b> — live event log with threat distribution metrics<br>
                • <b>Live Stream</b> — automated packet interception simulation<br><br>
                Scoring engine: <code>scorer.py</code> &nbsp;|&nbsp; History engine: <code>history.py</code>
            </div>
        </div>
        """, unsafe_allow_html=True)