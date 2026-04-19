# MaternaAI — 5-Day Submission Plan
## GNEC Hackathon 2026 | Deadline: May 3, 2026 @ 5:00pm GMT+1

---

## ✅ Day 1 — Today (Apr 18): Repo Setup

```bash
# 1. Create new GitHub repo
# Go to github.com → New repo → name: "maternaai" → Public → Add README

# 2. Clone locally
git clone https://github.com/YOUR_USERNAME/maternaai.git
cd maternaai

# 3. Copy in app files
# - Copy maternaai_app.py → rename to app.py
# - Copy requirements.txt

# 4. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 5. Test locally
streamlit run app.py

# 6. First commit
git add .
git commit -m "feat: initial MaternaAI app with risk scoring and CHW action recommender"
git push origin main
```

---

## ✅ Day 2–3 (Apr 19–20): Enhance the App

**Priority additions:**
1. Add a "Dashboard" view showing Nigeria's ANC Paradox data (use your Oracle charts)
2. Add Swahili/Pidgin toggle for CHW interface (even partial translation impresses judges)
3. Add a printable "Referral Card" button (generates a simple text summary to show at facility)

```python
# Referral card — add this to Tab 1 after assessment:
referral_text = f"""
MATERNITY REFERRAL CARD
Patient: {patient_name} | Date: {datetime.now().strftime('%d %b %Y')}
Age: {age} | Gestation: {gestation_weeks}wks | ANC Visits: {anc_visits}
Risk Level: {risk_level} ({score}/100)
Referred to: {lga_info['facility']}
Issued by: Community Health Worker
"""
st.download_button("📄 Print Referral Card", referral_text, file_name="referral.txt")
```

---

## ✅ Day 4 (Apr 21): Polish & Deploy to Render

### Deploy to Render.com

1. Go to render.com → New → Web Service → Connect GitHub → select `maternaai`
2. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Instance**: Free tier
3. Click Deploy → wait ~3 mins → copy your live URL

### Create a good README.md

```markdown
# MaternaAI 🤱
> Community Health Intelligence for Nigeria's Last Mile | GNEC Hackathon 2026

**Live Demo**: https://your-app.onrender.com

MaternaAI is a mobile-first AI decision-support tool for community health workers in 
Nigeria. It identifies high-risk pregnant women and recommends specific community 
actions — bridging the ANC Paradox that claims thousands of maternal lives annually.

## SDG Alignment
- SDG 3.1 — Reduce maternal mortality
- SDG 3.8 — Universal health coverage  
- SDG 3.d — Health risk management

## Tech Stack
Python · Streamlit · Pandas · scikit-learn · Render.com

## Run Locally
pip install -r requirements.txt
streamlit run app.py
```

---

## ✅ Day 5 (Apr 22): Record Video + Submit

### Video Script (3 minutes)

**[0:00–0:20] Hook**
"Every year in Nigeria, thousands of women complete their antenatal care — and still die 
in childbirth. Not because they didn't try. Because the system failed to act on what the 
data already knew. I built MaternaAI to close that gap."

**[0:20–1:00] Problem**
Show the ANC Paradox chart from your Oracle project. Explain the numbers.

**[1:00–2:00] Demo**
Screen record: enter a real patient scenario (age 16, rural LGA, 0 ANC visits, 8km away).
Show it flag CRITICAL and generate a community action plan in under 10 seconds.

**[2:00–2:30] Impact**
"This tool is designed for the health worker who has 40 women on her caseload, no 
internet, and a basic Android phone. Every assessment takes 60 seconds. Every action plan 
is specific, not generic."

**[2:30–3:00] SDG + Close**
Show SDG 3 badge. "MaternaAI is my contribution to SDG 3.1 — reducing maternal mortality 
in Nigeria. The code is open source. The need is urgent."

### Devpost Submission Checklist
- [ ] Project title: "MaternaAI — Community Health Intelligence for Nigeria's Last Mile"
- [ ] Live demo URL (Render.com link)
- [ ] GitHub repo link (public)
- [ ] 2–5 min video (upload to YouTube or Vimeo, paste link)
- [ ] ZIP of source code
- [ ] Paste text from devpost_submission.md into the description fields
- [ ] Tags: health, AI, Nigeria, SDG3, maternal-health, streamlit

---

## Judging Criteria Mapping

| Criterion | Your Advantage |
|---|---|
| **Impact** | Real Nigerian maternal mortality data. ANC Paradox is documented and cited. |
| **Innovation** | CHW-first design. Community Action Recommender is novel. Most health apps target clinicians. |
| **Feasibility** | Deployed live on Render. Working demo. Pure Python — no heavy ML infra needed. |
| **Design** | Mobile-first, large tap targets, color-coded risk, no medical jargon. |
| **Presentation** | Personal story + data hook + live demo = compelling 3-min video. |

---

Good luck, Ekpenyong. This is a strong submission. 🏆
