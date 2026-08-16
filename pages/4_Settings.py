"""
pages/5_Settings.py — Settings

Requires login (see require_login() below). Each section is rendered as a
white, rounded, expandable card — Streamlit's st.expander gives us the
header + chevron look for free, styled via the CSS block further down.
"""

import streamlit as st

# set_page_config must be the very first Streamlit command in the file
st.set_page_config(page_title="Settings - Sanctuary", page_icon=":material/settings:", layout="centered")

from datetime import time

from core import data_manager as dm
from core.layout import require_login, render_account_bar
from core.styles import inject_global_css

inject_global_css()
require_login()
render_account_bar()

username = st.session_state.username

# ---------- CONFIG ----------
INTEREST_OPTIONS = [
    "Reading", "Fitness", "Art & Design", "Music", "Cooking", "Writing",
    "Gardening", "Gaming", "Photography", "Finance", "Content Creation",
    "Travel", "Meditation", "Dance",
]

DEFAULT_SETTINGS = {
    "frequency": "Bi-weekly",
    "reminder_time": "09:00",
    "push_notifications": True,
    "gentle_nudges": True,
    "email_notifications": False,
    "email": "",
    "streak_goal_minutes": 10,
    "interests": [],
}


# ---------- HELPERS ----------
def load_settings():
    return {**DEFAULT_SETTINGS, **dm.get_user_settings(st.session_state.user_id)}


def save_settings(updates):
    current = load_settings()
    current.update(updates)
    dm.save_user_settings(st.session_state.user_id, current)


# ---------- STYLING ----------
st.markdown("""
<style>
    /* Card-style expanders, matching the reference design */
    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #e4e2dd;
        border-radius: 14px;
        margin-bottom: 18px;
    }
    [data-testid="stExpander"] summary {
        padding: 18px 24px;
    }
    [data-testid="stExpander"] summary p {
        font-size: 20px;
        font-weight: 700;
        color: #1b1c19;
    }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        padding: 0 24px 22px 24px;
    }
</style>
""", unsafe_allow_html=True)


settings = load_settings()

# ---------- HEADER ----------
st.title("Settings")
st.caption("Configure your sanctuary to best support your mental clarity.")

# ---------- ROUTINE & FREQUENCY ----------
with st.expander("Routine & Frequency", expanded=False):
    st.caption("Establish a gentle rhythm that feels right for you. No pressure, just invitations.")

    frequency = st.radio(
        "How often would you like to journal?",
        ["Daily", "Bi-weekly", "Custom"],
        index=["Daily", "Bi-weekly", "Custom"].index(settings["frequency"]),
        captions=[
            "A consistent daily reflection.",
            "Checking in twice a week.",
            "Set your own gentle cadence.",
        ],
    )

    reminder_time = st.time_input(
        "What time should we remind you?",
        value=time.fromisoformat(settings["reminder_time"]),
    )

# ---------- NOTIFICATIONS ----------
with st.expander("Notifications", expanded=False):
    push_notifications = st.toggle(
        "Personalized push notifications",
        value=settings["push_notifications"],
        help="Allow gentle nudges based on your activity patterns and chosen frequency. "
             "Designed to be invitations, not interruptions.",
    )

    gentle_nudges = st.toggle(
        "Gentle nudges when you leave mid-entry",
        value=settings["gentle_nudges"],
        help="If you close the app with an unsaved journal entry or a hobby/goal timer "
             "still running, we'll send a gentle reminder next time you open the app.",
    )

    email_notifications = st.toggle(
        "Email notifications",
        value=settings["email_notifications"],
        help="Get a weekly summary and reminder emails sent to your inbox instead of "
             "(or alongside) push notifications.",
    )

    email_address = st.text_input(
        "Email address",
        value=settings["email"],
        placeholder="you@example.com",
        disabled=not email_notifications,
    )

# ---------- STREAKS ----------
with st.expander("Streaks", expanded=False):
    st.caption("Build a habit with a minimum daily time goal — keep the streak alive!")

    streak_goal = st.slider(
        "Minimum minutes on the app per day to keep your streak",
        min_value=1, max_value=60, value=settings["streak_goal_minutes"],
    )

# ---------- INTERESTS ----------
with st.expander("Your Interests", expanded=False):
    st.caption("Used to suggest new hobbies and personalize your experience.")

    interests = st.multiselect(
        "Select your interests",
        options=INTEREST_OPTIONS,
        default=[i for i in settings["interests"] if i in INTEREST_OPTIONS],
        label_visibility="collapsed",
    )

# ---------- DELETE ACCOUNT ----------
with st.expander("Delete Account", expanded=False):
    st.caption(
        "This permanently deletes your account and all of your journal entries, "
        "goals, and settings. This cannot be undone."
    )

    confirm_text = st.text_input(
        'Type "DELETE" to confirm',
        key="delete_confirm_input",
    )

    if st.button("Delete my account", icon=":material/delete_forever:"):
        if confirm_text.strip().upper() == "DELETE":
            dm.delete_user_account(username)
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.success("Account deleted.", icon=":material/check_circle:")
            st.rerun()
        else:
            st.error('Please type "DELETE" exactly to confirm.', icon=":material/error:")
            
# ---------- SAVE ----------
if st.button("Save Settings", icon=":material/save:", type="primary", use_container_width=True):
    if email_notifications and not email_address.strip():
        st.error("Add an email address to enable email notifications.", icon=":material/error:")
    else:
        save_settings({
            "frequency": frequency,
            "reminder_time": reminder_time.strftime("%H:%M"),
            "push_notifications": push_notifications,
            "gentle_nudges": gentle_nudges,
            "email_notifications": email_notifications,
            "email": email_address.strip(),
            "streak_goal_minutes": streak_goal,
            "interests": interests,
        })
        st.success("Settings saved!", icon=":material/check_circle:")