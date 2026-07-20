"""
styles.py
Shared visual theme for the whole app: colors, fonts, CSS injection,
and small reusable UI building blocks (hero banner, section cards,
result banners) so every page looks consistent.
"""

import streamlit as st

# ----------------------------------------------------------------------
# Palette — soft clinical-but-warm theme (mint / sky / coral)
# ----------------------------------------------------------------------
COLORS = {
    "mint": "#6DD3CE",
    "mint_dark": "#2E6E68",
    "sky": "#77B7E8",
    "coral": "#FF6B6B",
    "coral_light": "#FF9A8B",
    "healthy_grad": ("#7FE3C0", "#58C9A8"),
    "risk_grad": ("#FF9A8B", "#FF6B6B"),
    "bg_grad": ("#F3FBF9", "#EAF6FB", "#FDF6F0"),
    "text_muted": "#6b7c8a",
}

PLOTLY_COLORWAY = ["#6DD3CE", "#FF6B6B", "#77B7E8", "#FFC46B", "#B79CED", "#58C9A8"]


def inject_css():
    """Call once near the top of every page."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Quicksand', sans-serif !important;
        }

        .stApp {
            background: linear-gradient(160deg, #F3FBF9 0%, #EAF6FB 45%, #FDF6F0 100%);
        }

        .hero {
            background: linear-gradient(120deg, #6DD3CE 0%, #77B7E8 100%);
            padding: 28px 32px;
            border-radius: 20px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 8px 24px rgba(109, 211, 206, 0.35);
        }
        .hero h1 { color: white !important; margin: 0 0 6px 0; font-size: 2.1rem; }
        .hero p { margin: 0; font-size: 1.02rem; opacity: 0.95; }

        .section-card {
            background: white;
            border-radius: 16px;
            padding: 18px 22px 6px 22px;
            margin-bottom: 18px;
            box-shadow: 0 3px 14px rgba(60, 90, 110, 0.08);
            border: 1px solid rgba(120, 170, 180, 0.15);
        }
        .section-title {
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            color: #2E6E68;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .result-healthy {
            background: linear-gradient(120deg, #7FE3C0 0%, #58C9A8 100%);
            padding: 26px 30px;
            border-radius: 18px;
            color: #0B3D33;
            text-align: center;
            box-shadow: 0 10px 26px rgba(88, 201, 168, 0.35);
        }
        .result-risk {
            background: linear-gradient(120deg, #FF9A8B 0%, #FF6B6B 100%);
            padding: 26px 30px;
            border-radius: 18px;
            color: #4A0E0E;
            text-align: center;
            box-shadow: 0 10px 26px rgba(255, 107, 107, 0.35);
        }
        .result-headline { font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 1.8rem; margin-bottom: 4px; }
        .result-sub { font-size: 1.0rem; opacity: 0.9; }

        .nav-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 3px 14px rgba(60, 90, 110, 0.08);
            border: 1px solid rgba(120, 170, 180, 0.15);
            height: 100%;
        }
        .nav-card h3 { margin-top: 0; color: #2E6E68; }
        .nav-card p { color: #5a6a75; font-size: 0.92rem; }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #EAF7F4 0%, #E7F1FB 100%);
        }

        .footer-note { font-size: 0.8rem; color: #6b7c8a; text-align: center; margin-top: 24px; }

        div[data-testid="stMetric"] {
            background: white;
            border-radius: 14px;
            padding: 12px 16px;
            box-shadow: 0 3px 12px rgba(60, 90, 110, 0.07);
            border: 1px solid rgba(120, 170, 180, 0.15);
        }

        .alert-emergency {
            background: #FDEAE7;
            border-left: 6px solid #C4453B;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #6E241D;
        }
        .alert-urgent {
            background: #FFF4E0;
            border-left: 6px solid #E8A93A;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #6B4E12;
        }
        .alert-tip {
            background: #E4F4F0;
            border-left: 6px solid #2E6E68;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #1B4842;
        }
        .alert-title { font-weight: 700; margin-bottom: 4px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def alert_card(level: str, title: str, body: str):
    """level: 'emergency' | 'urgent' | 'tip'"""
    css_class = {"emergency": "alert-emergency", "urgent": "alert-urgent", "tip": "alert-tip"}[level]
    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="alert-title">{title}</div>
            <div>{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_start(title: str):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def section_end():
    st.markdown("</div>", unsafe_allow_html=True)


def result_banner(is_healthy: bool, headline: str, subtext: str):
    css_class = "result-healthy" if is_healthy else "result-risk"
    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="result-headline">{headline}</div>
            <div class="result-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        '<div class="footer-note">Built with Streamlit · Random Forest model · '
        "Educational demo, not a substitute for professional medical advice.</div>",
        unsafe_allow_html=True,
    )
