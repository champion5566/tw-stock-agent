# 即時行情情境實驗

執行時間：2026-10-22T12:34:15.276997+08:00｜資料驗收：DATA_READY｜送達：NOT_ACKNOWLEDGED

現時資料流程試跑；不代表已在08:20或23:00執行或送達，亦非歷史時點回放。

必備資料驗收：

| 項目 | 狀態 | 缺漏／異常 |
|---|---|---|
| required_stock_quotes | PASS | — |
| tx_live | PASS | — |

持股／觀察清單的行情資料完整，不代表跨市場、帳本或送達驗收完成。

| 標的 | 價格 | 來源 | 資料種類 | 來源時間 | 狀態 |
|---|---:|---|---|---|---|
| TAIEX | 46261.79 | TWSE_MIS | quote_observation | 2026-10-22T12:34:05+08:00 | PASS |
| TPEX | 385.46 | TWSE_MIS | quote_observation | 2026-10-22T12:34:05+08:00 | PASS |
| 2313 | 228.5 | Shioaji_tick | tick | 2026-10-22T12:34:03.975270+08:00 | PASS |
| 2330 | 2395.0 | Shioaji_tick | tick | 2026-10-22T12:34:10.990952+08:00 | PASS |
| 0050 | 107.2 | Shioaji_tick | tick | 2026-10-22T12:34:13.078905+08:00 | PASS |
| 5483 | 189.0 | Shioaji_tick | tick | 2026-10-22T12:34:12.874596+08:00 | PASS |
| 3707 | 71.5 | Shioaji_tick | tick | 2026-10-22T12:34:10.541373+08:00 | PASS |
| 2367 | 45.35 | Shioaji_tick | tick | 2026-10-22T12:34:11.918532+08:00 | PASS |
| 3491 | 1355.0 | Shioaji_tick | tick | 2026-10-22T12:33:55.464761+08:00 | PASS |
| 006208 | 245.6 | Shioaji_tick | tick | 2026-10-22T12:34:07.545401+08:00 | PASS |
| 00631L | 35.82 | Shioaji_tick | tick | 2026-10-22T12:34:13.279218+08:00 | PASS |

台指期：{"TXFR1": {"price": 46484.0, "trade_time": "2026-10-22T12:34:12.379000+08:00", "source": "Shioaji", "contract_code": "TXFR1", "data_kind": "tick", "status": "PASS", "is_live": true}}

涵蓋狀態：{"requested_stocks": 9, "fresh_stocks": 9, "shioaji_selected": 9, "stock_ticks": 9}
