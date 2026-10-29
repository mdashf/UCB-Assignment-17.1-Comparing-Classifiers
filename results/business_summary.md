# Findings and recommendations — bank marketing

**Source:** 41,188 historical telephone contact records, 17 campaigns, May 2008–November 2010. **Positive subscription rate:** 11.27%.

## What the comparison shows

- **Logistic regression** was selected using 3-fold cross-validation average precision (CV AP 0.448). Its untouched holdout AP was **0.462**, ROC AUC **0.775** and accuracy **90.3%**.
- Raw accuracy is not a good business objective: a model that predicts every contact will decline is already **88.75% accurate**, yet misses 100% of subscriptions.
- At the selected model's default threshold, subscriber recall is **25.9%** and precision is **68.0%**. This threshold is not optimized for bank economics.
- If only **20%** of records could be contacted and the historical scores could rank them, that group contained **63.0% of observed subscriptions** with a **35.4% conversion fraction** (**3.15× retrospective lift**).
- The tuned decision tree has higher recall at its default class threshold (**65.2%**) but lower precision (**29.6%**) than logistic regression; comparative rankings depend on the chosen operational metric.
- Historical economic features exhibit predictive importance, but do not establish that they cause customers to accept deposits. Their usefulness may degrade outside the financial environment of 2008–2010.

## Actionable next steps

1. **Pilot, do not blindly deploy.** Use ranking as a *human-reviewed* outreach shortlist, subject to customer permission and appropriate regulations.
2. **Compare against an actual randomized control group** to determine whether using the model generates incremental subscriptions and profit rather than merely finding customers who would have subscribed anyway.
3. **Set call budgets and success criteria first.** Track contact cost, false positives, opt-outs, net revenue and customer experience. Evaluate alternative decision thresholds only on a fresh validation set.
4. **Guard against leakage and drift.** Exclude post-contact `duration`; validate on later time periods and contemporary data. Historical macroeconomic values may encode the campaign period.
5. **Check group-level harms and model performance.** Review uneven error rates by occupation/age bands and avoid discriminatory targeting policies.

**Limitations:** Modeling uses a 12,000-row stratified sample rather than the full historical training set. Sampling and random splitting are reproducible but do not validate deployment across time or unique customers. Results are historical associations, not measured customer willingness to buy or causal effects of calling.
