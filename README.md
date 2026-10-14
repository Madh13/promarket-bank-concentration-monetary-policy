# Bank Concentration and Monetary Policy Transmission

Replication and supporting materials for **“Bank Concentration Undermined the Fed’s Monetary Policy During the Last Tightening Cycle”**, by **Madhav Ritesh Parikh** (Monash University), forthcoming in **ProMarket** at the Stigler Center, University of Chicago Booth School of Business.

**Publication status:** scheduled for 30 October 2026. The live article link will be added after publication.

This repository contains the processed data, supporting calculations, figures, and code behind the article’s original analysis of how U.S. deposit-market concentration was associated with deposit-rate pass-through during the 2021–2026 monetary-policy cycle.

![Competition gap by quarter](Figures/promarket_competition_gap.png)

## Research question

The analysis asks whether banks operating in more concentrated deposit markets repriced their deposit funding costs differently from banks exposed to more competitive markets as the Federal Reserve tightened and later eased monetary policy.

The article uses a bank-quarter panel combining public U.S. regulatory and market data. The central result is that banks in more concentrated markets showed weaker deposit-rate repricing in both directions over the recent cycle.

## Data

The processed analytical panel contains **91,105 usable bank-quarter observations from 2021Q3 through 2026Q2**.

The underlying public sources are:

1. **FFIEC Call Reports** — bank financial statements and domestic deposit-interest expense  
   https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx
2. **FDIC Summary of Deposits (SOD)** — branch-level deposits used to construct county concentration and bank-level deposit-weighted HHI  
   https://banks.data.fdic.gov/bankfind-suite/SOD
3. **Federal Reserve Bank of New York EFFR** — effective federal funds rate used as the policy-rate benchmark  
   https://www.newyorkfed.org/markets/reference-rates/effr

Raw public-source downloads are not duplicated in this repository. Instead, the repository provides the processed bank-quarter panel used in the analysis together with exact result tables and reproduction code.

## Main results

- **Descriptive panel:** 91,105 usable bank-quarter observations, 2021Q3–2026Q2.
- **Cumulative tightening/hold beta (2021Q4–2024Q2):** 46.03% for the low-HHI group and 40.04% for the high-HHI group.
- **Cumulative easing beta (2024Q2–2026Q2):** 19.28% for the low-HHI group and 15.09% for the high-HHI group.
- **Balanced fixed-effects panel:** 4,123 banks observed every quarter from 2021Q4 through 2026Q2.
- **Extreme-quartile fixed-effects sample:** 2,064 banks.
- **Tightening/hold:** high-HHI banks show about 7.03 basis points less deposit-rate response per 100-basis-point EFFR movement.
- **Easing:** high-HHI banks show about 8.02 basis points less deposit-rate response per 100-basis-point EFFR movement.

These estimates are interpreted as associations rather than proof that concentration alone causes differences in monetary-policy transmission.

## Repository contents

```text
.
├── README.md
├── DATA_DICTIONARY.md
├── REPRODUCIBILITY.md
├── CITATION.cff
├── ProMarket_Supporting_Methodology_and_Results.pdf
├── ProMarket_Supporting_Calculations.xlsx
├── Data/
│   ├── promarket_bank_quarter_panel_mvp.csv
│   ├── promarket_quarter_summary.csv
│   ├── promarket_analysis_summary.csv
│   ├── endpoint_betas.csv
│   ├── regression_results.csv
│   └── sensitivity_checks.csv
├── Code/
│   ├── reproduce_support_results.py
│   └── requirements.txt
├── Figures/
│   ├── promarket_competition_gap.png
│   ├── promarket_full_cycle.png
│   ├── promarket_episode_betas.png
│   └── promarket_fixed_effects_robustness.png
└── Reproduced/
    ├── endpoint_betas_reproduced.csv
    └── regression_results_reproduced.csv
```

## Reproducing the core results

From the repository root:

```bash
python -m pip install -r Code/requirements.txt
python Code/reproduce_support_results.py
```

The script reads the processed panel in `Data/` and writes freshly reproduced endpoint-beta and fixed-effects outputs to `Reproduced/`.

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) for the exact scope of the supplied code and [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for the processed-panel variables.

## Measurement notes

The effective deposit funding rate is an annualized realized funding-cost measure based on domestic deposit interest expense and interest-bearing domestic deposit balances. It is **not** an advertised savings-account APY.

Deposit-market concentration is measured using county-level deposit HHI from FDIC Summary of Deposits data. Each bank’s concentration exposure is the deposit-weighted average of county HHIs across its branch footprint. HHI is stored on a 0–1 scale; 0.10 corresponds to 1,000 conventional HHI points.

For detailed sample construction, variable definitions, validation checks, fixed-effects specifications, and sensitivity analysis, see `ProMarket_Supporting_Methodology_and_Results.pdf`.

## Research status and disclosure

This analysis was developed independently for the ProMarket article using public data. There was no outside funding related to the article, and the author reports no conflicts of interest related to the analysis.
