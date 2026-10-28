# Selected Measures

Implementation step 3. Selected October 27, 2026 from the profile in [data_profile.md](data_profile.md). Counts come from the August 13, 2026 CMS release in `data/raw/20261026T233809576060Z/`; footnote text comes from the matching Footnote Crosswalk in `data/raw/20261028T014421Z_footnote_crosswalk/`.

## Summary
| Measure ID | Short name | Unit | Better when | Period | Numeric results |
| --- | --- | --- | --- | --- | ---: |
| OP_18b | ED time to departure, discharged patients | minutes (hospital median) | Lower | 10/01/2024-09/30/2025 | 4,081 |
| IMM_3 | Healthcare personnel flu vaccination | % of personnel | Higher | 10/01/2024-03/31/2025 | 4,260 |
| OP_22 | Left without being seen | % of ED patients | Lower | 01/01/2024-12/31/2024 | 3,821 |
| SEP_1 | Severe sepsis / septic shock bundle | % of eligible patients | Higher | 10/01/2024-09/30/2025 | 3,115 |
| SAFE_USE_OF_OPIOIDS | Concurrent opioid prescribing at discharge | % of hospitalizations | Lower | 01/01/2024-12/31/2024 | 3,740 |

The periods differ, so results are compared only within a measure, never across measures (DQ05). No composite score is created (DQ06).

## Definitions

### OP_18b: Median time from ED arrival to ED departure, discharged patients
- **What it measures:** each hospital's median minutes from emergency department arrival to departure for patients sent home from the ED.
- **Population:** the "reporting measure" stratum of OP-18. It excludes psychiatric/mental health patients (reported separately as OP_18c) and transfers to another facility (OP_18d); patients who died in the ED are excluded from all OP-18 strata.
- **Direction:** lower is better. The measure specification notes improvement as a decrease in the median, and CMS's own measure name in this dataset says "A lower number of minutes is better."
- **Unit caution (DQ08):** each value is already a hospital median. A median of these values across hospitals is a "median hospital", not the median ED stay of all patients.
- **Sample column:** number of ED encounters behind the hospital's median.

### IMM_3: Influenza vaccination coverage among healthcare personnel
- **What it measures:** percentage of healthcare personnel working at the facility during the flu season who received an influenza vaccination, reported to CDC's National Healthcare Safety Network.
- **Population:** personnel working in the facility between October 1 and March 31. Personnel with unknown vaccination status stay in the denominator, so incomplete tracking lowers the rate.
- **Direction:** higher is better.
- **Period quirk:** the data dictionary lists IMM-3 under both the 12-month and 6-month collection windows; the data itself uses the 6-month flu-season window (10/01/2024-03/31/2025).
- **Sample column:** number of personnel, not patients.

### OP_22: Left without being seen
- **What it measures:** percentage of patients who arrived at the ED and left before evaluation by a physician, advanced practice nurse, or physician assistant.
- **Population:** all patients who presented to the ED, reported annually by the hospital through a web-based tool.
- **Direction:** lower is better.
- **Zero caution (AC05):** 883 hospitals report exactly 0%. These are real values and must never be merged with "Not Available" (837 rows).
- **Sample column:** total ED patients in the year.

### SEP_1: Severe sepsis and septic shock management bundle
- **What it measures:** percentage of eligible adult sepsis patients who received every applicable element of the bundle (lactate measurement, blood cultures, broad-spectrum antibiotics within 3 hours; additional fluid, vasopressor and reassessment steps for septic shock).
- **Population:** inpatients aged 18 or over with a sepsis, severe sepsis or septic shock diagnosis, after exclusions such as comfort-care directives and transfers.
- **Direction:** higher is better.
- **Scoring caution:** all-or-none. Missing one element fails the whole case, so SEP_1 is much lower than its component bundles (SEV_SEP_3HR, SEV_SEP_6HR, SEP_SH_3HR, SEP_SH_6HR), which are not selected.
- **Sampling:** 2,303 of the 3,115 numeric results carry footnote 2 (based on a sample of cases). They are valid, but rates rest on fewer cases than total volume.

### SAFE_USE_OF_OPIOIDS: Safe use of opioids, concurrent prescribing (eCQM CMS506)
- **What it measures:** percentage of inpatient hospitalizations for patients 18 and over discharged on two or more opioids, or an opioid plus a benzodiazepine, concurrently.
- **Direction:** lower is better (an inverse measure). The specification notes that clinical judgement can justify concurrent prescribing, so the rate is not expected to reach zero.
- **Coverage caution:** only 4,426 of 4,658 timely-care facilities have a row at all. The other 232 are "row absent", which is different from "Not Available" and must be reported separately.

## Footnotes on the selected measures
Definitions are CMS's crosswalk text. Every code in both source files appears in the crosswalk.

| Code | CMS meaning | Where it appears in the selection |
| --- | --- | --- |
| 1 | Too few cases/patients to report | Unavailable SEP_1, SAFE_USE_OF_OPIOIDS, OP_22, OP_18b |
| 2 | Data based on a sample of cases/patients | 2,303 numeric SEP_1 results; 29 numeric OP_22 |
| 3 | Results based on a shorter period than required | 159 numeric OP_18b; 35 numeric SEP_1 |
| 5 | Results not available for this reporting period | Most unavailable rows in every measure |
| 7 | No cases met the criteria | Unavailable SEP_1, OP_18b, OP_22 (combined with other codes) |
| 12 | Measure does not apply to this hospital for this period | 1 row each in OP_18b and OP_22 |
| 19 | Shown only for hospitals in the IQR and OQR programs | 172 unavailable rows in each of OP_18b, IMM_3, OP_22, SEP_1 |
| 29 | Calculated with partial-period data under a CMS-approved exception | 69 numeric IMM_3; 36 numeric SAFE_USE_OF_OPIOIDS |

## Eligibility rules for comparisons
These rules turn the footnotes into explicit, reproducible decisions. They are first proposals to confirm when the reports are built in step 7.

| Situation | Status | Used in performance comparisons? |
| --- | --- | --- |
| Numeric score, no footnote | `reported` | Yes |
| Numeric score with footnote 2 (sampled) | `reported_sampled` | Yes; count disclosed |
| Numeric score with footnote 3 or 29 (shorter or partial period) | `reported_partial_period` | Excluded by default, shown in a sensitivity check |
| `Not Available` with any footnote | `not_available` plus the footnote codes | No; counted in BQ03 missingness |
| Facility has no row for the measure | `not_reported` (derived, not stored as a result row) | No; counted in coverage |

## Peer groups
Numeric results exist only for three hospital types:

| Hospital type | OP_18b | IMM_3 | OP_22 | SEP_1 | SAFE_USE_OF_OPIOIDS |
| --- | ---: | ---: | ---: | ---: | ---: |
| Acute Care Hospitals | 2,797 | 3,013 | 2,721 | 2,750 | 2,854 |
| Critical Access Hospitals | 1,253 | 1,247 | 1,071 | 343 | 886 |
| Acute Care - Department of Defense | 31 | 0 | 29 | 22 | 0 |

Psychiatric, children's, VA, rural emergency and long-term hospitals have no numeric results for these measures. BQ04 peer groups should therefore start with Acute Care versus Critical Access, report DoD separately because the counts are small, and show how many comparable hospitals each group contains.

## Sources
- CMS Hospital Data Dictionary, July 2026 (collection periods and refresh cycles).
- CMS Footnote Crosswalk, release August 13, 2026 (`y9us-9xdf`).
- eCQI Resource Center, CMS506 Safe Use of Opioids - Concurrent Prescribing.
- eCQI Resource Center, CMS32 Median Time from ED Arrival to ED Departure for Discharged ED Patients, and the OP-18 ED-Throughput measure information form.
- Hospital OQR web-based measure guidance for OP-22.
- NQF #0500 Severe Sepsis and Septic Shock: Management Bundle.
- CDC NHSN Healthcare Personnel Influenza Vaccination protocol.

Measure specifications change by year. Before publishing findings, check each definition against the specification version that covers the reporting periods above.
