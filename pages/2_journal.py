import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Journal - Sanctuary", page_icon="📝", layout="wide")

# ---------- CONFIG ----------
DATA_STORAGE_DIR = "Data_Storage"
JOURNAL_ENTRIES_DIR = os.path.join(DATA_STORAGE_DIR, "journal_entries")
ENTRIES_FILE = os.path.join(JOURNAL_ENTRIES_DIR, "journal_entries.json")

os.makedirs(JOURNAL_ENTRIES_DIR, exist_ok=True)

QUOTE_HISTORY_FILE = os.path.join(DATA_STORAGE_DIR, "journal_entries", "quote_history.json")

QUOTES = [
    ("Gratitude turns what we have into enough.", "Aesop"),
    ("Gratitude is not only the greatest of virtues, but the parent of all others.", "Cicero"),
    ("Enjoy the little things, for one day you may look back and realize they were the big things.", "Robert Brault"),
    ("Gratitude makes sense of our past, brings peace for today, and creates a vision for tomorrow.", "Melody Beattie"),
    ("When you arise in the morning, think of what a precious privilege it is to be alive.", "Marcus Aurelius"),
    ("He is a wise man who does not grieve for the things which he has not, but rejoices for those which he has.", "Epictetus"),
    ("Gratitude is the fairest blossom which springs from the soul.", "Henry Ward Beecher"),
    ("Let us be grateful to people who make us happy; they are the charming gardeners who make our souls blossom.", "Marcel Proust"),
    ("The unthankful heart discovers no mercies; but the thankful heart will find, in every hour, some heavenly blessings.", "Henry Ward Beecher"),
    ("Silent gratitude isn't very much use to anyone.", "Gertrude Stein"),
    ("Gratitude is the memory of the heart.", "Jean Baptiste Massieu"),
    ("As we express our gratitude, we must never forget that the highest appreciation is not to utter words, but to live by them.", "John F. Kennedy"),
    ("Piglet noticed that even though he had a Very Small Heart, it could hold a rather large amount of Gratitude.", "A.A. Milne"),
    ("Feeling gratitude and not expressing it is like wrapping a present and not giving it.", "William Arthur Ward"),
    ("This is a wonderful day. I've never seen this one before.", "Maya Angelou"),
    ("Cultivate the habit of being grateful for every good thing that comes to you.", "Ralph Waldo Emerson"),
    ("There is always, always, always something to be thankful for.", "Ann Voskamp"),
    ("Joy is the simplest form of gratitude.", "Karl Barth"),
    ("Reflect upon your present blessings, of which every man has plenty; not on your past misfortunes, of which all men have some.", "Charles Dickens"),
    ("Wear gratitude like a cloak, and it will feed every corner of your life.", "Rumi"),
    ("If the only prayer you say in your life is thank you, that would suffice.", "Meister Eckhart"),
    ("Gratitude helps you to grow and expand.", "Eileen Caddy"),
    ("When I started counting my blessings, my whole life turned around.", "Willie Nelson"),
    ("Be thankful for what you have; you'll end up having more.", "Oprah Winfrey"),
    ("Gratitude turns problems into opportunities and confusion into clarity.", "Deepak Chopra"),
    ("A grateful mind is a great mind which eventually attracts to itself great things.", "Plato"),
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
    os.makedirs(JOURNAL_ENTRIES_DIR, exist_ok=True)
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

def delete_entry(username, entry_index):
    entries = load_entries()
    user_entries = entries.get(username, [])
    if 0 <= entry_index < len(user_entries):
        user_entries.pop(entry_index)
        entries[username] = user_entries
        with open(ENTRIES_FILE, "w") as f:
            json.dump(entries, f, indent=2)

def get_fresh_quote(username):
    """Returns a gratitude quote the user hasn't seen recently.
    Once all quotes have been shown, the history resets so they start cycling again."""
    if os.path.exists(QUOTE_HISTORY_FILE):
        with open(QUOTE_HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = {}

    seen_indices = history.get(username, [])
    all_indices = list(range(len(QUOTES)))
    remaining = [i for i in all_indices if i not in seen_indices]

    if not remaining:
        # Seen them all — reset so they start seeing quotes again
        remaining = all_indices
        seen_indices = []

    chosen_index = random.choice(remaining)
    seen_indices.append(chosen_index)

    history[username] = seen_indices
    os.makedirs(os.path.dirname(QUOTE_HISTORY_FILE), exist_ok=True)
    with open(QUOTE_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return QUOTES[chosen_index]

# ---------- SESSION STATE ----------
if "daily_quote" not in st.session_state:
    st.session_state.daily_quote = get_fresh_quote(username)
if "shuffled_prompts" not in st.session_state:
    st.session_state.shuffled_prompts = random.sample(PROMPTS, 4)
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None
if "entry_nonce" not in st.session_state:
    st.session_state.entry_nonce = 0   # forces fresh widgets after each save/discard

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
st.title("Journal")
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
title_key = f"journal_title_{st.session_state.entry_nonce}"
body_key = f"journal_body_{st.session_state.entry_nonce}"

with col_main:
    st.text_input(
        "Entry Title (Optional)",
        placeholder="Entry Title (Optional)",
        label_visibility="collapsed",
        key=title_key,
    )

    now = datetime.now()
    st.caption(f":material/calendar_month: {now.strftime('%b %d, %Y')}   :material/schedule: {now.strftime('%I:%M %p')}")

    if st.session_state.selected_prompt:
        st.info(f"Prompt: {st.session_state.selected_prompt}", icon=":material/lightbulb:")

    st.text_area(
        "Start writing your reflection...",
        placeholder="Start writing your reflection...",
        height=350,
        label_visibility="collapsed",
        key=body_key,
    )

    col_discard, col_spacer, col_save = st.columns([1, 3, 1])
    with col_discard:
        if st.button("Discard", icon=":material/delete:", use_container_width=True):
            st.session_state.selected_prompt = None
            st.session_state.entry_nonce += 1   # fresh, empty widgets
            st.rerun()

    with col_save:
        if st.button("Save Entry", icon=":material/check_circle:", type="primary", use_container_width=True):
            body_value = st.session_state.get(body_key, "")
            title_value = st.session_state.get(title_key, "")
            if not body_value.strip():
                st.warning("Write something before saving.")
            else:
                save_entry(username, title_value, body_value, st.session_state.selected_prompt)
                st.success("Entry saved!")
                st.session_state.selected_prompt = None
                st.session_state.shuffled_prompts = random.sample(PROMPTS, 4)
                st.session_state.entry_nonce += 1   # fresh, empty widgets
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

if "selected_entry_index" not in st.session_state:
    st.session_state.selected_entry_index = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

with st.expander("View past entries", icon=":material/menu_book:"):
    entries = load_entries().get(username, [])

    if not entries:
        st.write("No entries yet — write your first one above!")
    else:
        # Reverse so newest entries show first, but keep track of original index
        reversed_entries = list(reversed(list(enumerate(entries))))

        if st.session_state.selected_entry_index is None:
            # ---- LIST VIEW: just titles/dates, clickable ----
            for original_index, entry in reversed_entries:
                label = f"{entry['title']} — {entry['date']} at {entry['time']}"
                if st.button(label, key=f"entry_{original_index}", use_container_width=True):
                    st.session_state.selected_entry_index = original_index
                    st.rerun()

        else:
            # ---- DETAIL VIEW: full entry for the selected one ----
            entry = entries[st.session_state.selected_entry_index]

            col_back, col_delete = st.columns([3, 1])
            with col_back:
                if st.button("Back to all entries", icon=":material/arrow_back:"):
                    st.session_state.selected_entry_index = None
                    st.session_state.confirm_delete = False
                    st.rerun()
            with col_delete:
                if st.button("Delete", icon=":material/delete:", use_container_width=True):
                    st.session_state.confirm_delete = True
                    st.rerun()

            st.markdown(f"**{entry['title']}** — {entry['date']} at {entry['time']}")
            if entry.get("prompt_used"):
                st.caption(f":material/lightbulb: Prompt: {entry['prompt_used']}")
            st.write(entry["body"])

            if st.session_state.confirm_delete:
                st.warning("Are you sure you want to delete this entry? This can't be undone.")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("Yes, delete it", type="primary", use_container_width=True):
                        delete_entry(username, st.session_state.selected_entry_index)
                        st.session_state.selected_entry_index = None
                        st.session_state.confirm_delete = False
                        st.success("Entry deleted.")
                        st.rerun()
                with col_no:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.confirm_delete = False
                        st.rerun()
