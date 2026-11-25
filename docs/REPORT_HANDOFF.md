# 晨報、老師與夜報的交接

交易研究和歷史重播沿用 `predictions/YYYY-MM-DD/{morning,evening}.md`、`[RESEARCH_STATE]`、`[ACT]` 和既有資料分支。原檔只建立一次，寫入後讀回實際 commit。補跑保留原檔，新證據另存。資料修復結果由既有 Market Data Snapshots 的 ledger-review 工作寫入 `evaluations/report-handoff-<run>-<attempt>.json`；Teacher Evidence Audit 同時上傳 `report-handoff`。每次依據一個資料 SHA 重算，樣本以交易日和 ACT ID 去重，不累加舊報告計數。

## 各時段責任

- 晨報以 08:38 截止，以 08:40 出報。按正式交易日曆查上一個交易日夜報原稿，確認已完成與來源日期，再沿用其中仍有效的情境、失效條件和到期日。把父檔的 `<commit>:predictions/YYYY-MM-DD/evening.md` 寫進本次 `[RESEARCH_STATE]`。上一交易日原稿缺失時，照常出報、保留缺漏，較舊假說只可明示日期作背景。開盤預測沿用來源 `opening_forecast`，正文只突出固定的 V1 或其不可用原因。四個可重算模型及權重留在原始帳本，寫上 `Source ref <40位SHA>`、實際時鐘、模型版本、目標日和 OPEN ID。發布時間用實際檔案 commit。
- 老師 19:00 讀今天晨報及上一份完成的夜報。讀同一 code commit 的樹確認 404。已在樹上時重試一次同一 ref，再查路徑或權限；缺少時以現行契約、程式、執行紀錄繼續。讀最新 `report-handoff` 後執行 `repair_gate.next`，逐項記錄可重現輸入、受影響環節、修正、測試及恢復條件，再跑 stop_gate。檔案缺失、等待 CI 或排程不得阻塞可獨立工作。到執行上限時將嘗試、證據與恢復點存入既有修復紀錄。可公開訂正另存 `ledger/corrections/YYYY-MM-DD-<run>.json`，只含非個資、原始 ref、issue ID、原因、已驗證結果與到期日；用 create-only 並回讀。遇相同 ID 保留第一筆。下次從最新 checkpoint 繼續。
- 夜報依 22:58 截止，以 23:00 出報。驗今天原始晨報和教師指正，老師未完成時照常出報。驗價格、來源日期和實際 commit，結算官方開盤；有號誤差＝預估減實際。查不到既有機器產物可按同版程式、同一 ref 重算。正式與重播分開。以 `[RESEARCH_STATE]` 保存仍有效假說、反證、待追蹤標的、到期與下一個交易日讀回所需的來源 ref。保留現有個股要求、引用、輸出品質和隱私門檻。
- 「全面漲停」須有同日、範圍一致的漲停家數和可信的獨立來源。上漲家數、指數漲幅和據此推論的反轉風險可各自陳述。缺獨立證據時表述為待驗假說，寫下反證。個別資料過期不抹掉其他欄位。

## 模擬交易

原始報告可在既有 `[ACT]` 區塊加一個 JSON，最後一個 ACT 後可接 `[RESEARCH_STATE]`。最多兩個情境。決策欄位用 `id`、`version`、`symbol`、`rule`、`limit`、`earliest_at`、`entry_day`、`exit_day`、`invalidation`、`benchmark` 和 `costs`。費用欄位 `version`、`instrument_type`（stock 或 etf）、`trade_method`（cash_swing）、`fee_bps_per_side`、`sell_tax_bps`、`slippage_bps_per_side` 使用公開的固定模擬假設，禁止現實帳戶費率與持倉。原始 commit 須早於入場時間。交易日、價格和觸發依據事前固定。

現行可計分規則 `PREPLACED_BUY_LIMIT_OPEN_TO_OPEN`（`invalidation=CANCEL_IF_ENTRY_AUCTION_MISSED`） 只模擬開盤前已決定的現金多單和預定交易日開盤出場。開盤嚴格優於限價且滑價後仍在限價內才使用保守成交代理。跳空超過限價不觸發；等於限價、單一價格鎖死、零量、缺同日資料、只有日線且需要盤中順序的條件都不計成交。未證實流動性時只能稱模擬。基準 0050 用相同日期開盤毛報酬，另列假設成本後淨報酬、每筆平倉後回撤、n 和樣本日期；這些只是已平倉樣本的資金曲線，並未量測盤中回撤。重疊樣本不疊加成獨立投資。沒有正優勢證據時正文寫等待。規則改版只影響未來原始 ACT。

## 採用依據

| 來源 | 對應故障 | 為何適用 | 驗證 |
|---|---|---|---|
| [GitHub 排程與事件](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) | 漏觸發、遲到重跑 | 以現有備援、run 身分、檔案發布時間及獨立讀回核實 | Quality Gate 驗證原時程和晚到樣本拒收；Teacher Evidence Audit 驗證實際資料 |
| [Freqtrade lookahead-analysis](https://www.freqtrade.io/en/stable/lookahead-analysis/) | 未來資料污染 | 將事前規則及原始輸入鎖在發布時點，未來資料只用於結算 | 測試拒收晚於開盤的規則、晚於截止的輸入及鎖死成交 |
