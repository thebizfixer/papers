# Capstone scripts plan

Jupyter notebooks for D606 live in this folder. They reuse **method** from the MSDA Archive at `C:\Users\Owner\OneDrive - Western Governors University\Courses\MSDA\Archive`. They do **not** reuse prior-course CSVs. Every notebook is written against the files already in `data/` (see `data/README.md`).

The project plan (`../Capstone Project Plan.md` §11) is the short map. This file is the cell-level plan.

**Assumption:** “Same code as D205/D206” means the same numbered ETL and assess→mitigate→save sequence, rewritten for Table 8 and ACS. It does not mean pasting churn SQL or `churn_raw_data.csv`.

---

## Archive what we keep vs drop

| Archive course | What that work actually was | Keep for D606 | Do not bring over |
| --- | --- | --- | --- |
| D205 Acquisition | Numbered SQL: create → load → join → view → confirm | Numbered load/join/confirm cells; print row counts after each step | Postgres, churn ERD, survey-response tables |
| D206 Cleaning | `churn_assess.py` then `churn_mitigate.py`: names, dups, missing, outliers; re-assess; `to_csv` | Assess → mitigate → re-assess → write `place_year_clean.csv` | Imputing the target; D206 PCA as a scored method |
| D207 Exploratory | Cleaned-file EDA + one bivariate test + plots | Univariate/bivariate on the frozen place-year table | Chi-square on churn; any test that replaces H0 |
| D208 Task 1 | `statsmodels` OLS, residual scatter, ANOVA table, then reduced models | OLS of property-crime rate on the three locked predictors; residuals; VIF | Stepwise/reduced models that drop a mediator; bandwidth/churn DVs |
| D208 Task 2 | Logistic regression | Nothing | Classification |
| D209 | Numbered functions; `train_test_split`; saved figures | Blocked place split (Census division); `RidgeCV`; save figures | kNN, random forests, SelectKBest that can drop a mediator |
| D210 | Owner-facing charts + presentation script | Control-mix table, predicted-vs-actual, one Northern Utah walk-through | Tableau-only workflow |
| D603 | Gradient boost / k-means | Nothing | Trees, clustering, SHAP |
| D605 | Objective, variables, constraints, PuLP, sensitivity | Security LP vs equal-share; ±25% on \(\alpha_k\) | Amazon air network |

D204 and D597 are out of scope for these notebooks.

---

## Folder layout

```text
scripts/
  README.md                                          this plan
  01_d205_d206_build_place_year.ipynb                done
  02_d207_eda.ipynb                                  done
  03_bigset_qa_and_feature_freeze.ipynb              done
  04_d208_ols_and_vif.ipynb                          done (H0 decided)
  05_ridge_and_d605_lp.ipynb                         done (Stage 3)
  06_d210_exhibits.ipynb                             done (exhibits; no new estimators)

data/processed/                                      written by notebooks (not collected)
  place_year_joined.csv
  place_year_clean.csv
  exclusion_log.csv
  feature_list.md
  alpha_k.csv
  blocked_split.csv
  bigset_qa_log.csv
  ols_coefficients.csv
  vif.csv
  ridge_predictions.csv
  control_mix.csv
  lp_equal_share.csv
  lp_comparison.csv
  lp_sensitivity.csv
  nu_briefing.csv
  lp_ppe_shares.csv

scripts/figures/
  02_univariate_histograms.png
  02_bivariate_scatters.png
  02_correlation_heatmap.png
  04_residual_vs_fitted.png
  06_nu_predictor_trends.png
  06_ppe_security_shares.png
```

Notebooks resolve the Capstone root from the working directory (`Capstone/` or `scripts/`). Do not hard-code a drive path.

---

## 01 — D205 + D206: build the cleaned place-year table

**Purpose.** One analysis table: place-year rows with the FBI property-crime rate and the ACS mediators/controls. This is gathering steps 1–3 and D206 cleaning. No OLS, Ridge, or LP in this notebook.

**Inputs (already collected).**

- `data/target/` Table 8 CSVs, 2022–2024
- `data/place_filter/` and copies of DP05 (population, race/ethnicity)
- `data/mediator_poverty/` DP03
- `data/mediator_residential_instability/` DP02, DP04
- `data/restricted_predictor/` DP02, B05002
- `data/controls/` Gazetteer (land area)

Use one copy of each official file (for example DP05 from `place_filter/`). Do not read BigSet here except later, in 03.

### D205 half — numbered ETL

Same spirit as D205 queries `1_Create` … `7_Confirm`: one step, then a confirmation print.

1. **Load Table 8.** Skip the published title rows. Forward-fill `State`. Keep City, Population, Property crime, Burglary, Larceny-theft, Motor vehicle theft, Arson. Add `year`. Stack 2022–2024. Confirm: row count per year, no empty city names.
2. **Load ACS place tables** for the same years: DP05 (total pop `DP05_0001E` + race/ethnicity estimates), DP03 (poverty, unemployment, median household income), DP02 (moved in last year), DP04 (renter-occupied), B05002 (foreign-born). Keep `GEO_ID`, `NAME`. Confirm: ~31.9k–32.0k places per year.
3. **Load Gazetteer** place national files (`GEOID`, `ALAND_SQMI`, lat/long). Confirm: one row per GEOID per year.
4. **Keys.** Table 8 is `state + city` (no GEOID). ACS is `GEO_ID` / `NAME` (`Ogden city, Utah`). Build a match key: uppercase state postal from Table 8 state name; strip `city` / `town` / `village` / `CDP` / punctuation from both sides; join ACS `NAME` the same way. Left-join Gazetteer on ACS `GEOID`. Confirm: match rate; list unmatched Table 8 cities with ACS population ≥ 50,000.
5. **Universe filter.** Keep ACS population ≥ 50,000. Prefer rows whose ACS `NAME` is an incorporated city (not CDP) unless the Table 8 agency is clearly that place. Confirm: count of places and place-years.
6. **Coverage.** Table 8 has no months-reported column. Document that CIUS Table 8 is the 12-month city table, so the plan’s 12-month floor is the table definition. Drop rows with missing burglary, larceny-theft, or motor vehicle theft. Do not impute the target. Confirm: dropped-row counts in `exclusion_log.csv`.
7. **Measures.**
   - Property crime count = burglary + larceny-theft + motor vehicle theft (do not add arson).
   - Rate per 100,000 = count / ACS population × 100,000 (ACS pop is the denominator; Table 8 pop is a check only).
   - Poverty rate from DP03.
   - Blau heterogeneity \(1 - \sum_g p_g^2\) from a **locked** DP05 race/ethnicity group list written in a markdown cell before the compute cell.
   - Residential instability = percent moved in the last year (DP02). Keep renter share (DP04) as a companion column, not a second H0 predictor.
   - Controls: unemployment, median household income, population, density = pop / `ALAND_SQMI`.
   - Restricted context: foreign-born share (B05002 / DP02). Not a hypothesis predictor.
8. **CDE gaps (optional attach only).** Do not replace Table 8. After the official join, flag place-years still missing a target that appear in `data/cde_gaps/`. Do not fill those holes until notebook 03 hand-check.

Confirm after step 8: n place-years. Plan target is ≥ 200. If n < 200, stop and apply the plan rollback (25,000 floor or burglary-only). Do not add rural places.

### D206 half — assess, mitigate, re-assess, save

Same sections as `churn_assess.py` / `churn_mitigate.py`, on the joined table.

**Assess (before changing values).**

- Column names: snake_case once (`place`, `state_abbr`, `year`, `property_crime_rate`, `poverty_rate`, `blau_heterogeneity`, `pct_moved_year`, …).
- `info()` / `describe()` in small column groups.
- Duplicates on `geoid + year` (and on `state + place + year`).
- Missingness by column; do not impute the target.
- Impossible values: negative counts or rates; poverty/renter/moved shares outside 0–100; Blau outside 0–1; density ≤ 0.
- Outliers on the three predictors and the rate (IQR flags only; do not delete high-crime cities just for being high).

**Mitigate.**

- Drop exact duplicate keys; keep a log.
- Drop rows with missing target or missing any of the three predictors.
- Fix types (`year` int, rates float).
- Do not winsorize the target to “improve” the regression.
- Do not run PCA (D206 required it; this capstone does not).

**Re-assess.** Repeat the assess block on the mitigated frame. Then:

```text
data/processed/place_year_joined.csv   # post-join, pre-drop
data/processed/place_year_clean.csv    # analysis table
data/processed/exclusion_log.csv
```

Screenshot each load, join, filter, and write cell for Task 2 C.

**Done when:** `place_year_clean.csv` exists, n ≥ 200 (or rollback recorded), exclusion log is complete, Blau groups are written in the notebook before the compute cell.

**Status (6 Sep 2026):** Done. 2,182 place-years, 771 places. No target imputation. Arson stored, not in the count. CDE-gap rows flagged only.

---

## 02 — D207 EDA

**Purpose.** Describe the cleaned table. Do not accept or reject H0 here.

- Univariate: property-crime rate and the three predictors (histograms, describe, IQR) — same plotting habit as D207 / D208 DV description.
- Bivariate: scatter of each predictor vs the rate; pairwise correlation (preview of Stage 2, not the test).
- Optional: one Northern Utah in-scope city highlighted on those plots (Ogden, Layton, Logan, or another city in Box Elder, Cache, Rich, Weber, Morgan, Davis that cleared the floor).
- Arson coverage check only: whether arson missingness is usable. Default is arson stays out of the target.

Write figures under `scripts/figures/02_`.

**Status (6 Sep 2026):** Done. Rate is right-skewed (median ~2,094; mean ~2,320). Pearson vs rate: poverty 0.37, mobility 0.25, Blau 0.13. Arson has 87 null values (4.0%) and stays out of the target. Ogden sits inside the national cloud. H0 is not decided here.

---

## 03 — BigSet QA and feature freeze

**Purpose.** Plan gathering steps 5–6. No model fit.

**D206-style QA on the three BigSet CSVs** (`cde_gaps`, `control_cost`, `feature_selection_corpus`):

- Sample source URLs; drop dead links, named private persons, non-property-crime stories.
- Restrict news to study places on the **training** side of the blocked split (define Census division on the clean table; do not mine holdout divisions).
- Tag offense / asset / site condition. Drop offender/victim demographic themes.
- Keep a theme only if it appears in ≥ 5 sourced stories **and** maps to an official field or an LP control. Map it; do not add headline counts.

**Freeze (write files, then stop).**

- `data/processed/feature_list.md` — the three mediators plus any accepted official adds. This list does not change after 03.
- `data/processed/alpha_k.csv` — one row per control family (fortification, surveillance, alarm, authorization) from the cleaned price book. Freeze before notebook 05.

CDE-gap rows may fill official holes only if the URL passed QA and the year is 2022–2024. Re-write `place_year_clean.csv` only if a gap fill is accepted; log it.

**Done when:** feature list and \(\alpha_k\) files exist. OLS is still not run.

**Status (6 Sep 2026):** Done. Official adds: none. Gap fill: none (`place_year_clean.csv` not rewritten). Holdout divisions: New England and Middle Atlantic (87 places holdout / 684 train). \(\alpha_k\) uses the 0.20 effectiveness fallback on all four families. Notebook 05 must read `alpha_k.csv` and must not refit those medians.

---

## 04 — D208 Stage 1 OLS and Stage 2 VIF

**Purpose.** This notebook decides H0. Copy D208’s `statsmodels` OLS, residual scatter, and coefficient/SE/p/F table. Do not copy D208’s reduced-model ladder.

- DV: `property_crime_rate`.
- Predictors (locked): `poverty_rate`, `blau_heterogeneity`, `pct_moved_year` (plus only columns listed in `feature_list.md`).
- Fit OLS. Report intercept, three slopes, each SE, each p-value, \(R^2\), overall F and its p-value.
- Decision rule (already locked): reject H0 if the overall F-test is significant at α = 0.05 **or** at least one coefficient p-value is < 0.05.
- Residual vs fitted (D208). Optional residual Moran’s I (plan guardrail); do not put a spatial lag of the target in the model.
- Stage 2: pairwise correlation of the three predictors; VIF (flag > 5). This is not a second hypothesis.

Do not add RMSE, the LP, or Ridge into this H0 write-up.

Fit OLS on the **full** cleaned table. The blocked split is for news-theme selection (already frozen) and for Ridge evaluation in notebook 05. It is not a holdout for H0.

**Done when:** coefficient table and VIF table exist.

**Status (6 Sep 2026):** Done. H0 rejected at α = 0.05. F = 148.91 (p = \(8.93 \times 10^{-88}\)). All three coefficient p-values < 0.05. \(R^2\) = 0.170. Predictor VIFs 1.16, 1.00, 1.16 (none flagged). Residual Durbin–Watson = 0.64; Moran’s I was not computed. Place-years repeat places, so default OLS standard errors are too small; added as a post-hoc addendum (after the scored decision), a place-clustered standard-error re-fit leaves every coefficient significant (clustered p-values all < 0.001) and is **not** the scored test. Files: `data/processed/ols_coefficients.csv`, `data/processed/vif.csv`, `scripts/figures/04_residual_vs_fitted.png`.

---

## 05 — Ridge (D209 split pattern) and D605 LP

**Purpose.** Stage 3 only. Does not accept or reject H0.

**Ridge (D209-style numbered steps, different estimator).**

1. Load `place_year_clean.csv` and the frozen feature list.
2. Reuse `blocked_split.csv` (places, not random rows). Do not pick a new holdout. Holdout divisions were not used to choose features (already frozen in 03). Read `alpha_k.csv`; do not refit the 0.20 effectiveness fallback.
3. `RidgeCV` on the training blocks.
4. RMSE and MAE on the holdout vs a mean-rate baseline.
5. Save \(\hat r_i\) on all study rows for the LP.

No kNN, no random forest, no gradient boosting.

**LP (D605 components: objective, variables, constraints).**

- Decision variables \(x_{g,k} \ge 0\): dollars of control \(k\) in risk group \(g\).
- Groups \(g\): fixed tiers from \(\hat r_i\) (for example top decile / top quartile / rest). Not clustering.
- Exposure \(E_g = \sum_{i \in g} \hat r_i \times w_i\) with \(w_i\) = ACS population (CBP only if a clean place/county join was accepted in 01/03).
- \(\alpha_k\) from the frozen `alpha_k.csv`. Residual loss cannot fall below 50% of exposure (plan guardrail).
- Baseline: equal-share of budget \(B\) across the four controls (and groups). Compare residual loss to that baseline.
- Sensitivity: rerun at ±25% on each \(\alpha_k\).
- Role floors (owner stack): fortification + surveillance \(\ge 60\%\) of \(B\); each of those two \(\ge 20\%\); alarm between 15% and 25%; preventive dollars and the alarm floor sit in the high and mid tiers. Authorization has no floor. Do not refit \(\alpha_k\).

**Done when:** control-mix table (dollars by tier and control) plus equal-share comparison exist.

**Status (6 Sep 2026):** Done. Ridge \\(\\lambda\\) = 26.37. Holdout RMSE 1,050 vs mean-baseline 1,021. Planning budget \\(B = \\$10\\) million. Hardened mix: \\$5M fortification (mid) + \\$3.5M surveillance (high) + \\$1.5M alarm (high). Prevention 85%, alarm 15%. Residual avoided vs equal-share ≈ 8,147 expected-count units. Files: `ridge_predictions.csv`, `control_mix.csv`, `lp_equal_share.csv`, `lp_comparison.csv`, `lp_sensitivity.csv`.

---

## 06 — D210 exhibits

**Purpose.** Owner-facing outputs that lead Task 3. No new estimators.

Required exhibits (project plan §3 Storytelling):

1. Residual plot from notebook 04.
2. OLS slopes and VIF from notebook 04 (quantitative benefit: +60 / +28 / +114 per 100,000).
3. Northern Utah (Ogden, Layton, Logan) 2022–2024 trends on the three predictors vs the national median.
4. LP as a split of the **security slice of fixed-asset investment** (50 / 35 / 15 / 0 on each $100 of PPE security capital), vs equal-share. Authorization stays at $0: access control is a theft/occupancy tool; property damage and street theft are delay and watch first.
5. Ogden walk-through on a $1 million security slice (do not assign Ogden the national high-tier camera pot).

Task 2 C screenshot PDF is later in Word, not this notebook’s logic. Task 3 slides are a separate deck.

**Status (6 Sep 2026):** Done. In-scope NU cities: Ogden and Layton (low Ridge tier; rates falling) and Logan (high Ridge score from poverty ~22–24% and mobility ~30%, actual rate 1,150–1,460). Files: `nu_briefing.csv`, `lp_ppe_shares.csv`, `scripts/figures/06_nu_predictor_trends.png`, `scripts/figures/06_ppe_security_shares.png`.

---

## Gates

| Gate | Rule |
| --- | --- |
| After 01 | Passed. n = 2,182. No models. |
| After 02 | Passed. EDA of the cleaned table. No models. |
| After 03 | Passed. Feature list and \(\alpha_k\) frozen. No models. |
| After 04 | Passed. H0 rejected at α = 0.05. Ridge/LP still not used as the hypothesis test. |
| After 05 | Passed. Mix vs equal-share written. H0 unchanged. |
| After 06 | Passed. Four exhibits + NU trends + PPE-slice percents. No new estimators. |
| Task 2 Word | After Task 1 has a passing score. |
| Task 3 slides | After Task 1 and Task 2 pass. |

Data work in 01–03 can run while Task 1 is in evaluation.

---

## Implementation order

1. Build **01** only. Verify: `place_year_clean.csv` and exclusion log. **Done.**
2. Build **02**. Verify: EDA figures. **Done.**
3. Build **03** then **04**. Verify: frozen `feature_list.md` and \(\alpha_k\), then OLS table + VIF. **Done.**
4. Build **05** then **06**. Verify: mix vs equal-share + four exhibits. **Done.**

Do not reopen 04 to change H0. Do not add notebooks beyond these six unless the CI requires a separate screenshot workbook.
