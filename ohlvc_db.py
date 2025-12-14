import time
import requests
from datetime import datetime
from sqlalchemy import create_engine, text
from config import DB_URL

BASE_URL = "https://api.binance.com/api/v3/klines"

INSERT_SQL = """
INSERT IGNORE INTO {table}
(open_time, open, high, low, close, volume, close_time)
VALUES (:open_time, :open, :high, :low, :close, :volume, :close_time)
"""
# Receive last open time from the database
def get_last_open_time(conn, table):
    result = conn.execute(
        text(f"SELECT MAX(open_time) FROM {table}")
    ).scalar()
    return result



def fetch_ohlcv(symbol, interval, table, start_date):

    engine = create_engine(DB_URL)
    limit = 1000

    with engine.begin() as conn:

        last_db_ts = get_last_open_time(conn, table)

        if last_db_ts:
            start_ts = last_db_ts + 1
            print(f"▶ {table}: resume from DB {start_ts}")
        else:
            start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
            print(f"▶ {table}: start from {start_date}")

        while True:

            params = {
                "symbol": symbol,
                "interval": interval,
                "startTime": start_ts,
                "limit": limit,
            }

            r = requests.get(BASE_URL, params=params)
            data = r.json()

            # IF EMPTY — NO MORE CANDLES
            if not data:
                print(f"✔ {table}: no more data")
                break

            rows = []
            for c in data:
                rows.append({
                    "open_time": c[0],
                    "open": c[1],
                    "high": c[2],
                    "low": c[3],
                    "close": c[4],
                    "volume": c[5],
                    "close_time": c[6],
                })

            conn.execute(
                text(INSERT_SQL.format(table=table)),
                rows
            )

            last_open = data[-1][0]
            start_ts = last_open + 1

            print(f"✔ {table}: inserted {len(rows)} candles")

            # If less than limit, we reached the end
            if len(data) < limit:
                print(f"✔ {table}: reached last available candle")
                break

            time.sleep(0.2)

def main():
    tasks = [
        ("BTCUSDT", "1h", "btc_ohlcv_1h", "2020-01-01"),
        ("BTCUSDT", "4h", "btc_ohlcv_4h", "2020-01-01"),
        ("BTCUSDT", "1d", "btc_ohlcv_1d", "2020-01-01"),
    ]

    for symbol, interval, table, start in tasks:
        fetch_ohlcv(symbol, interval, table, start)


if __name__ == "__main__":
    main()