import streamlit as st
from core import data_manager as dm
from core.styles import inject_global_css

st.set_page_config(page_title="Sanctuary - Log in", page_icon=":material/spa:")
inject_global_css()

# hide the whole sidebar
st.markdown(
    '<style>[data-testid="stSidebar"] {display: none;}</style>',
    unsafe_allow_html=True,
)

# Centered column so the form doesn't stretch across a wide screen
left, center, right = st.columns([1, 2, 1])

with center:
    st.title(":material/eco: Welcome to Sanctuary")
    st.caption("A gratitude journal to help you reflect, grow, and reconnect with yourself.")
    st.write("")

    login_tab, register_tab = st.tabs(["Log in", "Register"])

    with login_tab:
        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log in", icon=":material/login:", width="stretch")

            if submitted:
                if not login_username or not login_password:
                    st.warning("Please fill in both fields.", icon=":material/warning:")
                else:
                    success, message, user_id = dm.login_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.user_id = user_id
                        st.rerun()
                    else:
                        st.error(message, icon=":material/error:")

    with register_tab:
        with st.form("register_form"):
            reg_username = st.text_input("Choose a username", key="reg_username")
            reg_password = st.text_input("Choose a password", type="password", key="reg_password")
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
            submitted = st.form_submit_button("Register", icon=":material/person_add:", width="stretch")

            if submitted:
                if not reg_username or not reg_password:
                    st.warning("Please fill in all required fields.", icon=":material/warning:")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match.", icon=":material/error:")
                else:
                    success, message, user_id = dm.register_user(
                        reg_username, reg_password, reg_interests
                    )
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = reg_username
                        st.session_state.user_id = user_id
                        st.rerun()
                    else:
                        st.error(message, icon=":material/error:")