# Provider selection and unresolved-gap policy

Use maintained community and official work first. Search the repository, official API
catalogues and working community implementations, choose the smallest suitable adapter,
exercise the actual source, then test its date/units/schema and independent fallback.
Do not stop at the first failed endpoint or add repeated MISSING instructions as a repair.
Each remaining gap needs attempted sources, concrete failure evidence, fallback decision
and next check. New providers are deployed through tests/CI and target readback; reporting
runs use already-reviewed routes rather than attempting architectural changes at deadline.

## Active source matrix

| Need | Selected route | Fallback / qualification |
|---|---|---|
| KOSPI/KOSDAQ/KOSPI200 | Naver domestic index JSON | Existing global Yahoo; source localTradedAt/offset/market state preserved |
| Samsung/SK Hynix | Naver domestic stock JSON | Existing global Yahoo; after-market metadata never becomes a broker Tick |
| Nikkei/TOPIX | Yahoo Japan actual-index priceBoard | Naver `.N225`/`.TOPX` structured actual indices; preserve declared 15-minute delay |
| Advantest/Tokyo Electron | Yahoo Japan stock priceBoard | Naver world-stock JSON, then existing global Yahoo |
| US completed regular session | Existing yfinance daily reader | Existing FinMind USStockPrice, exact symbol/session/date, Close or close field |
| TAIEX OHLCV | TWSE current-month OpenAPI + dated market totals | FinMind TAIEX entire daily row if official target absent; never mix old target dates |
| TPEX OHLCV | TPEx tpex_index + daily_trading_index | Source dates must both match; market share/amount scope remains explicit |
| Breadth | TWSE stock-only official table | TPEx ordinary-stock derived breadth separately, with unparseable changes counted |
| Institutional totals | TWSE BFI82U + TPEx official summary | Both target dates and component sum checked; foreign dealers not double counted |
| Margin totals | TWSE MI_MARGN market table | TPEx unique-instrument balances separately, preserving source-native units |
| Foreign TX positioning | TAIFEX latest API, accepting JSON or CSV | Dated official POST CSV with TXF code, then existing FinMind institutional dataset if unavailable |
| Current US ticker identity | SEC company_tickers.json | Unknown if unavailable; never infer old position ownership from a reused current ticker |

Requests use existing requests/urllib3 retry support, one bounded retry on transient read-only GET/download-POST
errors, and bounded connect/read timeouts. HTML is not parsed as CSV. No CAPTCHA, sign-in
or blocked access path is bypassed; use other documented public interfaces. Date-keyed
historical data can be reused only after matching actual source dates; cached old values
never qualify current quotes. Every selected quote retains source-specific fields.

## Source references evaluated

- https://github.com/agent504330-ux/mcp-korean-stock — Naver basic/index JSON interface.
- https://github.com/dd3ok/naverfinance-api-skill — structured public index/quote endpoints.
- https://github.com/FinanceData/FinanceDataReader — historical versus realtime split;
  do not install a historical package expecting realtime opening quotes.
- https://github.com/ctk03272/mcp-korean-stock — separate intraday and daily sources.
- https://github.com/twjackysu/TWSEMCPServer — official endpoint schemas, named-column
  parsing, latest-only versus dated APIs, cp950 TAIFEX POST CSV.
- https://github.com/ZhuLinsen/daily_stock_analysis — provider failure isolation and
  Taiwan institutional named-column/date/unit semantics.
- Official TWSE/TPEx/TAIFEX OpenAPI catalogues and FinMind USStockPrice documentation.

These small project adapters reuse provider APIs and existing maintained clients; they
do not install an entire extra MCP server just to obtain a JSON quote.

## Timestamp and holiday semantics

Naver localTradedAt is preserved as a provider observation clock, not certified exchange
tick time. Yahoo Japan index and equity boards have different schemas and are parsed
independently with code identity checks. A date-only display has NO_TIMESTAMP; no closing
hour is invented. For HH:MM-only displays, the provider HTTP Date supplies the date only
while the maintained XTKS calendar confirms an open session. The inference, original
text and response date are exposed. Missing HTTP Date cannot qualify a quote.

Asia validation uses maintained XTKS/XKRX calendars: a real local holiday is MARKET_CLOSED,
not a broken feed. Intraday observations still face the original freshness/cutoff checks.
Morning Taiwan daily/context work can start at 08:20; formal regional quote collection
is aligned to 08:28 so an early preparation run does not collect quotes too old for 08:40.
Manual previews do not wait. All actual provider clocks remain authoritative.

## Gaps that are not solved by another quote API

- Exact platform start/completion and device notification receipt require platform
  evidence. Native cron and request-push preparation remain best effort; UNKNOWN is
  retained when no independent receipt exists.
- Forecast calibration requires original pre-open predictions and subsequent outcomes,
  not a quote-source replacement. Do not manufacture numerical forecasts or sample size.
- Historical personal position/security mapping needs the original holding identity;
  current SEC ticker identity does not authorize rewriting that history.
- Ad-hoc exchange closures not in maintained calendars require official closure evidence.
- Existing append-only data is retained. Repository growth is an operational follow-up;
  do not delete original ledgers/observations under a source repair.

Source availability is independently exercised in docs/SOURCE_ACCEPTANCE.md. Closed-market
checks establish retrieval and parsing, not freshness during the next morning window.
