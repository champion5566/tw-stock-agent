# 台股流程分工與上線驗收（2026-11-25）

全部時間為 Asia/Taipei。ChatGPT 任務已逐一回讀。GitHub 的實際檔案 commit 和任務結果才是驗收依據；ChatGPT 可證明有執行結果，手機通知回執目前為 UNKNOWN。

## 實際執行

| 案例 | 觸發 → 採集 → 持久化 → 報告 |
|---|---|
| 11/25 晨報 | GPT 08:20:03 開始，建立備料請求；Actions 08:21:00 解析 morning request，至 08:28:24 提交報告包並讀回；GPT 08:40:03 開始，08:40:28 寫入四模型不變原稿，08:40:53 產生手機可看的結果。後續老師用正式結算 39,983.91 核對。 [採集](https://github.com/champion5566/tw-stock-agent/actions/runs/45517348419/job/138880091694) · [資料包](https://github.com/champion5566/tw-stock-agent/blob/d16152e83a643326fcdfaa214b59a5633c56b03d/reports/2026-11-25/morning.json) · [不變原稿](https://github.com/champion5566/tw-stock-agent/blob/700198886f73dcd68dfcdf28cd4463ef696cd441/predictions/2026-11-25/morning.md) · [ChatGPT 結果](https://chatgpt.com/c/6b062e96-1ee0-83ee-9029-4ea305ce657d) |
| 11/24 夜報 | GPT 22:52:35 開始；Actions 22:53:42 解析 evening request，22:55:18 讀回準時的資料包。GPT 23:00:10 開始、23:01:17 有結果；備料驗收指出夜報原稿缺失。當日晨報亦無正式原稿，已有獨立回放，後來老師用 TWSE 官方開盤結算。現有證據無法證明夜報原稿曾嘗試寫入或為何缺失。 [採集](https://github.com/champion5566/tw-stock-agent/actions/runs/45419133196/job/138533488353) · [ChatGPT 結果](https://chatgpt.com/c/6ad8d3ee-2dc4-83e8-9122-e5eeec4c566f) · [兩類結算](https://github.com/champion5566/tw-stock-agent/actions/runs/45613208686/job/139201817640) |
| 11/16 夜報 | 22:58 截止前無可見備料請求或夜報採集 run。首個可見 evening run 於 11/17 00:27:33 啟動並以執行當天為鍵，00:29:33 寫進 11/17，11/16 原稿在 23:22:57 建立。可證實斷點是及時採集未啟動，且晚到跨日曾污染次日路徑。GitHub 原定 22:52 事件與排程佇列、GPT 22:50 嘗試寫入紀錄不足，無法區分漏觸發、延遲或兩者。 [採集](https://github.com/champion5566/tw-stock-agent/actions/runs/43907643571/job/133440671996) · [晚到提交](https://github.com/champion5566/tw-stock-agent/commit/dc64d3426ac0932186be00200a4b6fa0fe56b4cf) |

## 分工與去留

| 入口 | 獨有功能、移除代價與證據 |
|---|---|
| GPT 備料 08:20、22:50 | **保留，任務縮為提交提示。** 跨平台的主要喚起，去掉就只剩同一排程器的原生 cron。11/25 早、11/24 晚都有準時資料包及請求 run。過期、重複與就緒由 GitHub 裁決。 |
| main 的 push 請求檔 | **保留。** 既有連線能 create-only 並回讀，亦提供一次性 recovery 的明確日期/時段/提交。原生 cron 未觸發時仍能上游啟動。程式碼 push 沒有採集請求，會留下跳過紀錄。 |
| 原生 cron 08:30、08:35、22:52，另有 05:35 夜盤觀察 | **保留。** GPT 請求缺失時能啟動相同 runner，部分資料可再試；11/16 證明原生排程可能晚到，兩種入口是候選，不能互相假設會補救。共享時段與資料驗收，實際已發布完整資料時備援不打供應商。05:35 為已完成夜盤觀察，角色不同。 |
| Market Data Snapshots 08:25、22:15 | **保留。** 發布研究、既有 ledger review 與持久化 handoff，不取代正式晨夜報的 cross-market 資料包。兩邊都會取部分台股輸入，但各自有不同輸出，尚無證據足以收掉其中一個。 |
| GPT 晨報 08:40、夜報 23:00 | **保留。** 負責假說、決策摘要、手機報告、原稿 create-only 與精確回讀。GitHub 已寫報告資料包、驗證原稿與結算，可在 GPT 延遲時查看原始行情證據。只有 GPT task 結果能證明私人報告已產生。 |
| GPT 老師 19:00、GitHub Teacher Evidence Audit | **保留兩者。** GitHub 用固定版本做可執行驗收、兩類結算與去重；GPT 可看私人報告、判斷/勘誤並依審核推進隊列。404 後繼續、結案後下一項已實跑。GPT 老師無須阻塞兩份報告。 [404 實跑](https://github.com/champion5566/tw-stock-agent/actions/runs/45611500213) · [重啟](https://github.com/champion5566/tw-stock-agent/actions/runs/45613208686) |

## 恢復與驗收

唯一正式採集就緒來源是 GitHub data/snapshots 的固定版本資料包及 Git 檔案變更時間。只有同日、時段內、截止前已實際提交、已讀回且 DATA_READY 才跳過後續取數；PARTIAL 保留正確欄位並容許窗口內的備援改善。同一 branch 的現有 concurrency 不會中止跑著的工作，但 GitHub 可能替換 pending。這不保證每次喚起都運行。超時或跨日留下明確 gate 證據，手動預跑只供診斷，下一次不覆寫原稿。資料包、GPT 原稿及通知各自驗收。既有老師結算、唯一交易日計數、ACT 成本政策保留。

對 11/25 晚 → 11/26 早的正式驗收：觀測 GPT 請求、采集 gate/發布提交、報告執行結果、新原稿精確讀回；確認夜報採納勘誤，且次晨研究狀態包含夜報精確 commit:path。若一條喚起失敗，查另一條實際 run。過截止仍可手動預跑並標時效，禁止補造原始帳本。手機收件保留 UNKNOWN。排程或權限無變更，回復方式是撤銷本次 PR 並從既有任務歷史恢復備料指令。

## 成熟實作參考

- Dagster 檔案 sensor 從新檔啟動下游，用持久化 run key 避免重複；cursor 保留已處理位置，失敗重跑從出錯步驟繼續需要跨 run 可讀的 I/O。此處以日期/時段和已發布 Git 檔案取代 run key/共享 I/O，只略過已完成工作，partial 仍可重試，避免另建排程器及狀態資料庫。 [檔案 sensor 完整例子](https://docs.dagster.io/guides/automate/sensors) · [失敗重跑策略](https://docs.dagster.io/deployment/execution/run-retries)
- Airflow logical date 直接把工作資料期間和實際喚起時間分開。現有 GitHub cron payload 不提供可驗證的原定 occurrence，採用較保守的時段拒收，沒有證據時不回填舊日或把它寫成隔日。 [Airflow DAG run](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html)
- GitHub 文件明示 schedule 可延後或丟棄，且 concurrency 不等於持久佇列。保留獨立 push 和排程時鐘，在 runner 開始時以固定狀態決定是否採集。回歸測試覆蓋真實 00:27 跨日案例、重複、晚到的提交、單來源部分成功與恢復。 [排程事件](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) · [Concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
