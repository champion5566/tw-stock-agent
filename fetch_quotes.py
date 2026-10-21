import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")

STOCKS = {
    "2313": "tse",
    "2367": "tse",
    "3491": "otc",
}

OUTPUT = Path("quotes.json")


def now_tw():
    return datetime.now(TZ)


def valid_price(value):
    try:
        price = float(value)
        return price if price > 0 else None
    except (ValueError, TypeError):
        return None


def request_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://mis.twse.com.tw/",
        },
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def fetch_mis():
    symbols = "|".join(
        f"{market}_{code}.tw"
        for code, market in STOCKS.items()
    )

    params = urllib.parse.urlencode({
        "ex_ch": symbols,
        "json": "1",
        "delay": "0",
        "_": str(int(time.time() * 1000)),
    })

    url = (
        "https://mis.twse.com.tw/stock/api/"
        "getStockInfo.jsp?" + params
    )

    data = request_json(url)

    if not isinstance(data.get("msgArray"), list):
        raise ValueError("MIS missing msgArray")

    return {
        stock.get("c"): stock
        for stock in data["msgArray"]
        if stock.get("c") in STOCKS
    }


def fetch_yahoo(code, market):
    suffix = "TW" if market == "tse" else "TWO"

    symbol = f"{code}.{suffix}"

    url = (
        "https://query1.finance.yahoo.com/"
        f"v8/finance/chart/{symbol}"
        "?interval=1m&range=1d"
    )

    data = request_json(url)

    chart = data.get("chart", {})
    error = chart.get("error")

    if error:
        raise ValueError(str(error))

    results = chart.get("result") or []

    if not results:
        raise ValueError("Yahoo returned no chart")

    result = results[0]
    meta = result.get("meta", {})

    # Yahoo 最新市場價格及其對應時間
    price = valid_price(meta.get("regularMarketPrice"))
    timestamp = meta.get("regularMarketTime")

    if price is None or timestamp is None:
        raise ValueError("Yahoo missing price or timestamp")

    quote_time = datetime.fromtimestamp(
        int(timestamp), TZ
    )

    return {
        "price": price,
        "quote_time": quote_time,
        "symbol": meta.get("symbol"),
    }


def parse_mis_time(stock):
    try:
        date = stock["d"]
        clock = stock["t"]

        return datetime.strptime(
            date + " " + clock,
            "%Y%m%d %H:%M:%S",
        ).replace(tzinfo=TZ)
    except (KeyError, ValueError, TypeError):
        return None


def is_fresh(quote_time, current):
    if quote_time is None:
        return False

    # 只接受今天的資料
    if quote_time.date() != current.date():
        return False

    # 不接受未來超過 2 分鐘的時間
    if quote_time > current + timedelta(minutes=2):
        return False

    # 盤中最多允許 10 分鐘延遲
    if current.weekday() < 5 and (
        current.hour < 13
        or (current.hour == 13 and current.minute <= 30)
    ):
        return current - quote_time <= timedelta(minutes=10)

    # 收盤後允許當天的最後報價
    return True


def process_stock(code, market, mis_data, current):
    stock = mis_data.get(code, {})

    mis_time = parse_mis_time(stock)
    mis_price = valid_price(stock.get("z"))

    result = {
        "symbol": code,
        "name": stock.get("n"),
        "market": market,
        "price": None,
        "price_source": None,
        "quote_time": None,
        "status": "PRICE_UNAVAILABLE",
        "mis": {
            "date": stock.get("d"),
            "time": stock.get("t"),
            "last_trade_price": mis_price,
            "previous_close": valid_price(stock.get("y")),
            "open": valid_price(stock.get("o")),
            "high": valid_price(stock.get("h")),
            "low": valid_price(stock.get("l")),
            "volume_raw": stock.get("v"),
        },
        "errors": [],
    }

    if mis_price is not None and is_fresh(mis_time, current):
        result["price"] = mis_price
        result["price_source"] = "TWSE_MIS"
        result["quote_time"] = mis_time.isoformat()
        result["status"] = "OK"
        return result

    result["errors"].append(
        "MIS price missing or stale"
    )

    try:
        yahoo = fetch_yahoo(code, market)

        expected = f"{code}.{'TW' if market == 'tse' else 'TWO'}"

        if yahoo["symbol"] != expected:
            raise ValueError("Yahoo symbol mismatch")

        if not is_fresh(yahoo["quote_time"], current):
            raise ValueError("Yahoo quote is stale")

        result["price"] = yahoo["price"]
        result["price_source"] = "YAHOO_FINANCE"
        result["quote_time"] = yahoo["quote_time"].isoformat()
        result["status"] = "OK"

    except Exception as exc:
        result["errors"].append(
            f"Yahoo fallback failed: {type(exc).__name__}: {exc}"
        )

    return result


def main():
    current = now_tw()
    mis_error = None

    try:
        mis_data = fetch_mis()
    except Exception as exc:
        mis_data = {}
        mis_error = f"{type(exc).__name__}: {exc}"

    quotes = []

    for code, market in STOCKS.items():
        result = process_stock(
            code, market, mis_data, current
        )

        if mis_error:
            result["errors"].append(
                f"MIS request failed: {mis_error}"
            )

        quotes.append(result)

    success = sum(
        item["status"] == "OK"
        for item in quotes
    )

    output = {
        "fetched_at": current.isoformat(),
        "total": len(quotes),
        "successful": success,
        "failed": len(quotes) - success,
        "quotes": quotes,
    }

    OUTPUT.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps(
        output,
        ensure_ascii=False,
        indent=2,
    ))

    print(
        f"\nRESULT: {success}/{len(quotes)} "
        "stocks have valid prices"
    )

    # 三檔都必須有有效價格才算驗收成功
    if success != len(quotes):
        sys.exit(1)


if __name__ == "__main__":
    main()