import streamlit as st


def require_login():
    if not st.session_state.get("logged_in"):
        st.rerun()


def render_account_bar():
    pass
    # with st.sidebar:
    #     st.caption(f"Logged in as **{st.session_state.username}**")
    #     if st.button("Log out", icon=":material/logout:"):
    #         st.session_state.logged_in = False
    #         st.session_state.username = None
    #         st.session_state.user_id = None
    #         st.rerun()