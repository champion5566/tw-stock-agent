import json
import urllib.request
from datetime import datetime, timezone

STOCKS = {
    "2313": "tse",
    "2367": "tse",
    "3491": "otc",
}

def fetch_quotes():
    symbols = "|".join(
        f"{market}_{code}.tw"
        for code, market in STOCKS.items()
    )

    url = (
        "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        f"?ex_ch={symbols}&json=1&delay=0"
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://mis.twse.com.tw/stock/",
        },
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.load(response)

    results = []

    for stock in data.get("msgArray", []):
        results.append({
            "symbol": stock.get("c"),
            "name": stock.get("n"),
            "price": stock.get("z"),
            "date": stock.get("d"),
            "time": stock.get("t"),
            "volume": stock.get("v"),
            "source": "TWSE MIS",
        })

    return results


if __name__ == "__main__":
    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "quotes": fetch_quotes(),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))