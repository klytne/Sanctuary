import streamlit as st
from core.styles import inject_global_css

st.set_page_config(
    page_title="Sanctuary - Gratitude & Mindful Living",
    page_icon=":material/spa:",
    layout="wide",
)
inject_global_css()

for key, default in [("logged_in", False), ("username", None), ("user_id", None)]:
    st.session_state.setdefault(key, default)

login_page = st.Page("pages/1_Login.py", title="Login", icon=":material/person:")
home_page = st.Page("pages/0_Home.py", title="Home", icon=":material/eco:")
journal_page = st.Page("pages/2_Journal.py", title="Journal", icon=":material/edit_note:")
insights_page = st.Page("pages/3_Insights.py", title="Insights", icon=":material/insights:")
settings_page = st.Page("pages/4_Settings.py", title="Settings", icon=":material/settings:")

if st.session_state.logged_in:
    pages = [journal_page, insights_page, settings_page]
else:
    pages = [home_page, login_page]

pg = st.navigation(pages)
pg.run()