"""
dashboard.py — Password Strength Analyzer
& Security Suggestion Tool
Techno Neon Cyberpunk UI
Run: python -m streamlit run dashboard.py
⚠️ DEFENSIVE tool — no passwords stored/logged
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import random
from datetime import datetime

sys.path.insert(0, ".")
from src.analyzer          import PasswordAnalyzer
from src.suggestion_engine import SuggestionEngine
from src.password_generator import PasswordGenerator
from src.breach_checker    import BreachChecker
from src.entropy_engine    import EntropyEngine
from src.education         import (
    EDUCATION, INTERVIEW_QA
)

# ── Page config ───────────────────────────────
st.set_page_config(
    page_title="CyberPass — Password Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Init engines ──────────────────────────────
@st.cache_resource
def load_engines():
    return {
        "analyzer":   PasswordAnalyzer(),
        "suggester":  SuggestionEngine(),
        "generator":  PasswordGenerator(),
        "breach":     BreachChecker(),
        "entropy":    EntropyEngine(),
    }

engines = load_engines()

# ── Session state ─────────────────────────────
if "page"        not in st.session_state:
    st.session_state.page        = "analyzer"
if "history"     not in st.session_state:
    st.session_state.history     = []
if "show_pass"   not in st.session_state:
    st.session_state.show_pass   = False

# ── TECHNO CSS ────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');

:root {
  --bg:      #000000;
  --bg2:     #050510;
  --card:    #0a0a1a;
  --border:  #00ff4130;
  --green:   #00ff41;
  --cyan:    #00d4ff;
  --pink:    #ff0080;
  --yellow:  #ffff00;
  --orange:  #ff6b00;
  --purple:  #bf00ff;
  --red:     #ff0040;
  --muted:   #4a5568;
  --text:    #e0e0e0;
}

* { font-family:'Inter',sans-serif !important; }
.stApp {
  background: #000000;
  background-image:
    radial-gradient(ellipse at 20% 50%,
      rgba(0,255,65,0.03) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%,
      rgba(0,212,255,0.03) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%,
      rgba(191,0,255,0.03) 0%, transparent 50%);
  color: var(--text);
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #050510 !important;
  border-right: 1px solid #00ff4120;
}

/* Metrics */
[data-testid="stMetric"] {
  background: #0a0a1a;
  border: 1px solid #00ff4130;
  border-radius: 12px;
  padding: 16px !important;
  position: relative; overflow: hidden;
}
[data-testid="stMetric"]::before {
  content: '';
  position: absolute; top: 0; left: 0;
  right: 0; height: 2px;
  background: linear-gradient(90deg,
    #00ff41, #00d4ff, #bf00ff, #ff0080
  );
}
[data-testid="stMetricValue"] {
  font-size: 1.6rem !important;
  font-weight: 900 !important;
  color: #00ff41 !important;
  font-family: 'Orbitron',monospace !important;
}
[data-testid="stMetricLabel"] {
  color: #4a5568 !important;
  font-size: 0.68rem !important;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

/* Cards */
.cyber-card {
  background: #0a0a1a;
  border: 1px solid #00ff4130;
  border-radius: 14px;
  padding: 20px;
  margin: 8px 0;
  position: relative; overflow: hidden;
}
.cyber-card::before {
  content: '';
  position: absolute; top: 0; left: 0;
  right: 0; height: 2px;
  background: linear-gradient(90deg,
    transparent, #00ff41, transparent
  );
}

/* Password input */
.pass-input {
  background: #050510 !important;
  border: 1px solid #00ff4150 !important;
  border-radius: 10px !important;
  color: #00ff41 !important;
  font-family: 'Share Tech Mono',monospace !important;
  font-size: 1rem !important;
}
.pass-input:focus {
  border-color: #00ff41 !important;
  box-shadow: 0 0 20px rgba(0,255,65,0.2) !important;
}

/* Score bar */
.score-bar-bg {
  background: #0a0a1a;
  border: 1px solid #00ff4120;
  border-radius: 4px;
  height: 12px;
  margin: 8px 0;
  overflow: hidden;
}
.score-bar-fill {
  height: 12px;
  border-radius: 4px;
  transition: width 0.5s ease;
  position: relative;
}
.score-bar-fill::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg,
    transparent 0%, rgba(255,255,255,0.2) 50%,
    transparent 100%
  );
}

/* Issue cards */
.issue-critical {
  background: rgba(255,0,64,0.08);
  border-left: 3px solid #ff0040;
  border-radius: 0 8px 8px 0;
  padding: 10px 14px; margin: 5px 0;
}
.issue-high {
  background: rgba(255,107,0,0.08);
  border-left: 3px solid #ff6b00;
  border-radius: 0 8px 8px 0;
  padding: 10px 14px; margin: 5px 0;
}
.issue-medium {
  background: rgba(255,255,0,0.08);
  border-left: 3px solid #ffff00;
  border-radius: 0 8px 8px 0;
  padding: 10px 14px; margin: 5px 0;
}
.issue-low {
  background: rgba(0,255,65,0.05);
  border-left: 3px solid #00ff41;
  border-radius: 0 8px 8px 0;
  padding: 10px 14px; margin: 5px 0;
}

/* Suggestion cards */
.sug-critical {
  background: rgba(255,0,64,0.08);
  border: 1px solid #ff004040;
  border-radius: 10px;
  padding: 12px 16px; margin: 5px 0;
}
.sug-high {
  background: rgba(255,107,0,0.08);
  border: 1px solid #ff6b0040;
  border-radius: 10px;
  padding: 12px 16px; margin: 5px 0;
}
.sug-medium {
  background: rgba(255,255,0,0.06);
  border: 1px solid #ffff0030;
  border-radius: 10px;
  padding: 12px 16px; margin: 5px 0;
}
.sug-tip {
  background: rgba(0,212,255,0.06);
  border: 1px solid #00d4ff30;
  border-radius: 10px;
  padding: 12px 16px; margin: 5px 0;
}

/* Buttons */
.stButton>button {
  background: linear-gradient(
    135deg, #00ff4120, #00d4ff20
  ) !important;
  color: #00ff41 !important;
  border: 1px solid #00ff4150 !important;
  border-radius: 8px !important;
  font-family: 'Share Tech Mono',monospace !important;
  font-weight: 700 !important;
  letter-spacing: 1px !important;
  transition: all 0.2s !important;
}
.stButton>button:hover {
  background: linear-gradient(
    135deg, #00ff4130, #00d4ff30
  ) !important;
  border-color: #00ff41 !important;
  box-shadow: 0 0 15px rgba(0,255,65,0.3) !important;
  transform: translateY(-1px) !important;
}

/* Section title */
.section-title {
  font-family: 'Orbitron',monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: #00ff41;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 14px 0 8px;
  padding-left: 10px;
  border-left: 2px solid #00ff41;
}

/* Badges */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
  font-family: 'Share Tech Mono',monospace;
  letter-spacing: 1px;
}
.badge-green  {
  background: rgba(0,255,65,0.15);
  color: #00ff41;
  border: 1px solid #00ff4150;
}
.badge-red    {
  background: rgba(255,0,64,0.15);
  color: #ff0040;
  border: 1px solid #ff004050;
}
.badge-yellow {
  background: rgba(255,255,0,0.1);
  color: #ffff00;
  border: 1px solid #ffff0040;
}
.badge-cyan   {
  background: rgba(0,212,255,0.12);
  color: #00d4ff;
  border: 1px solid #00d4ff40;
}
.badge-purple {
  background: rgba(191,0,255,0.12);
  color: #bf00ff;
  border: 1px solid #bf00ff40;
}

/* Password display */
.pass-display {
  font-family: 'Share Tech Mono',monospace;
  background: #050510;
  border: 1px solid #00ff4140;
  border-radius: 8px;
  padding: 12px 16px;
  color: #00ff41;
  font-size: 1rem;
  letter-spacing: 2px;
  word-break: break-all;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: #050510;
  border-radius: 8px;
  padding: 4px; gap: 4px;
  border: 1px solid #00ff4120;
}
.stTabs [data-baseweb="tab"] {
  color: #4a5568 !important;
  font-family: 'Share Tech Mono',monospace !important;
  font-weight: 700 !important;
  border-radius: 6px !important;
  letter-spacing: 1px !important;
  font-size: 0.8rem !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(0,255,65,0.15) !important;
  color: #00ff41 !important;
  border: 1px solid #00ff4140 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
  border: 1px solid #00ff4130 !important;
  border-radius: 10px !important;
}

/* Glitch animation for title */
@keyframes flicker {
  0%,19%,21%,23%,25%,54%,56%,100% { opacity:1; }
  20%,24%,55% { opacity:0.4; }
}
.cyber-title {
  font-family: 'Orbitron',monospace;
  font-weight: 900;
  animation: flicker 8s infinite;
}

/* Scanline overlay */
.stApp::after {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0,0,0,0.03) 0px,
    rgba(0,0,0,0.03) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none; z-index: 9999;
}

/* Neon glow text */
.neon-green {
  color: #00ff41;
  text-shadow: 0 0 10px rgba(0,255,65,0.5);
}
.neon-cyan {
  color: #00d4ff;
  text-shadow: 0 0 10px rgba(0,212,255,0.5);
}
.neon-pink {
  color: #ff0080;
  text-shadow: 0 0 10px rgba(255,0,128,0.5);
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
      <div style='font-size:2.5rem'>🔐</div>
      <div style='font-family:Orbitron,monospace;
        font-size:1.1rem;font-weight:900;
        color:#00ff41;margin-top:6px;
        text-shadow:0 0 10px rgba(0,255,65,0.5)'>
        CyberPass
      </div>
      <div style='color:#4a5568;font-size:0.7rem;
        letter-spacing:2px;font-family:
        Share Tech Mono,monospace'>
        PASSWORD ANALYZER v2.0
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;
      margin-bottom:12px'>
      <span style='width:6px;height:6px;
        background:#00ff41;border-radius:50%;
        display:inline-block;
        animation:pulse 1.5s infinite'></span>
      <span style='color:#00ff41;font-size:0.7rem;
        font-weight:700;margin-left:6px;
        font-family:Share Tech Mono,monospace'>
        SYSTEM ONLINE
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    pages = [
        ("🔍","Analyzer",  "analyzer"),
        ("🔑","Generator", "generator"),
        ("💥","Breach Sim","breach"),
        ("📚","Education", "education"),
        ("📊","History",   "history"),
        ("🎤","Interview", "interview"),
    ]
    for icon, label, key in pages:
        is_active = st.session_state.page == key
        if st.sidebar.button(
            f"{icon}  {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary"
            if is_active else "secondary",
        ):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='background:#050510;
      border:1px solid #ff004030;
      border-radius:10px;padding:12px;
      font-size:0.72rem;
      font-family:Share Tech Mono,monospace'>
      <div style='color:#ff0040;
        font-weight:700;margin-bottom:6px'>
        ⚠️ DISCLAIMER
      </div>
      <div style='color:#4a5568;line-height:1.5'>
        Passwords analyzed locally.<br>
        Nothing stored or transmitted.<br>
        Defensive tool only.
      </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# ════════════════════════════════════════════
# PAGE: ANALYZER
# ════════════════════════════════════════════
if page == "analyzer":

    st.markdown("""
    <div style='margin-bottom:20px'>
      <h1 class='cyber-title'
        style='font-size:1.8rem;
        color:#00ff41;margin:0'>
        🔍 PASSWORD STRENGTH ANALYZER
      </h1>
      <p style='color:#4a5568;margin:6px 0 0;
        font-family:Share Tech Mono,monospace;
        font-size:0.8rem;letter-spacing:1px'>
        REAL-TIME SECURITY ANALYSIS •
        PATTERN DETECTION •
        ENTROPY CALCULATION
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Password input
    col_in, col_tog = st.columns([4,1])
    with col_in:
        input_type = (
            "text" if st.session_state.show_pass
            else "password"
        )
        password = st.text_input(
            "🔐 Enter Password to Analyze",
            type=input_type,
            placeholder="Type any password...",
            help="⚠️ Analyzed locally. Not stored.",
            key="main_password_input",
        )
    with col_tog:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "👁️ Show" if not st.session_state.show_pass
            else "🙈 Hide",
            use_container_width=True,
        ):
            st.session_state.show_pass = \
                not st.session_state.show_pass
            st.rerun()

    # Optional context
    with st.expander(
        "👤 Optional: Add personal context "
        "(improves detection)"
    ):
        col1,col2,col3 = st.columns(3)
        with col1:
            ctx_name = st.text_input(
                "Your name", placeholder="e.g. Neha"
            )
        with col2:
            ctx_dob  = st.text_input(
                "Birthday", placeholder="e.g. 2002"
            )
        with col3:
            ctx_city = st.text_input(
                "City", placeholder="e.g. Pune"
            )

    context = {}
    if ctx_name: context["name"] = ctx_name
    if ctx_dob:  context["birthday"] = ctx_dob
    if ctx_city: context["city"] = ctx_city

    if not password:
        st.markdown("""
        <div style='text-align:center;
          padding:60px 20px'>
          <div style='font-size:4rem'>🔐</div>
          <div style='font-family:Orbitron,monospace;
            color:#00ff41;font-size:1.2rem;
            margin-top:16px'>
            AWAITING INPUT...
          </div>
          <div style='color:#4a5568;
            font-family:Share Tech Mono,monospace;
            font-size:0.8rem;margin-top:8px'>
            Enter a password above to begin analysis
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── Run analysis ──────────────────────────
    result   = engines["analyzer"].analyze(
        password, context if context else None
    )
    suggest  = engines["suggester"].generate(result)
    breach   = engines["breach"].check_password(
        password
    )
    hash_prev= engines["breach"]\
        .get_hash_preview(password)

    # Save to history (no password stored)
    st.session_state.history.append({
        "time":    datetime.now().strftime("%H:%M:%S"),
        "length":  result["password_length"],
        "score":   result["score"],
        "label":   result["label"],
        "entropy": result["eff_entropy"],
    })
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

    # ── Score display ─────────────────────────
    score = result["score"]
    color = result["color"]
    label = result["label"]
    icon  = result["icon"]

    st.markdown(f"""
    <div class='cyber-card' style='
      border-color:{color}40;
      text-align:center;padding:24px'>
      <div style='font-size:3rem'>{icon}</div>
      <div style='font-family:Orbitron,monospace;
        font-size:2rem;font-weight:900;
        color:{color};margin:8px 0;
        text-shadow:0 0 20px {color}80'>
        {label}
      </div>
      <div style='font-family:Orbitron,monospace;
        font-size:3rem;font-weight:900;
        color:{color};
        text-shadow:0 0 30px {color}'>
        {score:.0f}<span style='font-size:1.5rem;
        color:#4a5568'>/100</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Score bar
    bar_gradient = {
        "VERY WEAK":   "linear-gradient(90deg,#ff0040,#ff0040)",
        "WEAK":        "linear-gradient(90deg,#ff0040,#ff6b00)",
        "MODERATE":    "linear-gradient(90deg,#ff6b00,#ffff00)",
        "STRONG":      "linear-gradient(90deg,#ffff00,#00ff88)",
        "VERY STRONG": "linear-gradient(90deg,#00ff88,#00d4ff)",
    }.get(label,
          "linear-gradient(90deg,#333,#333)")

    st.markdown(f"""
    <div class='score-bar-bg'>
      <div class='score-bar-fill'
        style='width:{score:.0f}%;
        background:{bar_gradient}'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI Row ───────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("📏 Length",
              result["password_length"])
    c2.metric("🎲 Entropy",
              f"{result['eff_entropy']:.1f} bits")
    c3.metric("⏱️ Crack Time",
              result["crack_time"])
    c4.metric("⚠️ Issues",
              len(result["issues"]))
    c5.metric("🔥 Breach",
              "FOUND 🚨"
              if breach["found"]
              else "SAFE ✅")

    st.markdown("---")

    # ── Main analysis tabs ────────────────────
    tab1,tab2,tab3,tab4,tab5 = st.tabs([
        "🔬 Analysis",
        "💡 Suggestions",
        "📊 Charts",
        "🔡 Characters",
        "🔑 Hash Info",
    ])

    # ── TAB 1: Analysis ───────────────────────
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Issues
            st.markdown(
                '<div class="section-title">'
                '⚠️ Issues Detected</div>',
                unsafe_allow_html=True,
            )
            if not result["issues"]:
                st.markdown("""
                <div style='background:rgba(0,255,65,0.05);
                  border:1px solid #00ff4130;
                  border-radius:10px;
                  padding:16px;text-align:center'>
                  <span style='font-size:1.5rem'>✅</span>
                  <div style='color:#00ff41;
                    font-weight:700;margin-top:6px'>
                    No major issues detected!
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for issue in result["issues"]:
                    sev   = issue.get(
                        "severity","MEDIUM"
                    )
                    css   = {
                        "CRITICAL":"issue-critical",
                        "HIGH":    "issue-high",
                        "MEDIUM":  "issue-medium",
                        "LOW":     "issue-low",
                    }.get(sev,"issue-medium")
                    sev_color = {
                        "CRITICAL":"#ff0040",
                        "HIGH":    "#ff6b00",
                        "MEDIUM":  "#ffff00",
                        "LOW":     "#00ff41",
                    }.get(sev,"#ffff00")
                    st.markdown(f"""
                    <div class='{css}'>
                      <div style='display:flex;
                        justify-content:space-between'>
                        <span style='color:#e0e0e0;
                          font-weight:600;
                          font-size:0.85rem'>
                          {issue['icon']}
                          {issue['desc']}
                        </span>
                        <span style='color:{sev_color};
                          font-size:0.7rem;
                          font-weight:700;
                          font-family:Share Tech Mono,
                          monospace'>
                          -{issue['penalty']}pts
                        </span>
                      </div>
                      <span style='color:{sev_color};
                        font-size:0.68rem;
                        font-family:Share Tech Mono,
                        monospace'>
                        {sev}
                      </span>
                    </div>
                    """, unsafe_allow_html=True)

            # Breach result
            st.markdown(
                '<div class="section-title">'
                '💥 Breach Check</div>',
                unsafe_allow_html=True,
            )
            b_css = (
                "background:rgba(255,0,64,0.08);"
                "border:1px solid #ff004040"
                if breach["found"]
                else
                "background:rgba(0,255,65,0.05);"
                "border:1px solid #00ff4130"
            )
            st.markdown(f"""
            <div style='{b_css};border-radius:10px;
              padding:14px;margin:4px 0'>
              <div style='display:flex;
                justify-content:space-between;
                align-items:center'>
                <span style='color:#e0e0e0;
                  font-weight:700'>
                  {breach['icon']} {breach['message']}
                </span>
                <span class='badge {"badge-red"
                  if breach["found"]
                  else "badge-green"}'>
                  {"BREACHED" if breach["found"]
                   else "CLEAN"}
                </span>
              </div>
              {f"<div style='color:#ff6b00;font-size:0.78rem;margin-top:6px;font-family:Share Tech Mono,monospace'>Found in {breach['count']:,} breach records</div>" if breach['found'] and breach.get('count',0) > 0 else ""}
              <div style='color:#4a5568;font-size:0.72rem;
                margin-top:6px;
                font-family:Share Tech Mono,monospace'>
                ⚠️ Simulation — local check only.
                Not using real breach API.
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Entropy breakdown
            st.markdown(
                '<div class="section-title">'
                '🎲 Entropy Analysis</div>',
                unsafe_allow_html=True,
            )
            ent = result["eff_entropy"]
            raw = result["entropy"]
            e_color = result["entropy_color"]
            e_label = result["entropy_label"]

            for label_e, val, color_e in [
                ("Raw Entropy",
                 f"{raw:.2f} bits", "#00d4ff"),
                ("Effective Entropy",
                 f"{ent:.2f} bits", e_color),
                ("Character Pool",
                 str(result["charset"].get(
                     "pool_size",0
                 )), "#bf00ff"),
                ("Entropy Level",
                 e_label, e_color),
                ("Crack Time (GPU)",
                 result["crack_time"],
                 "#00ff41"),
            ]:
                st.markdown(f"""
                <div style='display:flex;
                  justify-content:space-between;
                  padding:9px 12px;
                  background:#050510;
                  border:1px solid #00ff4120;
                  border-radius:8px;margin:3px 0'>
                  <span style='color:#4a5568;
                    font-size:0.82rem;
                    font-family:Share Tech Mono,
                    monospace'>{label_e}</span>
                  <span style='color:{color_e};
                    font-weight:700;font-size:0.82rem;
                    font-family:Share Tech Mono,
                    monospace'>{val}</span>
                </div>
                """, unsafe_allow_html=True)

            # Character checklist
            st.markdown(
                '<div class="section-title">'
                '🔡 Character Checklist</div>',
                unsafe_allow_html=True,
            )
            charset = result["charset"]
            for label_c, key, pts in [
                ("Lowercase (a-z)", "lowercase", 6),
                ("Uppercase (A-Z)", "uppercase", 6),
                ("Digits (0-9)",    "digits",    6),
                ("Special (!@#$)",  "special",   9),
                ("Spaces",          "space",     3),
            ]:
                has  = charset.get(key, False)
                icon_c = "✅" if has else "❌"
                c_col= "#00ff41" if has else "#ff0040"
                st.markdown(f"""
                <div style='display:flex;
                  justify-content:space-between;
                  padding:7px 12px;margin:2px 0;
                  background:#050510;
                  border:1px solid #00ff4110;
                  border-radius:6px'>
                  <span style='color:#e0e0e0;
                    font-size:0.82rem'>
                    {icon_c} {label_c}
                  </span>
                  <span style='color:{c_col};
                    font-size:0.75rem;
                    font-family:Share Tech Mono,
                    monospace;font-weight:700'>
                    {"+" if has else "0"}{pts} pts
                  </span>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2: Suggestions ────────────────────
    with tab2:
        st.markdown(
            '<div class="section-title">'
            '💡 Security Recommendations</div>',
            unsafe_allow_html=True,
        )
        for s in suggest:
            pri   = s["priority"]
            css   = {
                "CRITICAL": "sug-critical",
                "HIGH":     "sug-high",
                "MEDIUM":   "sug-medium",
                "TIP":      "sug-tip",
            }.get(pri, "sug-tip")
            badge_css = {
                "CRITICAL": "badge-red",
                "HIGH":     "badge-yellow",
                "MEDIUM":   "badge-cyan",
                "TIP":      "badge-green",
            }.get(pri, "badge-green")
            st.markdown(f"""
            <div class='{css}'>
              <div style='display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:6px'>
                <span style='color:#e0e0e0;
                  font-weight:700;font-size:0.88rem'>
                  {s['icon']} {s['title']}
                </span>
                <span class='badge {badge_css}'>
                  {pri}
                </span>
              </div>
              <div style='color:#a0aec0;
                font-size:0.82rem;line-height:1.6'>
                {s['detail']}
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Passphrase example
        st.markdown("---")
        st.markdown(
            '<div class="section-title">'
            '💬 Passphrase Alternative</div>',
            unsafe_allow_html=True,
        )
        eg = engines["suggester"]\
            .get_passphrase_example()
        st.markdown(f"""
        <div class='pass-display'
          style='text-align:center;
          font-size:1.2rem;letter-spacing:3px'>
          {eg}
        </div>
        <div style='color:#4a5568;
          font-size:0.75rem;margin-top:8px;
          text-align:center;
          font-family:Share Tech Mono,monospace'>
          4 random unrelated words •
          HIGH entropy • Easy to remember
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "🔄 New Passphrase Example"
        ):
            st.rerun()

    # ── TAB 3: Charts ─────────────────────────
    with tab3:

        PT = dict(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,5,16,0.95)",
            font=dict(
                family="Share Tech Mono, monospace",
                color="#00ff41", size=11,
            ),
        )

        col1, col2 = st.columns(2)

        with col1:
            # Score gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title=dict(
                    text="Strength Score",
                    font=dict(
                        color="#4a5568", size=13
                    ),
                ),
                number=dict(
                    font=dict(
                        size=28, color=color,
                        family="Orbitron"
                    ),
                ),
                gauge=dict(
                    axis=dict(
                        range=[0,100],
                        tickcolor="#00ff4140",
                        tickfont=dict(
                            color="#4a5568"
                        ),
                    ),
                    bar=dict(
                        color=color, thickness=0.28
                    ),
                    bgcolor="#050510",
                    bordercolor="#00ff4120",
                    steps=[
                        dict(range=[0,20],
                             color="rgba(255,0,64,0.1)"),
                        dict(range=[20,40],
                             color="rgba(255,107,0,0.1)"),
                        dict(range=[40,60],
                             color="rgba(255,255,0,0.08)"),
                        dict(range=[60,80],
                             color="rgba(0,255,136,0.08)"),
                        dict(range=[80,100],
                             color="rgba(0,212,255,0.1)"),
                    ],
                    threshold=dict(
                        line=dict(
                            color="#00ff41", width=2
                        ),
                        thickness=0.75, value=60,
                    ),
                ),
            ))
            fig.update_layout(
                **PT, height=240,
                margin=dict(t=40,b=10,l=20,r=20),
            )
            st.plotly_chart(
                fig, use_container_width=True
            )

            # Char composition bar
            ca     = result["char_analysis"]
            labels = [
                "Lowercase","Uppercase",
                "Digits","Special","Spaces",
            ]
            values = [
                ca.get("lowercase",0),
                ca.get("uppercase",0),
                ca.get("digits",0),
                ca.get("special",0),
                ca.get("spaces",0),
            ]
            colors_c = [
                "#00ff41","#00d4ff",
                "#ffff00","#ff0080","#bf00ff",
            ]
            fig2 = go.Figure(go.Bar(
                x=labels, y=values,
                marker=dict(
                    color=colors_c,
                    line=dict(
                        color="#050510", width=1
                    ),
                ),
                text=values,
                textposition="outside",
                textfont=dict(
                    color="#e0e0e0", size=11
                ),
            ))
            fig2.update_layout(
                **PT,
                title=dict(
                    text="Character Composition",
                    font=dict(
                        color="#00ff41", size=13
                    ),
                ),
                height=260,
                xaxis=dict(
                    gridcolor="#00ff4110",
                    color="#4a5568",
                ),
                yaxis=dict(
                    gridcolor="#00ff4110",
                    color="#4a5568",
                    title="Count",
                ),
                margin=dict(t=50,b=20,l=20,r=20),
            )
            st.plotly_chart(
                fig2, use_container_width=True
            )

        with col2:
            # Score components radar
            cats   = [
                "Length","Diversity","Entropy",
                "Pattern Resist","Uniqueness",
            ]
            length = result["password_length"]
            l_score= min(
                100, result["base_score"]*2.5
            )
            d_score= result["diversity_score"]*3.33
            e_score= min(
                100, result["eff_entropy"]*0.78
            )
            p_score= max(
                0, 100 - result["penalty"]*1.5
            )
            u_score= result["char_analysis"].get(
                "unique_pct", 50
            )

            vals = [
                l_score, d_score, e_score,
                p_score, u_score,
            ]

            fig3 = go.Figure()
            fig3.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=cats + [cats[0]],
                fill="toself",
                fillcolor="rgba(0,255,65,0.1)",
                line=dict(
                    color="#00ff41", width=2
                ),
                name="Score",
            ))
            fig3.update_layout(
                **PT,
                polar=dict(
                    bgcolor="#050510",
                    radialaxis=dict(
                        range=[0,100],
                        gridcolor="#00ff4120",
                        color="#4a5568",
                    ),
                    angularaxis=dict(
                        gridcolor="#00ff4120",
                        color="#00ff41",
                    ),
                ),
                title=dict(
                    text="Security Radar",
                    font=dict(
                        color="#00ff41", size=13
                    ),
                ),
                height=320,
                showlegend=False,
                margin=dict(t=50,b=20,l=20,r=20),
            )
            st.plotly_chart(
                fig3, use_container_width=True
            )

            # Entropy vs length scatter
            lengths  = list(range(6, 25))
            entropies= [
                engines["entropy"].calculate_entropy(
                    "A" * l + "1!a"
                ) for l in lengths
            ]
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(
                x=lengths, y=entropies,
                mode="lines+markers",
                line=dict(
                    color="#00d4ff", width=2
                ),
                marker=dict(
                    color="#00d4ff", size=6
                ),
                name="Entropy",
                fill="tozeroy",
                fillcolor="rgba(0,212,255,0.05)",
            ))
            # Mark current password
            cur_len = result["password_length"]
            cur_ent = result["entropy"]
            fig4.add_trace(go.Scatter(
                x=[cur_len], y=[cur_ent],
                mode="markers",
                marker=dict(
                    color="#ff0080",
                    size=14,
                    symbol="star",
                    line=dict(
                        color="#ff0080", width=2
                    ),
                ),
                name="Your Password",
            ))
            fig4.update_layout(
                **PT,
                title=dict(
                    text="Entropy vs Length",
                    font=dict(
                        color="#00ff41", size=13
                    ),
                ),
                height=250,
                xaxis=dict(
                    title="Length",
                    gridcolor="#00ff4110",
                    color="#4a5568",
                ),
                yaxis=dict(
                    title="Entropy (bits)",
                    gridcolor="#00ff4110",
                    color="#4a5568",
                ),
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#4a5568"),
                ),
                margin=dict(t=50,b=40,l=40,r=20),
            )
            st.plotly_chart(
                fig4, use_container_width=True
            )

    # ── TAB 4: Characters ─────────────────────
    with tab4:
        ca = result["char_analysis"]
        st.markdown(
            '<div class="section-title">'
            '🔡 Detailed Character Analysis</div>',
            unsafe_allow_html=True,
        )

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("🔤 Total",    ca["total"])
        c2.metric("✨ Unique",   ca["unique"])
        c3.metric("📊 Unique %", f"{ca['unique_pct']}%")
        c4.metric("💊 Pool Size",
                  result["charset"]["pool_size"])

        st.markdown("---")

        for label_c, val, color_c, desc in [
            ("Lowercase Letters", ca["lowercase"],
             "#00ff41",
             "a-z — forms base of most passwords"),
            ("Uppercase Letters", ca["uppercase"],
             "#00d4ff",
             "A-Z — doubles alphabetic pool"),
            ("Digits",           ca["digits"],
             "#ffff00",
             "0-9 — adds numeric variety"),
            ("Special Chars",    ca["special"],
             "#ff0080",
             "!@#$% — highest entropy per char"),
            ("Spaces",           ca["spaces"],
             "#bf00ff",
             "Spaces allowed — great for passphrases"),
        ]:
            total  = ca["total"] or 1
            pct    = round(val/total*100, 1)
            st.markdown(f"""
            <div style='background:#050510;
              border:1px solid #00ff4115;
              border-radius:10px;
              padding:12px 16px;margin:5px 0'>
              <div style='display:flex;
                justify-content:space-between;
                margin-bottom:6px'>
                <span style='color:#e0e0e0;
                  font-weight:600;
                  font-size:0.85rem'>{label_c}</span>
                <span style='color:{color_c};
                  font-weight:900;
                  font-family:Orbitron,monospace'>
                  {val}
                  <span style='color:#4a5568;
                    font-size:0.75rem'>
                    ({pct}%)
                  </span>
                </span>
              </div>
              <div style='background:#0a0a1a;
                border-radius:3px;height:6px;
                margin-bottom:6px'>
                <div style='width:{min(pct,100)}%;
                  height:6px;border-radius:3px;
                  background:{color_c};
                  opacity:0.8'></div>
              </div>
              <div style='color:#4a5568;
                font-size:0.72rem;
                font-family:Share Tech Mono,monospace'>
                {desc}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 5: Hash Info ─────────────────────
    with tab5:
        api_info = engines["breach"]\
            .simulate_api_call(password)

        st.markdown(
            '<div class="section-title">'
            '🔑 Cryptographic Hash Preview</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"""
        <div style='background:#050510;
          border:1px solid #00ff4130;
          border-radius:10px;padding:16px'>
          <div style='color:#4a5568;
            font-size:0.72rem;margin-bottom:8px;
            font-family:Share Tech Mono,monospace'>
            SHA-256 HASH (PARTIAL)
          </div>
          <div class='pass-display'
            style='letter-spacing:2px'>
            {hash_prev}
          </div>
          <div style='color:#4a5568;
            font-size:0.72rem;margin-top:8px;
            font-family:Share Tech Mono,monospace'>
            ⚠️ Hash computed locally.
            Full hash never displayed for safety.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">'
            '🌐 HIBP k-Anonymity Simulation</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"""
        <div style='background:#050510;
          border:1px solid #00d4ff30;
          border-radius:10px;padding:16px'>
          <div style='color:#4a5568;
            font-size:0.72rem;margin-bottom:10px;
            font-family:Share Tech Mono,monospace'>
            HOW REAL BREACH CHECK WORKS
          </div>
          <div style='font-family:Share Tech Mono,
            monospace;font-size:0.82rem'>
            <div style='color:#4a5568;
              margin-bottom:6px'>
              STEP 1 — Hash password locally:
            </div>
            <div style='color:#00ff41;
              margin-bottom:10px'>
              SHA1 = {api_info['full_hash']}
            </div>
            <div style='color:#4a5568;
              margin-bottom:6px'>
              STEP 2 — Send ONLY first 5 chars:
            </div>
            <div style='color:#ffff00;
              margin-bottom:10px'>
              API Request → "{api_info['sha1_prefix']}"
            </div>
            <div style='color:#4a5568;
              margin-bottom:6px'>
              STEP 3 — Check response locally:
            </div>
            <div style='color:#00d4ff'>
              Match suffix "{api_info['sha1_suffix']}"?
              → Password never transmitted! 🔐
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: GENERATOR
# ════════════════════════════════════════════
elif page == "generator":
    st.markdown("""
    <h1 class='cyber-title'
      style='color:#00d4ff;font-size:1.8rem'>
      🔑 SECURE PASSWORD GENERATOR
    </h1>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "🔐 Password",
        "💬 Passphrase",
        "📦 Batch Generate",
    ])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            length     = st.slider(
                "Length", 8, 64, 16
            )
            use_upper  = st.checkbox(
                "Uppercase (A-Z)", True
            )
            use_lower  = st.checkbox(
                "Lowercase (a-z)", True
            )
            use_digits = st.checkbox(
                "Digits (0-9)", True
            )
            use_special= st.checkbox(
                "Special (!@#$)", True
            )
            no_ambig   = st.checkbox(
                "Exclude ambiguous (0,O,l,1)",
                False,
            )

        with col2:
            if st.button(
                "⚡ GENERATE PASSWORD",
                use_container_width=True,
            ):
                pwd = engines["generator"]\
                    .generate_password(
                        length, use_upper,
                        use_lower, use_digits,
                        use_special, no_ambig,
                    )
                st.session_state[
                    "gen_password"
                ] = pwd
                # Analyze it
                r = engines["analyzer"]\
                    .analyze(pwd)
                st.session_state[
                    "gen_result"
                ] = r

            if "gen_password" in st.session_state:
                pwd = st.session_state[
                    "gen_password"
                ]
                r   = st.session_state.get(
                    "gen_result", {}
                )
                c   = r.get("color","#00ff41")
                st.markdown(f"""
                <div class='pass-display'
                  style='text-align:center;
                  font-size:1rem;letter-spacing:2px;
                  border-color:{c}40'>
                  {pwd}
                </div>
                <div style='display:flex;
                  justify-content:space-between;
                  margin-top:10px;font-size:0.8rem;
                  font-family:Share Tech Mono,monospace'>
                  <span style='color:{c}'>
                    ⭐ {r.get("label","")}: {r.get("score",0):.0f}/100
                  </span>
                  <span style='color:#4a5568'>
                    {r.get("eff_entropy",0):.1f} bits entropy
                  </span>
                </div>
                """, unsafe_allow_html=True)
                st.code(pwd, language=None)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            n_words   = st.slider(
                "Number of words", 3, 6, 4
            )
            separator = st.selectbox(
                "Separator",
                ["-","_","!","@","#",".",
                 " ","~"],
            )
            capitalize= st.checkbox(
                "Capitalize words", True
            )
            add_number= st.checkbox(
                "Add random number", True
            )

        with col2:
            if st.button(
                "💬 GENERATE PASSPHRASE",
                use_container_width=True,
            ):
                pp = engines["generator"]\
                    .generate_passphrase(
                        n_words, separator,
                        capitalize, add_number,
                    )
                st.session_state["gen_pp"] = pp

            if "gen_pp" in st.session_state:
                pp = st.session_state["gen_pp"]
                r  = engines["analyzer"]\
                    .analyze(pp)
                st.markdown(f"""
                <div class='pass-display'
                  style='text-align:center;
                  font-size:0.95rem;
                  letter-spacing:2px'>
                  {pp}
                </div>
                <div style='color:#00ff41;
                  margin-top:8px;font-size:0.8rem;
                  font-family:Share Tech Mono,
                  monospace;text-align:center'>
                  {r.get("label","")} •
                  {r.get("eff_entropy",0):.1f} bits •
                  Crack: {r.get("crack_time","")}
                </div>
                """, unsafe_allow_html=True)
                st.code(pp, language=None)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            batch_len = st.slider(
                "Password Length",
                8, 32, 16,
            )
            batch_n   = st.slider(
                "How many passwords",
                3, 10, 5,
            )
        with col2:
            if st.button(
                "📦 GENERATE BATCH",
                use_container_width=True,
            ):
                batch = engines["generator"]\
                    .generate_batch(
                        batch_n, batch_len
                    )
                for i, p in enumerate(batch, 1):
                    r  = engines["analyzer"]\
                        .analyze(p)
                    c  = r.get("color","#00ff41")
                    st.markdown(f"""
                    <div style='display:flex;
                      justify-content:space-between;
                      padding:8px 12px;
                      background:#050510;
                      border:1px solid {c}30;
                      border-radius:8px;margin:3px 0;
                      font-family:Share Tech Mono,
                      monospace;font-size:0.82rem'>
                      <span style='color:#4a5568'>
                        #{i:02d}
                      </span>
                      <span style='color:{c}'>
                        {p}
                      </span>
                      <span style='color:#4a5568'>
                        {r.get("score",0):.0f}/100
                      </span>
                    </div>
                    """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: BREACH SIM
# ════════════════════════════════════════════
elif page == "breach":
    st.markdown("""
    <h1 class='cyber-title'
      style='color:#ff0040;font-size:1.8rem'>
      💥 BREACH DATABASE SIMULATOR
    </h1>
    <p style='color:#4a5568;
      font-family:Share Tech Mono,monospace;
      font-size:0.75rem;letter-spacing:1px'>
      EDUCATIONAL SIMULATION — LOCAL ONLY —
      NO DATA TRANSMITTED
    </p>
    """, unsafe_allow_html=True)

    check_pw = st.text_input(
        "🔍 Enter password to check",
        type="password",
        placeholder="Check against breach database...",
    )

    if check_pw:
        result  = engines["breach"]\
            .check_password(check_pw)
        api_sim = engines["breach"]\
            .simulate_api_call(check_pw)
        hash_p  = engines["breach"]\
            .get_hash_preview(check_pw)

        if result["found"]:
            st.error(
                f"🚨 {result['message']}"
            )
        else:
            st.success(
                f"✅ {result['message']}"
            )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background:#050510;
              border:1px solid {result['color']}40;
              border-radius:12px;padding:16px'>
              <div style='font-size:2rem;
                text-align:center'>
                {result['icon']}
              </div>
              <div style='color:{result['color']};
                font-family:Orbitron,monospace;
                font-size:1.2rem;font-weight:900;
                text-align:center;margin:8px 0'>
                {result['type']}
              </div>
              <div style='color:#e0e0e0;
                text-align:center;
                font-size:0.85rem'>
                {result['message']}
              </div>
              {"<div style='color:#ff6b00;text-align:center;margin-top:8px;font-family:Share Tech Mono,monospace;font-size:0.8rem'>Found in " + f"{result['count']:,}" + " records</div>" if result.get('count',0) > 0 else ""}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background:#050510;
              border:1px solid #00d4ff30;
              border-radius:12px;padding:16px;
              font-family:Share Tech Mono,monospace;
              font-size:0.8rem'>
              <div style='color:#00d4ff;
                font-weight:700;margin-bottom:10px'>
                k-ANONYMITY PROCESS
              </div>
              <div style='color:#4a5568;
                margin-bottom:4px'>Step 1: Hash locally</div>
              <div style='color:#00ff41;
                margin-bottom:8px'>
                SHA-256: {hash_p}
              </div>
              <div style='color:#4a5568;
                margin-bottom:4px'>Step 2: Send prefix only</div>
              <div style='color:#ffff00;
                margin-bottom:8px'>
                API → "{api_sim['sha1_prefix']}"
              </div>
              <div style='color:#4a5568;
                margin-bottom:4px'>Step 3: Check locally</div>
              <div style='color:#00d4ff'>
                Password NEVER transmitted! 🔐
              </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: EDUCATION
# ════════════════════════════════════════════
elif page == "education":
    st.markdown("""
    <h1 class='cyber-title'
      style='color:#bf00ff;font-size:1.8rem'>
      📚 SECURITY EDUCATION CENTER
    </h1>
    """, unsafe_allow_html=True)

    for key, content in EDUCATION.items():
        with st.expander(
            f"{content['icon']} "
            f"{content['title']}"
        ):
            st.markdown(content["content"])

# ════════════════════════════════════════════
# PAGE: HISTORY
# ════════════════════════════════════════════
elif page == "history":
    st.markdown("""
    <h1 class='cyber-title'
      style='color:#ffff00;font-size:1.8rem'>
      📊 ANALYSIS HISTORY
    </h1>
    <p style='color:#4a5568;
      font-family:Share Tech Mono,monospace;
      font-size:0.72rem'>
      SESSION ONLY — NO PASSWORDS STORED —
      SCORE METADATA ONLY
    </p>
    """, unsafe_allow_html=True)

    history = st.session_state.history
    if not history:
        st.info(
            "No analysis history yet. "
            "Analyze passwords to see history!"
        )
    else:
        df = pd.DataFrame(history)
        c1,c2,c3 = st.columns(3)
        c1.metric("🔍 Analyzed",   len(history))
        c2.metric("📊 Avg Score",
                  f"{df['score'].mean():.1f}")
        c3.metric("🎲 Avg Entropy",
                  f"{df['entropy'].mean():.1f}b")

        # Score over time chart
        PT = dict(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,5,16,0.95)",
            font=dict(
                color="#00ff41",
                family="Share Tech Mono",
                size=11,
            ),
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["score"],
            mode="lines+markers",
            line=dict(color="#00ff41", width=2),
            marker=dict(
                color=df["score"].apply(
                    lambda s: (
                        "#ff0040" if s < 40
                        else "#ffff00" if s < 60
                        else "#00ff41"
                    )
                ),
                size=10,
            ),
            name="Score",
            fill="tozeroy",
            fillcolor="rgba(0,255,65,0.05)",
        ))
        fig.update_layout(
            **PT,
            title=dict(
                text="Score History (Session)",
                font=dict(
                    color="#00ff41", size=13
                ),
            ),
            height=280,
            xaxis=dict(
                color="#4a5568",
                gridcolor="#00ff4110",
            ),
            yaxis=dict(
                range=[0,105],
                gridcolor="#00ff4110",
                color="#4a5568",
                title="Score",
            ),
            margin=dict(t=50,b=30,l=40,r=20),
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

        st.markdown(
            '<div class="section-title">'
            'Session Log</div>',
            unsafe_allow_html=True,
        )
        for h in reversed(history):
            c = (
                "#ff0040" if h["score"] < 40
                else "#ffff00" if h["score"] < 60
                else "#00ff41"
            )
            st.markdown(f"""
            <div style='display:flex;
              justify-content:space-between;
              padding:8px 14px;
              background:#050510;
              border:1px solid {c}20;
              border-radius:8px;margin:3px 0;
              font-family:Share Tech Mono,monospace;
              font-size:0.78rem'>
              <span style='color:#4a5568'>
                {h['time']}
              </span>
              <span style='color:#e0e0e0'>
                Len:{h['length']}
              </span>
              <span style='color:{c};
                font-weight:700'>
                {h['score']:.0f}/100
              </span>
              <span class='badge {"badge-green"
                if h["score"]>=60
                else "badge-yellow"
                if h["score"]>=40
                else "badge-red"}'>
                {h['label']}
              </span>
              <span style='color:#4a5568'>
                {h['entropy']:.1f}b
              </span>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: INTERVIEW
# ════════════════════════════════════════════
elif page == "interview":
    st.markdown("""
    <h1 class='cyber-title'
      style='color:#00d4ff;font-size:1.8rem'>
      🎤 INTERVIEW PREP
    </h1>
    <p style='color:#4a5568;
      font-family:Share Tech Mono,monospace;
      font-size:0.72rem'>
      CYBERSECURITY INTERVIEW Q&A
    </p>
    """, unsafe_allow_html=True)

    for i, qa in enumerate(INTERVIEW_QA, 1):
        with st.expander(
            f"Q{i}. {qa['q']}"
        ):
            st.markdown(f"""
            <div style='background:#050510;
              border-left:3px solid #00ff41;
              border-radius:0 10px 10px 0;
              padding:14px'>
              <div style='color:#4a5568;
                font-size:0.7rem;
                font-family:Share Tech Mono,
                monospace;margin-bottom:6px'>
                ✅ ANSWER
              </div>
              <div style='color:#e0e0e0;
                font-size:0.88rem;
                line-height:1.6'>
                {qa['a']}
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────
st.markdown(f"""
<div style='text-align:center;
  color:#4a5568;font-size:0.68rem;
  font-family:Share Tech Mono,monospace;
  letter-spacing:1px;padding:10px 0'>
  🔐 CYBERPASS v2.0 — DEFENSIVE TOOL ONLY —
  NO DATA STORED OR TRANSMITTED —
  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)