"""
MaternaAI — Community Health Intelligence for Nigeria's Last Mile
Streamlit App | GNEC Hackathon 2026 | SDG 3
Real data: Nigeria DHS + WHO Global Health Observatory
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MaternaAI",
    page_icon="🤱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .main { background-color: #FAFAF7; }

  .maternity-header {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
    padding: 2rem 1.5rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    color: white;
  }
  .maternity-header h1 { font-family: 'DM Serif Display', serif; font-size: 2rem; margin: 0; color: #D8F3DC; }
  .maternity-header p  { font-size: 0.85rem; margin: 0.4rem 0 0; color: #95D5B2; font-weight: 300; }

  .risk-card       { padding: 1.2rem 1.5rem; border-radius: 14px; margin: 1rem 0; }
  .risk-low        { background: #D8F3DC; border-left: 5px solid #40916C; color: #1B4332; }
  .risk-moderate   { background: #FFF3CD; border-left: 5px solid #E9A800; color: #5C3D00; }
  .risk-high       { background: #FFDDD2; border-left: 5px solid #E07A5F; color: #6B1A0A; }
  .risk-critical   { background: #FFB3C1; border-left: 5px solid #D00000; color: #5C0000; }
  .risk-label      { font-size: 1.4rem; font-weight: 600; margin-bottom: 0.3rem; }

  .action-box { background: white; border: 1px solid #E0E0E0; border-radius: 12px;
                padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; }
  .action-box strong { color: #1B4332; display: block; margin-bottom: 0.3rem;
                       font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }

  .paradox-box { background: #FFF8E1; border: 2px solid #F9A825; border-radius: 14px;
                 padding: 1.2rem 1.5rem; margin: 1rem 0; }
  .paradox-title { font-family: 'DM Serif Display', serif; font-size: 1.2rem;
                   color: #5C3D00; margin-bottom: 0.5rem; }

  .log-entry { background: white; border: 1px solid #E8E8E8; border-radius: 10px;
               padding: 0.8rem 1rem; margin: 0.4rem 0; font-size: 0.82rem; color: #444; }

  .sdg-badge { display: inline-block; background: #1B4332; color: #D8F3DC;
               padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.72rem;
               font-weight: 500; margin-right: 0.3rem; }

  div[data-testid="stButton"] > button {
    background: #2D6A4F; color: white; border: none; border-radius: 10px;
    padding: 0.6rem 2rem; font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem; font-weight: 500; width: 100%;
  }
  div[data-testid="stButton"] > button:hover { background: #1B4332; }

  .footer-note { text-align: center; color: #999; font-size: 0.72rem;
                 margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #EEE; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ────────────────────────────────────────────────────────────────
@st.cache_data
def load_who_data():
    """Load and process WHO maternal health indicators for Nigeria."""
    # Try both relative and absolute paths for deployment flexibility
    possible_paths = [
        "who_maternal.csv.csv",
        "data/who_maternal.csv.csv",
        os.path.join(os.path.dirname(__file__), "who_maternal.csv.csv"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    return None


@st.cache_data
def load_dhs_data():
    """Load and process DHS maternal mortality data for Nigeria."""
    possible_paths = [
        "dhs_maternal_mortality.csv.csv",
        "data/dhs_maternal_mortality.csv.csv",
        os.path.join(os.path.dirname(__file__), "dhs_maternal_mortality.csv.csv"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    return None


@st.cache_data
def build_anc_paradox_data(who_df):
    """
    Extract ANC coverage vs facility delivery rates — the ANC Paradox dataset.
    Returns a DataFrame with Year, ANC_Coverage, Facility_Delivery columns.
    """
    anc = who_df[who_df['GHO (DISPLAY)'].str.contains('Antenatal care coverage', na=False)][['YEAR (DISPLAY)', 'Numeric']].copy()
    anc.columns = ['Year', 'ANC_Coverage']

    fac = who_df[who_df['GHO (DISPLAY)'].str.contains('Proportion of births delivered', na=False)][['YEAR (DISPLAY)', 'Numeric']].copy()
    fac.columns = ['Year', 'Facility_Delivery']

    merged = pd.merge(anc, fac, on='Year', how='inner').dropna()
    merged = merged.sort_values('Year')
    merged['Gap'] = merged['ANC_Coverage'] - merged['Facility_Delivery']
    return merged


@st.cache_data
def build_mmr_data(dhs_df):
    """Extract Maternal Mortality Ratio from DHS data."""
    mmr = dhs_df[dhs_df['Indicator'] == 'Maternal mortality ratio'][['SurveyYear', 'Value']].copy()
    mmr.columns = ['Year', 'MMR']
    mmr = mmr.dropna().sort_values('Year')
    return mmr


@st.cache_data
def build_anemia_data(who_df):
    """Extract anaemia prevalence trend."""
    anemia = who_df[who_df['GHO (DISPLAY)'].str.contains('Prevalence of anaemia', na=False)][['YEAR (DISPLAY)', 'Numeric']].copy()
    anemia.columns = ['Year', 'Anaemia_Prevalence']
    anemia = anemia.dropna().sort_values('Year')
    return anemia


# ─── LGA DATA ────────────────────────────────────────────────────────────────────
LGA_DATA = {
    "Lagos Island":       {"tier": "urban",      "facility": "Lagos Island General Hospital",         "zone": "South-West"},
    "Ikeja":              {"tier": "urban",       "facility": "Lagos University Teaching Hospital (LUTH)", "zone": "South-West"},
    "Calabar Municipal":  {"tier": "urban",       "facility": "UCTH Calabar",                          "zone": "South-South"},
    "Abi":                {"tier": "rural",       "facility": "Abi General Hospital",                  "zone": "South-South"},
    "Obudu":              {"tier": "semi-urban",  "facility": "Obudu General Hospital",                "zone": "South-South"},
    "Kano Municipal":     {"tier": "urban",       "facility": "Murtala Muhammad Specialist Hospital",  "zone": "North-West"},
    "Bichi":              {"tier": "rural",       "facility": "Bichi Primary Health Centre",           "zone": "North-West"},
    "Ibadan North":       {"tier": "urban",       "facility": "UCH Ibadan",                            "zone": "South-West"},
    "Iseyin":             {"tier": "semi-urban",  "facility": "Iseyin General Hospital",               "zone": "South-West"},
    "Maiduguri":          {"tier": "urban",       "facility": "UMTH Maiduguri",                        "zone": "North-East"},
    "Bama":               {"tier": "rural",       "facility": "Bama General Hospital",                 "zone": "North-East"},
    "Enugu North":        {"tier": "urban",       "facility": "ESUT Teaching Hospital",                "zone": "South-East"},
    "Igbo-Eze South":     {"tier": "rural",       "facility": "Igbo-Eze PHC",                          "zone": "South-East"},
    "Jos North":          {"tier": "urban",       "facility": "JUTH Jos",                              "zone": "North-Central"},
    "Shendam":            {"tier": "rural",       "facility": "Shendam General Hospital",              "zone": "North-Central"},
    "Other (Urban)":      {"tier": "urban",       "facility": "Nearest Teaching Hospital",             "zone": "Various"},
    "Other (Semi-Urban)": {"tier": "semi-urban",  "facility": "Nearest General Hospital",              "zone": "Various"},
    "Other (Rural)":      {"tier": "rural",       "facility": "Nearest PHC",                           "zone": "Various"},
}


# ─── RISK SCORING ENGINE ─────────────────────────────────────────────────────────
def calculate_risk_score(age, gestation_weeks, anc_visits, parity,
                          facility_distance_km, lga_tier, complications):
    score = 0
    factors = []

    if age < 18:
        score += 20
        factors.append("Adolescent pregnancy (age < 18) — significantly elevated risk")
    elif age > 35:
        score += 15
        factors.append("Advanced maternal age (> 35) — elevated risk")
    elif 18 <= age <= 24:
        score += 5

    expected_anc = gestation_weeks / 8
    if anc_visits == 0:
        score += 25
        factors.append("No ANC visits recorded — critical gap in prenatal monitoring")
    elif anc_visits < expected_anc * 0.5:
        score += 15
        factors.append(f"Low ANC attendance ({anc_visits} visits at {gestation_weeks}wks) — ANC Paradox risk")
    elif anc_visits >= expected_anc:
        score -= 5

    if parity == 0:
        score += 8
        factors.append("Primigravida — first delivery carries higher complication risk")
    elif parity >= 5:
        score += 18
        factors.append("Grand multiparity (5+ births) — high-risk factor for hemorrhage")
    elif parity >= 3:
        score += 8

    if facility_distance_km > 20:
        score += 20
        factors.append(f"Facility distance {facility_distance_km}km — transport barrier is critical")
    elif facility_distance_km > 10:
        score += 12
        factors.append(f"Facility distance {facility_distance_km}km — moderate transport barrier")
    elif facility_distance_km > 5:
        score += 6

    if lga_tier == "rural":
        score += 10
        factors.append("Rural LGA — limited emergency response capacity")
    elif lga_tier == "semi-urban":
        score += 5

    comp_scores = {
        "Hypertension / Pre-eclampsia":    (25, "Hypertension/pre-eclampsia — leading cause of maternal death in Nigeria"),
        "Diabetes / Gestational diabetes": (18, "Gestational diabetes — requires specialist monitoring"),
        "Anaemia":                         (15, "Anaemia — increases hemorrhage risk at delivery"),
        "Previous C-section":              (12, "Previous C-section — scar rupture risk requires facility delivery"),
        "Multiple pregnancy (twins+)":     (20, "Multiple pregnancy — high-risk delivery requiring specialist care"),
        "Heavy bleeding episodes":         (22, "Bleeding episodes — potential placenta previa/abruption"),
        "None reported":                   (0, None),
    }
    for comp in complications:
        pts, msg = comp_scores.get(comp, (0, None))
        score += pts
        if msg:
            factors.append(msg)

    return min(score, 100), factors


def get_risk_level(score):
    if score < 20:   return "LOW",      "risk-low",      "✅"
    elif score < 45: return "MODERATE", "risk-moderate", "⚠️"
    elif score < 70: return "HIGH",     "risk-high",     "🔴"
    else:            return "CRITICAL", "risk-critical", "🚨"


def get_community_actions(risk_level, lga_tier, facility_distance_km,
                           gestation_weeks, complications):
    actions = {}

    if risk_level == "CRITICAL":
        actions["Immediate Action"] = "REFER NOW. Do not wait for next scheduled visit. Arrange transport to nearest tertiary/general hospital immediately."
        actions["Transport"]        = "Contact State Emergency Transport Scheme (SETS) or nearest NEMA office. If unavailable, mobilize community transport immediately."
        actions["Notify"]           = "Alert LGA Health Coordinator and Supervisor today. Document referral in paper register AND report to state DHIS2."
        actions["Follow-up"]        = "Call to confirm arrival at facility within 2 hours of referral."

    elif risk_level == "HIGH":
        actions["Next Visit"] = "Schedule facility ANC visit within 72 hours — do not wait for routine schedule."
        if facility_distance_km > 10:
            actions["Transport Plan"] = "Pre-arrange transport NOW for delivery date. Identify a birth companion who can escort her."
        actions["Birth Plan"] = "Complete and document a facility birth plan this week. Identify 2 emergency contacts."
        actions["Referral"]   = "Refer to facility-level midwife for specialist ANC review."
        if "Hypertension / Pre-eclampsia" in complications:
            actions["Emergency Signs"] = "Educate on danger signs: severe headache, blurred vision, swollen face/hands. Tell her to go to facility immediately if these occur."

    elif risk_level == "MODERATE":
        actions["Next Visit"]        = "Schedule ANC visit within 2 weeks. Confirm she has transport arranged for delivery."
        actions["Education"]         = "Reinforce facility delivery: discuss cost barriers, transport options, and community savings schemes."
        actions["Birth Plan"]        = "Document birth plan if not already done. Identify a birth companion."
        if lga_tier == "rural":
            actions["Community Support"] = "Connect with Village Health Team (VHT) for additional support and transport coordination."

    else:
        actions["Routine Care"] = "Continue scheduled ANC visits per protocol."
        actions["Birth Plan"]   = "Confirm birth plan is documented. Remind her that facility delivery is safest."
        actions["Next Visit"]   = "Next scheduled ANC visit as per national protocol."

    if gestation_weeks >= 36:
        actions["⚡ Imminent Delivery"] = "Delivery is imminent. Confirm facility, transport, and birth companion are ALL arranged and confirmed — not just planned."

    return actions


# ─── SESSION STATE ───────────────────────────────────────────────────────────────
if "caseload_log" not in st.session_state:
    st.session_state.caseload_log = []

# ─── LOAD DATA ───────────────────────────────────────────────────────────────────
who_df = load_who_data()
dhs_df = load_dhs_data()

# ─── HEADER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="maternity-header">
  <h1>🤱 MaternaAI</h1>
  <p>Community Health Intelligence · Nigeria's Last Mile</p>
  <p style="margin-top:0.6rem;">
    <span class="sdg-badge">SDG 3.1</span>
    <span class="sdg-badge">SDG 3.8</span>
    <span class="sdg-badge">SDG 3.d</span>
  </p>
</div>
""", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📋 Assess Patient", "📊 Nigeria Data", "🗂️ Caseload Log", "ℹ️ About"])


# ══════════════════════════════════════════════════════
# TAB 1: ASSESSMENT
# ══════════════════════════════════════════════════════
with tab1:
    st.markdown("### Patient Information")
    st.caption("Enter details as recorded in ANC register")

    col1, col2 = st.columns(2)
    with col1:
        patient_name         = st.text_input("Patient Identifier / Code", placeholder="e.g. ANC-0042")
        age                  = st.number_input("Age (years)", min_value=10, max_value=55, value=24)
        parity               = st.number_input("Parity (previous births)", min_value=0, max_value=15, value=0)
    with col2:
        gestation_weeks      = st.number_input("Gestation (weeks)", min_value=4, max_value=42, value=28)
        anc_visits           = st.number_input("ANC Visits Completed", min_value=0, max_value=20, value=2)
        facility_distance_km = st.number_input("Distance to Nearest Facility (km)", min_value=0, max_value=200, value=8)

    lga      = st.selectbox("LGA", list(LGA_DATA.keys()))
    lga_info = LGA_DATA[lga]

    complications = st.multiselect(
        "Reported Complications / Risk Conditions",
        options=[
            "None reported", "Hypertension / Pre-eclampsia",
            "Diabetes / Gestational diabetes", "Anaemia",
            "Previous C-section", "Multiple pregnancy (twins+)",
            "Heavy bleeding episodes",
        ],
        default=["None reported"]
    )

    st.divider()

    if st.button("🔍 Assess Risk & Get Recommendations"):
        score, factors = calculate_risk_score(
            age, gestation_weeks, anc_visits, parity,
            facility_distance_km, lga_info["tier"], complications
        )
        risk_level, risk_class, icon = get_risk_level(score)
        actions = get_community_actions(
            risk_level, lga_info["tier"],
            facility_distance_km, gestation_weeks, complications
        )

        st.markdown(f"""
        <div class="risk-card {risk_class}">
          <div class="risk-label">{icon} {risk_level} RISK</div>
          <div>Risk Score: <strong>{score}/100</strong> &nbsp;·&nbsp;
               {lga_info['zone']} Zone &nbsp;·&nbsp; {lga_info['tier'].title()} LGA</div>
        </div>
        """, unsafe_allow_html=True)

        if factors:
            with st.expander("📌 Risk Factors Identified", expanded=True):
                for f in factors:
                    st.markdown(f"• {f}")

        st.markdown(f"""
        <div class="action-box">
          <strong>🏥 Recommended Facility</strong>
          {lga_info['facility']} &nbsp;·&nbsp; {facility_distance_km} km away
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📋 Community Action Plan")
        for action_title, action_detail in actions.items():
            st.markdown(f"""
            <div class="action-box">
              <strong>{action_title}</strong>
              {action_detail}
            </div>
            """, unsafe_allow_html=True)

        # Referral card download
        referral_text = f"""
MATERNITY REFERRAL CARD
========================
Patient: {patient_name or 'Unnamed'} | Date: {datetime.now().strftime('%d %b %Y')}
Age: {age} | Gestation: {gestation_weeks}wks | ANC Visits: {anc_visits}
LGA: {lga} | Distance to facility: {facility_distance_km}km
Risk Level: {risk_level} ({score}/100)
Referred to: {lga_info['facility']}
Complications noted: {', '.join(complications)}
Issued by: Community Health Worker (MaternaAI)
========================
"""
        st.download_button("📄 Download Referral Card", referral_text,
                           file_name=f"referral_{patient_name or 'patient'}.txt")

        log_entry = {
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
            "patient": patient_name or "Unnamed",
            "age": age, "gestation": gestation_weeks, "anc_visits": anc_visits,
            "lga": lga, "risk_level": risk_level, "score": score,
            "facility": lga_info["facility"],
        }
        st.session_state.caseload_log.insert(0, log_entry)
        st.success(f"Assessment logged. {len(st.session_state.caseload_log)} patients assessed this session.")


# ══════════════════════════════════════════════════════
# TAB 2: NIGERIA DATA (Real Dataset Charts)
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown("### The ANC Paradox — Real Data from Nigeria")

    if who_df is not None:
        paradox_df = build_anc_paradox_data(who_df)

        if not paradox_df.empty:
            # ── ANC Paradox headline numbers
            latest = paradox_df.iloc[-1]
            st.markdown(f"""
            <div class="paradox-box">
              <div class="paradox-title">⚠️ The ANC Paradox in Numbers</div>
              In Nigeria's most recent data year (<strong>{int(latest['Year'])}</strong>):
              <ul>
                <li><strong>{latest['ANC_Coverage']:.1f}%</strong> of pregnant women attended at least 4 ANC visits</li>
                <li>But only <strong>{latest['Facility_Delivery']:.1f}%</strong> delivered in a health facility</li>
                <li>That's a <strong>{latest['Gap']:.1f} percentage point gap</strong> — women who showed up for care,
                    but were lost before delivery</li>
              </ul>
              MaternaAI is built to close this gap at the community level.
            </div>
            """, unsafe_allow_html=True)

            # ── ANC vs Facility Delivery Chart
            st.markdown("#### ANC Coverage vs. Facility Delivery Rate Over Time")
            chart_df = paradox_df.set_index('Year')[['ANC_Coverage', 'Facility_Delivery']]
            chart_df.columns = ['ANC Coverage (≥4 visits) %', 'Facility Delivery Rate %']
            st.line_chart(chart_df, use_container_width=True)
            st.caption("Source: WHO Global Health Observatory — Nigeria Maternal Health Indicators")

            # ── Gap chart
            st.markdown("#### The Gap: Women Lost Between ANC and Delivery")
            gap_df = paradox_df.set_index('Year')[['Gap']]
            gap_df.columns = ['ANC–Facility Delivery Gap (%)']
            st.bar_chart(gap_df, use_container_width=True, color="#E07A5F")
            st.caption("A positive gap means more women attended ANC than delivered in facilities — the ANC Paradox.")

        # ── Anaemia Prevalence
        anemia_df = build_anemia_data(who_df)
        if not anemia_df.empty:
            st.divider()
            st.markdown("#### Anaemia Prevalence in Nigerian Women of Reproductive Age (%)")
            st.area_chart(anemia_df.set_index('Year'), use_container_width=True, color="#2D6A4F")
            st.caption("Source: WHO Global Health Observatory. Anaemia is a major risk factor for maternal hemorrhage death.")

        # ── Adolescent birth rate
        adol = who_df[who_df['GHO (DISPLAY)'].str.contains('Adolescent birth rate', na=False)][['YEAR (DISPLAY)', 'Numeric']].copy()
        adol.columns = ['Year', 'Adolescent_Birth_Rate']
        adol = adol.dropna().sort_values('Year')
        if not adol.empty:
            st.divider()
            st.markdown("#### Adolescent Birth Rate in Nigeria (per 1,000 women aged 15–19)")
            st.line_chart(adol.set_index('Year'), use_container_width=True, color="#E9A800")
            st.caption("Source: WHO Global Health Observatory. High adolescent birth rates correlate strongly with maternal mortality risk.")

    else:
        st.warning("""
        ⚠️ Data files not found in app directory.

        To enable real data charts, copy these files into the same folder as app.py:
        - `who_maternal.csv.csv`
        - `dhs_maternal_mortality.csv.csv`
        """)

    if dhs_df is not None:
        mmr_df = build_mmr_data(dhs_df)
        if not mmr_df.empty:
            st.divider()
            st.markdown("#### Nigeria Maternal Mortality Ratio (per 100,000 live births) — DHS Survey Data")
            st.bar_chart(mmr_df.set_index('Year'), use_container_width=True, color="#1B4332")
            st.caption("Source: Nigeria DHS (Demographic and Health Survey). MMR remains among the highest globally.")


# ══════════════════════════════════════════════════════
# TAB 3: CASELOAD LOG
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("### Today's Caseload")

    if not st.session_state.caseload_log:
        st.info("No assessments yet. Use the 'Assess Patient' tab to add patients.")
    else:
        log_df = pd.DataFrame(st.session_state.caseload_log)
        total    = len(log_df)
        critical = len(log_df[log_df["risk_level"] == "CRITICAL"])
        high     = len(log_df[log_df["risk_level"] == "HIGH"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Assessed", total)
        col2.metric("🔴 High/Critical", critical + high)
        col3.metric("Avg Risk Score",  f"{log_df['score'].mean():.0f}/100")
        st.divider()

        risk_icons = {"LOW": "✅", "MODERATE": "⚠️", "HIGH": "🔴", "CRITICAL": "🚨"}
        for entry in st.session_state.caseload_log:
            icon = risk_icons.get(entry["risk_level"], "")
            st.markdown(f"""
            <div class="log-entry">
              <strong>{icon} {entry['patient']}</strong> &nbsp;·&nbsp;
              {entry['risk_level']} ({entry['score']}/100) &nbsp;·&nbsp;
              Age {entry['age']}, {entry['gestation']}wks, {entry['anc_visits']} ANC visits
              &nbsp;·&nbsp; {entry['lga']} &nbsp;·&nbsp; <em>{entry['timestamp']}</em>
            </div>
            """, unsafe_allow_html=True)

        csv = log_df.to_csv(index=False)
        st.download_button("⬇️ Export Caseload as CSV", data=csv,
                           file_name=f"maternity_caseload_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv")


# ══════════════════════════════════════════════════════
# TAB 4: ABOUT
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    ### About MaternaAI

    **MaternaAI** is a mobile-first community health decision-support tool designed for
    frontline health workers in Nigeria. It addresses the **ANC Paradox** — the documented
    pattern where Nigerian women complete antenatal care visits but still do not deliver in
    health facilities.

    #### How the Risk Score Works
    The risk engine uses evidence-based weights derived from Nigeria DHS 2018, WHO ANC
    guidelines, and NHMIS data. Factors include:
    - Maternal age (adolescent / advanced)
    - ANC visit attendance relative to gestation week
    - Parity (grand multiparity ≥ 5 is a leading Nigerian risk factor)
    - Distance to nearest health facility
    - LGA urban/rural tier
    - Reported complications (hypertension, anaemia, etc.)

    #### Data Sources
    - **Nigeria DHS 2018** — Pregnancy-related mortality, MMR
    - **WHO Global Health Observatory** — ANC coverage, facility delivery rates, anaemia prevalence
    - **NHMIS** — State-level maternal health indicators

    #### SDG Alignment
    - **SDG 3.1** — Reduce global maternal mortality ratio to < 70 per 100,000 live births
    - **SDG 3.8** — Achieve universal health coverage
    - **SDG 3.d** — Strengthen health risk early warning and management

    ---
    Built solo by **Ekpenyong Asuquo** · GNEC Hackathon 2026 · Nigeria
    """)

# ─── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
  MaternaAI · GNEC Hackathon 2026 · SDG 3 Health & Well-being ·
  Data: Nigeria DHS 2018 + WHO Global Health Observatory
</div>
""", unsafe_allow_html=True)
