# Comparing Classifiers — Required Assignment 17.1

**UC Berkeley Professional Certificate in Machine Learning & Artificial Intelligence**  
**Business case:** Improving outreach prioritization for a Portuguese bank's telephone term-deposit campaigns  
**Main deliverable:** [Fully executed Jupyter notebook](Bank_Marketing_Comparing_Classifiers_17_1.ipynb)  
**Bank-manager summary:** [Actionable business findings](results/business_summary.md) · [Five figures](figures/) · [Model results](results/)

## Executive summary (for a nontechnical banking manager)

This project examines **41,188 historical contact records from 17 campaigns (May 2008–November 2010)**. Only **4,640 (11.27%)** resulted in a term-deposit subscription, so predicting that *no one* would subscribe already achieves ~88.7% accuracy while identifying **zero** subscribers. We therefore evaluate whether models can *rank potential subscribers*, not merely improve raw accuracy.

An initial **client-only logistic model** (seven customer descriptors) achieved **AP 0.199**. We then compare **logistic regression, k-nearest neighbors (KNN), decision tree, and support vector machine (SVM)**, each with the same expanded pre-call preprocessing pipeline. Experiments use a **reproducible stratified 12,000-record sample** from the official full source (9,600 training; 2,400 untouched test), with **3-fold cross-validation and GridSearchCV** on training data. Raw data statistics are calculated on all 41,188 records; modeling metrics are measured on the disclosed sample, not claimed for all records.

**The winner chosen by *training-CV average precision* was Logistic regression.** On the previously unseen holdout it achieved:

- **Average precision (AP): 0.462**, against **0.113** base subscription rate.
- **ROC AUC: 0.775**, indicating moderate ranking discrimination.
- **Accuracy: 90.3%**, but **recall: 25.9%** at the classifier's default threshold. Accuracy alone hides missed subscribers.
- **Top-20%-of-calls screening:** 35.4% subscription share in the highest-ranked 20% of holdout contacts; that subset contains **63.0%** of observed subscriptions, or **3.15× lift** relative to untargeted selection.

These are **retrospective ranking statistics**, not estimates of incremental conversions, willingness to subscribe in a different campaign, or monetary profit. No uncontacted-person outcomes or randomized trial are available.

### Four-classifier comparison (tuned models, untouched holdout)

| Model | CV AP | Holdout AP | ROC AUC | Accuracy | Recall (yes) |
|---|---:|---:|---:|---:|---:|
| Logistic regression | 0.448 | 0.462 | 0.775 | 0.903 | 0.259 |
| KNN | 0.416 | 0.427 | 0.755 | 0.903 | 0.252 |
| Decision tree | 0.410 | 0.461 | 0.785 | 0.787 | 0.652 |
| SVM (RBF) | 0.407 | 0.400 | 0.689 | 0.900 | 0.215 |

The tuned decision tree recovers more subscribers at its default threshold, but its precision is lower; thresholds need to reflect the bank's capacity and outreach costs. Small differences in AP (logistic vs. tree) should not be treated as proof of a universal winner. All four candidates were compared on the **same** train/holdout records, with no `duration` feature.

## Findings and actionable recommendations

1. **Prioritize for review, do not automatically call.** Use the model's ranking only as a first-pass, human-reviewed screening tool. The top-quintile result suggests a potentially more focused contact list under a fixed call budget, not established incremental marketing impact.
2. **Measure meaningful commercial outcomes.** Before deployment, collect actual incremental term deposits, contact costs, opt-outs, call duration, customer complaints and realized profit, comparing ranked calling with a randomized outreach control.
3. **Check context drift.** Labor/economic indicators such as `emp.var.rate` and `cons.price.idx` dominate permutation-based predictive dependence, which can encode **2008–2010 period effects**, not stable individual preferences. Validate on a later period and a current market.
4. **Prevent target leakage.** Never use `duration` (how long the call lasted) to decide whether to make the call. Keep all preprocessing **inside** training folds.
5. **Respect context and customer treatment.** The raw data include demographics, and explanatory relationships are not causal. Review fairness, consent, compliance and business suitability before targeting customers.

## CRISP-DM workflow and starter problems

| Phase | Starter problems | Work completed |
|---|---|---|
| Business understanding | 1, 4 | 17 campaigns from paper; prospectively usable business question and metrics |
| Data understanding | 2, 3 | Read 41,188 × 21 source CSV; inspect class balance, `unknown` values, numeric distributions |
| Data preparation | 5, 6 | Treat `pdays=999` as a special sentinel; exclude post-call `duration`; stratified sample/split; train-fold preprocessing |
| Modeling | 7–10 | Majority baseline and default logistic, KNN, tree and RBF SVM; fit times and accuracies |
| Evaluation | 11 | 3-fold stratified training CV, per-model grids, untouched test, precision–recall/ROC, confusion, coefficient and permutation diagnostics |
| Deployment considerations | 11 extension | Ranked outreach pilot proposal, limitations, drift controls, data collection plan |

**Data note:** The historical full CSV is *ordered by date*, but this project uses a random stratified split for cross-sectional comparisons in accordance with the classroom exercise. It does **not** establish future-period generalization. No stable customer ID was supplied, so repeated clients may appear in different splits; a client-grouped, time-forward follow-up is advisable.

## How to reproduce

1. Obtain `module17_starter.zip` from the official assignment and extract `data/bank-additional-full.csv` into this repository's `data/` folder (the file is deliberately **not** committed to GitHub). Alternative: put `module17_starter.zip` directly in `data/`, or set `UC_BANK_DATA_PATH` to the CSV/ZIP path.
2. Install Python 3.11+ and `python -m pip install -r requirements.txt`.
3. Open [`Bank_Marketing_Comparing_Classifiers_17_1.ipynb`](Bank_Marketing_Comparing_Classifiers_17_1.ipynb) and **Run All**.
4. Run `python verify_project.py` to verify notebook execution and supporting artifacts. The notebook creates/updates figures and results in place.

`MODEL_N=12000`, `SEED=42`, 80/20 stratified train/holdout split, 3-fold training CV and fixed grids are defined directly in the notebook. Feature preprocessing uses pipelines fitted **inside each CV fold**. CPU runtime depends on hardware; a standard laptop may run SVM searches slower than the environment used to generate this submission.

**Source provenance:** the byte-for-byte UCI `bank-additional-full.csv` extracted from the course starter ZIP has SHA-256 `{s['dataset_sha256']}`. The source data are 41,188 contact rows × 21 fields, and there is no attempt to represent this as 41,188 unique clients.

## Repository contents

```text
README.md
Bank_Marketing_Comparing_Classifiers_17_1.ipynb
requirements.txt
verify_project.py
.gitignore
data/README.md                 # no raw CSV in public repository
figures/                       # 5 rendered, captioned statistical figures
results/                       # default/tuned/CV metrics, coefficients, importance and business summary
```

**References:** Moro, S., Cortez, P. & Rita, P. (2014), *A Data-Driven Approach to Predict the Success of Bank Telemarketing*, *Decision Support Systems*, **62**, 22–31. https://doi.org/10.1016/j.dss.2014.03.001. Dataset: https://archive.ics.uci.edu/dataset/222/bank+marketing.

**Submission:** The Emeritus assignment expects **one public GitHub repository URL**, not the ZIP. Review the notebook's saved outputs personally, publish the files, confirm README/notebook rendering on GitHub, then submit the **repository URL** by November 2, 2026 (course-platform deadline).
