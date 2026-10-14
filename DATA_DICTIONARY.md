# Data dictionary

This file documents the columns in `Data/promarket_bank_quarter_panel_mvp.csv`, the processed bank-quarter panel used in the analysis.

| Variable | Description | Unit / format |
|---|---|---|
| `date` | Quarter-end date | `YYYY-MM-DD` |
| `year` | Calendar year | Integer |
| `quarter` | Calendar quarter | 1–4 |
| `rssd` | Federal Reserve RSSD bank identifier | Integer |
| `cert` | FDIC certificate number | Integer |
| `name` | Institution name | Text |
| `filing_type` | Call Report filing/form indicator carried from the source workflow | Numeric/source code |
| `assets` | Total assets | USD thousands |
| `ib_deposits` | Interest-bearing domestic deposits used in the rate denominator construction | USD thousands |
| `total_deposits` | Total deposits | USD thousands |
| `dep_interest_exp_q` | Domestic deposit interest expense for the quarter after converting year-to-date income items to quarterly flows | USD thousands |
| `avg_ib_deposits` | Average interest-bearing domestic deposits used as the denominator | USD thousands |
| `deposit_rate` | Annualized effective deposit funding rate: quarterly domestic deposit interest expense / average interest-bearing domestic deposits × 400 | Percent per year |
| `sod_year` | FDIC Summary of Deposits vintage applied to the observation without look-ahead | Year |
| `hhi` | Bank-level deposit-weighted average of county deposit HHIs | 0–1 scale |
| `sod_deposits` | Branch deposits represented in the SOD footprint used for concentration weighting | USD thousands |
| `n_counties` | Number of counties represented in the bank’s SOD branch footprint | Count |

## Key construction details

### Effective deposit funding rate

Domestic deposit interest expense is based on the following Call Report income items:

- `RIAD4508` — interest on interest-bearing transaction accounts
- `RIAD0093` — interest on savings deposits / MMDAs
- `RIADHK03` — interest on time deposits of $250,000 or less
- `RIADHK04` — interest on time deposits above $250,000

`RIAD4172` (interest on deposits in foreign offices) is excluded. Year-to-date income items are differenced to obtain quarterly flows. The annualized rate equals quarterly domestic deposit interest expense divided by average interest-bearing domestic deposits, multiplied by 400.

### Deposit-market concentration

For each SOD year, branch deposits are aggregated by bank within county. County HHI is the sum of squared bank deposit shares. Each bank’s `hhi` is then the deposit-weighted average of county HHIs across its branch footprint. The latest SOD vintage available without look-ahead is applied to each quarter.

For endpoint and fixed-effects comparisons, competitive and concentrated groups are fixed using the bottom and top quartiles of 2021Q4 bank HHI.
