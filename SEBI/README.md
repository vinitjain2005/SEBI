# Investor Education Prototype (Streamlit)

## Setup

```bash
pip install -r requirements.txt
```

Windows one-click:
- Double-click `run.bat`

## Run

```bash
streamlit run app.py
```

Or on PowerShell:

```powershell
python -m streamlit run app.py
```

## Features

- Dashboard: badges, progress, strengths/weaknesses from quiz.
- Tutorials: basics, risk, algo/HFT, diversification, orders, costs, psychology.
- Quizzes: 5 Qs with explanations, best score saved; optional leaderboard entry.
- Leaderboard: local top scores stored under user profile.
- Virtual Trading: delayed prices, buy/sell, PnL, CSV export.
- Learn Hub: translate and summarize; quick demo buttons (Hindi/Tamil/Bengali) for SEBI circulars.
- Risk Profiler: simple questionnaire -> Conservative/Balanced/Aggressive with lesson suggestions.
- Resources: curated links to SEBI, NISM, NSE, BSE.
- Persistence: Save Progress stores to `~/.sebi_app/`.
- Certificate: download when scoring 4+ / 5.

## Deployment (optional)

- Render/Heroku style (Procfile included):
  - Create a new web service, build with `pip install -r requirements.txt`.
  - Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` (already in Procfile).
- Streamlit Community Cloud:
  - Repo must contain `app.py`, `requirements.txt`.
  - Set main file to `app.py`.

## Notes

- Data from `yfinance` is delayed and may occasionally fail; adjust tickers if needed.
- Translation requires internet; relies on `deep-translator` (GoogleTranslator).
- Local files: `~/.sebi_app/state.json` and `leaderboard.json`.
