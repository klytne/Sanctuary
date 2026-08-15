import streamlit as st
import json
import os
import re
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title="Insights - Sanctuary", page_icon=":material/monitoring:", layout="wide")

# ---------- CONFIG ----------
DATA_STORAGE_DIR = "Data_Storage"
ENTRIES_FILE = os.path.join(DATA_STORAGE_DIR, "journal_entries", "journal_entries.json")
MOOD_EMOJI = {"Tired": "🥱", "Neutral": "😐", "Happy": "🙂", "Grateful": "😊"}

# --- Hobby/Goals log files (not wired up yet — commented out until those pages exist) ---
# HOBBY_LOG_FILE = "hobby_logs.json"       # produced by the Hobby Tracker page
# GOALS_LOG_FILE = "goals_logs.json"       # produced by the Goals page

MOOD_SCALE = ["Tired", "Neutral", "Happy", "Grateful"]  # low -> high

# Simple keyword list used to surface recurring gratitude themes from entry text.
# (Descriptive word-frequency only — not sentiment/mental-health analysis.)
THEME_KEYWORDS = [
    "family", "friends", "nature", "work", "coffee", "health",
    "music", "food", "home", "pets", "sunshine", "rest",
]

# ---------- ACCESS CONTROL ----------
if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.page_link("pages/1_Profile.py", label="Go to Profile / Login", icon=":material/person:")
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


def get_current_streak_days(entries):
    """Returns (current_streak_count, set_of_dates) for the streak that is
    still active right now (i.e. includes today or yesterday)."""
    if not entries:
        return 0, set()

    days = sorted({datetime.fromisoformat(e["timestamp"]).date() for e in entries})
    today = datetime.now().date()

    if days[-1] not in (today, today - timedelta(days=1)):
        return 0, set()  # streak broken — most recent entry isn't today/yesterday

    streak_days = [days[-1]]
    for d in reversed(days[:-1]):
        if (streak_days[-1] - d).days == 1:
            streak_days.append(d)
        else:
            break

    return len(streak_days), set(streak_days)


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

# --- Hobby/Goals log loading (commented out until those pages exist) ---
# hobby_logs = load_json(HOBBY_LOG_FILE).get(username, [])
# goal_logs = load_json(GOALS_LOG_FILE).get(username, [])

days_journaled = len({datetime.fromisoformat(e["timestamp"]).date() for e in week_entries})
longest_streak = compute_streak(all_entries)
themes = extract_themes(week_entries)
# hobbies_this_week = {h.get("hobby") for h in hobby_logs if h.get("hobby")}


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
        padding: 14px;
        height: 100%;
    }
    .metric-label {
        font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;
        color: #424843; opacity: 0.8; margin-bottom: 4px;
    }
    .metric-value { font-size: 26px; font-weight: 700; color: #1b1c19; }
    .bar-track { width: 100%; height: 6px; background: #eae8e3; border-radius: 999px; margin-top: 10px; overflow: hidden; }
    .bar-fill { height: 100%; background: #476550; border-radius: 999px; }

    /* ---- Mood Trend bar chart ---- */
    .mood-chart-wrap {
        background: #ffffff; border: 1px solid #eae8e3; border-radius: 12px;
        padding: 24px; height: 100%;
    }
    .mood-gridlines {
        position: relative;
        height: 220px;
        border-left: 1px solid #eae8e3;
        border-bottom: 1px solid #eae8e3;
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
        padding: 0 8px;
        margin-top: 8px;
    }
    .mood-gridlines::before, .mood-gridlines::after {
        content: "";
        position: absolute;
        left: 0; right: 0;
        border-top: 1px dashed #eae8e3;
    }
    .mood-gridlines::before { top: 25%; }
    .mood-gridlines::after { top: 75%; }
    .mood-col { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .mood-value-label {
        font-size: 11px; font-weight: 700; color: #476550; margin-bottom: 4px;
    }
    .mood-bar {
        width: 22px; border-radius: 6px 6px 3px 3px; background: #7d9d85;
        transition: height 0.2s ease;
    }
    .mood-bar.no-entry { background: #e4e2dd; }
    .mood-day-label { font-size: 12px; color: #424843; margin-top: 8px; font-weight: 600; }

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

    /* ---- Streak circles (smaller) ---- */
    .streak-circle {
        width: 20px; height: 20px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 9px; font-weight: 700;
    }
    .streak-day-label { font-size: 10px; color: #75746D; margin-top: 3px; }
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("Weekly Reflections & Patterns")

summary_bits = [f"you journaled {days_journaled} day{'s' if days_journaled != 1 else ''}"]
# if hobbies_this_week:
#     summary_bits.append(f"spent time on {len(hobbies_this_week)} different hobbies")
summary = "Great week — " + " and ".join(summary_bits) + "!" if week_entries else \
    "No entries yet this week — write your first reflection to see insights here."

st.markdown(
    f'<div class="insight-banner">{summary}</div>',
    unsafe_allow_html=True,
)


# ---------- MOOD TREND (BAR GRAPH) + STREAK (SIDE BY SIDE) ----------
col_mood, col_stats = st.columns([2.5, 0.8])

with col_mood:
    st.subheader("Mood Trend")
    st.caption("Monday to Sunday — based on your self-reported mood tag per entry")

    if week_entries:
        day_moods = {}
        for e in week_entries:
            day_label = datetime.fromisoformat(e["timestamp"]).strftime("%a")
            day_moods[day_label] = mood_for_entry(e)

        days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        bars_html = '<div class="mood-chart-wrap"><div class="mood-gridlines">'
        for d in days_order:
            mood = day_moods.get(d)
            if mood:
                height = 30 + MOOD_SCALE.index(mood) * 45
                value_label = MOOD_EMOJI.get(mood, "–")
                bar_class = "mood-bar"
            else:
                height = 8
                value_label = "–"
                bar_class = "mood-bar no-entry"
            bars_html += f'<div class="mood-col"><span class="mood-value-label">{value_label}</span><div class="{bar_class}" style="height:{height}px;" title="{mood or "No entry"}"></div><span class="mood-day-label">{d}</span></div>'
        bars_html += "</div></div>"
        st.markdown(bars_html, unsafe_allow_html=True)
        st.caption("Scale (low → high): 🥱 Tired · 😐 Neutral · 🙂 Happy · 😊 Grateful")
    else:
        st.info("Write a few journal entries this week to see your mood trend here.")

with col_stats:
    st.write("")
    st.write("")

    current_streak, streak_days = get_current_streak_days(all_entries)

    # st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Streak</div>', unsafe_allow_html=True)
    st.markdown(f"🔥 **{current_streak} days**")

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    days_order_labels = ["M", "T", "W", "T", "F", "S", "S"]

    circle_divs = []
    for i, label in enumerate(days_order_labels):
        day_date = start_of_week + timedelta(days=i)
        is_filled = day_date in streak_days
        is_future = day_date > today
        if is_filled:
            circle_style = "background:#476550;color:#ffffff;border:2px solid #476550;"
        elif is_future:
            circle_style = "background:#ffffff;color:#c7c5bf;border:2px solid #eae8e3;"
        else:
            circle_style = "background:#ffffff;color:#424843;border:2px solid #eae8e3;"

        circle_divs.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;">'
            f'<div class="streak-circle" style="{circle_style}">{day_date.day}</div>'
            f'<span class="streak-day-label">{label}</span>'
            f'</div>'
        )

    circles_html = f'<div style="display:flex;justify-content:space-between;margin-top:10px;flex-wrap:wrap;gap:4px;">{"".join(circle_divs)}</div>'
    st.markdown(circles_html, unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;color:#725a41;margin-top:6px;">Keep it going!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- GRATITUDE THEMES ----------
# st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown("##### :material/favorite: Gratitude Themes")
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