# Data collection

This folder holds the public files for Topher Maile’s WGU D606 capstone. The research question asks to what extent poverty rate, ethnic heterogeneity, and residential instability affect the property crime rate in U.S. cities with population ≥ 50,000. The analysis unit is the **place-year**. The panel is **2022–2024**, the latest three complete years that both FBI Crime Data Explorer (CDE) city tables and ACS 5-year place tables cover.

Official FBI, Census, and County Business Patterns (CBP) products were downloaded as published files. BigSet was used only for three supplemental tables that those agencies do not publish: CDE coverage gaps, a commercial security price book, and a sourced property-crime news corpus. No fabricated counts, prices, or headlines were added.

Collection ran 5–6 September 2026. Notebooks 01–06 then wrote the analysis files under `processed/`. Those files are derived, not collected.

## Folder convention

- **Subfolder** = the variable’s role in the plan (target, place filter, mediators, and so on).
- **Filename** = the official source product name (or the BigSet export name for the three supplements).
- When one official file serves more than one role, the same CSV is stored in each role folder. Those copies are identical.

ACS 2025 5-year tables were not published at collection time. CBP 2024 county files were not published at collection time (Census listed a summer 2026 release). Those years are absent on purpose.

| Role folder | What it is for | Files on disk |
| --- | --- | --- |
| `target/` | Property-crime counts for the dependent variable | FBI CIUS Table 8, 2022–2024 |
| `place_filter/` | Place population (study-universe filter) | ACS DP05, 2022–2024 |
| `restricted_predictor/` | Foreign-born share (context; not a hypothesis predictor) | ACS DP02 and B05002, 2022–2024 |
| `mediator_poverty/` | Poverty rate | ACS DP03, 2022–2024 |
| `mediator_heterogeneity/` | Race/ethnicity shares for the Blau index | ACS DP05, 2022–2024 |
| `mediator_residential_instability/` | Renter share and recent movers | ACS DP02 and DP04, 2022–2024 |
| `controls/` | Unemployment, income, land area | ACS DP03 and Gazetteer place files, 2022–2024 |
| `exposure_weight/` | Population and establishment counts for the later LP | ACS DP05, 2022–2024; CBP county, 2022–2023 |
| `cde_gaps/` | Agency property-crime counts posted outside CDE | BigSet CSV |
| `control_cost/` | Installed cost and claimed loss-reduction for four control families | BigSet CSV |
| `feature_selection_corpus/` | Sourced news stories used only to choose extra official fields | BigSet CSV |

`_bigset_one_at_a_time.py` is a helper used during BigSet collection. It is not a dataset.

---

## Official products

### Shared method

If FBI, Census, or CBP already publish a field, that published file was used. Pages were not scraped.

**FBI CIUS Table 8.** For each year 2022–2024, a signed download URL was requested from CDE:

`https://cde.ucr.cjis.gov/LATEST/s3/signedurl?key=cius/{year}/offenses-known-to-le-{year}.zip`

The zip was opened and the official Table 8 workbook was converted to CSV with the workbook’s own name kept:

- 2022: `Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2022.csv`
- 2023: `Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2023.csv`
- 2024: `CIUS_Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2024.csv`

Title rows from the workbook were left in place. These tables are 12-month city-agency offense counts known to law enforcement.

**ACS 5-year place tables.** The Census Data API requires a key. Tables were pulled instead from the data.census.gov access endpoint, one state at a time, for every state and DC, then stacked into one national CSV per table-year:

`https://data.census.gov/api/access/data/table?id=ACSDP5Y{year}.{table}&g=040XX00US{state}$1600000`

Detailed table B05002 used the same geography with id `ACSDT5Y{year}.B05002`. Geography `040XX00US{state}$1600000` is all places in that state. Headers are ACS variable IDs (`GEO_ID`, `NAME`, `DP05_0001E`, and so on). Place counts are about 31,894 (2022), 32,033 (2023), and 32,038 (2024), plus a header row.

**Gazetteer.** Census national place Gazetteer files for 2022–2024 were downloaded from the Census Gazetteer program and stored as CSV under the official base name (`2022_Gaz_place_national.csv`, and the 2023 and 2024 counterparts). They supply land area for density.

**CBP.** County-level County Business Patterns CSVs `cbp22co.csv` and `cbp23co.csv` were downloaded from the Census CBP datasets site (`https://www.census.gov/programs-surveys/cbp.html` / www2.census.gov CBP datasets). They are county establishment files, not place files; a later join is needed if they are used as an LP exposure weight.

FBI and Census products are U.S. government public-domain statistical files.

### Dataset summaries

**Target — FBI CIUS Table 8 (city).** Annual offenses known to law enforcement by state and city. Columns include city population and counts for violent crime, murder, rape, robbery, aggravated assault, property crime, burglary, larceny-theft, motor vehicle theft, and arson. The hypothesis target is the FBI property-crime rate (burglary + larceny-theft + motor vehicle theft per 100,000). Arson stays out of the target unless coverage later clears the same 12-month floor as the other offenses. CSV line counts (including title and header rows): 7,890 (2022), 8,379 (2023), 9,002 (2024).

**Place filter — ACS DP05.** Demographic and Housing Estimates. `DP05` total population is the field that will restrict the study to incorporated places ≥ 50,000. The same table also supplies race and ethnicity shares (see heterogeneity).

**Restricted predictor — ACS DP02 and B05002.** DP02 (Selected Social Characteristics) and B05002 (Place of Birth by Nativity and Citizenship Status) support foreign-born population share. The plan treats foreign-born share as a restricted context variable, not as one of the three hypothesis predictors.

**Mediator — poverty — ACS DP03.** Selected Economic Characteristics. Poverty rate is the first hypothesis predictor. The same table also has unemployment and median household income for optional controls.

**Mediator — heterogeneity — ACS DP05.** Race and ethnicity group shares will be locked before compute, then turned into the Blau index \(1 - \sum_g p_g^2\).

**Mediator — residential instability — ACS DP02 and DP04.** DP02 has mobility (moved in the last year). DP04 has housing tenure (renter-occupied). The form hypothesis uses percent who moved in the last year; renter share is the companion instability measure in the plan.

**Controls — ACS DP03 and Gazetteer.** Unemployment and median household income from DP03; land area (and lat/long) from the Gazetteer. Population for density comes from DP05.

**Exposure weight — ACS DP05 and CBP.** Place population from DP05 is the default LP exposure weight. CBP `est` (establishments) by county and NAICS is a fallback if a clean place/county join is possible. `cbp22co.csv` has 1,100,804 data rows; `cbp23co.csv` has 1,100,961 data rows (plus a header).

---

## BigSet supplements

### Shared method

Local BigSet (`npm install --global @adamexu/bigset`, then `bigset start`) collected only public pages (no logins, no paywalls). TinyFish provided search; OpenRouter provided the models. Three datasets were created once and then populated; they were not recreated.

Each populate run resets the live BigSet table. After every run, rows were exported and **merged on unique `source_url`** into the role CSV so earlier unique rows were not lost. Populates were run **one dataset at a time**. `_bigset_one_at_a_time.py` implemented that loop.

Create prompts and row targets followed the project plan:

| Live dataset | BigSet id | Role CSV | Target rows |
| --- | --- | --- | --- |
| Us City Ucr Supplemental Crimes | `jd72cgyf6qmj29f8mrz3p6b0s98dvx71` | `cde_gaps/bigset_cde_gaps.csv` | 200 |
| Commercial Security Hardening Costs | `jd76egy011hjzj15966cj4p9v58dtmf7` | `control_cost/bigset_security_prices.csv` | 80 |
| Commercial Crime News | `jd7ahsc4xbjd3wtrwxre0snm018dtpmx` | `feature_selection_corpus/bigset_property_crime_news.csv` | 200 |

Early runs used `qwen/qwen3.7-max` and hit OpenRouter’s new-account 20 requests/minute cap, so each populate stopped after a few rows. The working settings were a non-batch chat model for both Populate Orchestrator and Investigate Subagent: `deepseek/deepseek-v4-pro-0813`. OpenRouter `:batch` model IDs fail immediately on live populate. Free-tier Investigate models stalled. TinyFish search is also capped (30 requests/minute).

Facts on the cited pages remain owned by those sites. Rows are not a census of crime or of security prices.

Notebook 03 hand-checked a sample of BigSet rows against the cited URL (plan step 5): dead sources, named private persons, and stories that are not property crime were logged in `processed/bigset_qa_log.csv`. No CDE-gap fill was accepted. No official predictor was added from the news.

### Dataset summaries

**CDE gaps — `cde_gaps/bigset_cde_gaps.csv`.** Public police-department or state UCR pages that post annual burglary, larceny-theft, or motor-vehicle-theft counts for cities of 50,000 or more that may be missing from CDE. Columns: `source_url`, `city`, `year`, `offense`, `count`, `rate`. **228** unique-URL rows (229 lines including header). These rows do not replace Table 8. They are only candidates for filling CDE holes after the official join.

**Control cost — `control_cost/bigset_security_prices.csv`.** Published installed-cost ranges and claimed loss-reduction for commercial fortification (fence/lighting), video surveillance, intrusion alarms, and electronic access control sold to U.S. urban business sites. Columns: `source_url`, `control_family`, `unit_description`, `installed_cost_low_usd`, `installed_cost_high_usd`, `claimed_loss_reduction_pct`. **89** unique-URL rows (90 lines including header). After cleaning, this table is the source for the linear program’s \(\alpha_k\) coefficients. Freeze those coefficients before the solver runs.

**Feature-selection corpus — `feature_selection_corpus/bigset_property_crime_news.csv`.** Public news stories from recent years on burglary, breaking and entering, grand larceny, arson, vandalism, or theft of commercial equipment in large U.S. cities. Columns: `source_url`, `city_state`, `story_date`, `headline`, `offense_tags`, `asset_target`, `site_conditions`. **213** unique-URL rows (214 lines including header). News is a **selection log only**. It is not a model column and not the target. Themes may add official ACS/CBP/FBI fields or change LP emphasis if they appear in at least five sourced stories and map to an official field or control family. Offender or victim demographic themes are dropped. Vandalism may inform the LP; it is not part of the FBI property-crime index.

---

## Inventory (line counts)

Line counts include headers. ACS and Gazetteer counts are one header plus one row per place. Table 8 counts include the published title rows. BigSet counts are one header plus unique `source_url` rows.

| Path | Lines |
| --- | ---: |
| `target/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2022.csv` | 7,890 |
| `target/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2023.csv` | 8,379 |
| `target/CIUS_Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2024.csv` | 9,002 |
| `place_filter/ACSDP5Y2022.DP05.csv` | 31,895 |
| `place_filter/ACSDP5Y2023.DP05.csv` | 32,034 |
| `place_filter/ACSDP5Y2024.DP05.csv` | 32,039 |
| `restricted_predictor/ACSDP5Y{2022–2024}.DP02.csv` | 31,895 / 32,034 / 32,039 |
| `restricted_predictor/ACSDT5Y{2022–2024}.B05002.csv` | 31,895 / 32,034 / 32,039 |
| `mediator_poverty/ACSDP5Y{2022–2024}.DP03.csv` | 31,895 / 32,034 / 32,039 |
| `mediator_heterogeneity/ACSDP5Y{2022–2024}.DP05.csv` | same as `place_filter` |
| `mediator_residential_instability/ACSDP5Y{2022–2024}.DP02.csv` | same as restricted DP02 |
| `mediator_residential_instability/ACSDP5Y{2022–2024}.DP04.csv` | 31,895 / 32,034 / 32,039 |
| `controls/ACSDP5Y{2022–2024}.DP03.csv` | same as mediator poverty |
| `controls/2022_Gaz_place_national.csv` | 32,188 |
| `controls/2023_Gaz_place_national.csv` | 32,330 |
| `controls/2024_Gaz_place_national.csv` | 32,334 |
| `exposure_weight/ACSDP5Y{2022–2024}.DP05.csv` | same as `place_filter` |
| `exposure_weight/cbp22co.csv` | 1,100,805 |
| `exposure_weight/cbp23co.csv` | 1,100,962 |
| `cde_gaps/bigset_cde_gaps.csv` | 229 |
| `control_cost/bigset_security_prices.csv` | 90 |
| `feature_selection_corpus/bigset_property_crime_news.csv` | 214 |

---

## Processed (written by notebooks)

These files are not official downloads. Notebook 01 wrote the place-year tables. Notebook 03 wrote the freeze files. Notebook 04 wrote the H0 tables. Notebook 05 wrote the Ridge scores and the LP mix. Notebook 06 wrote the Task 3 briefing tables.

| Path | Written by | What it is |
| --- | --- | --- |
| `processed/place_year_joined.csv` | 01 | Post-join, pre-drop universe (2,183 rows) |
| `processed/place_year_clean.csv` | 01 | Analysis table: 2,182 place-years, 771 places, 2022–2024 |
| `processed/exclusion_log.csv` | 01 | 188 logged exclusions (unmatched Table 8, ACS pop < 50,000, pop-ratio mismatch, CDE-gap candidates, one duplicate key) |
| `processed/feature_list.md` | 03 | Frozen DV and three mediators; official adds: none |
| `processed/alpha_k.csv` | 03 | Four CPTED families; effectiveness fallback 0.20 |
| `processed/blocked_split.csv` | 03 | Place-level train/holdout by Census division (holdout = New England, Middle Atlantic) |
| `processed/bigset_qa_log.csv` | 03 | URL and theme QA notes |
| `processed/ols_coefficients.csv` | 04 | Stage 1 intercept, slopes, SE, p-values |
| `processed/vif.csv` | 04 | Stage 2 VIF (flag > 5); no predictor flagged |
| `processed/ridge_predictions.csv` | 05 | Train-fit Ridge \\(\\hat r_i\\) and risk tier on every place-year |
| `processed/control_mix.csv` | 05 | Solved dollars by tier and control family |
| `processed/lp_equal_share.csv` | 05 | Equal-share baseline dollars |
| `processed/lp_comparison.csv` | 05 | Residual loss, solved vs equal-share |
| `processed/lp_sensitivity.csv` | 05 | ±25 percent on each frozen \\(\\alpha_k\\) |
| `processed/nu_briefing.csv` | 06 | Ogden, Layton, Logan place-years with Ridge score and tier |
| `processed/lp_ppe_shares.csv` | 06 | Solved mix as shares of a PPE security slice ($1M worked example) |

The cleaned table is the H0 sample. Notebook 05 reused `blocked_split.csv` and `alpha_k.csv` and did not rewrite `place_year_clean.csv`. Notebook 06 did not refit OLS, Ridge, or the LP.

---

## Sources

- FBI Crime Data Explorer — Crime in the United States, Offenses Known to Law Enforcement, Table 8 (city): https://cde.ucr.cjis.gov/
- Census ACS 5-year Data Profiles DP02–DP05 and detailed table B05002: https://data.census.gov/
- Census Gazetteer place files: https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html
- Census County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- BigSet (local public-web agents): https://github.com/tinyfish-io/bigset-oss
