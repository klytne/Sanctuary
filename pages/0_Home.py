import streamlit as st

st.set_page_config(page_title="Sanctuary", page_icon=":material/spa:", layout="wide")

from core.styles import inject_global_css
inject_global_css()

# No nav on the landing page — same as Login
st.markdown(
    '<style>[data-testid="stSidebar"] {display: none;}</style>',
    unsafe_allow_html=True,
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 0; max-width: 1100px; }

    /* Ambient background — soft, imperfect blobs of color rather than a flat
       fill, per DESIGN.md's "organic textures" + "glow-shadow" language.
       Pure CSS gradients, no image assets. */
    .stApp {
        background:
            radial-gradient(circle at 88% -8%, rgba(71,101,80,0.10) 0%, rgba(71,101,80,0) 55%),
            radial-gradient(circle at -8% 105%, rgba(125,157,133,0.16) 0%, rgba(125,157,133,0) 50%),
            radial-gradient(circle at 105% 100%, rgba(210,230,236,0.40) 0%, rgba(210,230,236,0) 45%),
            #fbf9f4;
    }

    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        font-size: 46px;
        letter-spacing: -0.02em;
        color: #1b1c19;
        text-align: center;
        margin-top: 5vh;
        margin-bottom: 14px;
    }
    .hero-title .accent { color: #476550; }

    .hero-sub {
        font-family: 'Literata', serif;
        font-size: 18px;
        color: #424843;
        max-width: 560px;
        margin: 0 auto;
        line-height: 1.6;
        text-align: center;
    }

    .st-key-chip_journal, .st-key-chip_insights, .st-key-chip_pace {
        text-align: center;
        padding: 10px 8px;
    }
    .st-key-chip_journal p, .st-key-chip_insights p, .st-key-chip_pace p {
        justify-content: center;
    }

    /* Scoped to just these two buttons so their labels never wrap onto a
       second line in the narrow top-right column. */
    .st-key-home_login_btn button, .st-key-home_register_btn button {
        white-space: nowrap;
    }
</style>
""", unsafe_allow_html=True)

# ---------- TOP BAR ----------
col_brand, col_spacer, col_actions = st.columns([2, 4, 3])

with col_brand:
    st.markdown("### :material/eco: Sanctuary")

with col_actions:
    btn_login, btn_register = st.columns(2)
    with btn_login:
        if st.button("Log in", use_container_width=True, key="home_login_btn"):
            st.switch_page("pages/1_Login.py")
    with btn_register:
        if st.button("Register", type="primary", use_container_width=True, key="home_register_btn"):
            st.switch_page("pages/1_Login.py")

# ---------- HERO ----------
st.markdown("""
    <div class="hero-title">A calm space for <span class="accent">gratitude</span></div>
    
    <div class="hero-sub">
        Sanctuary is a gentle journal for reflecting on your day, tracking your mood,
        and noticing the small things worth being thankful for — at your own pace.
    </div>
""", unsafe_allow_html=True)

st.write("")

col_cta = st.columns([4, 2, 4])[1]
with col_cta:
    if st.button("Get started", type="primary", use_container_width=True, icon=":material/arrow_forward:"):
        st.switch_page("pages/1_Login.py")

st.write("")

# ---------- FEATURE HIGHLIGHTS ----------
c1, c2, c3 = st.columns(3)
with c1:
    with st.container(key="chip_journal"):
        st.markdown("##### :material/edit_note: Journal")
        st.caption("Guided prompts, whenever you're ready")
with c2:
    with st.container(key="chip_insights"):
        st.markdown("##### :material/insights: Insights")
        st.caption("See your patterns over time")
with c3:
    with st.container(key="chip_pace"):
        st.markdown("##### :material/spa: Mindful pace")
        st.caption("Gentle nudges, never pressure")