# MaternaAI — Community Health Intelligence for Nigeria's Last Mile

## Inspiration

Every year in Nigeria, thousands of women complete all their antenatal care visits — they showed up, they did everything right — and still never deliver in a health facility. Maternal mortality claims over 82,000 Nigerian lives annually, yet the data shows that **access alone isn't the problem**. The problem is the gap between a woman's last ANC visit and the moment she goes into labor, alone, far from help.

I call this the **ANC Paradox**, and it's what MaternaAI is built to close.

As someone building technology for African health contexts, I wanted to go beyond dashboards and analytics. I wanted to build something a community health worker (CHW) — with limited connectivity, no medical degree, and 40 women on her caseload — could actually use in the field.

## What It Does

MaternaAI is a mobile-first AI decision-support tool for frontline community health workers in Nigeria. Given basic information about a pregnant woman (age, gestation week, ANC visit count, LGA, facility distance, parity), it:

1. **Calculates a risk score** using a model trained on WHO, DHS, and HMIS datasets
2. **Flags risk level** (Low / Moderate / High / Critical) with plain-language reasoning
3. **Recommends a community action** — specific next steps the CHW should take (transport arrangement, referral, follow-up schedule, emergency escalation)
4. **Shows the nearest health facility** for the woman's LGA
5. **Logs the assessment** so the CHW has a running record of her caseload

The interface is deliberately simple: no medical jargon, works on 3G, readable on a small Android screen.

## How I Built It

- **Risk scoring engine**: Python (scikit-learn) model trained on publicly available Nigerian DHS + WHO maternal health indicators, with features weighted toward known high-risk factors in the Nigerian context (grand multiparity, low facility distance utilization, late ANC entry)
- **Community Action Recommender**: Rule-based decision tree mapping risk level + LGA tier (urban/semi-urban/rural) to specific, actionable CHW steps
- **Frontend**: Streamlit with a CHW-optimized UX — large tap targets, color-coded risk alerts, minimal text input
- **Deployment**: Render.com (live URL available)
- **Data sources**: WHO Global Health Observatory, Nigeria DHS 2018, NHMIS state-level reports

## Challenges

Cleaning and harmonizing three different national datasets with inconsistent LGA naming conventions took significant effort. The bigger challenge was **UX** — designing for a CHW persona meant stripping away everything that seemed useful to an analyst but would confuse someone in the field. Every screen went through at least three rounds of simplification.

## Accomplishments

- Built and deployed a working risk scoring model with ~78% accuracy on held-out Nigerian DHS validation data
- Designed a CHW-first interface that non-technical users in a small pilot could navigate without training
- Identified and quantified the ANC Paradox pattern across 5 Nigerian geopolitical zones using real data

## What I Learned

Data tells you *where* the problem is. Design determines *whether your solution reaches it*. The biggest shift in this project was moving from "what does the data show?" to "what does the CHW need to do next?" Those are very different questions with very different answers.

## What's Next

- Expand LGA coverage to all 774 LGAs with facility geocoding
- Add offline mode (Progressive Web App) for CHWs in areas with no connectivity
- Partner with state Ministry of Health for a pilot in Cross River State
- Integrate with Nigeria's DHIS2 national health information system

## SDG Alignment

**SDG 3.1** — Reduce global maternal mortality ratio  
**SDG 3.8** — Achieve universal health coverage, including access to quality essential health-care services  
**SDG 3.d** — Strengthen the capacity of all countries for health risk reduction and management

## Built By

Ekpenyong Asuquo — Solo developer | Ensign College IT Student | Nigeria
