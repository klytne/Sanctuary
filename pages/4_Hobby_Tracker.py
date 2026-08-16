import uuid
from datetime import datetime

import streamlit as st

from core import data_manager as dm
from core.layout import require_login, render_account_bar

require_login()
render_account_bar()

user_id = st.session_state.user_id

# ---------------------------------------------------------------------------
# Scoped CSS for the hobby/suggestion cards. Containers below are created
# with a unique `key`, which Streamlit exposes as a `st-key-<key>` class on
# the wrapping div — we target that instead of touching the global
# .sanctuary-card styling in core/styles.py.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    [class*="st-key-hobby_card_"], [class*="st-key-suggestion_card_"] {
        background: #ffffff;
        border: 1px solid transparent !important;
        box-shadow: none !important;
        border-radius: 16px !important;
        padding: 24px !important;
    }
    .hobby-badge {
        background: #7d9d85;
        color: #173422;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .hobby-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 8px;
    }
    .hobby-card-title {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Curated suggestion pool for "Discover New Pursuits".
# Each entry's "tags" are matched (case-insensitive) against the user's
# interests saved in Settings. If none of the user's interests match
# anything in the pool, we fall back to showing a small popular set so the
# section is never empty.
# ---------------------------------------------------------------------------
HOBBY_SUGGESTIONS = [
    {"name": "Creative Writing", "category": "Writing", "tags": ["reading", "writing"],
     "description": "Express your inner thoughts and build new worlds, one page at a time."},
    {"name": "Journaling Poetry", "category": "Writing", "tags": ["reading", "writing", "mindfulness"],
     "description": "Turn quiet reflection into short, personal poems."},
    {"name": "Learning an Instrument", "category": "Music", "tags": ["music"],
     "description": "Pick up guitar, piano, or ukulele and build a small daily practice habit."},
    {"name": "Curating Playlists", "category": "Music", "tags": ["music"],
     "description": "Discover new artists and build playlists for different moods."},
    {"name": "Urban Sketching", "category": "Creativity", "tags": ["art", "creativity"],
     "description": "Step outside and document your surroundings through mindful observation."},
    {"name": "Pottery Making", "category": "Creativity", "tags": ["art", "creativity"],
     "description": "Tactile, grounding work with clay."},
    {"name": "Morning Runs", "category": "Fitness", "tags": ["fitness", "health"],
     "description": "A simple, repeatable way to start the day with movement."},
    {"name": "Yoga", "category": "Mindfulness", "tags": ["mindfulness", "fitness", "health"],
     "description": "Gentle movement paired with breath, good for body and mind."},
    {"name": "Cooking New Recipes", "category": "Cooking", "tags": ["cooking", "food"],
     "description": "Try one new recipe a week and build kitchen confidence."},
    {"name": "Houseplant Care", "category": "Nature", "tags": ["nature", "gardening"],
     "description": "Slow, patient work tending something that grows."},
    {"name": "Photography Walks", "category": "Creativity", "tags": ["art", "creativity", "nature"],
     "description": "Explore your neighborhood with a camera and a fresh eye."},
    {"name": "Learning to Code", "category": "Tech", "tags": ["tech"],
     "description": "Build small projects and pick up a new technical skill."},
]

POPULAR_FALLBACK = ["Creative Writing", "Morning Runs", "Urban Sketching"]

CATEGORY_OPTIONS = sorted({s["category"] for s in HOBBY_SUGGESTIONS} | {"Other"})


def _new_hobby(name, category, description):
    return {
        "id": uuid.uuid4().hex,
        "name": name,
        "category": category,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "total_minutes": 0,
        "sessions": [],
    }


# ---------------------------------------------------------------------------
# Dialogs
# ---------------------------------------------------------------------------
@st.dialog("Add a Hobby")
def add_hobby_dialog():
    hobbies = dm.get_user_hobbies(user_id)
    existing_names = {h["name"].strip().lower() for h in hobbies}

    name = st.text_input("Hobby name")
    category = st.selectbox("Category", CATEGORY_OPTIONS)
    description = st.text_area("Description (optional)")

    if st.button("Add Hobby", type="primary", use_container_width=True):
        if not name.strip():
            st.warning("Give your hobby a name first.")
        elif name.strip().lower() in existing_names:
            st.warning("You already have a hobby with that name.")
        else:
            hobbies.append(_new_hobby(name.strip(), category, description.strip()))
            dm.save_user_hobbies(user_id, hobbies)
            st.rerun()


@st.dialog("Log Session")
def log_session_dialog(hobby):
    st.write(f"How long did you spend on **{hobby['name']}** today?")
    minutes = st.number_input("Minutes", min_value=1, max_value=600, value=15, step=5)

    if st.button("Save Session", type="primary", use_container_width=True):
        hobbies = dm.get_user_hobbies(user_id)
        for h in hobbies:
            if h["id"] == hobby["id"]:
                now = datetime.now()
                h.setdefault("sessions", []).append({
                    "date": now.strftime("%b %d, %Y"),
                    "minutes": minutes,
                    "timestamp": now.isoformat(),
                })
                h["total_minutes"] = h.get("total_minutes", 0) + minutes
                break
        dm.save_user_hobbies(user_id, hobbies)
        st.rerun()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
col_title, col_button = st.columns([5, 1])
with col_title:
    st.title("Hobby Tracker")
    st.caption("Keep up with the pursuits that keep you grounded.")
with col_button:
    st.markdown("<div style='height:38px'></div>", unsafe_allow_html=True)
    if st.button("+ Add Hobby", type="primary", use_container_width=True):
        add_hobby_dialog()

hobbies = dm.get_user_hobbies(user_id)
existing_names = {h["name"].strip().lower() for h in hobbies}

# ---------------------------------------------------------------------------
# Active Hobbies
# ---------------------------------------------------------------------------
st.header("Active Hobbies")

if not hobbies:
    st.info("You haven't added any hobbies yet. Use \"+ Add Hobby\" above, or pick something from Discover New Pursuits.")
else:
    cols = st.columns(3)
    for i, hobby in enumerate(hobbies):
        with cols[i % 3]:
            with st.container(border=True, key=f"hobby_card_{hobby['id']}"):
                st.markdown(
                    f"""<div class="hobby-card-header">
                        <span class="hobby-card-title">{hobby['name']}</span>
                        <span class="hobby-badge">Active</span>
                    </div>
                    <span style="color:#727972;font-size:0.85rem;">{hobby.get('category', '')}</span>
                    <p style="margin-top:8px;color:#424843;">{hobby.get('description', '')}</p>
                    <p style="color:#727972;font-size:0.85rem;">Total logged: {hobby.get('total_minutes', 0)} min</p>""",
                    unsafe_allow_html=True,
                )

                if st.button("▶ Start Session", key=f"start_{hobby['id']}", type="primary", use_container_width=True):
                    log_session_dialog(hobby)

                if st.button("View Insights", key=f"insights_{hobby['id']}", type="secondary", use_container_width=True):
                    st.switch_page("pages/5_Insights.py")

st.divider()

# ---------------------------------------------------------------------------
# Discover New Pursuits — filtered by the user's interests from Settings
# ---------------------------------------------------------------------------
st.header("Discover New Pursuits")

settings = dm.get_user_settings(user_id)
user_interests = [i.strip().lower() for i in settings.get("interests", [])]

if user_interests:
    recommended = [
        s for s in HOBBY_SUGGESTIONS
        if any(tag in user_interests for tag in s["tags"])
        and s["name"].strip().lower() not in existing_names
    ]
    st.caption(f"Based on your interests: {', '.join(settings.get('interests', []))}")
else:
    recommended = []

if not recommended:
    recommended = [
        s for s in HOBBY_SUGGESTIONS
        if s["name"] in POPULAR_FALLBACK and s["name"].strip().lower() not in existing_names
    ]
    st.caption("Popular with other users:")

if not recommended:
    st.info("You've added all our current suggestions. Nice work!")
else:
    cols = st.columns(3)
    for i, suggestion in enumerate(recommended):
        with cols[i % 3]:
            with st.container(border=True, key=f"suggestion_card_{i}_{suggestion['name']}"):
                st.markdown(
                    f"""<span class="hobby-card-title">{suggestion['name']}</span><br/>
                    <span style="color:#727972;font-size:0.85rem;">{suggestion['category']}</span>
                    <p style="margin-top:8px;color:#424843;">{suggestion['description']}</p>""",
                    unsafe_allow_html=True,
                )
                if st.button("Add to My Hobbies", key=f"add_suggestion_{suggestion['name']}", type="secondary", use_container_width=True):
                    hobbies.append(_new_hobby(suggestion["name"], suggestion["category"], suggestion["description"]))
                    dm.save_user_hobbies(user_id, hobbies)
                    st.rerun()