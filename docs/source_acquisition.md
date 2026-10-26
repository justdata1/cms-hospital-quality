# Source acquisition completed

Implementation step 1 completed October 26, 2026.

## Selected snapshot
Both official CMS metadata records report release date **August 13, 2026** and modification date **July 22, 2026**. This project pins the downloaded files by SHA-256; it does not claim these dates are the measurement periods or that this is the newest possible archive release.

| Dataset | CMS identifier | Data rows | Columns | Download size |
| --- | --- | ---: | ---: | ---: |
| Hospital General Information | xubh-q36u | 5,419 | 38 | 1,450,767 bytes |
| Timely and Effective Care Hospital | yv7e-xc69 | 138,084 | 16 | 34,150,899 bytes |

Both datasets link to the same Hospital Data Dictionary. The downloaded PDF is 100 pages and identifies itself as July 2026 on page 2. CMS metadata explicitly supplies that dictionary for these datasets; this is not an independently inferred release match.

## Files and verification
The snapshot is in `data/raw/20261026T233809576060Z/`. It contains untouched CSV downloads, two original metadata JSON records, the dictionary PDF, and a manifest. UTF-8 decoding and CSV parsing succeeded. SHA-256 checksums were recomputed and matched for both CSVs and the PDF. Row counts exclude headers.

See [source manifest](source_manifest.json) for exact source URLs, checksums, column lists, and acquisition time. Raw downloads stay local and are excluded from Git.

## Reproduce
From the repository root, run `python3 scripts/download_sources.py`. Python 3 and curl are required. The script retrieves the current official CMS distribution URLs and creates a new timestamped directory without overwriting prior snapshots. Compare its release metadata and checksums with the committed manifest; live CMS URLs may change and cannot guarantee the same historical snapshot. The original downloaded files are therefore preserved locally.

## Next step
Profile the downloaded records: verify identifier uniqueness, result grain, reporting periods, missing-value tokens, footnotes, and facility joins. Then select three to five measures. No database has been created or loaded yet.

## Official sources
- [Hospital General Information](https://data.cms.gov/provider-data/dataset/xubh-q36u)
- [Timely and Effective Care Hospital](https://data.cms.gov/provider-data/dataset/yv7e-xc69)
- [Hospital dictionary](https://data.cms.gov/provider-data/sites/default/files/data_dictionaries/hospital/HOSPITAL_Data_Dictionary.pdf)
