# Forecast ledger

The 08:50 ChatGPT morning report is expected to create
`predictions/YYYY-MM-DD/morning.md` on this branch, preserving the exact
[PREDICTION_LEDGER] written **before** the trading session.

The 23:00 evening report reads that original file and grades it; when possible,
it creates `predictions/YYYY-MM-DD/evening.md` containing the next-session
forecast. If the morning file is missing, label the validation **MISSING** and
do not reconstruct it from hindsight.

**Important:** The GitHub Actions market-data workflow only writes the dated
market snapshot JSON. It does *not* generate or save ChatGPT forecasts.
Whether scheduled ChatGPT tasks can write their own ledger files must be
verified on an actual task run. Do not publish account values, positions,
private information or other secrets here: this repository is public.
