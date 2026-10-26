# CMS Hospital Quality Database Requirements

Version 1.0 | October 26, 2026

## Purpose and scope
Build a reproducible PostgreSQL relational database using public CMS hospital data. The project will demonstrate relational design, CSV ingestion, data quality validation, and SQL reporting. Its central question is how reported hospital measures vary by location, ownership, and hospital type.

The first release will use one documented CMS release, national hospital coverage, Hospital General Information, and three to five measures from Timely and Effective Care Hospital. Select exact measures after profiling the downloaded files and reading their definitions. Patient records, clinical recommendations, predictive modeling, a web application, and scheduled refreshes are outside the initial scope.

## Business questions
- BQ01: How many hospitals are represented by state, ownership, and hospital type?
- BQ02: How do selected results vary across those groups within the same measure and reporting period?
- BQ03: Which results are missing, suppressed, or otherwise unavailable, and what explanations does CMS provide?
- BQ04: Which hospitals differ most from a defined peer group, and how many comparable hospitals are available?
- BQ05: How complete and internally consistent are the source datasets?

Results will describe reported data. Group differences do not establish causes, and a single release will not support claims about trends.

## Data sources and provenance
- DS01: Obtain Hospital General Information and Timely and Effective Care Hospital from the CMS Provider Data Catalog, with the matching dictionary and relevant footnote definitions. Use files from the same release where possible and document mismatches.
- DS02: Record dataset title, identifier, source page, resolved download URL, release date when available, download timestamp in UTC, original filename, SHA-256 checksum, row count, encoding, and dictionary version in a source manifest.
- DS03: Distinguish source release dates, download dates, and measurement periods. Do not substitute one for another.
- DS04: Preserve downloaded CSV files unchanged in data/raw. Keep raw downloads and database dumps out of Git by default; document retrieval steps and filters.
- DS05: Profile headers, identifiers, dates, score values, missing-value tokens, duplicates, and footnote formats before finalizing the schema.

## Functional requirements
- FR01: Import raw values into staging tables as text, retaining source file and row references.
- FR02: Transform staging rows into normalized tables through explicit mappings. Load parent records before dependent records and use transactions.
- FR03: Filter reports by facility, state, hospital type, ownership, measure, reporting period, and release.
- FR04: Provide executable SQL for all five business questions. State each report's grain, filters, units, reporting period, and denominator.
- FR05: Export report results to CSV and keep SQL as the authoritative report definition.
- FR06: Re-running the same source load must not duplicate core records. Detect changed source files by checksum and stop or record a distinct source version.
- FR07: Log rejected records and actionable reasons. Reconcile source rows to accepted, excluded, and rejected dispositions without double counting.
- FR08: Produce coverage and missingness reports alongside performance comparisons.

## Proposed relational model
Confirm keys and cardinalities through profiling. The following entities establish the design direction rather than final DDL.

- source_releases: Source publication labels and metadata.
- source_files: Dataset identity, release, retrieval details, checksum, and original filename.
- load_batches: Source file, load timing, status, and row counts.
- hospitals: Stable CMS facility identifiers stored as text to preserve leading zeros.
- hospital_snapshots: Facility name, address, state, type, and ownership as reported in a release, with provenance. Preserve historical attributes when future releases are added.
- measures: Source measure identifier, description, category, unit, and documented direction of interpretation.
- reporting_periods: Measurement start and end dates, separate from publication dates.
- hospital_results: Hospital, measure, period, source version, original score text, parsed numeric score when valid, original sample text, parsed sample when valid, availability status, and source row reference.
- footnotes: Dataset and release scoped codes and definitions.
- result_footnotes: Junction table linking results to zero or more footnotes.
- load_rejections: Source row, failed rule, and diagnostic details.

The candidate result grain is facility plus measure plus reporting period plus source release. If additional dimensions explain duplicates, revise the grain and key rather than discarding rows arbitrarily. Retain original footnote strings even when parsing succeeds.

## Data integrity and reporting rules
- DQ01: Enforce primary keys, foreign keys, validated uniqueness constraints, and required fields. Quarantine unmatched references and report them.
- DQ02: Keep facility identifiers and postal codes as text. Preserve original score and sample strings.
- DQ03: Convert valid numeric scores to numeric types. Store unavailable scores as NULL with a separate status or reason. Never replace missing data with zero.
- DQ04: Parse dates explicitly. When both period dates exist, end must be on or after start. Flag missing dates without inventing them.
- DQ05: Compare only matching measures, units, periods, and compatible facility populations. Apply footnotes and suppression rules to determine eligibility.
- DQ06: Do not combine unrelated measures into an invented overall score. Confirm whether higher or lower is favorable from each measure definition.
- DQ07: Label group summaries as summaries across hospitals. A mean of hospital percentages is not a patient-level rate; use weighting only with valid compatible denominators and a documented method.
- DQ08: A median of hospital medians is not an overall patient median. Label time summaries precisely.
- DQ09: Show included and excluded hospital counts and reasons. Document coverage limitations and avoid causal interpretations.

## Technical requirements
- NFR01: Use PostgreSQL and version-controlled SQL. Record the exact tested database version and any Python dependencies during implementation.
- NFR02: Separate staging and core schemas. Keep credentials in local environment variables or an ignored .env file. Provide placeholders in .env.example if configuration is needed.
- NFR03: Document commands for acquisition, schema creation, loading, transformation, validation, and reporting in execution order.
- NFR04: Index validated join keys and common report filters. Capture EXPLAIN ANALYZE for one representative query with dataset size and environment. Set performance targets after measuring a baseline.
- NFR05: Use one active Git checkout and avoid simultaneous edits from multiple OneDrive devices. Store PostgreSQL server data outside OneDrive.
- NFR06: Preserve original data and make every cleaning decision traceable. A second person must be able to rebuild from an empty development database.

## Implementation steps
1. Identify a CMS release and its dictionary; download the two source datasets.
2. Create a source manifest and profile identifiers, values, periods, coverage, and duplicates.
3. Select three to five measures and document definitions, units, interpretation, and exclusions.
4. Draw the ER diagram and write the data dictionary, field mappings, and result grain.
5. Implement staging and core schemas, keys, constraints, and indexes.
6. Build repeatable loading and transformation, with rejection logs and row reconciliation.
7. Implement the five SQL reports and export representative results.
8. Validate source-to-database mappings, calculations, idempotency, and constraint failures.
9. Rebuild from an empty database using only the documented instructions.
10. Finish the README, findings, limitations, and a short portfolio walkthrough.

## Acceptance criteria
- AC01: Both datasets, their release metadata, and definitions are captured in a complete source manifest.
- AC02: ER diagram, data dictionary, schema, and actual database agree on keys, relationships, types, and nullability.
- AC03: Every input row has an accounted-for disposition with no unexplained row loss.
- AC04: Core records have no orphan references or duplicate validated keys. Loading identical files again leaves core counts unchanged.
- AC05: Leading-zero identifiers survive import; numeric zero remains distinct from unavailable or suppressed scores.
- AC06: All five business questions have executable SQL and documented outputs. Independently verify at least ten source records and one small aggregate.
- AC07: Isolated validation fixtures detect invalid dates, duplicate keys, unknown references, unavailable-score tokens, and multiple footnotes.
- AC08: A clean rebuild succeeds without committed credentials or reliance on an existing database.

## Deliverables and folder structure
- README.md: purpose, current status, setup, script order, and limitations.
- docs/: Word and Markdown requirements, future ER diagram, data dictionary, source manifest, mappings, and findings.
- sql/: future numbered schema, transformation, validation, and report scripts.
- scripts/: future acquisition and loading helpers.
- data/raw/ and data/processed/: local source and transformed files excluded from Git.
- outputs/: selected reproducible report exports.

Requirements and the starter repository establish scope. Data downloads, database implementation, and analysis are subsequent milestones and must not be represented as completed features.

## Source references
CMS hospital datasets: https://data.cms.gov/provider-data/datasets?theme%5B0%5D=Hospitals

Timely and Effective Care Hospital: https://data.cms.gov/provider-data/dataset/yv7e-xc69

CMS Hospital Data Dictionary reference reviewed during planning: https://data.cms.gov/provider-data/sites/default/files/data_dictionaries/hospital/HOSPITAL_Data_Dictionary.pdf

Use a dictionary matching the release actually downloaded. The July 2026 reference inspected during planning does not establish which release is latest.
