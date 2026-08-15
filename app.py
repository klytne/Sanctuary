"""
app.py — Main entry point / Dashboard
This is the file you run with: streamlit run app.py

File structure this expects:
CS-Girlies-Hackathon/
├── app.py                  <- this file
├── pages/
│   ├── 1_Profile.py
│   ├── 2_Journal.py
│   ├── 3_Insights.py
│   ├── 4_Goals.py
│   └── 5_Settings.py
├── requirements.txt
├── .gitignore
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Sanctuary - Gratitude & Mindful Living",
    page_icon="🌿",
    layout="wide",
)

# ---------- CONFIG ----------
ENTRIES_FILE = "journal_entries.json"
GOALS_FILE = "goals_data.json"
SETTINGS_FILE = "user_settings.json"


# ---------- SESSION STATE DEFAULTS ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None


# ---------- HELPERS ----------
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def compute_streak(entries):
    if not entries:
        return 0
    days = sorted({datetime.fromisoformat(e["timestamp"]).date() for e in entries})
    longest = current = 1
    for i in range(1, len(days)):
        if (days[i] - days[i - 1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    # only counts as an *active* streak if it includes today or yesterday
    today = datetime.now().date()
    if days[-1] not in (today, today - timedelta(days=1)):
        return 0
    return current


# ---------- STYLING ----------
st.markdown("""
<style>
    .stApp { background-color: #fbf9f4; }
    .hero-card {
        background: linear-gradient(135deg, rgba(71,101,80,0.08), rgba(125,157,133,0.08));
        border: 1px solid rgba(71,101,80,0.15);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 28px;
    }
    .quick-card {
        background: #ffffff; border: 1px solid #e4e2dd; border-radius: 16px;
        padding: 22px; text-align: center; height: 100%;
    }
    .quick-card h3 { margin-bottom: 4px; }
    .stat-pill {
        display: inline-block; background: #f0eee9; border-radius: 999px;
        padding: 6px 16px; margin-right: 8px; font-size: 14px; color: #424843;
    }
</style>
""", unsafe_allow_html=True)


# ---------- NOT LOGGED IN ----------
if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero-card">
        <h1 style="color:#476550;">🌿 Welcome to Sanctuary</h1>
        <p style="font-size:18px;color:#424843;">
            A gratitude journal built to support your wellness — reflect daily,
            track your hobbies and goals, and see how they connect to how you feel.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info("Please log in or create an account to get started.")
    st.page_link("pages/1_Profile.py", label="Go to Profile / Login", icon="👤")
    st.stop()


# ---------- LOGGED IN: DASHBOARD ----------
username = st.session_state.username

entries = load_json(ENTRIES_FILE).get(username, [])
goals = load_json(GOALS_FILE).get(username, [])
settings = load_json(SETTINGS_FILE).get(username, {})

streak = compute_streak(entries)
entries_this_week = len({
    datetime.fromisoformat(e["timestamp"]).date()
    for e in entries
    if datetime.fromisoformat(e["timestamp"]) >= datetime.now() - timedelta(days=7)
})
active_goals = [g for g in goals if not g.get("completed")]

st.markdown(f"""
<div class="hero-card">
    <h1 style="color:#476550;">🌿 Welcome back, {username}</h1>
    <p style="font-size:16px;color:#424843;">Here's a quick look at your week.</p>
    <div style="margin-top:16px;">
        <span class="stat-pill">🔥 {streak}-day streak</span>
        <span class="stat-pill">📝 {entries_this_week} entries this week</span>
        <span class="stat-pill">🎯 {len(active_goals)} active goals</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("Where would you like to go?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="quick-card">', unsafe_allow_html=True)
    st.markdown("### 📝")
    st.markdown("**Journal**")
    st.caption("Write today's reflection")
    st.page_link("pages/2_Journal.py", label="Open Journal")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="quick-card">', unsafe_allow_html=True)
    st.markdown("### 📊")
    st.markdown("**Insights**")
    st.caption("See your weekly patterns")
    st.page_link("pages/3_Insights.py", label="Open Insights")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="quick-card">', unsafe_allow_html=True)
    st.markdown("### 🎯")
    st.markdown("**Goals**")
    st.caption("Track hobbies & life goals")
    st.page_link("pages/4_Goals.py", label="Open Goals")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="quick-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️")
    st.markdown("**Settings**")
    st.caption("Reminders, streaks & privacy")
    st.page_link("pages/5_Settings.py", label="Open Settings")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

if entries_this_week == 0:
    st.info("You haven't journaled yet this week — even a short reflection counts. 🌱")
else:
    st.success(f"Nice work — you've journaled {entries_this_week} day(s) this week. Keep it up!")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(f"### 🌿 Sanctuary")
    st.caption(f"Logged in as **{username}**")
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()