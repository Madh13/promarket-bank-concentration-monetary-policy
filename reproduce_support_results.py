from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'Data'
OUT = ROOT / 'Reproduced'
OUT.mkdir(exist_ok=True)

panel = pd.read_csv(DATA / 'promarket_bank_quarter_panel_mvp.csv', parse_dates=['date'])
qsum = pd.read_csv(DATA / 'promarket_quarter_summary.csv', parse_dates=['date'])
effr_map = qsum.set_index('date')['effr']

# Balanced bank sample: present in every quarter from 2021Q4 through 2026Q2.
window = panel[(panel.date >= '2021-12-31') & (panel.date <= '2026-06-30')].copy()
all_dates = sorted(window.date.unique())
counts = window.groupby('rssd').date.nunique()
ids = counts[counts == len(all_dates)].index
bal = window[window.rssd.isin(ids)].copy()
bal['log_assets'] = np.log(bal['assets'])
base = bal[bal.date == '2021-12-31'][['rssd', 'hhi', 'assets']].drop_duplicates('rssd').set_index('rssd')
bal = bal.join(base['hhi'].rename('hhi0'), on='rssd')
bal['effr'] = bal.date.map(effr_map)
q25, q75 = base.hhi.quantile([0.25, 0.75])
bal['high_grp'] = (bal.hhi0 >= q75).astype(int)
bal['low_grp'] = (bal.hhi0 <= q25).astype(int)


def two_way_demean(df, cols, entity='rssd', time='date'):
    out = pd.DataFrame(index=df.index)
    for c in cols:
        x = df[c].astype(float)
        out[c] = x - df.groupby(entity)[c].transform('mean') - df.groupby(time)[c].transform('mean') + x.mean()
    return out


def fit_fe(df, interaction_col):
    d = df.dropna(subset=['deposit_rate', interaction_col, 'log_assets']).copy()
    z = two_way_demean(d, ['deposit_rate', interaction_col, 'log_assets'])
    res = sm.OLS(z.deposit_rate, z[[interaction_col, 'log_assets']]).fit(
        cov_type='cluster', cov_kwds={'groups': d.rssd, 'use_correction': True}
    )
    return res, d

# Main extreme-quartile and continuous-HHI regressions.
reg_rows = []
extreme = bal[(bal.high_grp == 1) | (bal.low_grp == 1)].copy()
extreme['high_effr'] = extreme.high_grp * extreme.effr
for episode, start, end in [('Tightening/hold', '2021-12-31', '2024-06-30'), ('Easing', '2024-06-30', '2026-06-30')]:
    d = extreme[(extreme.date >= start) & (extreme.date <= end)]
    r, used = fit_fe(d, 'high_effr')
    c, se = float(r.params.high_effr), float(r.bse.high_effr)
    reg_rows.append({
        'model': 'Extreme quartiles (High HHI x EFFR)', 'episode': episode,
        'banks': used.rssd.nunique(), 'observations': len(used),
        'raw_coefficient_pctpt_per_1pp_effr': c, 'clustered_se': se, 'p_value': float(r.pvalues.high_effr),
        'less_response_bp_per_100bp_effr': -c * 100,
        'ci95_low_bp': -(c + 1.96 * se) * 100, 'ci95_high_bp': -(c - 1.96 * se) * 100,
        'within_r2': float(r.rsquared)
    })

bal['hhi_effr'] = bal.hhi0 * bal.effr
for episode, start, end in [('Tightening/hold', '2021-12-31', '2024-06-30'), ('Easing', '2024-06-30', '2026-06-30')]:
    d = bal[(bal.date >= start) & (bal.date <= end)]
    r, used = fit_fe(d, 'hhi_effr')
    c, se = float(r.params.hhi_effr), float(r.bse.hhi_effr)
    reg_rows.append({
        'model': 'Continuous baseline HHI x EFFR', 'episode': episode,
        'banks': used.rssd.nunique(), 'observations': len(used),
        'raw_coefficient_pctpt_per_1pp_effr': c, 'clustered_se': se, 'p_value': float(r.pvalues.hhi_effr),
        'less_response_bp_per_100bp_effr': -c * 0.1 * 100,
        'ci95_low_bp': -(c + 1.96 * se) * 0.1 * 100, 'ci95_high_bp': -(c - 1.96 * se) * 0.1 * 100,
        'within_r2': float(r.rsquared)
    })
pd.DataFrame(reg_rows).to_csv(OUT / 'regression_results_reproduced.csv', index=False)

# Endpoint cumulative betas.
endpoints = [pd.Timestamp('2021-12-31'), pd.Timestamp('2024-06-30'), pd.Timestamp('2026-06-30')]
ep = panel[panel.date.isin(endpoints)].copy()
ep_counts = ep.groupby('rssd').date.nunique()
ep_ids = ep_counts[ep_counts == 3].index
ep = ep[ep.rssd.isin(ep_ids)].copy()
ep_base = ep[ep.date == endpoints[0]][['rssd', 'hhi']].set_index('rssd').hhi
lo, hi = ep_base.quantile([0.25, 0.75])
ep = ep.join(ep_base.rename('hhi0'), on='rssd')
ep['group'] = np.where(ep.hhi0 <= lo, 'Competitive (bottom HHI quartile)', np.where(ep.hhi0 >= hi, 'Concentrated (top HHI quartile)', 'Middle'))
rows = []
for group in ['Competitive (bottom HHI quartile)', 'Concentrated (top HHI quartile)']:
    med = ep[ep.group == group].groupby('date').deposit_rate.median()
    for episode, s, t in [('Tightening/hold', endpoints[0], endpoints[1]), ('Easing', endpoints[1], endpoints[2])]:
        dr = med.loc[t] - med.loc[s]
        df = effr_map.loc[t] - effr_map.loc[s]
        rows.append({'group': group, 'episode': episode, 'common_endpoint_banks': len(ep_ids),
                     'start_date': s.date(), 'end_date': t.date(), 'start_rate_pct': med.loc[s], 'end_rate_pct': med.loc[t],
                     'start_effr_pct': effr_map.loc[s], 'end_effr_pct': effr_map.loc[t], 'deposit_change_pp': dr,
                     'effr_change_pp': df, 'cumulative_beta_pct': 100 * dr / df})
pd.DataFrame(rows).to_csv(OUT / 'endpoint_betas_reproduced.csv', index=False)

print('Reproduced outputs written to:', OUT)
