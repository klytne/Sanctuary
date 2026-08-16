import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700&family=Literata:wght@400;500&display=swap');

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Journal / long-form writing uses Literata, per DESIGN.md */
    textarea, .stTextArea textarea {
        font-family: 'Literata', serif !important;
        font-size: 16px !important;
        line-height: 1.7 !important;
    }

    /* Pill-shaped buttons */
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 999px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
    }

    /* Reusable card surface — wrap content in a div with class="sanctuary-card" */
    .sanctuary-card {
        background: #ffffff;
        border: 1px solid #e4e2dd;
        border-radius: 16px;
        padding: 24px;
    }

    /* Sidebar nav: rounded, spaced-out items so the active page reads as a pill.
    Streamlit already tints the active link with the theme's primaryColor —
    this just adds the shape/spacing around it. Selectors can shift between
    Streamlit versions, so this is deliberately non-critical styling. */
    [data-testid="stSidebarNav"] {
        padding-top: 0.5rem;
    }
    [data-testid="stSidebarNavItems"] li {
        margin: 2px 8px;
    }
    [data-testid="stSidebarNavItems"] li a {
        border-radius: 999px !important;
        padding: 0.5rem 1rem !important;
    }
</style>
"""

def inject_global_css():
    st.markdown(CSS, unsafe_allow_html=True)