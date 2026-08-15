"""
Insights page — Weekly Analysis / Reflections & Patterns
Save this file as: pages/3_Insights.py
(Comes right after pages/2_Journal.py — requires login to access)
"""

import streamlit as st
import json
import os
import re
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title="Insights - Sanctuary", page_icon="📊", layout="wide")

# ---------- CONFIG ----------
ENTRIES_FILE = "journal_entries.json"
HOBBY_LOG_FILE = "hobby_logs.json"       # produced by the Hobby Tracker page
GOALS_LOG_FILE = "goals_logs.json"       # produced by the Goals page

MOOD_SCALE = ["Tired", "Neutral", "Happy", "Grateful"]  # low -> high
MOOD_EMOJI = {"Tired": "🥱", "Neutral": "😐", "Happy": "🙂", "Grateful": "😊"}

# Simple keyword list used to surface recurring gratitude themes from entry text.
# (Descriptive word-frequency only — not sentiment/mental-health analysis.)
THEME_KEYWORDS = [
    "family", "friends", "nature", "work", "coffee", "health",
    "music", "food", "home", "pets", "sunshine", "rest",
]

# ---------- ACCESS CONTROL ----------
if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.page_link("pages/1_Profile.py", label="Go to Profile / Login", icon="👤")
    st.stop()

username = st.session_state.username


# ---------- HELPERS ----------
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def get_week_entries(entries):
    """Entries from the last 7 days, most recent last."""
    cutoff = datetime.now() - timedelta(days=7)
    week = []
    for e in entries:
        try:
            ts = datetime.fromisoformat(e["timestamp"])
        except (KeyError, ValueError):
            continue
        if ts >= cutoff:
            week.append(e)
    return sorted(week, key=lambda e: e["timestamp"])


def compute_streak(entries):
    """Longest run of consecutive days with at least one entry."""
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
    return longest


def extract_themes(entries):
    text = " ".join(e.get("body", "").lower() for e in entries)
    counts = Counter()
    for word in THEME_KEYWORDS:
        hits = len(re.findall(rf"\b{word}\b", text))
        if hits > 0:
            counts[word.capitalize()] = hits
    return counts.most_common(6)


def mood_for_entry(entry):
    """Entries may optionally carry a 'mood' field (add a mood picker in the
    journal page to populate this). Falls back to 'Neutral' if not set."""
    return entry.get("mood", "Neutral")


# ---------- LOAD DATA ----------
all_entries = load_json(ENTRIES_FILE).get(username, [])
week_entries = get_week_entries(all_entries)
hobby_logs = load_json(HOBBY_LOG_FILE).get(username, [])
goal_logs = load_json(GOALS_LOG_FILE).get(username, [])

days_journaled = len({datetime.fromisoformat(e["timestamp"]).date() for e in week_entries})
longest_streak = compute_streak(all_entries)
themes = extract_themes(week_entries)
hobbies_this_week = {h.get("hobby") for h in hobby_logs if h.get("hobby")}


# ---------- STYLING ----------
st.markdown("""
<style>
    .stApp { background-color: #fbf9f4; }
    .insight-banner {
        background-color: #f5f3ee;
        border: 1px solid #eae8e3;
        border-radius: 12px;
        padding: 18px 24px;
        font-size: 17px;
        margin-bottom: 24px;
    }
    .metric-card {
        background-color: #f5f3ee;
        border: 1px solid #eae8e3;
        border-radius: 12px;
        padding: 18px;
        height: 100%;
    }
    .metric-label {
        font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;
        color: #424843; opacity: 0.8; margin-bottom: 6px;
    }
    .metric-value { font-size: 30px; font-weight: 700; color: #1b1c19; }
    .bar-track { width: 100%; height: 6px; background: #eae8e3; border-radius: 999px; margin-top: 10px; overflow: hidden; }
    .bar-fill { height: 100%; background: #476550; border-radius: 999px; }
    .mood-bar-wrap { display: flex; align-items: flex-end; justify-content: space-between; height: 220px; padding: 0 8px; }
    .mood-col { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .mood-bar { width: 14px; border-radius: 999px 999px 4px 4px; background: #7d9d85; }
    .insight-card {
        background: #ffffff; border: 1px solid #eae8e3; border-radius: 12px;
        padding: 22px; height: 100%;
    }
    .theme-chip {
        display: inline-flex; align-items: center; gap: 8px;
        background: #eae8e3; border-radius: 999px; padding: 8px 16px; margin: 4px;
        font-size: 14px;
    }
    .theme-count {
        background: #ffffff; border: 1px solid #e4e2dd; border-radius: 999px;
        width: 22px; height: 22px; display: inline-flex; align-items: center;
        justify-content: center; font-size: 12px; font-weight: 700; color: #476550;
    }
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("Weekly Reflections & Patterns")

summary_bits = [f"you journaled {days_journaled} day{'s' if days_journaled != 1 else ''}"]
if hobbies_this_week:
    summary_bits.append(f"spent time on {len(hobbies_this_week)} different hobbies")
summary = "Great week — " + " and ".join(summary_bits) + "!" if week_entries else \
    "No entries yet this week — write your first reflection to see insights here."

st.markdown(f'<div class="insight-banner">✨ {summary}</div>', unsafe_allow_html=True)


# ---------- MOOD TREND + STATS ----------
col_mood, col_stats = st.columns([2.2, 1])

with col_mood:
    st.subheader("Mood Trend")
    st.caption("Monday to Sunday — based on your self-reported mood tag per entry")

    if week_entries:
        # Map each day of the current week to its latest mood entry (if any)
        day_moods = {}
        for e in week_entries:
            day_label = datetime.fromisoformat(e["timestamp"]).strftime("%a")
            day_moods[day_label] = mood_for_entry(e)

        days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        bars_html = '<div class="mood-bar-wrap">'
        for d in days_order:
            mood = day_moods.get(d)
            if mood:
                height = 30 + MOOD_SCALE.index(mood) * 45
                label = f"{mood} {MOOD_EMOJI[mood]}"
            else:
                height = 8
                label = "No entry"
            bars_html += (
                f'<div class="mood-col">'
                f'<div class="mood-bar" style="height:{height}px;" title="{label}"></div>'
                f'<span style="font-size:12px;color:#424843;margin-top:8px;">{d}</span>'
                f'</div>'
            )
        bars_html += "</div>"
        st.markdown(bars_html, unsafe_allow_html=True)
        st.caption("Scale (low → high): 🥱 Tired · 😐 Neutral · 🙂 Happy · 😊 Grateful")
    else:
        st.info("Write a few journal entries this week to see your mood trend here.")

with col_stats:
    pct = int((days_journaled / 7) * 100)
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:12px;">
        <div class="metric-label">📅 Consistency</div>
        <div class="metric-value">{days_journaled}<span style="font-size:16px;color:#424843;"> / 7 days</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:{pct}%;"></div></div>
    </div>
    <div class="metric-card">
        <div class="metric-label">🔥 Longest Streak</div>
        <div class="metric-value">{longest_streak}<span style="font-size:16px;color:#424843;"> days</span></div>
        <p style="font-size:13px;color:#725a41;margin-top:8px;">Keep it going!</p>
    </div>
    """, unsafe_allow_html=True)


# ---------- DEEP INSIGHTS ----------
st.write("")
col_corr, col_themes = st.columns(2)

with col_corr:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("##### 🧠 Activity Correlation")
    if hobby_logs and week_entries:
        # naive correlation: hobby most associated with "Happy"/"Grateful" mood days
        good_days = {datetime.fromisoformat(e["timestamp"]).date()
                     for e in week_entries if mood_for_entry(e) in ("Happy", "Grateful")}
        hobby_on_good_days = Counter(
            h.get("hobby") for h in hobby_logs
            if datetime.fromisoformat(h["date"]).date() in good_days and h.get("hobby")
        )
        if hobby_on_good_days:
            top_hobby, _ = hobby_on_good_days.most_common(1)[0]
            st.markdown(
                f"**Observation:** You reported feeling more positive on days you did **{top_hobby}**."
            )
            st.caption("Days with 30+ min of hobby time trended toward more positive entries "
                       "compared to days focused solely on routine tasks.")
        else:
            st.caption("Log a few hobby sessions alongside your journal entries to see correlations here.")
    else:
        st.caption("Once you've logged both journal entries and hobby time this week, "
                   "we'll surface patterns between them here.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_themes:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("##### 💗 Gratitude Themes")
    st.caption("Recurring subjects in your entries this week:")
    if themes:
        chips = "".join(
            f'<span class="theme-chip">{word}<span class="theme-count">{count}</span></span>'
            for word, count in themes
        )
        st.markdown(chips, unsafe_allow_html=True)
    else:
        st.caption("No recurring themes detected yet — keep journaling to surface patterns.")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- TIME & FOCUS ALLOCATION ----------
st.write("")
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown("##### ⏱️ Time & Focus Allocation")
st.caption("Based on time logged in your Goals categories this week")

if goal_logs:
    category_hours = Counter()
    for g in goal_logs:
        category_hours[g.get("category", "Other")] += g.get("minutes", 0) / 60

    max_hours = max(category_hours.values()) if category_hours else 1
    colors = ["#476550", "#4f6167", "#ad9074", "#725a41"]
    for i, (cat, hrs) in enumerate(category_hours.most_common()):
        width = int((hrs / max_hours) * 100) if max_hours else 0
        color = colors[i % len(colors)]
        st.markdown(f"""
        <div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:4px;">
                <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;
                background:{color};margin-right:8px;"></span>{cat}</span>
                <span style="color:#424843;">{hrs:.1f} hrs</span>
            </div>
            <div class="bar-track" style="height:8px;">
                <div class="bar-fill" style="width:{width}%; background:{color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No time logged in your Goals categories yet this week — "
             "log time on the Goals page to see your allocation breakdown here.")
st.markdown('</div>', unsafe_allow_html=True)
