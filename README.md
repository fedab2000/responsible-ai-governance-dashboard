# Responsible AI Governance Dashboard

A Streamlit portfolio project that evaluates AI ethics, governance maturity, and risk across deployed AI/ML systems.

## Purpose

This project demonstrates how an analytics or ML manager can monitor an organization's AI portfolio from an executive governance perspective.

It uses existing deployed portfolio projects as example AI systems, including insurance fraud detection, insurance pricing, healthcare prediction, higher education analytics, and student support classification.

## Features

- Executive KPI overview
- AI system inventory
- Governance maturity scoring
- Risk level classification
- Risk heatmap
- Gap analysis and recommended actions
- Framework alignment placeholder for Responsible AI standards

## Scoring Logic

Each AI system is scored across six governance controls:

- Bias testing
- Explainability
- Monitoring
- Human oversight
- Documentation
- Privacy controls

Scores:

- Yes = 100
- Medium = 60
- No = 0
- Not Applicable = 100

The governance score is the average of the control scores.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Next Enhancements

- Add scenario planning sliders
- Add framework mapping to NIST AI RMF, OECD AI Principles, EU Trustworthy AI, and Canadian AIA-style categories
- Add ML model to predict governance risk level
- Add downloadable executive report
- Add project links to GitHub and Streamlit deployments
