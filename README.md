# NeighborBoost ATL

**Atlanta shows up for Atlanta.**

Built for Hack RenderATL — "Best Hack for Good" category.

## Mission

NeighborBoost ATL helps Atlanta mom-and-pop businesses post one immediate,
time-sensitive need. Community members can commit to visiting, sharing, or
helping that business — turning a quiet afternoon into a wave of neighborhood
support.

## Community Problem

Small, independently owned businesses in Atlanta often face short-term,
urgent gaps — a slow afternoon, surplus food about to go to waste, a single
skilled task they can't staff — that a handful of nearby neighbors could
easily solve if they simply knew about it in the moment. NeighborBoost ATL
closes that gap with a simple, low-friction way for businesses to ask and
neighbors to act.

## How It Works

1. A local business posts one specific, time-sensitive request (e.g. "help
   us welcome 10 first-time customers this afternoon").
2. The request appears in the community Discover feed alongside its story,
   neighborhood, category, and support goal.
3. Neighbors browse the feed and commit to **I'll Visit**, **I'll Share**, or
   **I Can Help** — whichever fits the business's need.
4. Each commitment updates the business's progress bar, the site-wide impact
   stats, and the "Hot Right Now" ranking in real time.

## Key Features

- **Discover & Post tabs** — browse active community requests, or submit a
  new one via a simple form.
- **Live impact summary** — active requests, businesses boosted, and total
  neighbor commitments, calculated from current session data.
- **Hot Store Ranking** — the post (or posts, in a tie) with the highest
  combined Visit + Share + Help commitments gets a "🔥 Hot Right Now" badge,
  recalculated as new commitments come in.
- **Filters** — by neighborhood, business category, and type of support
  needed, each with an "All" option.
- **Dark / light mode toggle** — a sidebar toggle switches the whole app
  between a warm light theme and a deep navy/charcoal dark theme, both built
  from the same peach/cream/green palette. The choice persists for the
  session and survives every rerun (button clicks, filters, form submits).
- **Simulated $5 credit moment** — after committing support, there's a small
  random chance of a celebratory "🎉 You've won a $5 credit" banner with
  balloons. Purely cosmetic — no real money, wallet, or payment system is
  involved.
- **One-click Reset Demo** — restores the four seeded businesses, clears all
  session commitments, and keeps your theme preference.
- **Optional photo upload** — attach a photo to your own request; it's held
  only in-memory for the session (no disk or cloud storage).

## Technology

- Python 3
- Streamlit (UI + `st.session_state` for posts, support actions, hot
  ranking, credit-trigger state, and theme preference)
- Minimal custom CSS injected via `st.markdown(unsafe_allow_html=True)`
- No database, no authentication, no payment processing, no maps, no
  external APIs, no AI integration

## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Deploy on Render

1. Push this repo to GitHub.
2. Create a new **Web Service** on [Render](https://render.com), pointing at
   the repo.
3. Build command:
   ```bash
   pip install -r requirements.txt
   ```
4. Start command:
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
   ```

## Social Impact

NeighborBoost ATL makes it effortless for Atlanta residents to convert a
spare five minutes into concrete support for a neighborhood business —
showing up, spreading the word, or lending a hand — reinforcing the idea that
a strong local economy is built through small, immediate acts of community
care.

## Prototype Limitations

This is a hackathon MVP, intentionally scoped small:

- **State is per-browser-session**, stored in `st.session_state`. It is not
  shared across users or devices — two people in separate browser tabs will
  see independent supporter counts.
- **"Time remaining" is static display text** (from seed data or the post
  form), not a live countdown. There is no timestamp math or expiration
  logic.
- **"Hot Right Now" ranking is session-scoped**, based on total commitments
  across currently active posts in your session — not a true rolling 24-hour
  window, since there is no persistent timestamp tracking.
- **The $5 credit is simulated and cosmetic only.** It has no real monetary
  value, no wallet, no redemption code, and touches no payment system.

## Future Improvements

- Add MP4 video upload alongside photo upload (skipped in this MVP to keep
  scope tight ahead of the submission deadline).
- Shared, persistent state (a real database) so commitments and posts sync
  across all users and devices.
- Real timestamp-based "time remaining" countdowns and a true rolling
  24-hour window for hot-store ranking.
- Real incentive/rewards infrastructure if a genuine credit or loyalty
  program is ever pursued.

## A Note on Seed Data

The four seeded businesses (Peach & Bean Coffee, Nia's Neighborhood Bakes,
Southside Plant Studio, and Cultura Kitchen ATL) are entirely fictional and
included only to demonstrate the app. They are clearly labeled "Demo
Business" throughout the UI.
