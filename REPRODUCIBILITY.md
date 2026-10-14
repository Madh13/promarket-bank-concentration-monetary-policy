# Reproducibility scope

This repository is designed to make the empirical results reported in the ProMarket article easy to inspect and reproduce from the processed analytical panel.

## What the supplied code reproduces

Running:

```bash
python -m pip install -r Code/requirements.txt
python Code/reproduce_support_results.py
```

reconstructs from `Data/promarket_bank_quarter_panel_mvp.csv` and `Data/promarket_quarter_summary.csv`:

1. the common-endpoint cumulative deposit betas for the competitive and concentrated groups;
2. the main extreme-quartile bank fixed-effects regressions for tightening/hold and easing; and
3. the continuous-HHI fixed-effects regressions for both episodes.

Fresh outputs are written to `Reproduced/`.

## What is provided as stored verification output

The repository also includes:

- the complete quarterly descriptive series;
- sensitivity-check results;
- the article figures;
- a supporting calculations workbook; and
- a detailed methodology and results note.

These files document the broader analysis and robustness checks used during the article workflow.

## What is not included

The repository does **not** contain an end-to-end script that downloads and cleans every raw FFIEC, FDIC, and New York Fed source file into the processed panel. The raw source downloads are public and can be obtained from the official providers:

- FFIEC Call Reports: https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx
- FDIC Summary of Deposits: https://banks.data.fdic.gov/bankfind-suite/SOD
- New York Fed EFFR: https://www.newyorkfed.org/markets/reference-rates/effr

The public repository begins from the processed bank-quarter panel used in the article. This scope is intentional: it keeps the repository compact while allowing readers to inspect the analytical data and reproduce the principal reported estimates.

## Final verification

Before the repository was prepared for public release, the supplied reproduction script was rerun against the included processed panel. The reproduced cumulative betas and fixed-effects coefficients matched the stored core results.
