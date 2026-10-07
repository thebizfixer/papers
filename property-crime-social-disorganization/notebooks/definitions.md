# Definitions Companion

A plain-language reference for every technical term that appears in the notebook narration. Organized by topic so a non-technical reader can look up a word during or after the Task 3 presentation.

---

## Data Sources

| Term | Definition |
| --- | --- |
| **FBI Table 8** | A published table from the Federal Bureau of Investigation listing crimes reported to police in each U.S. city for a 12-month period. The project uses the 2022, 2023, and 2024 editions. |
| **Uniform Crime Reporting (UCR)** | The FBI program that collects crime statistics from local law-enforcement agencies across the country. Table 8 is one of its products. |
| **Crime Data Explorer (CDE)** | The FBI's public website for browsing and downloading crime data. Used here only to flag cities missing from Table 8. |
| **American Community Survey (ACS)** | A large, ongoing Census Bureau survey that measures social, economic, and housing characteristics of U.S. communities every year. All poverty, mobility, and population figures in this project come from the ACS 5-year estimates. |
| **5-year estimate** | An ACS product that pools survey responses over five years to produce reliable numbers for small places. It is not a single-year snapshot. |
| **Data Profile (DP03, DP05, etc.)** | Pre-built summary tables the Census Bureau publishes from the ACS. Each profile covers a topic: DP03 is economic, DP05 is demographic, DP02 is social, DP04 is housing. |
| **Gazetteer** | A Census Bureau reference file that lists every named place in the U.S. with its land area and map coordinates. The project uses it for population density. |
| **Census division** | One of nine geographic regions (e.g., New England, Mountain, Pacific) the Census Bureau uses to group states. The project holds out two of these divisions for testing. |
| **Census-designated place (CDP)** | A community that the Census Bureau names for statistical purposes but that is not a legally incorporated city or town. |
| **County Business Patterns (CBP)** | A Census Bureau dataset counting business establishments by county. Mentioned in the notebooks but not used in the final analysis. |
| **BigSet** | The project's term for three supplemental CSV files compiled from public web sources: gap-fill crime counts, security-equipment prices, and property-crime news stories. |

---

## Crime and Criminology

| Term | Definition |
| --- | --- |
| **Property crime** | Crimes against possessions rather than persons. In this project the count is burglary + larceny-theft + motor vehicle theft. |
| **Burglary** | Unlawful entry of a building to commit a crime, typically theft. |
| **Larceny-theft** | Taking someone else's property without force or unlawful entry (e.g., shoplifting, pocket-picking, theft from a vehicle). |
| **Motor vehicle theft** | Theft or attempted theft of a car, truck, or other motor vehicle. |
| **Arson** | Deliberately setting fire to property. The FBI classifies it as property crime but excludes it from volume totals because reporting is incomplete. This project follows that rule. |
| **Property-crime rate** | The number of property crimes per 100,000 residents. Dividing by population lets cities of different sizes be compared on the same scale. |
| **Social disorganization** | A criminology theory that community-level conditions — poverty, ethnic diversity, and residential turnover — weaken neighborhood ties and raise the opportunity for crime. |
| **CPTED** | Crime Prevention Through Environmental Design. A framework that reduces crime by changing the physical environment: better fencing, lighting, cameras, and access control. |

---

## Variables and Measures

| Term | Definition |
| --- | --- |
| **Place-year** | One row in the analysis table: a single city observed in a single year. The table has 2,182 place-years across 771 cities over three years. |
| **Dependent variable (DV)** | The outcome the study is trying to explain — here, the property-crime rate. |
| **Predictor (independent variable)** | A measure used to explain or forecast the dependent variable. |
| **Mediator** | A predictor that theory says carries the effect of broader social conditions to the outcome. The three mediators are poverty rate, ethnic heterogeneity, and residential instability. |
| **Control variable** | A measure included for context (unemployment, income, density, population) but not part of the hypothesis test. |
| **Poverty rate** | The ACS percentage of residents living below the federal poverty line. |
| **Blau heterogeneity (Blau index)** | A number between 0 and 1 that measures how evenly a city's population is split across racial and ethnic groups. Zero means everyone belongs to one group; higher values mean more even diversity. Computed as \(H = 1 - \sum p_g^2\), where each \(p_g\) is a group's share of the population. |
| **Residential instability** | The ACS percentage of residents who lived in a different house one year earlier. Higher values mean more people moving in or out. |
| **Renter share** | The ACS percentage of housing units that are renter-occupied. A companion measure, not one of the three locked predictors. |
| **Population density** | Residents per square mile of land. Computed from ACS population divided by Gazetteer land area. |
| **Foreign-born share** | The percentage of residents born outside the United States. Stored for context; not entered as a predictor. |

---

## Statistics and Hypothesis Testing

| Term | Definition |
| --- | --- |
| **Null hypothesis (H0)** | The starting assumption that poverty, heterogeneity, and instability have no statistically significant effect on the property-crime rate. The analysis either rejects or fails to reject this statement. |
| **Alternate hypothesis** | The opposite claim: at least one of the three conditions does significantly affect the rate. |
| **Significance level (α = 0.05)** | The threshold for "unlikely enough to reject H0." A 5 % level means we accept up to a 5 % chance of wrongly rejecting a true null. |
| **p-value** | The probability of seeing results at least as extreme as the observed ones if the null hypothesis were true. A p-value below 0.05 leads to rejection of H0. |
| **F-test / F-statistic** | A single number that tests whether the set of predictors, taken together, explains a significant share of the variation in the outcome. A larger F-statistic, with a small p-value, means the predictors collectively matter. |
| **Coefficient (slope)** | The estimated change in the crime rate when one predictor rises by one unit, holding the other predictors constant. For example, a poverty coefficient of 60 means each additional percentage point of poverty is associated with about 60 more crimes per 100,000. |
| **Intercept** | The predicted crime rate when all three predictors equal zero. It anchors the equation but has no practical interpretation on its own. |
| **Standard error** | A measure of how precisely each coefficient is estimated. Smaller is better. |
| **R² (R-squared)** | The fraction of the variation in the crime rate that the three predictors account for. An R² of 0.17 means 17 %. It describes explanatory share, not prediction accuracy or practical importance. |
| **Pearson correlation** | A number between −1 and +1 that measures how tightly two variables move together in a straight line. Values near 0 mean little linear relationship. |

---

## Regression and Modeling

| Term | Definition |
| --- | --- |
| **Ordinary Least Squares (OLS)** | The standard method for fitting a straight-line equation to data. It finds the line that makes the squared prediction errors as small as possible. This is the method that tests the hypothesis. |
| **Multiple linear regression** | OLS with more than one predictor. The project fits one crime-rate equation using three predictors simultaneously. |
| **Residual** | The difference between a city's actual crime rate and the rate the equation predicts. A scatter plot of residuals shows whether the model's assumptions hold. |
| **Residual scatter (residual vs. fitted plot)** | A chart with predicted rates on the horizontal axis and residuals on the vertical axis. A random cloud is good; a funnel or curve signals a limitation. |
| **Variance Inflation Factor (VIF)** | A number that checks whether two predictors are so similar that the model cannot tell their effects apart. VIF below 5 is acceptable. All three predictors in this project are below 1.2. |
| **Collinearity (multicollinearity)** | When two or more predictors are highly correlated, making their individual coefficients unstable. VIF is the diagnostic. |
| **Durbin–Watson statistic** | A check for whether residuals are correlated with their neighbors. A value near 2 is ideal. The project's value of 0.64 reflects the fact that the same city appears in three consecutive years. |
| **Ridge regression** | A variant of OLS that adds a small penalty to keep coefficients from growing too large. Used here to produce risk scores, not to test the hypothesis. |
| **Lambda (λ)** | The size of the Ridge penalty. A larger λ shrinks coefficients more. The project chose λ = 26.37 automatically via cross-validation. |
| **Standardization** | Rescaling each predictor so it has a mean of 0 and a standard deviation of 1. Required before Ridge so that the penalty treats all predictors equally. |
| **RMSE (Root Mean Square Error)** | A measure of prediction error in the same units as the outcome (crimes per 100,000). Lower is better. |
| **MAE (Mean Absolute Error)** | Average size of the prediction errors, ignoring direction. Also in crimes per 100,000. |
| **Risk tier** | A label (high / mid / low) assigned to each place-year based on its Ridge-predicted rate. High is the top 10 %, mid is the next 15 %, low is the remaining 75 %. |

---

## Data Splitting and Evaluation

| Term | Definition |
| --- | --- |
| **Blocked split** | Dividing the data into a training set and a holdout set by geography (Census divisions) rather than by random draw. Prevents the model from memorizing nearby cities during training. |
| **Training set** | The seven Census divisions whose cities are used to fit the Ridge model and count news themes. |
| **Holdout set** | New England and Middle Atlantic cities set aside to check whether Ridge predicts well on regions it has never seen. |
| **Mean-rate baseline** | The simplest possible forecast: predict every holdout city's rate as the training set's average rate. If Ridge cannot beat this, its predictions add no value on that holdout. |
| **Cross-validation (RidgeCV)** | An automated process that tries many values of λ on subsets of the training data and picks the one that predicts best on the left-out subset. |

---

## Linear Program (Security Budget)

| Term | Definition |
| --- | --- |
| **Linear program (LP)** | A mathematical method that finds the best way to divide a fixed budget among several options, subject to rules (constraints). Here it divides a security budget across four control families and three risk tiers. |
| **Decision variable** | What the solver is choosing — in this case, the dollar amount assigned to each combination of control family and risk tier. There are 12 variables (4 families × 3 tiers). |
| **Objective function** | The quantity the solver tries to minimize: expected residual crime exposure after spending. |
| **Constraint** | A rule the solution must follow. Examples: the total cannot exceed the budget; no single family can take more than half; alarm must stay between 15 % and 25 %. |
| **Exposure** | The expected number of property crimes in a risk tier, computed from the Ridge-predicted rate and the city's population. It is what the budget is trying to reduce. |
| **Residual loss** | The crime exposure that remains after security spending. The solver cannot drive it below 50 % of exposure (a realism floor). |
| **α_k (effectiveness per dollar)** | A coefficient that converts one dollar of control family k into an expected share of crime avoided. Frozen in notebook 03 from the security-price book. |
| **Planning budget (B)** | A fixed $10 million pot used for comparison. It is not an estimate of what any single owner should spend. |
| **Equal-share baseline** | The comparison scenario: spread the budget evenly across all 12 cells ($833,333 each). The solved mix beats this baseline by about 8,147 expected-count units. |
| **Sensitivity analysis** | Rerunning the solver after raising or lowering each α_k by 25 %, one at a time, to see whether the recommended mix changes. |

---

## Security Control Families

| Term | Definition |
| --- | --- |
| **Fortification (delay)** | Physical barriers — fences, walls, bollards, reinforced doors, lighting — that slow or discourage an intruder. The solved mix assigns 50 % of the security slice to this family. |
| **Surveillance (watch)** | Cameras (CCTV) and monitoring systems that observe activity and deter offenders. The solved mix assigns 35 %. |
| **Alarm (notify)** | Intrusion-detection systems that alert a response team after a breach is detected. The solved mix assigns 15 %. |
| **Authorization (access control)** | Electronic badge readers, key cards, and locks that restrict who may enter. The solved mix assigns 0 % because the scored property crimes (burglary, larceny, vehicle theft) are external-entry and lot problems, not credentialed-access problems. |
| **PPE (plant, property, and equipment)** | The line on a company's books that carries the value of physical assets. The security slice is the portion of PPE investment earmarked for protecting those assets. |
| **Security slice** | The share of a company's fixed-asset spending dedicated to security controls. The 50 / 35 / 15 mix applies to whatever dollar amount the owner sets for that line. |

---

## Data Cleaning

| Term | Definition |
| --- | --- |
| **ETL (extract, transform, load)** | The sequence of pulling raw files, reshaping them, and writing a clean table. Notebooks 01 and 03 do this work. |
| **Join** | Combining two tables by matching rows on a shared key (e.g., city name and year). |
| **Match key** | A cleaned, standardized version of the city name used to link FBI and Census records that label the same city differently. |
| **Exclusion log** | A record of every city-year dropped from the study and the reason (missing data, population mismatch, duplicate key, etc.). |
| **Imputation** | Filling in missing values with an estimate. This project does not impute the crime rate or the three predictors. |
| **Feature freeze** | The point (notebook 03) after which no new predictor columns are added or removed. Prevents the analyst from shopping for variables that happen to look good after seeing results. |
| **IQR (interquartile range)** | The span between the 25th and 75th percentiles. Values more than 1.5 × IQR above the 75th percentile are flagged as potential outliers. Flagged cities are kept in this study. |
| **Outlier** | A data point far from the bulk of the distribution. High-crime cities are not removed just for being high; they are part of what the study examines. |
| **Right-skewed** | A distribution where most values cluster on the left and a long tail stretches to the right. The property-crime rate has this shape: many cities near 2,000 per 100,000, a few near 10,000. |
| **Winsorize** | Capping extreme values at a percentile cutoff. Not done here. |

---

## Geography

| Term | Definition |
| --- | --- |
| **Northern Utah** | The briefing case geography: Ogden, Layton, and Logan. Used to illustrate findings for a local owner, not as a separate statistical sample. |
| **Ogden** | A city in Weber County, Utah (population ~94,000). It sits inside the national cloud on every scatter — a typical study city, not an outlier. Its crime rate fell from about 2,541 to 1,922 per 100,000 over the study period. |
| **Layton** | A city in Davis County, Utah. Lower crime rate and lower poverty than Ogden. Also in the low Ridge tier. |
| **Logan** | A city in Cache County, Utah. A university town with high poverty (~22–24 %) and high mobility (~30 %). Ridge scores it high, but the recorded crime rate stayed moderate (~1,150–1,460). |
| **Incorporated city** | A municipality that has a legal charter and government. Distinguished from a CDP, which is a Census statistical boundary only. |

---

## Notebook Stages

| Stage | What it answers |
| --- | --- |
| **Stage 1 (notebook 04)** | Is the null rejected? OLS says yes — H0 is rejected at α = 0.05. |
| **Stage 2 (notebook 04)** | Are the three predictors too similar to one another? VIF says no; they are independent enough. |
| **Stage 3 (notebook 05)** | After rejecting H0, how should a security budget be split? Ridge scores feed the linear program. This stage does not change the H0 decision. |
