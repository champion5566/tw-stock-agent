# 夜報情境實驗

執行時間：2026-10-22T12:33:24.353924+08:00｜資料驗收：DATA_PARTIAL｜送達：NOT_ACKNOWLEDGED

現時資料流程試跑；不代表已在08:20或23:00執行或送達，亦非歷史時點回放。
交易日使用 exchange_calendars XTAI；臨時停市以來源實際狀態另行核對。

必備資料驗收：

| 項目 | 狀態 | 缺漏／異常 |
|---|---|---|
| required_stock_data | PARTIAL | 0050=MISSING_OR_INVALID_FIELDS, 006208=MISSING_OR_INVALID_FIELDS, 00631L=MISSING_OR_INVALID_FIELDS, 2330=MISSING_OR_INVALID_FIELDS, 3707=MISSING_OR_INVALID_FIELDS, 5483=MISSING_OR_INVALID_FIELDS |
| market_context | PARTIAL | TAIEX=NOT_COLLECTED_OR_WRONG_SESSION, TPEX=NOT_COLLECTED_OR_WRONG_SESSION, breadth=NOT_COLLECTED_OR_WRONG_SESSION, institutional_totals=NOT_COLLECTED_OR_WRONG_SESSION, margin_totals=NOT_COLLECTED_OR_WRONG_SESSION, futures_positioning=NOT_COLLECTED_OR_WRONG_SESSION |
| us_intraday | PARTIAL | SP500=STALE, NASDAQ=STALE, SOX=STALE, VIX=STALE, TSM_ADR=STALE, NVDA=STALE, AMD=STALE, AVGO=STALE, MU=STALE |
| tx_live | PARTIAL | TXFR1=STALE |
| cutoff | PASS | — |

持股／觀察清單的行情資料完整，不代表跨市場、帳本或送達驗收完成。

台股基準交易日：2026-10-22

| 股票／角色 | 日期 | 開 | 高 | 低 | 收 | 成交股數 | OHLC狀態 | 法人資料日期／狀態 | 融資券日期／狀態 |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| 2313（觀察） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 2330（必備） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 0050（必備） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 5483（必備） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 3707（必備） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 2367（觀察） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 3491（觀察） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 006208（必備） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |
| 00631L（必備） | 2026-10-21 | — | — | — | — | — | SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED | 2026-10-21 / SESSION_NOT_CLOSED |

六檔必備衍生欄位（同一 FinMind 來源；法人單位為股，融資券為來源原生張數）：

| 股票 | 前收 | 成交值TWD | 振幅% | 5日量比 | 20日量比 | 外資淨買 | 投信淨買 | 自營淨買 | 法人5日合計 | 融資增減 | 融券增減 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0050 | — | — | — | — | — | — | — | — | — | — | — |
| 006208 | — | — | — | — | — | — | — | — | — | — | — |
| 00631L | — | — | — | — | — | — | — | — | — | — | — |
| 2330 | — | — | — | — | — | — | — | — | — | — | — |
| 3707 | — | — | — | — | — | — | — | — | — | — | — |
| 5483 | — | — | — | — | — | — | — | — | — | — | — |

跨市場觀測（依來源時間；Yahoo K線不等於正式收盤）：

| 市場／標的 | 價格 | 來源時間 | 狀態 |
|---|---:|---|---|
| us/SP500 | 7757.169921875 | 2026-10-22T04:00:00+08:00 | HISTORICAL_BAR |
| us/NASDAQ | 26702.857421875 | 2026-10-22T04:00:00+08:00 | HISTORICAL_BAR |
| us/SOX | 11505.5556640625 | 2026-10-22T04:00:00+08:00 | HISTORICAL_BAR |
| us/VIX | 16.68000030517578 | 2026-10-22T04:15:00+08:00 | HISTORICAL_BAR |
| us/NVDA | 219.2585 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/AMD | 540.5 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/AVGO | 333.4 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/MU | 898.31 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/TSM_ADR | 426.5 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/AMZN | 261.4 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/BRK.B | 539.84 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/GOOG | 329.12 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/META | 712.3134 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/QCOM | 176.2816 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/SPCX | 156.7 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/TLT | 80.49 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/TSLA | 373.63 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| us/QQQ | 719.42 | 2026-10-22T07:55:00+08:00 | HISTORICAL_BAR |
| jp/NIKKEI225 | 63335.0 | 2026-10-22T12:15:00+08:00 | PASS |
| jp/TOPIX_ETF_PROXY | 422.1000061035156 | 2026-10-22T12:15:00+08:00 | PASS |
| jp/ADVANTEST | 32700.0 | 2026-10-22T12:15:00+08:00 | PASS |
| jp/TOKYO_ELECTRON | 9575.0 | 2026-10-22T12:15:00+08:00 | PASS |
| kr/KOSPI | 5563.3798828125 | 2026-10-22T12:10:00+08:00 | PASS |
| kr/KOSDAQ | 773.02001953125 | 2026-10-22T12:10:00+08:00 | PASS |
| kr/SAMSUNG | 214250.0 | 2026-10-22T12:10:00+08:00 | PASS |
| kr/SK_HYNIX | 1231000.0 | 2026-10-22T12:10:00+08:00 | PASS |

台指期：{"TXFR1": {"price": 46500.0, "trade_time": "2026-10-22T12:33:20.467000+08:00", "source": "Shioaji", "contract_code": "TXFR1", "data_kind": "tick", "status": "PASS", "is_live": true}}

涵蓋狀態：{"stocks_total": 9, "daily_ohlcv_target_session": 0, "institutional_target_session": 0, "margin_target_session": 0}
