"""NeighborBoost ATL — Hack RenderATL MVP.

Base design/structure from Jasmin’s MVP, with enhancements adapted from
Ulises’s MVP (hot ranking, theme toggle, simulated credit moment, UX polish).
"""

from __future__ import annotations

import random
from typing import Any

import streamlit as st

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NEIGHBORHOODS = [
    "Sweet Auburn",
    "West End",
    "South Atlanta",
    "Downtown",
    "East Atlanta",
    "Grant Park",
    "Old Fourth Ward",
    "Kirkwood",
]

CATEGORIES = [
    "Coffee Shop",
    "Bakery",
    "Retail",
    "Restaurant",
    "Salon / Beauty",
    "Other",
]

SUPPORT_TYPES = ["Visit", "Share", "Help"]

ACTION_LABELS = {
    "Visit": "I’ll Visit",
    "Share": "I’ll Share",
    "Help": "I Can Help",
}

ACTION_DONE_LABELS = {
    "Visit": "✓ Visited",
    "Share": "✓ Shared",
    "Help": "✓ Helped",
}

PLACEHOLDER_STYLES = [
    ("☕", "linear-gradient(135deg, #E07A5F 0%, #F2CC8F 100%)"),
    ("🥐", "linear-gradient(135deg, #81B29A 0%, #F2CC8F 100%)"),
    ("🌿", "linear-gradient(135deg, #3D5A80 0%, #81B29A 100%)"),
    ("🍲", "linear-gradient(135deg, #E07A5F 0%, #3D5A80 100%)"),
    ("💈", "linear-gradient(135deg, #C85A3E 0%, #3D5A80 100%)"),
    ("📚", "linear-gradient(135deg, #2F6F5E 0%, #F2CC8F 100%)"),
    ("🧵", "linear-gradient(135deg, #E07A5F 0%, #81B29A 100%)"),
    ("🎧", "linear-gradient(135deg, #1B2A4A 0%, #E07A5F 100%)"),
]

# Roughly 1-in-5 chance of a cosmetic demo “$5 credit” celebration.
CREDIT_CHANCE = 0.20


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

def make_seed_posts() -> list[dict[str, Any]]:
    """Fictional Atlanta demo businesses — clearly labeled Demo Business."""
    return [
        {
            "id": "demo-peach-bean",
            "business_name": "Peach & Bean Coffee",
            "neighborhood": "Sweet Auburn",
            "category": "Coffee Shop",
            "story": (
                "An independent neighborhood café creating a welcoming "
                "gathering place for local residents."
            ),
            "request": (
                "Help us welcome 10 first-time customers during today’s "
                "afternoon slowdown."
            ),
            "goal": 10,
            "supporters": 4,
            "hours_remaining": 6,
            "support_actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 0,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-nias-bakes",
            "business_name": "Nia’s Neighborhood Bakes",
            "neighborhood": "West End",
            "category": "Bakery",
            "story": (
                "A family-run bakery sharing small-batch pastries inspired "
                "by family recipes."
            ),
            "request": (
                "We have 12 pastry boxes available before closing and want "
                "to prevent food waste."
            ),
            "goal": 12,
            "supporters": 3,
            "hours_remaining": 3,
            "support_actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 1,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-southside-plant",
            "business_name": "Southside Plant Studio",
            "neighborhood": "South Atlanta",
            "category": "Retail",
            "story": (
                "A small plant shop helping residents bring affordable "
                "greenery into their homes."
            ),
            "request": (
                "We need one local photographer to help photograph our "
                "newest products."
            ),
            "goal": 1,
            "supporters": 0,
            "hours_remaining": 24,
            "support_actions": ["Help", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 2,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-cultura-kitchen",
            "business_name": "Cultura Kitchen ATL",
            "neighborhood": "Downtown",
            "category": "Restaurant",
            "story": (
                "A family-operated restaurant preserving traditional recipes "
                "and introducing them to new neighbors."
            ),
            "request": (
                "Help us share our new weekday lunch special with 20 "
                "Atlanta residents."
            ),
            "goal": 20,
            "supporters": 8,
            "hours_remaining": 8,
            "support_actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 3,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-edgewood-cuts",
            "business_name": "Edgewood Cuts & Co.",
            "neighborhood": "Old Fourth Ward",
            "category": "Salon / Beauty",
            "story": (
                "A neighborhood barbershop known for sharp fades and "
                "community conversations on the porch."
            ),
            "request": (
                "We’re quiet until 4 PM — help us fill 6 open chair "
                "slots with walk-ins today."
            ),
            "goal": 6,
            "supporters": 5,
            "hours_remaining": 5,
            "support_actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 4,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-beltline-pages",
            "business_name": "Beltline Pages Bookstore",
            "neighborhood": "Grant Park",
            "category": "Retail",
            "story": (
                "A tiny indie bookstore highlighting Atlanta authors and "
                "hosting free weekend reading hours for kids."
            ),
            "request": (
                "Share our tonight’s author meetup so we can fill the "
                "last 15 seats."
            ),
            "goal": 15,
            "supporters": 11,
            "hours_remaining": 4,
            "support_actions": ["Share", "Visit"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 5,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-kirkwood-stitch",
            "business_name": "Kirkwood Stitch Lab",
            "neighborhood": "Kirkwood",
            "category": "Other",
            "story": (
                "A community sewing studio teaching mending skills and "
                "upcycling clothes instead of tossing them."
            ),
            "request": (
                "We need 2 neighbors who can help set up sewing machines "
                "before tonight’s free class."
            ),
            "goal": 2,
            "supporters": 1,
            "hours_remaining": 7,
            "support_actions": ["Help", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 6,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
        {
            "id": "demo-eastside-vinyl",
            "business_name": "Eastside Vinyl & Tea",
            "neighborhood": "East Atlanta",
            "category": "Retail",
            "story": (
                "A record shop and tea bar where locals dig for vinyl "
                "and linger over Atlanta playlists."
            ),
            "request": (
                "Stop by for our first-timer tea flight special — we want "
                "8 new faces before closing."
            ),
            "goal": 8,
            "supporters": 2,
            "hours_remaining": 9,
            "support_actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
            "placeholder_idx": 7,
            "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
        },
    ]


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

SEED_VERSION = 2  # bump when demo seed data changes


def init_state() -> None:
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if (
        "posts" not in st.session_state
        or st.session_state.get("seed_version") != SEED_VERSION
    ):
        st.session_state.posts = make_seed_posts()
        st.session_state.seed_version = SEED_VERSION
        st.session_state.user_actions = {}
        st.session_state.post_counter = 0
        st.session_state.credit_celebration = None
    if "user_actions" not in st.session_state:
        # {(post_id, action): True}
        st.session_state.user_actions = {}
    if "post_counter" not in st.session_state:
        st.session_state.post_counter = 0
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Discover Local Businesses"
    if "flash_message" not in st.session_state:
        st.session_state.flash_message = None
    if "form_success" not in st.session_state:
        st.session_state.form_success = None
    if "credit_celebration" not in st.session_state:
        st.session_state.credit_celebration = None


def reset_demo() -> None:
    """Restore seed data and clear commitments; keep theme preference."""
    st.session_state.posts = make_seed_posts()
    st.session_state.seed_version = SEED_VERSION
    st.session_state.user_actions = {}
    st.session_state.post_counter = 0
    st.session_state.flash_message = None
    st.session_state.form_success = None
    st.session_state.credit_celebration = None
    st.session_state.active_tab = "Discover Local Businesses"


# ---------------------------------------------------------------------------
# Metrics / ranking helpers
# ---------------------------------------------------------------------------

def compute_metrics(posts: list[dict[str, Any]]) -> tuple[int, int, int]:
    active = len(posts)
    boosted = sum(1 for p in posts if p["supporters"] > 0)
    commitments = sum(p["supporters"] for p in posts)
    return active, boosted, commitments


def progress_ratio(supporters: int, goal: int) -> float:
    if goal <= 0:
        return 0.0
    return min(supporters / goal, 1.0)


def compute_hot_ids(posts: list[dict[str, Any]]) -> set[str]:
    """Posts tied for highest supporter count earn the Hot Right Now badge."""
    if not posts:
        return set()
    max_supporters = max(p["supporters"] for p in posts)
    if max_supporters <= 0:
        return set()
    return {p["id"] for p in posts if p["supporters"] == max_supporters}


def sort_feed(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Hottest businesses first (most supporters), then soonest to expire."""
    return sorted(
        posts,
        key=lambda p: (
            -int(p.get("supporters", 0)),
            int(p.get("hours_remaining", 9999)),
            p["id"],
        ),
    )


# ---------------------------------------------------------------------------
# Theming / CSS (Jasmin visual language + Ulises dark mode)
# ---------------------------------------------------------------------------

def theme_vars(theme: str) -> str:
    if theme == "dark":
        return """
  --peach: #FFB37B;
  --peach-deep: #FFC899;
  --cream: #FFF4E8;
  --cream-deep: #2A3356;
  --navy: #F7F1E8;
  --navy-soft: #D5DBEF;
  --green: #6ED4A0;
  --green-soft: #55C08B;
  --gold: #F2CC8F;
  --white: #FFFFFF;
  --page-bg: #0E1426;
  --card-bg: #1A2340;
  --card-border: rgba(247, 241, 232, 0.18);
  --shadow: 0 10px 28px rgba(0, 0, 0, 0.5);
  --header-bg: linear-gradient(135deg, #1A2340 0%, #222C4D 100%);
  --header-border: rgba(255, 179, 123, 0.45);
  --progress-track: #2F3A5C;
  --sidebar-bg: linear-gradient(180deg, #151C33, #0E1426);
  --hot-bg: #5C2A1C;
  --hot-fg: #FFD0A8;
  --goal-bg: #1F4A38;
  --goal-fg: #A6F0C8;
  --request-bg: #243152;
  --hero-badge-bg: #FFB37B;
  --hero-badge-fg: #1A1208;
  --demo-bg: #5C2A1C;
  --demo-fg: #FFD0A8;
  --meta-bg: #1F4A38;
  --meta-fg: #A6F0C8;
  --time-bg: #2A3A66;
  --time-fg: #D5DBEF;
  --input-bg: #151C33;
  --input-border: rgba(247, 241, 232, 0.28);
  --muted-surface: rgba(247, 241, 232, 0.06);
"""
    return """
  --peach: #E07A5F;
  --peach-deep: #C85A3E;
  --cream: #FFF8F1;
  --cream-deep: #FFE8D6;
  --navy: #1B2A4A;
  --navy-soft: #3D5A80;
  --green: #2F6F5E;
  --green-soft: #81B29A;
  --gold: #F2CC8F;
  --white: #FFFFFF;
  --page-bg: #FFF8F1;
  --card-bg: #FFFFFF;
  --card-border: rgba(27, 42, 74, 0.08);
  --shadow: 0 8px 24px rgba(27, 42, 74, 0.08);
  --header-bg: linear-gradient(135deg, rgba(255,248,241,0.95), rgba(255,232,214,0.92));
  --header-border: rgba(224, 122, 95, 0.28);
  --progress-track: #F0E6DC;
  --sidebar-bg: linear-gradient(180deg, #FFF4EA, #FFE8D6);
  --hot-bg: #FFE1D6;
  --hot-fg: #C1440E;
  --goal-bg: #E8F2ED;
  --goal-fg: #2F6F5E;
  --request-bg: #FFF4EA;
  --hero-badge-bg: #1B2A4A;
  --hero-badge-fg: #FFF8F1;
  --demo-bg: #FFE0C8;
  --demo-fg: #8A3B22;
  --meta-bg: #E8F2ED;
  --meta-fg: #2F6F5E;
  --time-bg: #E7EEF8;
  --time-fg: #3D5A80;
  --input-bg: #FFFFFF;
  --input-border: rgba(27, 42, 74, 0.18);
  --muted-surface: rgba(27, 42, 74, 0.04);
"""


def inject_css(theme: str) -> None:
    vars_css = theme_vars(theme)
    bg_layers = (
        "radial-gradient(circle at 12% 8%, rgba(255,179,123,0.12), transparent 36%),"
        "radial-gradient(circle at 88% 0%, rgba(85,192,139,0.12), transparent 32%),"
        "linear-gradient(180deg, #101528 0%, #171E35 45%, #101528 100%)"
        if theme == "dark"
        else
        "radial-gradient(circle at 12% 8%, rgba(224, 122, 95, 0.18), transparent 36%),"
        "radial-gradient(circle at 88% 0%, rgba(129, 178, 154, 0.22), transparent 32%),"
        "linear-gradient(180deg, #FFF8F1 0%, #FFEDE0 45%, #FFF8F1 100%)"
    )

    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:wght@400;500;600;700&display=swap');

:root {{
{vars_css}
}}

html, body, [class*="css"] {{
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  color: var(--navy);
}}

.stApp {{
  background: {bg_layers};
  color: var(--navy);
}}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {{
  background: transparent;
  color: var(--navy);
}}

.main .block-container {{
  padding-top: 1.4rem;
  padding-bottom: 2.5rem;
  max-width: 980px;
}}

/* Streamlit text & controls — keep contrast even in dark mode */
.stMarkdown, .stMarkdown p, .stMarkdown span, .stCaption, .stText,
label, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span, [data-testid="stCaption"] {{
  color: var(--navy) !important;
}}

h1, h2, h3, .brand-title, [data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {{
  font-family: "Fraunces", Georgia, serif !important;
  color: var(--navy) !important;
  letter-spacing: -0.02em;
}}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
.stTextInput input, .stTextArea textarea, .stNumberInput input,
.stMultiSelect [data-baseweb="select"] {{
  background-color: var(--input-bg) !important;
  color: var(--navy) !important;
  border-color: var(--input-border) !important;
}}

div[data-baseweb="select"] *,
.stTextInput input, .stTextArea textarea, .stNumberInput input {{
  color: var(--navy) !important;
}}

[data-baseweb="menu"],
[data-baseweb="popover"] {{
  background-color: var(--card-bg) !important;
  color: var(--navy) !important;
}}

[data-baseweb="menu"] li,
[role="option"] {{
  color: var(--navy) !important;
}}

.nb-header {{
  background: var(--header-bg);
  border: 1px solid var(--header-border);
  border-radius: 22px;
  padding: 1.4rem 1.5rem 1.2rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.1rem;
}}

.nb-badge {{
  display: inline-block;
  background: var(--hero-badge-bg);
  color: var(--hero-badge-fg);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  margin-bottom: 0.75rem;
}}

.brand-title {{
  font-size: clamp(1.9rem, 4vw, 2.55rem);
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  line-height: 1.1;
}}

.brand-tagline {{
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--peach-deep);
  margin: 0 0 0.55rem 0;
}}

.brand-desc {{
  margin: 0;
  color: var(--navy-soft);
  font-size: 1.02rem;
  line-height: 1.45;
  max-width: 42rem;
}}

.impact-wrap {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  margin: 0.4rem 0 1.1rem;
}}

.impact-card {{
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 16px;
  padding: 0.95rem 1rem;
  box-shadow: var(--shadow);
  text-align: center;
}}

.impact-value {{
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.85rem;
  font-weight: 700;
  color: var(--green);
  line-height: 1;
  margin-bottom: 0.35rem;
}}

.impact-label {{
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--navy-soft);
  line-height: 1.25;
}}

.biz-card {{
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 20px;
  padding: 1.15rem 1.2rem 1.05rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.1rem;
}}

.biz-card.is-hot {{
  border-color: rgba(224, 122, 95, 0.45);
  box-shadow: 0 10px 28px rgba(224, 122, 95, 0.16);
}}

.biz-top {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.45rem 0.55rem;
  margin-bottom: 0.55rem;
}}

.biz-name {{
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--navy);
  margin: 0;
}}

.badge {{
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  padding: 0.28rem 0.55rem;
  border-radius: 999px;
}}

.badge-demo {{
  background: var(--demo-bg);
  color: var(--demo-fg);
}}

.badge-meta {{
  background: var(--meta-bg);
  color: var(--meta-fg);
}}

.badge-time {{
  background: var(--time-bg);
  color: var(--time-fg);
}}

.badge-hot {{
  background: var(--hot-bg);
  color: var(--hot-fg);
}}

.badge-goal {{
  background: var(--goal-bg);
  color: var(--goal-fg);
}}

.biz-story {{
  color: var(--navy);
  line-height: 1.45;
  margin: 0.35rem 0;
  font-size: 0.98rem;
}}

.biz-request {{
  color: var(--navy);
  line-height: 1.45;
  margin: 0.55rem 0 0.35rem;
  font-size: 0.98rem;
  background: var(--request-bg);
  border-left: 4px solid var(--green);
  border-radius: 8px;
  padding: 0.65rem 0.8rem;
}}

.biz-request strong {{
  color: var(--peach-deep);
}}

.media-placeholder {{
  width: 100%;
  min-height: 140px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
  margin: 0.65rem 0 0.85rem;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.25);
}}

.progress-track {{
  width: 100%;
  height: 12px;
  background: var(--progress-track);
  border-radius: 999px;
  overflow: hidden;
  margin: 0.45rem 0 0.35rem;
}}

.progress-fill {{
  height: 100%;
  background: linear-gradient(90deg, var(--green-soft), var(--green));
  border-radius: 999px;
  transition: width 0.35s ease;
}}

.progress-meta {{
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--navy-soft);
  margin-bottom: 0.55rem;
}}

.support-label {{
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--navy);
  margin: 0.2rem 0 0.15rem;
}}

div.stButton > button {{
  border-radius: 12px !important;
  font-weight: 700 !important;
  min-height: 2.7rem;
  border: 1px solid transparent !important;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}}

div.stButton > button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(27, 42, 74, 0.12);
}}

div.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, var(--peach), var(--peach-deep)) !important;
  color: white !important;
}}

div.stButton > button[kind="secondary"] {{
  background: var(--cream-deep) !important;
  color: var(--navy) !important;
  border: 1px solid var(--input-border) !important;
}}

div.stButton > button:disabled {{
  opacity: 0.85 !important;
  color: var(--navy-soft) !important;
  background: var(--muted-surface) !important;
  border: 1px solid var(--input-border) !important;
}}

section[data-testid="stSidebar"] {{
  background: var(--sidebar-bg);
  border-right: 1px solid var(--header-border);
  color: var(--navy);
}}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {{
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  color: var(--navy) !important;
}}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
  font-family: "Fraunces", Georgia, serif !important;
}}

/* Tabs readable on dark backgrounds */
button[data-baseweb="tab"] {{
  color: var(--navy-soft) !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  color: var(--navy) !important;
}}

.nb-footer {{
  margin-top: 1.8rem;
  padding: 1.1rem 0.4rem 0.2rem;
  border-top: 1px solid var(--card-border);
  text-align: center;
  color: var(--navy-soft);
  font-size: 0.92rem;
  line-height: 1.5;
}}

.nb-footer strong {{
  color: var(--navy);
}}

.empty-state {{
  background: var(--muted-surface);
  border: 1px dashed var(--input-border);
  border-radius: 16px;
  padding: 1.4rem;
  text-align: center;
  color: var(--navy-soft);
}}

/* Hide Streamlit hover tooltips (keyboard shortcut hints, widget help) */
div[data-testid="stTooltipContent"],
[data-testid="stTooltipContent"],
.stTooltipContent {{
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}}

@media (max-width: 700px) {{
  .impact-wrap {{
    grid-template-columns: 1fr;
  }}
  .biz-card {{
    padding: 1rem;
  }}
  .main .block-container {{
    padding-left: 0.9rem;
    padding-right: 0.9rem;
  }}
}}
</style>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# UI pieces
# ---------------------------------------------------------------------------

def render_header() -> None:
    st.markdown(
        """
        <div class="nb-header">
          <div class="nb-badge">Built for Hack RenderATL</div>
          <h1 class="brand-title">NeighborBoost ATL</h1>
          <p class="brand-tagline">Atlanta shows up for Atlanta.</p>
          <p class="brand-desc">
            Discover one simple action you can take to support an Atlanta
            small business today.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_impact(posts: list[dict[str, Any]]) -> None:
    active, boosted, commitments = compute_metrics(posts)
    st.markdown(
        f"""
        <div class="impact-wrap">
          <div class="impact-card">
            <div class="impact-value">{active}</div>
            <div class="impact-label">Active business requests</div>
          </div>
          <div class="impact-card">
            <div class="impact-value">{boosted}</div>
            <div class="impact-label">Local businesses boosted</div>
          </div>
          <div class="impact-card">
            <div class="impact-value">{commitments}</div>
            <div class="impact-label">Total neighbor commitments</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_media(post: dict[str, Any]) -> None:
    media_bytes = post.get("media_bytes")
    media_type = post.get("media_type")

    if media_bytes and media_type:
        if media_type.startswith("image/"):
            st.image(media_bytes, use_container_width=True)
            return
        if media_type.startswith("video/"):
            try:
                st.video(media_bytes)
                return
            except Exception:
                st.caption("Video preview unavailable — photo upload is preferred.")

    idx = post.get("placeholder_idx", 0) % len(PLACEHOLDER_STYLES)
    emoji, gradient = PLACEHOLDER_STYLES[idx]
    st.markdown(
        f"""
        <div class="media-placeholder" style="background: {gradient};" aria-hidden="true">
          {emoji}
        </div>
        """,
        unsafe_allow_html=True,
    )


def record_support(post_id: str, action: str) -> None:
    key = (post_id, action)
    if key in st.session_state.user_actions:
        st.session_state.flash_message = (
            f"You already committed to “{action}” for this business. "
            "Thank you — one commitment per action goes a long way."
        )
        return

    business_name = ""
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["supporters"] += 1
            post["actions_taken"][action] = post["actions_taken"].get(action, 0) + 1
            business_name = post["business_name"]
            break

    st.session_state.user_actions[key] = True
    st.session_state.flash_message = (
        f"Thank you! Your “{action}” commitment for {business_name} is locked in. "
        "Atlanta shows up for Atlanta."
    )

    # Cosmetic demo reward only — no real money or payments.
    if random.random() < CREDIT_CHANCE:
        st.session_state.credit_celebration = business_name


def render_business_card(post: dict[str, Any], is_hot: bool = False) -> None:
    ratio = progress_ratio(post["supporters"], post["goal"])
    pct = int(round(ratio * 100))
    goal_met = post["supporters"] >= post["goal"]

    badges = []
    if post.get("is_demo"):
        badges.append('<span class="badge badge-demo">Demo Business</span>')
    else:
        badges.append('<span class="badge badge-meta">Community Post</span>')
    if is_hot:
        badges.append('<span class="badge badge-hot">🔥 Hot Right Now</span>')
    if goal_met:
        badges.append('<span class="badge badge-goal">Goal Met</span>')
    badges.append(f'<span class="badge badge-meta">{post["neighborhood"]}</span>')
    badges.append(f'<span class="badge badge-meta">{post["category"]}</span>')
    badges.append(
        f'<span class="badge badge-time">{post["hours_remaining"]} hours left</span>'
    )
    badge_html = "".join(badges)
    hot_class = " is-hot" if is_hot else ""

    st.markdown(f'<div class="biz-card{hot_class}">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="biz-top">
          <h3 class="biz-name">{post["business_name"]}</h3>
          {badge_html}
        </div>
        <p class="biz-story">{post["story"]}</p>
        <p class="biz-request"><strong>Needs today:</strong> {post["request"]}</p>
        """,
        unsafe_allow_html=True,
    )

    render_media(post)

    st.markdown(
        f"""
        <div class="progress-meta">
          <span>{post["supporters"]} of {post["goal"]} supporters</span>
          <span>{pct}%</span>
        </div>
        <div class="progress-track" role="progressbar"
             aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}">
          <div class="progress-fill" style="width: {pct}%;"></div>
        </div>
        <p class="support-label">How will you show up?</p>
        """,
        unsafe_allow_html=True,
    )

    available = set(post.get("support_actions", SUPPORT_TYPES))
    cols = st.columns(3)
    for col, action in zip(cols, SUPPORT_TYPES):
        with col:
            already = (post["id"], action) in st.session_state.user_actions
            enabled = action in available and not already
            btn_label = (
                ACTION_DONE_LABELS[action] if already else ACTION_LABELS[action]
            )
            if st.button(
                btn_label,
                key=f"support-{post['id']}-{action}",
                disabled=not enabled,
                use_container_width=True,
                type="primary" if enabled else "secondary",
            ):
                if enabled:
                    record_support(post["id"], action)
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def filter_posts(
    posts: list[dict[str, Any]],
    neighborhood: str,
    category: str,
    support_type: str,
) -> list[dict[str, Any]]:
    result = posts
    if neighborhood != "All":
        result = [p for p in result if p["neighborhood"] == neighborhood]
    if category != "All":
        result = [p for p in result if p["category"] == category]
    if support_type != "All":
        result = [p for p in result if support_type in p.get("support_actions", [])]
    return result


def discover_tab() -> None:
    if st.session_state.flash_message:
        st.success(st.session_state.flash_message)
        st.session_state.flash_message = None

    if st.session_state.form_success:
        st.success(st.session_state.form_success)
        st.session_state.form_success = None

    render_impact(st.session_state.posts)

    st.subheader("Find a business to boost")
    f1, f2, f3, f4 = st.columns([1.2, 1.2, 1.2, 0.8])
    with f1:
        neighborhood = st.selectbox(
            "Neighborhood",
            ["All"] + NEIGHBORHOODS,
            key="filter-neighborhood",
        )
    with f2:
        category = st.selectbox(
            "Business category",
            ["All"] + CATEGORIES,
            key="filter-category",
        )
    with f3:
        support_type = st.selectbox(
            "Type of support needed",
            ["All"] + SUPPORT_TYPES,
            key="filter-support",
        )
    with f4:
        st.write("")  # align with selectboxes
        st.write("")
        if st.button("Clear filters", key="clear-filters", use_container_width=True):
            st.session_state["filter-neighborhood"] = "All"
            st.session_state["filter-category"] = "All"
            st.session_state["filter-support"] = "All"
            st.rerun()

    filtered = filter_posts(
        st.session_state.posts, neighborhood, category, support_type
    )
    filtered = sort_feed(filtered)
    hot_ids = compute_hot_ids(st.session_state.posts)

    st.caption(
        f"Showing {len(filtered)} request(s), hottest first. "
        "🔥 marks the top-supported business(es) citywide."
    )

    if not filtered:
        st.markdown(
            """
            <div class="empty-state">
              No requests match these filters. Try “Clear filters” or post a new request.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for post in filtered:
        render_business_card(post, is_hot=post["id"] in hot_ids)


def post_request_tab() -> None:
    st.subheader("Post a time-sensitive request")
    st.write(
        "Share one clear need your Atlanta mom-and-pop business has today. "
        "Neighbors can commit to visit, share, or help."
    )

    with st.form("post-request-form", clear_on_submit=True):
        business_name = st.text_input(
            "Business name *",
            placeholder="e.g. Peach & Bean Coffee",
            key="form-business-name",
        )
        c1, c2 = st.columns(2)
        with c1:
            neighborhood = st.selectbox(
                "Atlanta neighborhood *",
                NEIGHBORHOODS,
                key="form-neighborhood",
            )
        with c2:
            category = st.selectbox(
                "Business category *",
                CATEGORIES,
                key="form-category",
            )

        story = st.text_area(
            "Short business story *",
            placeholder="Tell neighbors who you are in 1–2 sentences.",
            max_chars=280,
            key="form-story",
        )
        request = st.text_area(
            "What support do you need today? *",
            placeholder="One immediate, time-sensitive need.",
            max_chars=280,
            key="form-request",
        )

        g1, g2 = st.columns(2)
        with g1:
            goal = st.number_input(
                "Support goal *",
                min_value=1,
                max_value=500,
                value=10,
                step=1,
                key="form-goal",
            )
        with g2:
            hours_remaining = st.number_input(
                "Expiration time (hours) *",
                min_value=1,
                max_value=168,
                value=6,
                step=1,
                key="form-hours",
            )

        support_actions = st.multiselect(
            "Available support actions *",
            SUPPORT_TYPES,
            default=["Visit", "Share"],
            key="form-actions",
        )

        media = st.file_uploader(
            "Optional photo or short video",
            type=["png", "jpg", "jpeg", "mp4"],
            key="form-media",
        )

        submitted = st.form_submit_button(
            "Publish request",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    errors: list[str] = []
    if not business_name or not business_name.strip():
        errors.append("Business name is required.")
    if not story or not story.strip():
        errors.append("Business story is required.")
    if not request or not request.strip():
        errors.append("Today’s support request is required.")
    if not support_actions:
        errors.append("Select at least one support action.")

    if errors:
        for err in errors:
            st.error(err)
        return

    media_bytes = None
    media_type = None
    if media is not None:
        try:
            media_bytes = media.getvalue()
            media_type = media.type or ""
            if media_type.startswith("video/") and len(media_bytes) > 8_000_000:
                st.warning(
                    "Video is larger than 8MB for this prototype. "
                    "Publishing without video — try a photo instead."
                )
                media_bytes = None
                media_type = None
        except Exception:
            st.warning("Could not process the upload. Publishing without media.")
            media_bytes = None
            media_type = None

    st.session_state.post_counter += 1
    new_post = {
        "id": f"user-{st.session_state.post_counter}",
        "business_name": business_name.strip(),
        "neighborhood": neighborhood,
        "category": category,
        "story": story.strip(),
        "request": request.strip(),
        "goal": int(goal),
        "supporters": 0,
        "hours_remaining": int(hours_remaining),
        "support_actions": list(support_actions),
        "is_demo": False,
        "media_bytes": media_bytes,
        "media_type": media_type,
        "placeholder_idx": st.session_state.post_counter % len(PLACEHOLDER_STYLES),
        "actions_taken": {"Visit": 0, "Share": 0, "Help": 0},
    }

    st.session_state.posts = [new_post] + list(st.session_state.posts)
    st.session_state.form_success = (
        f"“{new_post['business_name']}” is live! "
        "Open the Discover Local Businesses tab to see your request."
    )
    st.session_state.active_tab = "Discover Local Businesses"
    st.success(st.session_state.form_success)
    st.info("Select the **Discover Local Businesses** tab to view your new card.")


def render_footer() -> None:
    st.markdown(
        """
        <div class="nb-footer">
          <strong>Built in Atlanta for Hack RenderATL</strong><br/>
          Supporting local businesses through community action<br/>
          Seeded businesses are fictional and provided only for demonstration.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(
        page_title="NeighborBoost ATL",
        page_icon="🍑",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_state()

    # Sidebar first so theme changes apply in the same rerun (Ulises pattern).
    with st.sidebar:
        st.markdown("### NeighborBoost ATL")
        st.caption("Atlanta shows up for Atlanta.")
        is_dark = st.toggle(
            "Dark mode",
            value=(st.session_state.theme == "dark"),
            key="theme-toggle",
        )
        st.session_state.theme = "dark" if is_dark else "light"
        st.write(
            "This hackathon prototype stores posts and support actions in "
            "session state only — refresh or reset to start clean."
        )
        st.divider()
        if st.button("Reset Demo", key="reset-demo", use_container_width=True):
            reset_demo()
            st.rerun()
        st.caption(
            "Restores the seeded demo businesses and clears commitments. "
            "Your theme preference is kept."
        )

    inject_css(st.session_state.theme)

    # Simulated $5 credit celebration (cosmetic only).
    if st.session_state.credit_celebration:
        biz = st.session_state.credit_celebration
        st.success(
            f"🎉 You’ve won a $5 credit to visit **{biz}**! "
            "(Simulated demo reward — not real currency.)"
        )
        st.balloons()
        st.session_state.credit_celebration = None

    render_header()

    tab_discover, tab_post = st.tabs(
        ["Discover Local Businesses", "Post a Request"]
    )

    # Render Post first so a just-submitted request appears in Discover
    # on the same rerun (Ulises pattern); visual tab order is unchanged.
    with tab_post:
        post_request_tab()
    with tab_discover:
        discover_tab()

    render_footer()


if __name__ == "__main__":
    main()
