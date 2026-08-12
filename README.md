# NeighborBoost ATL

<img width="1672" height="941" alt="ChatGPT Image Aug 12, 2026, 07_11_27 PM" src="https://github.com/user-attachments/assets/9103ea1a-7edf-4ad9-a14b-efc678b4e3fb" />



**Atlanta shows up for Atlanta.**

## Mission

NeighborBoost ATL helps Atlanta mom-and-pop businesses post one immediate, time-sensitive need. Community members can commit to visiting, sharing, or helping that business.

Built for Hack RenderATL’s **Best Hack for Good** category.

## Community problem

Small Atlanta businesses often need a quick boost during slow hours, before closing, or when launching something new — but they lack a simple way to ask neighbors for one clear action. Social posts get buried; generic platforms feel impersonal. NeighborBoost ATL makes the ask local, urgent, and actionable.

## How it works

1. A local business posts **one** time-sensitive request (visit, share, or help).
2. Neighbors browse the Discover feed (hottest businesses first), filter by neighborhood / category / support type.
3. Supporters click **I’ll Visit**, **I’ll Share**, or **I Can Help**.
4. Progress bars, impact metrics, and the **Hot Right Now** ranking update immediately.

All data lives in Streamlit session state for this hackathon prototype — no accounts, no database.

## Key features

- Eight seeded Atlanta demo businesses with progress goals and countdowns
- Support actions with per-session duplicate prevention and ✓ done labels
- **Hot Right Now** ranking — hottest businesses sort to the top of the feed
- Clear-filters control
- Goal Met badge when a request hits its support goal
- Dark / light mode toggle (persists across Reset Demo)
- Occasional simulated $5 credit celebration (cosmetic only — not real money)
- Neighborhood, category, and support-type filters
- “Post a Request” form with optional photo/video preview
- Impact summary (active requests, businesses boosted, commitments)
- Reset Demo in the sidebar
- Warm, mobile-friendly UI (peach, cream, navy, community green)

## Technology

- Python 3
- Streamlit
- Streamlit session state (posts, counters, actions)
- Minimal custom CSS
- Pillow (image handling via Streamlit)

No React, database, auth, payments, maps, external APIs, AI, or cloud file storage.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

## Deploy on Render

### One-click (Blueprint)

1. Open: [Deploy to Render](https://render.com/deploy?repo=https://github.com/devchicajas/NeighborBoostATL)
2. Sign in to Render and connect GitHub if prompted.
3. Confirm the `neighborboost-atl` web service and click **Apply**.

### Manual Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/) → **New** → **Web Service**.
2. Connect `devchicajas/NeighborBoostATL` (branch `main`).
3. Runtime: **Python 3**
4. Build command: `pip install -r requirements.txt`
5. Start command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

6. Create the service. No environment secrets are required for the MVP.

A `render.yaml` blueprint is included in this repo for repeatable deploys.

## Social impact

NeighborBoost ATL turns “I want to support local” into a concrete commitment — walk in today, share a lunch special, or lend a skill. That keeps dollars and attention circulating in Atlanta neighborhoods.

## Prototype limitations

- Data resets when the browser session ends or when **Reset Demo** is clicked
- No user accounts or business verification
- No real payments, maps, or messaging (the $5 credit moment is simulated only)
- Media uploads stay in memory for the session only
- Seeded businesses are **fictional** and labeled **Demo Business**

## Collaboration note

This app uses Jasmin’s MVP design and structure as the base, with selected enhancements adapted from Ulises’s MVP (`feature/neighborboost-mvp`).

## Future improvements

- Persistent storage and verified business profiles
- SMS / email reminders for commitments
- Neighborhood ambassador moderation
- Real photo libraries with owner consent
- Accessibility audits and multilingual support

## Demo data note

All seeded businesses (including Peach & Bean Coffee, Nia’s Neighborhood Bakes, Southside Plant Studio, Cultura Kitchen ATL, Edgewood Cuts & Co., Beltline Pages Bookstore, Kirkwood Stitch Lab, and Eastside Vinyl & Tea) are **fictional** and provided only for demonstration. They are not affiliated with real Atlanta businesses.
