🤱 MaternaAI
Community Health Intelligence for Nigeria's Last Mile
GNEC Hackathon 2026 · SDG 3 Health & Well-being · Solo Submission
🔴 Live Demo → maternaai-aemv.onrender.com
The Problem — The ANC Paradox
In Nigeria, 51.5% of pregnant women complete at least 4 antenatal care (ANC) visits.
But only 49.0% deliver in a health facility.
That gap — women who showed up for care but were still lost before delivery — costs thousands of lives every year. Nigeria's maternal mortality ratio remains among the highest in the world at over 800 deaths per 100,000 live births (Nigeria DHS).
This is the ANC Paradox. MaternaAI is built to close it.
What MaternaAI Does
A mobile-first AI decision-support tool for community health workers (CHWs) in Nigeria. Given basic patient information, it:
✅ Calculates a risk score (0–100) using evidence-based weights from Nigeria DHS + WHO data
✅ Flags risk level — Low / Moderate / High / Critical with plain-language reasoning
✅ Recommends specific community actions — not generic advice, but exact next steps for the CHW
✅ Identifies the nearest health facility for the patient's LGA
✅ Generates a downloadable referral card the patient presents at the facility
✅ Logs the full caseload with CSV export for LGA reporting
Nigeria Data Tab — Real Evidence
The app includes a dedicated data tab with 5 real charts from Nigeria DHS 2018 and WHO Global Health Observatory:
ANC Coverage vs Facility Delivery Rate over time (the Paradox visualized)
The ANC–Facility gap trend (1990–2021)
Anaemia prevalence in Nigerian women of reproductive age
Adolescent birth rate trend
Maternal Mortality Ratio from DHS survey data
SDG Alignment
Goal
Target
SDG 3.1
Reduce global maternal mortality ratio to < 70 per 100,000 live births
SDG 3.8
Achieve universal health coverage including quality essential health services
SDG 3.d
Strengthen capacity for health risk early warning and management
Tech Stack
Layer
Tool
Frontend
Streamlit
Data Processing
Python, Pandas, NumPy
Risk Engine
Evidence-based weighted scoring (DHS + WHO)
Data Sources
Nigeria DHS 2018, WHO Global Health Observatory
Deployment
Render.com
Run Locally
git clone https://github.com/ekpenyongasuquo/maternaai.git
cd maternaai
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
streamlit run app.py
App opens at http://localhost:8501
Data Sources
Nigeria Demographic and Health Survey (DHS) 2018 — pregnancy-related mortality, MMR
WHO Global Health Observatory — ANC coverage, facility delivery rates, anaemia prevalence, adolescent birth rate
National Health Management Information System (NHMIS) — LGA-level facility mapping
Built By
Ekpenyong Asuquo — Solo Developer
Ensign College (BYU-Pathway Worldwide) · IT Student
Lagos, Nigeria
GitHub: @ekpenyongasuquo
MaternaAI · GNEC Hackathon 2026 · Open Source · MIT License
