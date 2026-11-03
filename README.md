# BRIDGE
# Project BRIDGE: Can AI Add Practical Value for a Small Retailer? (Pilot Study)

Project BRIDGE is a small research pilot that tests three ways a small online retailer could use AI: answering customer enquiries, analysing customer feedback, and writing product descriptions. The retailer is a **fictional business called NOVA Retail**, and all data in this project is **synthetic** (created by the author for the study).

> **Please read first:** This is a controlled pilot on made-up data. Results show how the methods behaved in this simulation. They are **not** evidence of how AI would perform, or how much money it would save, in a real business.

**Live dashboard:** https://bridge-fptceptyf238jhk2pwnzeo.streamlit.app/
**Main notebook:** `BRIDGE_01_Research_and_Data_Exploration (1).ipynb`

---

## Research question

Under what conditions could AI-assisted workflows create practical value for a small retailer, and what risks must be managed?

## What is in this repository

| File | Purpose |
|---|---|
| `BRIDGE_01_Research_and_Data_Exploration (1).ipynb` | Full workflow: dataset creation, validation, experiments, scoring, financial scenarios, risk register |
| `app.py` | Streamlit dashboard code |
| `requirements.txt` | Python packages needed to run the dashboard |
| `PROJECT_BRIDGE_backup.zip` | Backup of the project folder created by the notebook (datasets, logs, reports) |
| `PROJECTBRIDGE_...gif` (3 files) | Short screen recordings of the dashboard |

## Datasets (all synthetic)

| Dataset | Size | Description |
|---|---|---|
| A: Customer enquiries | 100 enquiries | 7 categories (Delivery, Returns, Refunds, Cancellation, Payment, Availability, Customer Support). Complexity: 36 Simple, 40 Moderate, 24 Complex. Each has a reference answer, required answer points, an escalation label, the policy it relies on, and what information is *not* available. |
| B: Customer feedback | 120 reviews | 6 topics x 20 reviews each. Sentiment labels: 45 Negative, 40 Positive, 35 Neutral. Ratings are synthetic helper values, not ground truth. |
| C: Product catalogue | 30 products | 6 categories x 5 products. Each record lists approved claims and prohibited (unsupported) claims. |

A fictional policy file (delivery times, 14-day returns, 5-7 business day refunds, cancellation before dispatch, card and cash on delivery, 24 business hour support response) is the source of truth for Dataset A.

## Experiments and results

### Experiment A: Customer enquiry responses (human vs AI)

- 100 enquiries were answered by a human and by AI, then both were scored with the same 5-criterion rubric (policy accuracy, completeness, unsupported claims, escalation correctness, clarity; each 0-2, total /10).
- **Human baseline time (measured):** 5,520 seconds in total (92 minutes), average 55.2 seconds per enquiry. Simple enquiries averaged 23.75 s, Moderate 56.12 s, Complex 100.83 s.
- **Average quality score:** Human 6.85/10, AI 9.90/10.
- The biggest gap was "unsupported claims" (Human 0.51/2, AI 2.00/2). Human answers often added details the policy did not contain.
- **AI processing time and human review time were not measured.**

### Experiment B: Feedback classification

- Input: review text only. Targets: sentiment and topic. Method: TF-IDF features, stratified 80/20 split (96 train, 24 test).

| Task | Model | Accuracy | Macro F1 |
|---|---|---:|---:|
| Sentiment | Logistic Regression | 0.833 | 0.826 |
| Sentiment | Linear SVM | 0.750 | 0.752 |
| Topic | Logistic Regression | 0.917 | 0.911 |
| Topic | Linear SVM | 0.917 | 0.911 |

- Neutral reviews were hardest for sentiment (4 of 7 correct). Topic errors were Customer Support reviews predicted as Returns and Refunds (2 of 24).
- With only 24 test reviews, one prediction changes accuracy by about 4 percentage points, so these numbers are rough.

### Experiment C: Product descriptions

- 30 descriptions were written from catalogue facts (set "A") and a second set was written with a revised prompt (set "B").
- Both sets were AI-written, so this is **not** a human vs AI test. The rubric scores were entered as 2/2 on every criterion, so they do **not** show a real quality difference between the sets. No writing time was measured.
- What this experiment does provide is the catalogue, the claim rules and the scoring template for a proper future test.

### Financial scenarios (assumptions, not measured results)

Using the measured human time (55.2 s per enquiry), the notebook calculates the **maximum human review time** at which AI would still cost no more than the human-only approach. Wage and AI cost inputs are illustrative.

| Assumed wage (PKR/hour) | AI cost 0 PKR | AI cost 1 PKR | AI cost 5 PKR |
|---|---:|---:|---:|
| 200 | 55.2 s | 37.2 s | 0 s |
| 300 | 55.2 s | 43.2 s | 0 s |
| 500 | 55.2 s | 48.0 s | 19.2 s |

This shows AI is not automatically cheaper: review time and service cost decide. It does **not** show that AI saves money for any real business.

### Risk register and adoption framework

The notebook includes a 10-item responsible-AI risk register (for example wrong policy information, failure to escalate, fabricated product claims, data exposure, over-reliance) and a decision framework: conditional adoption for enquiries and product descriptions, assisted use only for feedback analysis.

## Dashboard

The Streamlit dashboard presents the project. Demo recordings are included as GIFs in this repository.

To run it locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to reproduce the notebook

1. Open the notebook in Google Colab.
2. Run the cells in order. They create a `PROJECT_BRIDGE` folder with `data/` and `04_Experiments/` subfolders and save datasets, logs and reports there.
3. Some steps use files uploaded manually (the human response CSVs) and were scored by hand inside the notebook, so exact reproduction requires those inputs.

## Limitations

1. **Synthetic data.** Enquiries, reviews and products were written by the author, so they are cleaner and more repetitive than real customer data.
2. **Single author and evaluator.** The same person created the data, wrote the human responses, and scored both human and AI responses. Scoring was not blind and was not independently checked.
3. **Unequal information in Experiment A.** The AI received the relevant policy text and a list of unavailable information for each enquiry. The human response sheet showed only the enquiry, category and complexity. Part of the quality gap may come from this difference rather than from AI ability.
4. **Experiment A scores are provisional and contain a known error.** AI scores sit near the ceiling (9.90/10), which leaves little room to separate good from excellent. The AI response stored for task 96 (support confirming dispatch) actually answers a refund question that belongs to task 97, yet task 96 was scored 10/10. The reported AI average of 9.90 therefore slightly overstates AI quality. The notebook was left unchanged, so the figures in this README match the notebook as submitted.
5. **Small test sets.** Experiment B used 24 test reviews per task and one split. The model comparison used the same test set, so the choice of Logistic Regression is not a clean held-out result.
6. **Experiment C has no real comparison.** No human-written baseline, no timing, and uniform scores.
7. **Missing measurements.** AI processing time, human review time, correction effort and real costs were not measured, so no ROI or time-saving claim is made.
8. **Labels from one annotator.** No agreement between independent annotators was measured.
9. **Catalogue inconsistency.** Product P020 is named "Linen Table Runner" but its listed material is cotton.
10. **Dashboard not independently documented.** The Streamlit app and demo GIFs present the project, but this README does not list every dashboard page or feature.

## Things to watch when reading the results

- **Do not read "AI 9.90 vs Human 6.85" as "AI is better than people."** The AI was given the policy details for each enquiry, while the human response sheet showed only the enquiry, category and complexity. The comparison is not equal, and the largest gap (unsupported claims) is the one most likely affected.
- **Both sets of scores in Experiment A came from one non-blind evaluator.** Treat them as a first pass, not a verified measurement.
- **Experiment C scores (10/10 everywhere) carry no information.** Do not use them to say one prompt is better.
- **Experiment B percentages are rough.** With 24 test reviews, one prediction is worth about 4 percentage points, and the 83.3% vs 75.0% sentiment difference between models is two predictions. The model comparison used the same test set that is reported, so the numbers may be slightly optimistic.
- **Break-even numbers depend entirely on assumed wages and AI costs.** They show conditions, not real savings.
- **Human timing method.** Human times were recorded by the author; the exact timing method was not documented in the notebook.
- **Synthetic ratings.** Ratings in Dataset B were hand-set and partly revised, so rating-versus-sentiment results say nothing about real customers.

## Future work

- Give humans and AI the **same** policy information and re-run Experiment A.
- Measure AI processing time and human review time, then replace the break-even assumptions with measured values.
- Have a second person score responses and labels without knowing which answers are human or AI; report agreement.
- Use a held-out test set and cross-validation for Experiment B, and test on real or anonymised customer feedback.
- Write a real human baseline for product descriptions and time both workflows.
- Test additional models and prompts, and track errors by enquiry type.
- Add an escalation test: does the system hand over to a human when it should?
- Re-check every AI response against its enquiry (starting with task 96), re-score, and update the Experiment A averages.
- Fix the P020 name or material in the product catalogue.
- Document how human response times were measured.
- Write a full description of each dashboard page in this README.

## Author

GitHub: [amnafatimaa6-ops](https://github.com/amnafatimaa6-ops)
