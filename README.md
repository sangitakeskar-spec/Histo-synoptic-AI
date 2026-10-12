# HISTO-SYNOPTIC AI — Research Prototype

A **human-supervised, rule-based** demonstration of histopathology synoptic-report completeness checks. Includes a Streamlit app, 500 synthetic examples, protocol-checklist configuration, audit export, and capstone evaluation tools.

> **NOT FOR CLINICAL USE.** The included checklists are **illustrative teaching subsets**, not verified CAP protocols. Never use this app for sign-out, patient care, or as evidence of CAP compliance. A pathologist must confirm protocol version, applicability, and every finding. No clinical data should be uploaded to public services.

## Quick start (Windows / Mac)
1. Install Python 3.10+.
2. Extract ZIP; open terminal in the `HISTO-SYNOPTIC-AI` folder.
3. Run `python -m pip install -r requirements.txt`.
4. Run `python -m streamlit run app.py`.
5. Paste a **synthetic** report, choose specimen/procedure, click **Analyze demonstration report**.
6. Review every flag; download CSV/JSON if needed.

## Features
- Specialty-aware selection of *illustrative* checklist fields (CRC, breast, endometrial, lung).
- Explicit **not applicable**, **unknown**, and **needs human verification** states.
- Conservative phrase matching; never infers staging or fabricates clinical values.
- A reviewer decision panel and downloadable per-report audit JSON.
- Synthetic dataset and evaluation script with a fixed 80/20 partition.
- Optional CSV dashboard for synthetic cases.

## Methodology
The system is **rules + text heuristics**, not a trained ML model. An 80/20 split is provided for reproducible development/evaluation, not claimed model training. Synthetic labels reflect the generator's design, not independent clinical truth. No sensitivity, specificity, or accuracy claims are made without independently adjudicated reference labels.

## Repository layout
`app.py`, `src/checker.py`, `standards/demo_checklists.json`, `data/synthetic_reports.csv`, `scripts/evaluate.py`, `templates/google_sheets_template.xlsx`, `docs/`, `gemini-prompts/`, `examples/`, `dashboards/`, `results/`.

## Clinical governance
Before any real-world study: verify current CAP/AJCC/other applicable protocols and specimen inclusion criteria, license any protocol text, obtain approvals, de-identify data, establish a gold-standard adjudication protocol, and validate performance per specialty. Do not commit patient data, credentials, or proprietary protocol PDFs.

## Future work
1. **LIS integration:** controlled interface, HL7/FHIR where supported, access control, staging environment, traceable reviewer sign-off.
2. **Real-world validation:** ethics/institutional approval, de-identified multicentre data, blinded dual-pathologist labels, discordance adjudication, sensitivity/precision/specificity with confidence intervals, prospective silent-mode trial.
3. **Scaling:** verified versioned protocol registry, multi-site deployment, monitoring for drift and false alerts, role-based access, secure audit logs.

## License
MIT for original prototype code only; external clinical protocols retain their respective copyrights.
