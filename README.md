CFPB Consumer Complaint Dashboard

Live app: https://cfpb-consumer-complaints-dashboard.onrender.com

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Rory503/CFPB_VERSION5/tree/restore-website)

Overview
- Interactive Streamlit dashboard analyzing the official CFPB Consumer Complaint Database.
- Real data downloaded at runtime; no large CSVs are stored in the repo.
- Optional AI chat assistant; users can paste their own OpenAI API key in the app.

Local Run
- pip install -r requirements.txt
- streamlit run web_dashboard.py

Notes
- Free hosting may cold‑start; first request can take 30–60 seconds.
- Exports are written to `outputs/` during a session.
