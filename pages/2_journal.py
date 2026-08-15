"""
Journal page — Gratitude Journal entry screen
Save this file as: pages/2_Journal.py
(Comes right after pages/1_Profile.py — requires login to access)
"""

import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Journal - Sanctuary", page_icon="📝", layout="wide")

# ---------- CONFIG ----------
ENTRIES_FILE = "journal_entries.json"

QUOTES = [
    ("Gratitude turns what we have into enough.", "Aesop"),
    ("Gratitude is not only the greatest of virtues, but the parent of all others.", "Cicero"),
    ("Enjoy the little things, for one day you may look back and realize they were the big things.", "Robert Brault"),
    ("Gratitude makes sense of our past, brings peace for today, and creates a vision for tomorrow.", "Melody Beattie"),
    ("When you arise in the morning, think of what a precious privilege it is to be alive.", "Marcus Aurelius"),
]

PROMPTS = [
    "What is one thing you learned today, however small?",
    "Who or what made you smile today, and why?",
    "What is a recurring thought you've had lately? Let's unpack it.",
    "Describe a moment of peace you experienced this week.",
    "What's something you're looking forward to?",
    "Name one person you're grateful for and why.",
    "What's a small comfort you often take for granted?",
]

# ---------- ACCESS CONTROL ----------
if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.page_link("pages/1_Profile.py", label="Go to Profile / Login", icon="👤")
    st.stop()

username = st.session_state.username

# ---------- HELPERS ----------
def load_entries():
    if not os.path.exists(ENTRIES_FILE):
        return {}
    with open(ENTRIES_FILE, "r") as f:
        return json.load(f)


def save_entry(username, title, body, prompt_used=None):
    entries = load_entries()
    entries.setdefault(username, [])
    entries[username].append({
        "title": title or "Untitled Entry",
        "body": body,
        "prompt_used": prompt_used,
        "date": datetime.now().strftime("%b %d, %Y"),
        "time": datetime.now().strftime("%I:%M %p"),
        "timestamp": datetime.now().isoformat(),
    })
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=2)


# ---------- SESSION STATE ----------
if "daily_quote" not in st.session_state:
    st.session_state.daily_quote = random.choice(QUOTES)
if "shuffled_prompts" not in st.session_state:
    st.session_state.shuffled_prompts = random.sample(PROMPTS, 4)
if "journal_body" not in st.session_state:
    st.session_state.journal_body = ""
if "journal_title" not in st.session_state:
    st.session_state.journal_title = ""
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None


# ---------- STYLING (Sage Green / Cream "Sanctuary" theme) ----------
st.markdown("""
<style>
    .stApp { background-color: #fbf9f4; }
    .quote-card {
        background-color: rgba(71,101,80,0.05);
        border: 1px solid rgba(71,101,80,0.1);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin-bottom: 24px;
    }
    .quote-text {
        font-size: 24px;
        font-style: italic;
        color: #476550;
        font-weight: 600;
    }
    .quote-author {
        color: #424843;
        opacity: 0.7;
        margin-top: 8px;
    }
    div.stButton > button {
        border-radius: 999px;
    }
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("📝 Journal")
st.caption("Writing Reflection")

# Quote of the day
quote, author = st.session_state.daily_quote
st.markdown(f"""
<div class="quote-card">
    <div class="quote-text">"{quote}"</div>
    <div class="quote-author">— {author}</div>
</div>
""", unsafe_allow_html=True)

col_main, col_sidebar = st.columns([2.5, 1])

# ---------- MAIN WRITING AREA ----------
with col_main:
    st.session_state.journal_title = st.text_input(
        "Entry Title (Optional)",
        value=st.session_state.journal_title,
        placeholder="Entry Title (Optional)",
        label_visibility="collapsed",
    )

    now = datetime.now()
    st.caption(f"📅 {now.strftime('%b %d, %Y')}   🕐 {now.strftime('%I:%M %p')}")

    if st.session_state.selected_prompt:
        st.info(f"💡 Prompt: {st.session_state.selected_prompt}")

    st.session_state.journal_body = st.text_area(
        "Start writing your reflection...",
        value=st.session_state.journal_body,
        placeholder="Start writing your reflection...",
        height=350,
        label_visibility="collapsed",
    )

    col_discard, col_spacer, col_save = st.columns([1, 3, 1])
    with col_discard:
        if st.button("🗑️ Discard", use_container_width=True):
            st.session_state.journal_body = ""
            st.session_state.journal_title = ""
            st.session_state.selected_prompt = None
            st.rerun()

    with col_save:
        if st.button("✅ Save Entry", type="primary", use_container_width=True):
            if not st.session_state.journal_body.strip():
                st.warning("Write something before saving.")
            else:
                save_entry(
                    username,
                    st.session_state.journal_title,
                    st.session_state.journal_body,
                    st.session_state.selected_prompt,
                )
                st.success("Entry saved!")
                st.session_state.journal_body = ""
                st.session_state.journal_title = ""
                st.session_state.selected_prompt = None
                st.session_state.shuffled_prompts = random.sample(PROMPTS, 4)
                st.rerun()

# ---------- GUIDED PROMPTS SIDEBAR ----------
with col_sidebar:
    st.subheader("Guided Prompts")
    st.caption("Need inspiration? Try answering one of these.")

    for i, prompt in enumerate(st.session_state.shuffled_prompts):
        if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
            st.session_state.selected_prompt = prompt
            st.rerun()

    st.write("")
    if st.button("🔄 Shuffle Prompts", use_container_width=True):
        st.session_state.shuffled_prompts = random.sample(PROMPTS, 4)
        st.rerun()

# ---------- PAST ENTRIES ----------
st.divider()
with st.expander("📚 View past entries"):
    entries = load_entries().get(username, [])
    if not entries:
        st.write("No entries yet — write your first one above!")
    else:
        for entry in reversed(entries):
            st.markdown(f"**{entry['title']}** — {entry['date']} at {entry['time']}")
            st.write(entry["body"])
            st.markdown("---")