# Data Profile: CMS Hospital Snapshot

Implementation step 2 (profiling). Profiled October 27, 2026 against the snapshot in `data/raw/20261026T233809576060Z/` (CMS release dated August 13, 2026). All values were read as text first, so nothing below depends on automatic type conversion.

## Summary
- Both files are structurally clean: no duplicate keys, no unparseable dates, no conflicting facility attributes between files.
- **Result grain is facility + measure.** Each measure has exactly one reporting period in this release, so the planned grain (facility + measure + period + release) holds with no collisions.
- **Every timely-care row joins to a hospital.** 761 hospitals have no timely-care rows at all; reports must count them as "not reported", not drop them silently.
- **58% of scores are "Not Available".** Missingness reporting (BQ03, FR08) is a core result, not an edge case.
- **Zero is a real value.** 2,046 numeric scores are exactly 0 and must stay distinct from unavailable scores (AC05).
- **Footnote definitions:** they live in CMS's separate Footnote Crosswalk file. Acquired October 28, 2026 (same August 13, 2026 release) and applied in [measures.md](measures.md).

## Hospital General Information (`xubh-q36u`)
| Check | Result |
| --- | --- |
| Rows / columns | 5,419 / 38 |
| `Facility ID` | Unique; always 6 characters; 854 start with `0`; store as text |
| `ZIP Code` | Always 5 characters; 352 start with `0`; store as text |
| States and territories | 56 distinct codes (largest: TX 467, CA 377, FL 221) |
| Hospital types | 8 values (Acute Care 3,107; Critical Access 1,382; Psychiatric 624; VA 132; Childrens 94; Rural Emergency 43; DoD 32; Long-term 5) |
| Ownership | 12 values (largest: Voluntary non-profit - Private 2,322; Proprietary 1,063) |
| Overall rating | 1-5 for 3,174 hospitals; `Not Available` for 2,245 |
| Rating footnote | Blank for 3,103; codes include `16`, `19`, `5`, `29`, `22`, `23`, `11`, and one multi-code form `16, 23` |
| Birthing-friendly flag | `Y` or blank only; blank means "not designated", not unknown, so document that interpretation |

## Timely and Effective Care (`yv7e-xc69`)
| Check | Result |
| --- | --- |
| Rows | 138,084 |
| Facilities | 4,658, all present in Hospital General Information |
| Rows per facility | 30 for 4,361 facilities; 23, 24 or 29 for the remaining 297 (some eCQM rows are absent rather than marked unavailable) |
| Duplicates | 0 on facility + measure + period, 0 on facility + measure, 0 full-row |
| Measures | 30 IDs, each with one consistent name and one reporting period |
| Conditions | eCQM 68,214; Emergency Department 32,606; Sepsis 23,290; Vaccination, Colonoscopy and Cataract 4,658 each |
| Repeated facility attributes | Name, address, state and ZIP match the general file for every facility; keep them only in the hospital snapshot table (3NF) |

### Reporting periods
| Start | End | Rows | Notes |
| --- | --- | ---: | --- |
| 01/01/2024 | 12/31/2024 | 86,846 | Annual measures |
| 10/01/2024 | 09/30/2025 | 46,580 | Quarterly-refreshed measures (SEP-1, OP-18a-d, OP-23) |
| 10/01/2024 | 03/31/2025 | 4,658 | IMM-3 (six-month flu season window) |

Dates parse as `MM/DD/YYYY` with no failures, and no end date precedes its start date. Periods differ between measures, so compare results only within a measure (DQ05).

### Score and sample values
| Value | Score rows | Handling |
| --- | ---: | --- |
| Numeric | 53,920 | Parse to `numeric` |
| `Not Available` | 80,338 | NULL score plus an availability status |
| `low` / `medium` / `high` / `very high` | 3,826 | Categorical; occurs only in EDV (ED volume). Store as a category, not a number |
| Exactly `0` | 2,046 (within numeric) | Keep as zero |

`Sample` is numeric in 54,607 rows, `Not Available` in 78,819, and blank in 4,658 (all EDV rows; the categorical ED-volume measure publishes no sample).

### Footnotes
- Blank in 46,249 rows. Codes seen: `1`, `2`, `3`, `4`, `5`, `7`, `12`, `19`, `29`.
- 2,812 rows carry several codes, comma-separated (for example `1, 2, 3`), which confirms the need for the `result_footnotes` junction table.
- Code `5` accounts for 63,815 of the 80,338 unavailable scores. Code `2` appears on 10,583 rows that still have numeric scores, so a footnote does not always mean a score is unusable.
- Meanings are **not** in the data dictionary PDF; it points to `FOOTNOTE_CROSSWALK.CSV`, now in `data/raw/20261028T014421Z_footnote_crosswalk/` and the source manifest. Every code in both files has a definition.

## Measure coverage
Numeric coverage is the share of the measure's rows with a numeric score.

| Measure | Description | Unit | Rows | Numeric | Coverage | Median |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| IMM_3 | Healthcare workers given flu vaccination | % | 4,658 | 4,260 | 91.5% | 79 |
| OP_18b | ED median time to departure, excl. transfers/psych | minutes | 4,658 | 4,081 | 87.6% | 148 |
| OP_18a | ED median time to departure, all patients | minutes | 4,658 | 4,052 | 87.0% | 154 |
| SAFE_USE_OF_OPIOIDS | Concurrent opioid prescribing | % | 4,426 | 3,740 | 84.5% | 15 |
| OP_22 | Left before being seen | % | 4,658 | 3,821 | 82.0% | 1 |
| SEP_1 | Severe sepsis/septic shock bundle | % | 4,658 | 3,115 | 66.9% | 65 |
| SEV_SEP_3HR | Severe sepsis 3-hour bundle | % | 4,658 | 3,094 | 66.4% | 82 |
| OP_18c | ED median time, psych/mental health | minutes | 4,658 | 3,023 | 64.9% | 247 |
| SEV_SEP_6HR | Severe sepsis 6-hour bundle | % | 4,658 | 2,957 | 63.5% | 94 |
| OP_29 | Colonoscopy follow-up interval | % | 4,658 | 2,849 | 61.2% | 97 |
| (14 others) | Sepsis sub-bundles, VTE, stroke, hospital harm, STEMI, cataract | mixed | | | 0.3-57% | |
| GMCS (5 IDs) | Global Malnutrition Composite and components | % | 4,658 each | 0 | 0% | n/a |
| EDV | ED volume | category | 4,658 | 0 | categorical | n/a |

GMCS publishes no numeric scores in this release, and EDV is categorical, so both are excluded from performance comparisons.

## Proposed measures for step 3
These five cover four conditions, include both percentage and time units, and have the highest usable coverage.

| Measure | Unit | Favorable direction | Why |
| --- | --- | --- | --- |
| OP_18b | minutes | Lower (stated in CMS measure name) | Best ED timeliness coverage; a median-of-medians caution applies (DQ08) |
| IMM_3 | % | Higher (confirm in definition) | Highest coverage; distinct 6-month period |
| OP_22 | % | Lower (confirm in definition) | Many true zeros, which tests AC05 |
| SEP_1 | % | Higher (confirm in definition) | Clinically important; 33% unavailable, which exercises BQ03 |
| SAFE_USE_OF_OPIOIDS | % | Lower (confirm in definition) | eCQM with absent rows for 232 facilities, which exercises coverage reporting |

Before finalizing, read each measure's definition and exclusions in CMS documentation and record them in the data dictionary (step 3, DQ06).

## Implications for the schema (step 4)
- `hospitals.facility_id`, postal codes, and phone numbers: `text`, never integer.
- `hospital_results`: keep `score_text` and `sample_text` verbatim; add `score_numeric`, `sample_numeric`, `score_category` (EDV) and `availability_status`.
- Key: (`facility_id`, `measure_id`, `reporting_period_id`, `source_file_id`). No collisions in this snapshot.
- `footnotes` and `result_footnotes`: split comma-separated codes on load; retain the original string.
- Distinguish "row absent" (the 297 facilities with fewer than 30 rows and the 761 hospitals with no rows) from "row present but Not Available".

## Reproduce
Profiling used pandas 2.3.3 with every column read as text (`dtype=str, keep_default_na=False`) so that `Not Available`, blanks and leading zeros were preserved. A reusable profiling script can be added under `scripts/` when loading is implemented.
