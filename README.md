# Harness.io PLS Signal Engine (Proof of Concept)

## 🚀 Project Overview
This repository contains the architectural logic for a **Product-Led Sales (PLS) Signal Engine** designed specifically for the Harness multi-product ecosystem. 

**The Objective:** Bridge the gap between "Free Tier" product usage (Segment data) and Enterprise Sales outreach (Salesforce/Outreach.io). 

**The Problem Solved:** Harness has high-velocity product usage data (12.8T API calls). Sales reps often lack visibility into *which* specific module (CI, CD, Feature Flags, or Cloud Cost) a prospect is using. This engine detects "High Intent" usage patterns and automatically routes the lead to the correct specialist sequence.

## 🛠 Tech Stack
* **Data Source:** Segment (Product Events) / Snowflake (Warehouse)
* **Orchestration:** Python / Workato (Middleware)
* **CRM:** Salesforce (Lead Object & Task Creation)
* **Engagement:** Outreach.io (Sequencing)
* **Enrichment:** Clearbit (Identity Resolution)

## ⚡ Architecture
1.  **Ingest:** Listen for specific Segment `track()` events (e.g., `deployment_success`, `feature_flag_toggled`).
2.  **Filter:** SQL Logic identifies users crossing "PQL Thresholds" (e.g., >10 deployments in 24h).
3.  **Enrich:** Call Clearbit API to hydrate firmographic data.
4.  **Route:** * If `Employee_Count > 500` -> **Enterprise Rep**
    * If `Employee_Count < 500` -> **PLG Automated Sequence**
5.  **Act:** Update Salesforce Lead Status to `Open - High Intent` and add to Outreach Sequence.

## 📈 Impact
* Reduces "Speed to Lead" from days to seconds.
* Increases SDR efficiency by removing manual research on active free-tier users.
* Aligns messaging to the *exact* product module being used.
