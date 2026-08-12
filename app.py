"""
NeighborBoost ATL — "Atlanta shows up for Atlanta."

A Hack RenderATL "Best Hack for Good" MVP built with Streamlit.

Helps Atlanta mom-and-pop businesses post one immediate, time-sensitive need,
so community members can commit to visiting, sharing, or helping.

See README.md for known limitations of this session-based demo.
"""

import random
import uuid

import streamlit as st

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="NeighborBoost ATL",
    page_icon="🍑",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATEGORY_ICONS = {
    "Coffee Shop": "☕",
    "Bakery": "🥐",
    "Retail": "🌱",
    "Restaurant": "🍽️",
}
DEFAULT_ICON = "🏪"

ACTION_LABELS = {
    "Visit": "🚶 I'll Visit",
    "Share": "📣 I'll Share",
    "Help": "🤝 I Can Help",
}

ACTION_PAST_TENSE = {
    "Visit": "✓ Visited",
    "Share": "✓ Shared",
    "Help": "✓ Helped",
}

ALL_ACTIONS = ["Visit", "Share", "Help"]


# --------------------------------------------------------------------------
# Seed data
# --------------------------------------------------------------------------
def get_seed_posts():
    return [
        {
            "id": "demo-1",
            "name": "Peach & Bean Coffee",
            "neighborhood": "Sweet Auburn",
            "category": "Coffee Shop",
            "story": (
                "An independent neighborhood café creating a welcoming "
                "gathering place for local residents."
            ),
            "request": "Help us welcome 10 first-time customers during today's afternoon slowdown.",
            "goal": 10,
            "supporters": 4,
            "time_remaining": "6 hours",
            "actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
        },
        {
            "id": "demo-2",
            "name": "Nia's Neighborhood Bakes",
            "neighborhood": "West End",
            "category": "Bakery",
            "story": (
                "A family-run bakery sharing small-batch pastries inspired "
                "by family recipes."
            ),
            "request": "We have 12 pastry boxes available before closing and want to prevent food waste.",
            "goal": 12,
            "supporters": 3,
            "time_remaining": "3 hours",
            "actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
        },
        {
            "id": "demo-3",
            "name": "Southside Plant Studio",
            "neighborhood": "South Atlanta",
            "category": "Retail",
            "story": (
                "A small plant shop helping residents bring affordable "
                "greenery into their homes."
            ),
            "request": "We need one local photographer to help photograph our newest products.",
            "goal": 1,
            "supporters": 0,
            "time_remaining": "24 hours",
            "actions": ["Help", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
        },
        {
            "id": "demo-4",
            "name": "Cultura Kitchen ATL",
            "neighborhood": "Downtown",
            "category": "Restaurant",
            "story": (
                "A family-operated restaurant preserving traditional "
                "recipes and introducing them to new neighbors."
            ),
            "request": "Help us share our new weekday lunch special with 20 Atlanta residents.",
            "goal": 20,
            "supporters": 8,
            "time_remaining": "8 hours",
            "actions": ["Visit", "Share"],
            "is_demo": True,
            "media_bytes": None,
            "media_type": None,
        },
    ]


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
def init_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "posts" not in st.session_state:
        st.session_state.posts = get_seed_posts()
    if "actions_taken" not in st.session_state:
        st.session_state.actions_taken = {}  # post_id -> set of actions
    if "confirmations" not in st.session_state:
        st.session_state.confirmations = {}  # post_id -> message
    if "credit_celebration" not in st.session_state:
        st.session_state.credit_celebration = None


def reset_demo():
    st.session_state.posts = get_seed_posts()
    st.session_state.actions_taken = {}
    st.session_state.confirmations = {}
    st.session_state.credit_celebration = None
    # theme is intentionally preserved


# --------------------------------------------------------------------------
# Theming / CSS
# --------------------------------------------------------------------------
def inject_css():
    if st.session_state.theme == "dark":
        vars_css = """
            --nb-bg: #101528;
            --nb-bg-alt: #171e35;
            --nb-card-bg: #1c2440;
            --nb-card-border: #303c66;
            --nb-text: #F5EDE3;
            --nb-text-muted: #C7CCDE;
            --nb-peach: #FFB37B;
            --nb-peach-strong: #FF9F5B;
            --nb-cream: #2A3356;
            --nb-navy: #F5EDE3;
            --nb-green: #55C08B;
            --nb-green-strong: #3EA873;
            --nb-shadow: rgba(0, 0, 0, 0.45);
        """
    else:
        vars_css = """
            --nb-bg: #FFF8F0;
            --nb-bg-alt: #FFEFE0;
            --nb-card-bg: #FFFFFF;
            --nb-card-border: #F0DCC8;
            --nb-text: #1B2A4A;
            --nb-text-muted: #5B6785;
            --nb-peach: #FFB37B;
            --nb-peach-strong: #FF9143;
            --nb-cream: #FFF3E4;
            --nb-navy: #1B2A4A;
            --nb-green: #2E7D5B;
            --nb-green-strong: #21633f;
            --nb-shadow: rgba(27, 42, 74, 0.12);
        """

    st.markdown(
        f"""
        <style>
        :root {{
            {vars_css}
        }}

        .stApp {{
            background: var(--nb-bg);
        }}

        [data-testid="stAppViewContainer"] {{
            background: var(--nb-bg);
        }}
        [data-testid="stSidebar"] {{
            background: var(--nb-bg-alt);
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}

        html, body, p, span, div, label, li {{
            color: var(--nb-text);
        }}

        /* ---------- Header ---------- */
        .nb-title {{
            font-size: 2.6rem;
            font-weight: 800;
            color: var(--nb-navy);
            margin-bottom: 0;
            line-height: 1.1;
        }}
        .nb-tagline {{
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--nb-green);
            margin-top: 0.2rem;
            margin-bottom: 0.4rem;
        }}
        .nb-subdesc {{
            font-size: 1rem;
            color: var(--nb-text-muted);
            max-width: 640px;
            margin-bottom: 0.8rem;
        }}
        .nb-hero-badge {{
            display: inline-block;
            background: var(--nb-navy);
            color: var(--nb-bg);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            margin-bottom: 0.8rem;
        }}

        /* ---------- Impact stats ---------- */
        .nb-stat-card {{
            background: linear-gradient(135deg, var(--nb-peach) 0%, var(--nb-peach-strong) 100%);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            color: #221208;
            text-align: center;
            box-shadow: 0 4px 14px var(--nb-shadow);
            height: 100%;
        }}
        .nb-stat-number {{
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.1;
        }}
        .nb-stat-label {{
            font-size: 0.85rem;
            font-weight: 600;
            opacity: 0.85;
            margin-top: 0.15rem;
        }}

        /* ---------- Business cards ---------- */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div.nb-card-marker) {{
            background: var(--nb-card-bg);
            border: 1px solid var(--nb-card-border);
            border-radius: 18px;
            box-shadow: 0 6px 18px var(--nb-shadow);
            padding: 0.4rem 0.2rem;
            margin-bottom: 1.1rem;
        }}

        .nb-card-media {{
            font-size: 3rem;
            text-align: center;
            background: var(--nb-cream);
            border-radius: 14px;
            padding: 1.4rem 0;
            margin-bottom: 0.6rem;
        }}

        .nb-badge-row {{
            margin-bottom: 0.35rem;
        }}
        .nb-badge {{
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.22rem 0.6rem;
            border-radius: 999px;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }}
        .nb-badge-demo {{
            background: var(--nb-cream);
            color: var(--nb-text-muted);
            border: 1px solid var(--nb-card-border);
        }}
        .nb-badge-hot {{
            background: #FFE1D6;
            color: #C1440E;
            border: 1px solid #FFAE8A;
        }}
        .nb-badge-user {{
            background: var(--nb-green);
            color: #ffffff;
        }}

        .nb-biz-name {{
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--nb-navy);
            margin-bottom: 0.1rem;
        }}
        .nb-biz-meta {{
            font-size: 0.85rem;
            color: var(--nb-text-muted);
            margin-bottom: 0.5rem;
        }}
        .nb-biz-story {{
            font-size: 0.92rem;
            color: var(--nb-text);
            margin-bottom: 0.5rem;
        }}
        .nb-biz-request {{
            font-size: 0.95rem;
            font-weight: 600;
            background: var(--nb-cream);
            border-left: 4px solid var(--nb-green);
            padding: 0.55rem 0.7rem;
            border-radius: 8px;
            margin-bottom: 0.6rem;
        }}
        .nb-time-remaining {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--nb-peach-strong);
            margin-bottom: 0.5rem;
        }}

        /* ---------- Progress bar ---------- */
        .nb-progress-track {{
            width: 100%;
            height: 14px;
            background: var(--nb-cream);
            border-radius: 999px;
            overflow: hidden;
            border: 1px solid var(--nb-card-border);
        }}
        .nb-progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--nb-green) 0%, var(--nb-green-strong) 100%);
            border-radius: 999px;
            transition: width 0.3s ease;
        }}
        .nb-progress-caption {{
            font-size: 0.8rem;
            color: var(--nb-text-muted);
            margin-top: 0.25rem;
            margin-bottom: 0.6rem;
        }}

        /* ---------- Buttons ---------- */
        .stButton > button {{
            border-radius: 12px;
            font-weight: 700;
            padding: 0.5rem 0.6rem;
            border: 1.5px solid var(--nb-green);
            background: var(--nb-green);
            color: #ffffff;
            width: 100%;
            min-height: 2.6rem;
        }}
        .stButton > button:hover {{
            background: var(--nb-green-strong);
            border-color: var(--nb-green-strong);
            color: #ffffff;
        }}
        .stButton > button:disabled {{
            background: var(--nb-cream);
            color: var(--nb-text-muted);
            border-color: var(--nb-card-border);
        }}
        .stFormSubmitButton > button {{
            background: var(--nb-peach-strong);
            border: 1.5px solid var(--nb-peach-strong);
            color: #221208;
            border-radius: 12px;
            font-weight: 700;
            width: 100%;
            min-height: 2.8rem;
        }}
        .stFormSubmitButton > button:hover {{
            background: var(--nb-peach);
            border-color: var(--nb-peach);
        }}

        /* ---------- Footer ---------- */
        .nb-footer {{
            text-align: center;
            color: var(--nb-text-muted);
            font-size: 0.82rem;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--nb-card-border);
        }}

        /* ---------- Responsive ---------- */
        @media (max-width: 640px) {{
            .nb-title {{ font-size: 2rem; }}
            .nb-stat-number {{ font-size: 1.5rem; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def compute_hot_ids(posts):
    if not posts:
        return set()
    max_supporters = max(p["supporters"] for p in posts)
    if max_supporters <= 0:
        return set()
    return {p["id"] for p in posts if p["supporters"] == max_supporters}


def handle_support_action(post, action):
    post_id = post["id"]
    taken = st.session_state.actions_taken.setdefault(post_id, set())
    if action in taken:
        return  # already recorded for this visitor this session

    taken.add(action)
    post["supporters"] += 1
    st.session_state.confirmations[post_id] = (
        f"🙌 Thanks for choosing to {action.lower()} **{post['name']}**! "
        f"Your commitment has been recorded."
    )

    # Roughly 1-in-5 chance of a celebratory (simulated, cosmetic-only) $5 credit moment.
    if random.random() < 0.2:
        st.session_state.credit_celebration = post["name"]


def render_impact_summary(posts):
    active_requests = len(posts)
    businesses_boosted = len({p["id"] for p in posts if p["supporters"] > 0})
    total_commitments = sum(p["supporters"] for p in posts)

    cols = st.columns(3)
    stats = [
        (active_requests, "Active Business Requests"),
        (businesses_boosted, "Local Businesses Boosted"),
        (total_commitments, "Total Neighbor Commitments"),
    ]
    for col, (number, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="nb-stat-card">
                    <div class="nb-stat-number">{number}</div>
                    <div class="nb-stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_card(post, is_hot):
    with st.container(border=True):
        st.markdown('<div class="nb-card-marker"></div>', unsafe_allow_html=True)

        # Media (uploaded photo or emoji placeholder)
        if post.get("media_bytes") and post.get("media_type") == "image":
            st.image(post["media_bytes"], use_container_width=True)
        else:
            icon = CATEGORY_ICONS.get(post["category"], DEFAULT_ICON)
            st.markdown(f'<div class="nb-card-media">{icon}</div>', unsafe_allow_html=True)

        # Badges
        badges = ""
        if post["is_demo"]:
            badges += '<span class="nb-badge nb-badge-demo">Demo Business</span>'
        else:
            badges += '<span class="nb-badge nb-badge-user">Community Submitted</span>'
        if is_hot:
            badges += '<span class="nb-badge nb-badge-hot">🔥 Hot Right Now</span>'
        st.markdown(f'<div class="nb-badge-row">{badges}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="nb-biz-name">{post["name"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="nb-biz-meta">📍 {post["neighborhood"]} &nbsp;•&nbsp; {post["category"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="nb-biz-story">{post["story"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="nb-biz-request">📌 {post["request"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="nb-time-remaining">⏳ {post["time_remaining"]} remaining</div>',
            unsafe_allow_html=True,
        )

        goal = max(1, post["goal"])
        pct = min(100, int(round(post["supporters"] / goal * 100)))
        st.markdown(
            f"""
            <div class="nb-progress-track">
                <div class="nb-progress-fill" style="width:{pct}%;"></div>
            </div>
            <div class="nb-progress-caption">{post['supporters']} of {post['goal']} supporters &nbsp;({pct}%)</div>
            """,
            unsafe_allow_html=True,
        )

        taken = st.session_state.actions_taken.get(post["id"], set())
        available = [a for a in ALL_ACTIONS if a in post["actions"]]
        cols = st.columns(len(available)) if available else []
        for col, action in zip(cols, available):
            with col:
                already_done = action in taken
                label = ACTION_PAST_TENSE[action] if already_done else ACTION_LABELS[action]
                if st.button(
                    label,
                    key=f"action_{action}_{post['id']}",
                    disabled=already_done,
                    use_container_width=True,
                ):
                    handle_support_action(post, action)
                    st.rerun()

        confirmation = st.session_state.confirmations.get(post["id"])
        if confirmation:
            st.success(confirmation)


def render_discover_tab():
    posts = st.session_state.posts
    render_impact_summary(posts)

    st.markdown("###")  # spacer
    st.subheader("Filter Requests")

    neighborhoods = ["All"] + sorted({p["neighborhood"] for p in posts})
    categories = ["All"] + sorted({p["category"] for p in posts})
    support_types = ["All"] + ALL_ACTIONS

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        chosen_neighborhood = st.selectbox("Neighborhood", neighborhoods, key="filter_neighborhood")
    with fcol2:
        chosen_category = st.selectbox("Business Category", categories, key="filter_category")
    with fcol3:
        chosen_support = st.selectbox("Type of Support Needed", support_types, key="filter_support")

    filtered = posts
    if chosen_neighborhood != "All":
        filtered = [p for p in filtered if p["neighborhood"] == chosen_neighborhood]
    if chosen_category != "All":
        filtered = [p for p in filtered if p["category"] == chosen_category]
    if chosen_support != "All":
        filtered = [p for p in filtered if chosen_support in p["actions"]]

    st.markdown("###")  # spacer
    st.subheader(f"Community Requests ({len(filtered)})")

    if not filtered:
        st.info("No business requests match these filters right now. Try broadening your search.")
        return

    hot_ids = compute_hot_ids(posts)

    card_cols = st.columns(2)
    for i, post in enumerate(filtered):
        with card_cols[i % 2]:
            render_card(post, is_hot=post["id"] in hot_ids)


def render_post_tab():
    st.subheader("Post a Request for Your Business")
    st.caption(
        "Share one immediate, time-sensitive need. Your request will appear "
        "at the top of the Discover feed as soon as it's submitted."
    )

    with st.form("post_request_form", clear_on_submit=True):
        name = st.text_input("Business name *")
        neighborhood = st.text_input("Atlanta neighborhood *", placeholder="e.g. Old Fourth Ward")
        category = st.text_input("Business category *", placeholder="e.g. Bakery, Coffee Shop, Retail")
        story = st.text_area("Short business story *", placeholder="Tell neighbors a bit about your business.")
        request = st.text_area("What support do you need today? *")
        goal = st.number_input("Support goal *", min_value=1, max_value=1000, value=10, step=1)
        expiration = st.text_input("Time remaining *", placeholder="e.g. 5 hours")
        actions = st.multiselect(
            "Available support actions *",
            options=ALL_ACTIONS,
            default=["Visit", "Share"],
        )
        photo = st.file_uploader("Optional photo", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Post Request")

        if submitted:
            missing = []
            if not name.strip():
                missing.append("Business name")
            if not neighborhood.strip():
                missing.append("Atlanta neighborhood")
            if not category.strip():
                missing.append("Business category")
            if not story.strip():
                missing.append("Short business story")
            if not request.strip():
                missing.append("Support request")
            if not expiration.strip():
                missing.append("Time remaining")
            if not actions:
                missing.append("At least one support action")

            if missing:
                st.error("Please fill in the required fields: " + ", ".join(missing))
            else:
                new_post = {
                    "id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "neighborhood": neighborhood.strip(),
                    "category": category.strip(),
                    "story": story.strip(),
                    "request": request.strip(),
                    "goal": int(goal),
                    "supporters": 0,
                    "time_remaining": expiration.strip(),
                    "actions": actions,
                    "is_demo": False,
                    "media_bytes": photo.getvalue() if photo is not None else None,
                    "media_type": "image" if photo is not None else None,
                }
                st.session_state.posts.insert(0, new_post)
                st.success(
                    f"🎉 Your request for **{new_post['name']}** is live! "
                    "Head to the Discover tab to see it in the feed."
                )


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    init_state()

    # ---------------- Sidebar ----------------
    # Resolved before inject_css() so a theme change takes effect the same
    # rerun it's toggled, instead of lagging one rerun behind.
    with st.sidebar:
        st.markdown("### 🌗 Theme")
        is_dark = st.toggle("Dark mode", value=(st.session_state.theme == "dark"), key="theme_toggle")
        st.session_state.theme = "dark" if is_dark else "light"

        st.markdown("---")
        st.markdown("### Demo Controls")
        if st.button("🔄 Reset Demo", use_container_width=True):
            reset_demo()
            st.rerun()
        st.caption("Restores the four seeded businesses and clears all commitments made this session.")

    inject_css()

    # Celebratory $5 credit moment (shows once, then clears)
    if st.session_state.credit_celebration:
        biz_name = st.session_state.credit_celebration
        st.success(f"🎉 You've won a $5 credit to visit **{biz_name}**! (Simulated demo reward — not real currency.)")
        st.balloons()
        st.session_state.credit_celebration = None

    # ---------------- Header ----------------
    st.markdown('<div class="nb-hero-badge">Built for Hack RenderATL</div>', unsafe_allow_html=True)
    st.markdown('<div class="nb-title">NeighborBoost ATL</div>', unsafe_allow_html=True)
    st.markdown('<div class="nb-tagline">Atlanta shows up for Atlanta.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="nb-subdesc">Discover one simple action you can take to support an '
        "Atlanta small business today.</div>",
        unsafe_allow_html=True,
    )

    tab_discover, tab_post = st.tabs(["🔎 Discover Local Businesses", "📝 Post a Request"])
    # Post tab's form-submit logic (which can mutate st.session_state.posts)
    # is executed before the Discover tab is rendered, so a just-submitted
    # request shows up immediately rather than lagging one rerun behind.
    # (Filling order here does not affect the visual tab order above.)
    with tab_post:
        render_post_tab()
    with tab_discover:
        render_discover_tab()

    # ---------------- Footer ----------------
    st.markdown(
        """
        <div class="nb-footer">
            Built in Atlanta for Hack RenderATL<br/>
            Supporting local businesses through community action<br/>
            Seeded businesses are fictional and provided only for demonstration.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
