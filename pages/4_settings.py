"""
Settings page
Save this file as: pages/5_Settings.py
(Comes right after pages/4_Goals.py — requires login to access)
"""

import streamlit as st
import json
import os
import hashlib
from datetime import time

st.set_page_config(page_title="Settings - Sanctuary", page_icon="⚙️", layout="centered")

# ---------- CONFIG ----------
SETTINGS_FILE = "user_settings.json"

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
    "streak_goal_minutes": 10,
    "interests": [],
    "app_lock_enabled": False,
    "app_lock_pin_hash": None,
    "biometric_enabled": False,
}

# ---------- ACCESS CONTROL ----------
if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.page_link("pages/1_Profile.py", label="Go to Profile / Login", icon="👤")
    st.stop()

username = st.session_state.username


# ---------- HELPERS ----------
def load_all_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_all_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user_settings():
    all_settings = load_all_settings()
    user_settings = {**DEFAULT_SETTINGS, **all_settings.get(username, {})}
    return user_settings


def update_user_settings(updates):
    all_settings = load_all_settings()
    current = {**DEFAULT_SETTINGS, **all_settings.get(username, {})}
    current.update(updates)
    all_settings[username] = current
    save_all_settings(all_settings)


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


# ---------- STYLING ----------
st.markdown("""
<style>
    .stApp { background-color: #fbf9f4; }
    .settings-section {
        background: #ffffff; border: 1px solid #e4e2dd; border-radius: 14px;
        padding: 24px; margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)


settings = get_user_settings()

# ---------- HEADER ----------
st.title("⚙️ Settings")
st.caption("Configure your sanctuary to best support your mental clarity.")

# ---------- ROUTINE & FREQUENCY ----------
with st.container():
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Routine & Frequency")
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
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- NOTIFICATIONS ----------
with st.container():
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Notifications")

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
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- STREAKS ----------
with st.container():
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Streaks")
    st.caption("Build a habit with a minimum daily time goal — keep the streak alive!")

    streak_goal = st.slider(
        "Minimum minutes on the app per day to keep your streak",
        min_value=1, max_value=60, value=settings["streak_goal_minutes"],
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- INTERESTS ----------
with st.container():
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Your Interests")
    st.caption("Used to suggest new hobbies and personalize your experience.")

    interests = st.multiselect(
        "Select your interests",
        options=INTEREST_OPTIONS,
        default=[i for i in settings["interests"] if i in INTEREST_OPTIONS],
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PRIVACY & SECURITY ----------
with st.container():
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Privacy & Security")
    st.caption("Your reflections are entirely your own. Protect your sanctuary with an additional layer of security.")

    app_lock_enabled = st.toggle("App Lock (require a PIN to open the app)", value=settings["app_lock_enabled"])

    if app_lock_enabled:
        with st.expander("Set / change your PIN"):
            pin1 = st.text_input("New PIN (4-6 digits)", type="password", max_chars=6, key="pin1")
            pin2 = st.text_input("Confirm PIN", type="password", max_chars=6, key="pin2")
            if st.button("Save PIN"):
                if not pin1.isdigit() or not (4 <= len(pin1) <= 6):
                    st.error("PIN must be 4-6 digits.")
                elif pin1 != pin2:
                    st.error("PINs do not match.")
                else:
                    update_user_settings({"app_lock_pin_hash": hash_pin(pin1)})
                    st.success("PIN saved.")

    biometric_enabled = st.toggle(
        "Biometric unlock (Touch ID / Face ID)",
        value=settings["biometric_enabled"],
        help="Note: browser-based apps can't directly access device biometrics — "
             "this stores your preference, but true biometric unlock would need a "
             "native app wrapper.",
        disabled=not app_lock_enabled,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SAVE ----------
if st.button("💾 Save Settings", type="primary", use_container_width=True):
    update_user_settings({
        "frequency": frequency,
        "reminder_time": reminder_time.strftime("%H:%M"),
        "push_notifications": push_notifications,
        "gentle_nudges": gentle_nudges,
        "streak_goal_minutes": streak_goal,
        "interests": interests,
        "app_lock_enabled": app_lock_enabled,
        "biometric_enabled": biometric_enabled,
    })
    st.success("Settings saved!")