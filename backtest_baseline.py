"""Research-only baseline using the community-maintained backtesting.py engine.

Predeclared SMA20/60 crossover, next-bar orders, transaction costs,
chronological holdout and a buy-and-hold comparator. Never trades live.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

TZ = ZoneInfo("Asia/Taipei")
MIN_BARS = 120
COMMISSION_PER_SIDE = 0.0015  # illustrative, NOT verified broker-specific Taiwan fees
SPREAD = 0.001  # conservative assumed spread, not measured


def sma(arr, n):
    return pd.Series(arr).rolling(n).mean().to_numpy()


class SMA2060(Strategy):
    def init(self):
        self.fast = self.I(sma, self.data.Close, 20)
        self.slow = self.I(sma, self.data.Close, 60)

    def next(self):
        if np.isnan(self.fast[-1]) or np.isnan(self.slow[-1]):
            return
        if self.fast[-2] <= self.slow[-2] and self.fast[-1] > self.slow[-1]:
            if not self.position:
                self.buy()
        elif self.fast[-2] >= self.slow[-2] and self.fast[-1] < self.slow[-1]:
            if self.position:
                self.position.close()


def prepare(rows):
    frame = pd.DataFrame(rows)
    if frame.empty or "date" not in frame:
        return None
    rename = {"open": "Open", "max": "High", "min": "Low",
              "close": "Close", "Trading_Volume": "Volume"}
    required = list(rename)
    if any(col not in frame.columns for col in required):
        return None
    frame = frame[["date"] + required].rename(columns=rename)
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    for col in rename.values():
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna().drop_duplicates("date", keep="last").sort_values("date")
    frame = frame.set_index("date")
    frame = frame[(frame["Close"] > 0) & (frame["Open"] > 0)
                  & (frame["High"] >= frame["Low"])]
    return frame


def score(frame):
    bt = Backtest(frame, SMA2060, cash=1_000_000,
                  commission=COMMISSION_PER_SIDE, spread=SPREAD,
                  trade_on_close=False, exclusive_orders=True, finalize_trades=True)
    s = bt.run()
    return {
        "return_pct": round(float(s["Return [%]"]), 3),
        "buy_hold_return_pct": round(float(s["Buy & Hold Return [%]"]), 3),
        "max_drawdown_pct": round(float(s["Max. Drawdown [%]"]), 3),
        "trades": int(s["# Trades"]),
        "win_rate_pct": (round(float(s["Win Rate [%]"]), 3)
                         if pd.notna(s["Win Rate [%]"]) else None),
    }


def main():
    now = datetime.now(TZ)
    date, slot = now.date().isoformat(), os.getenv("REPORT_SLOT", "evening")
    src = Path("out") / date / (slot + ".json")
    if not src.exists():
        raise SystemExit("Missing dated market input")
    stocks = json.loads(src.read_text(encoding="utf-8")).get("stocks", {})
    output = {
        "schema_version": "backtest-baseline-v1",
        "created_at_taipei": now.isoformat(),
        "library": "backtesting.py", "strategy": "SMA20_60_LONG_ONLY",
        "execution": "signals on close, market order next bar open; no lookahead",
        "cost_assumptions": {"commission_each_side": COMMISSION_PER_SIDE, "spread": SPREAD,
                             "note": "Assumed research friction, not Taiwan broker fee/tax schedule"},
        "minimum_bars": MIN_BARS, "holdout_fraction": 0.30,
        "status": "EXPLORATORY_ONLY", "stocks": {},
        "warnings": ["No parameter optimization or statistical significance claims.",
                     "Corporate actions, dividends, taxes and survivorship effects not fully modeled.",
                     "Holdout is chronological but remains exploratory with limited history."],
    }
    for code, stock in stocks.items():
        rows = stock.get("daily_ohlcv", {}).get("history") or []
        frame = prepare(rows)
        n = 0 if frame is None else len(frame)
        if n < MIN_BARS:
            output["stocks"][code] = {"status": "INSUFFICIENT_HISTORY", "bars": n}
            continue
        cut = int(n * 0.70)
        # Holdout receives prior 60 bars as warmup; trades before cutoff are not evaluated.
        train = frame.iloc[:cut]
        test = frame.iloc[max(0, cut - 60):]
        try:
            output["stocks"][code] = {
                "status": "EXPLORATORY_ONLY", "bars": n,
                "train_end": str(train.index[-1].date()),
                "holdout_start": str(frame.index[cut].date()),
                "in_sample": score(train),
                "holdout_with_warmup": score(test),
                "caution": "Holdout includes 60-bar indicator warmup; performance may include warmup trades. Not a clean out-of-sample PnL.",
            }
        except Exception as exc:
            output["stocks"][code] = {"status": "ERROR", "bars": n, "error_type": type(exc).__name__}
    dst = Path("out") / date / ("backtest-" + slot + ".json")
    dst.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("BACKTEST_BASELINE", str(dst),
          {k: v["status"] for k, v in output["stocks"].items()})


if __name__ == "__main__":
    main()
