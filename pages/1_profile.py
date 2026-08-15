"""
Profile page — Login / Register
Save this file as: pages/1_Profile.py
(Streamlit auto-generates the sidebar link + URL from the filename,
so it will appear as "Profile" and be reachable at .../Profile)
"""

import streamlit as st
import json
import hashlib
import os
from datetime import datetime

# ---------- CONFIG ----------
USERS_FILE = "users.json"

st.set_page_config(page_title="Profile - Login / Register", page_icon="👤")


# ---------- HELPERS ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password, salt=None):
    """Hash a password with a random salt using SHA-256 + PBKDF2."""
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 100_000
    ).hex()
    return hashed, salt


def verify_password(password, stored_hash, salt):
    check_hash, _ = hash_password(password, salt)
    return check_hash == stored_hash


def register_user(username, password, interests=None):
    users = load_users()
    if username in users:
        return False, "That username is already taken."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    hashed, salt = hash_password(password)
    users[username] = {
        "password_hash": hashed,
        "salt": salt,
        "created_at": datetime.now().isoformat(),
        "interests": interests or [],
    }
    save_users(users)
    return True, "Account created! You can now log in."


def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "No account found with that username."

    user = users[username]
    if verify_password(password, user["password_hash"], user["salt"]):
        return True, "Login successful!"
    return False, "Incorrect password."


# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None


# ---------- UI ----------
st.title("👤 Profile")

# If already logged in, show profile view + logout option
if st.session_state.logged_in:
    st.success(f"Logged in as **{st.session_state.username}**")

    users = load_users()
    user_data = users.get(st.session_state.username, {})

    st.subheader("Your interests")
    st.write(user_data.get("interests", []) or "No interests added yet.")

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

else:
    # Login / Register tabs
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Log in to your account")
        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input(
                "Password", type="password", key="login_password"
            )
            submitted = st.form_submit_button("Log in")

            if submitted:
                if not login_username or not login_password:
                    st.warning("Please fill in both fields.")
                else:
                    success, message = login_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    with register_tab:
        st.subheader("Create a new account")
        with st.form("register_form"):
            reg_username = st.text_input("Choose a username", key="reg_username")
            reg_password = st.text_input(
                "Choose a password", type="password", key="reg_password"
            )
            reg_password_confirm = st.text_input(
                "Confirm password", type="password", key="reg_password_confirm"
            )
            reg_interests = st.multiselect(
                "What are you interested in? (used for hobby suggestions)",
                options=[
                    "Reading", "Fitness", "Art & Design", "Music",
                    "Cooking", "Writing", "Gardening", "Gaming",
                    "Photography", "Finance", "Content Creation",
                ],
                key="reg_interests",
            )
            submitted = st.form_submit_button("Register")

            if submitted:
                if not reg_username or not reg_password:
                    st.warning("Please fill in all required fields.")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(
                        reg_username, reg_password, reg_interests
                    )
                    if success:
                        st.success(message)
                        st.info("Switch to the Login tab to sign in.")
                    else:
                        st.error(message)