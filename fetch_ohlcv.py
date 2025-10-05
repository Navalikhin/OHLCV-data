import ccxt
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from config import DB_URL, SYMBOL, EXCHANGE, TIMEFRAMES, START_DATE

def get_exchange(name):
    exchange_class = getattr(ccxt, name)
    exchange = exchange_class({'enableRateLimit': True})
    return exchange

def fetch_ohlcv(exchange, symbol, timeframe, since_ms):
    all_data = []
    limit = 1000
    while True:
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since_ms, limit=limit)
        if not data:
            break
        all_data += data
        since_ms = data[-1][0] + 1
        # Binance limit — less than 1200 requests per minute
        if len(data) < limit:
            break
    return all_data

def ohlcv_to_df(ohlcv):
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def get_last_timestamp(engine, table):
    try:
        query = f"SELECT MAX(timestamp) FROM {table}"
        last_ts = pd.read_sql(query, engine).iloc[0, 0]
        return pd.Timestamp(last_ts) if last_ts else None
    except Exception:
        return None

def update_data(engine, exchange, symbol, timeframe):
    table_name = f"{symbol.replace('/', '_')}_{timeframe}"
    last_ts = get_last_timestamp(engine, table_name)
    since = int(last_ts.timestamp() * 1000) if last_ts else exchange.parse8601(START_DATE)
    print(f"Fetching {symbol} {timeframe} since {datetime.utcfromtimestamp(since / 1000)}")
    ohlcv = fetch_ohlcv(exchange, symbol, timeframe, since)
    if not ohlcv:
        print(f"No new data for {timeframe}")
        return
    df = ohlcv_to_df(ohlcv)
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"✅ Updated {table_name}: {len(df)} rows")

def main():
    engine = create_engine(DB_URL)
    exchange = get_exchange(EXCHANGE)
    for tf in TIMEFRAMES:
        update_data(engine, exchange, SYMBOL, tf)

if __name__ == "__main__":
    main()
