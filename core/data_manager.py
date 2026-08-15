import json
import os
import uuid
import hashlib
from datetime import datetime

# ---------- PATHS ----------
DATA_DIR = "data_storage"

USERS_PATH = os.path.join(DATA_DIR, "users", "users.json")
ENTRIES_PATH = os.path.join(DATA_DIR, "journal_entries", "journal_entries.json")
QUOTES_PATH = os.path.join(DATA_DIR, "journal_entries", "quote_history.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings", "user_settings.json")


def _ensure_parent(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    _ensure_parent(path)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ---------- PASSWORD HASHING ----------
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 100_000
    ).hex()
    return hashed, salt


def verify_password(password, stored_hash, salt):
    check_hash, _ = hash_password(password, salt)
    return check_hash == stored_hash


# ---------- AUTH ----------
def register_user(username, password, interests=None):
    """
    Create a new account. Every account gets a fresh random user_id (uuid4)
    generated at registration time, and ALL journal/goals/settings data is
    keyed by user_id rather than by username.

    Why this fixes the "deleted user, same username, old entries reappear"
    bug: previously everything was keyed by username, which is stable and
    user-chosen. Delete a user's record from users.json, then let someone
    (or the same person) register that same username again, and the old
    username-keyed rows in journal_entries.json / goals_data.json /
    user_settings.json were still sitting there waiting to be picked back
    up. Because user_id is freshly generated every time someone registers,
    a reused username can never collide with old data again — the old rows
    are simply orphaned under a user_id nothing points to anymore.
    """
    users = load_json(USERS_PATH)
    if username in users:
        return False, "That username is already taken.", None
    if len(password) < 6:
        return False, "Password must be at least 6 characters.", None

    hashed, salt = hash_password(password)
    user_id = uuid.uuid4().hex

    users[username] = {
        "user_id": user_id,
        "password_hash": hashed,
        "salt": salt,
        "created_at": datetime.now().isoformat(),
        "interests": interests or [],
    }
    save_json(USERS_PATH, users)
    return True, "Account created!", user_id


def login_user(username, password):
    users = load_json(USERS_PATH)
    if username not in users:
        return False, "No account found with that username.", None

    user = users[username]
    if verify_password(password, user["password_hash"], user["salt"]):
        return True, "Login successful!", user["user_id"]
    return False, "Incorrect password.", None


def get_user_record(username):
    return load_json(USERS_PATH).get(username, {})


# ---------- PER-USER DATA HELPERS (all keyed by user_id) ----------
def get_user_entries(user_id):
    return load_json(ENTRIES_PATH).get(user_id, [])


def save_user_entries(user_id, entries):
    all_entries = load_json(ENTRIES_PATH)
    all_entries[user_id] = entries
    save_json(ENTRIES_PATH, all_entries)


def get_user_settings(user_id):
    return load_json(SETTINGS_PATH).get(user_id, {})


def save_user_settings(user_id, settings):
    all_settings = load_json(SETTINGS_PATH)
    all_settings[user_id] = settings
    save_json(SETTINGS_PATH, all_settings)