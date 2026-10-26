# CMS Hospital Quality Database

A PostgreSQL relational database project using public CMS hospital information and quality measures.

## Status
Requirements and project structure are established. Data acquisition, database implementation, and analysis have not started.

## Scope
One documented CMS release, Hospital General Information, and three to five measures from Timely and Effective Care Hospital. Compare reported measures by state, ownership, and hospital type with explicit treatment of missing values, footnotes, and reporting periods.

## Requirements
See [project requirements](docs/requirements.md) for scope, proposed entities, implementation steps, and acceptance criteria. A formatted Word copy is maintained in the project's OneDrive folder.

## Milestones
1. Acquire and profile the source data.
2. Design the relational model and field mappings.
3. Implement PostgreSQL schemas and constraints.
4. Build repeatable ingestion and reconciliation.
5. Write SQL reports and document results.
6. Validate and demonstrate a clean rebuild.

## Layout
- docs/: requirements and future design documentation.
- sql/: future database scripts.
- scripts/: future acquisition and loading helpers.
- data/raw/ and data/processed/: local files excluded from Git.
- outputs/: future report exports.

## Source
[CMS Provider Data Catalog](https://data.cms.gov/provider-data/datasets?theme%5B0%5D=Hospitals). Preserve source attribution and release metadata. Results will be descriptive, with measure definitions and coverage limitations documented.

## Next step
Identify a specific CMS release, acquire both datasets and a matching dictionary, and profile identifiers, periods, missingness, and available measures before writing DDL.
