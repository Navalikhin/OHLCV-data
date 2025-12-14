from sqlalchemy import create_engine, text
from config import DB_URL

TABLES = {
    "btc_ohlcv_1h": "1h",
    "btc_ohlcv_4h": "4h",
    "btc_ohlcv_1d": "1d",
}

SQL = """
CREATE TABLE IF NOT EXISTS {table} (
    open_time BIGINT PRIMARY KEY,
    open DECIMAL(18,8),
    high DECIMAL(18,8),
    low DECIMAL(18,8),
    close DECIMAL(18,8),
    volume DECIMAL(18,8),
    close_time BIGINT
)
"""

def main():
    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        for table in TABLES:
            conn.execute(text(SQL.format(table=table)))
            print(f"✔ Table {table} ready")

if __name__ == "__main__":
    main()
