import streamlit as st

st.set_page_config(page_title="Goals - Sanctuary", page_icon=":material/track_changes:", layout="wide")

import uuid
from datetime import date, datetime

from core import data_manager as dm
from core.layout import require_login, render_account_bar
from core.styles import inject_global_css

inject_global_css()
require_login()
render_account_bar()

user_id = st.session_state.user_id

# ---------- CONFIG (customize freely) ----------
CATEGORY_ICONS = {
    "education": ":material/school:",
    "content": ":material/edit:",
    "side hustle": ":material/rocket_launch:",
    "health": ":material/favorite:",
    "finance": ":material/payments:",
    "hobby": ":material/palette:",
    "hobbies": ":material/palette:",
}
DEFAULT_CATEGORY_ICON = ":material/track_changes:"

PRIORITY_OPTIONS = ["None", "Low Priority", "Medium Priority", "High Priority", "Planning"]


def icon_for_category(category):
    key = category.lower()
    for k, icon in CATEGORY_ICONS.items():
        if k in key:
            return icon
    return DEFAULT_CATEGORY_ICON


# ---------- HELPERS ----------
def save_goal(goal):
    goals = dm.get_user_goals(user_id)
    goals.append(goal)
    dm.save_user_goals(user_id, goals)


def update_goal(goal_id, updates):
    goals = dm.get_user_goals(user_id)
    for g in goals:
        if g["id"] == goal_id:
            g.update(updates)
            break
    dm.save_user_goals(user_id, goals)


def delete_goal(goal_id):
    goals = dm.get_user_goals(user_id)
    goals = [g for g in goals if g["id"] != goal_id]
    dm.save_user_goals(user_id, goals)


def existing_categories(goals):
    seen = []
    for g in goals:
        if g["category"] not in seen:
            seen.append(g["category"])
    return seen


# ---------- STYLING ----------
st.markdown("""
<style>
    .stApp { background-color: #fbf9f4; }
    .goal-category-card {
        background: #ffffff; border: 1px solid #e4e2dd; border-radius: 16px;
        padding: 22px; margin-bottom: 20px;
    }
    .goal-due { font-size: 12.5px; color: #75746D; }
    .goal-due.overdue { color: #ba1a1a; font-weight: 600; }
    .priority-pill {
        display: inline-block; font-size: 11px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.03em;
        background: #eae8e3; color: #424843;
        border-radius: 999px; padding: 3px 10px; margin-right: 6px;
    }
    .priority-pill.high { background: rgba(186,26,26,0.10); color: #ba1a1a; }
    .completed-badge {
        font-size: 12px; font-weight: 700; text-transform: uppercase;
        color: #476550;
    }
    .goal-progress-pct { font-size: 12px; color: #476550; font-weight: 700; }
    .goal-bar-track { width: 100%; height: 6px; background: #eae8e3; border-radius: 999px; overflow: hidden; margin-top: 4px; }
    .goal-bar-fill { height: 100%; background: #476550; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)


# ---------- NEW GOAL DIALOG ----------
@st.dialog("New Goal")
def new_goal_dialog():
    goals = dm.get_user_goals(user_id)
    cats = existing_categories(goals)

    cat_choice = st.selectbox("Category", options=cats + ["+ New category"], index=0)
    if cat_choice == "+ New category" or not cats:
        category = st.text_input("New category name")
    else:
        category = cat_choice

    title = st.text_input("Goal title")

    has_due = st.checkbox("Set a due date")
    due_date = st.date_input("Due date", value=date.today()) if has_due else None

    priority = st.selectbox("Priority", PRIORITY_OPTIONS)
    hours_logged = st.number_input("Hours already spent (optional)", min_value=0.0, step=0.5, value=0.0)
    progress = st.slider("Starting progress", 0, 100, 0)

    if st.button("Create Goal", type="primary", use_container_width=True):
        if not category.strip() or not title.strip():
            st.warning("Category and title are required.", icon=":material/warning:")
        else:
            save_goal({
                "id": uuid.uuid4().hex,
                "category": category.strip(),
                "title": title.strip(),
                "due_date": due_date.isoformat() if due_date else None,
                "priority": None if priority == "None" else priority,
                "progress": progress,
                "completed": progress >= 100,
                "hours_logged": hours_logged,
                "created_at": datetime.now().isoformat(),
            })
            st.rerun()


# ---------- HEADER ----------
col_title, col_new = st.columns([5, 1])
with col_title:
    st.title("Mindful Goals")
    st.caption("Structure your intentions with clarity and focus.")
with col_new:
    st.write("")
    if st.button("New Goal", icon=":material/add:", type="primary", use_container_width=True, key="new_goal_btn"):
        new_goal_dialog()

st.write("")

# ---------- GOALS LIST, GROUPED BY CATEGORY ----------
goals = dm.get_user_goals(user_id)

if not goals:
    st.info("No goals yet — click **New Goal** to set your first intention.")
else:
    today = date.today()

    for category in existing_categories(goals):
        cat_goals = [g for g in goals if g["category"] == category]
        icon = icon_for_category(category)
        
        st.markdown(f"### {icon} {category}")

        for g in cat_goals:
            row_l, row_r, row_menu = st.columns([4, 1.6, 0.6])

            with row_l:
                checked = st.checkbox(g["title"], value=g["completed"], key=f"goal_check_{g['id']}")
                if checked != g["completed"]:
                    update_goal(g["id"], {"completed": checked, "progress": 100 if checked else g["progress"]})
                    st.rerun()

                meta_html = ""
                if g.get("priority"):
                    pill_class = "priority-pill high" if "high" in g["priority"].lower() else "priority-pill"
                    meta_html += f'<span class="{pill_class}">{g["priority"]}</span>'
                if g.get("due_date"):
                    due_dt = date.fromisoformat(g["due_date"])
                    if due_dt < today and not checked:
                        meta_html += f'<span class="goal-due overdue">Overdue: {due_dt.strftime("%b %d")}</span>'
                    else:
                        meta_html += f'<span class="goal-due">Due: {due_dt.strftime("%b %d")}</span>'
                if meta_html:
                    st.markdown(meta_html, unsafe_allow_html=True)

            with row_r:
                if checked:
                    st.markdown('<div class="completed-badge">Completed</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="goal-progress-pct">{g["progress"]}% progress</div>'
                        f'<div class="goal-bar-track"><div class="goal-bar-fill" style="width:{g["progress"]}%;"></div></div>',
                        unsafe_allow_html=True,
                    )

            with row_menu:
                with st.popover("", icon=":material/more_vert:", use_container_width=True):
                    new_progress = st.slider("Progress", 0, 100, g["progress"], key=f"progress_{g['id']}")
                    new_hours = st.number_input(
                        "Hours logged", min_value=0.0, step=0.5,
                        value=float(g.get("hours_logged", 0) or 0), key=f"hours_{g['id']}",
                    )
                    if st.button("Save changes", key=f"save_goal_{g['id']}", use_container_width=True):
                        update_goal(g["id"], {
                            "progress": new_progress,
                            "completed": new_progress >= 100,
                            "hours_logged": new_hours,
                        })
                        st.rerun()

                    st.divider()
                    confirm = st.text_input('Type "DELETE" to remove this goal', key=f"del_confirm_{g['id']}")
                    if st.button("Delete goal", key=f"del_btn_{g['id']}", use_container_width=True):
                        if confirm.strip().upper() == "DELETE":
                            delete_goal(g["id"])
                            st.rerun()
                        else:
                            st.error('Type "DELETE" to confirm.', icon=":material/error:")

            st.divider()

        st.markdown('</div>', unsafe_allow_html=True)