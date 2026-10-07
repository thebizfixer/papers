# Frozen feature list

Written by `scripts/03_bigset_qa_and_feature_freeze.ipynb`. This list does not change after notebook 03.

## Hypothesis predictors (locked)

- `poverty_rate` — ACS DP03, percent of all people below the poverty level
- `blau_heterogeneity` — Blau index from the DP05 groups locked in notebook 01 (Blau, 1977; Messner, 1986)
- `pct_moved_year` — ACS DP02, percent who lived in a different house one year earlier

## Dependent variable (locked)

- `property_crime_rate` — (burglary + larceny-theft + motor vehicle theft) / ACS population × 100,000
- Arson is a companion column and is not in the count (Federal Bureau of Investigation, 2019; notebook 02 coverage check).

## Official adds from the news pass

none

News themes that cleared five training-place stories mapped to fields already in the target or to LP families. No ACS vacancy column and no CBP establishment column were added. Headline counts are not features.

## Companion columns (not form predictors)

- `renter_share`, `unemployment_rate`, `median_hh_income`, `acs_population`, `density`, `foreign_born_share`

## Blocked split (locked)

- Holdout Census divisions: New England, Middle Atlantic
- File: `data/processed/blocked_split.csv`
- Feature selection used training divisions only.

## LP emphasis from kept news themes

alarm, fortification, surveillance

## Coefficients alpha_k

File: `data/processed/alpha_k.csv`. One row per control family. Notebook 05 reads this file and does not refit the medians.

## Gap fill

None. `place_year_clean.csv` was not rewritten.
