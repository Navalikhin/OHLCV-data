import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, Float, String
from config import DB_URL, SYMBOL, TIMEFRAMES

def create_database_if_not_exists(db_url):
    from sqlalchemy.engine.url import make_url

    url = make_url(db_url)
    db_name = url.database

    # Create a temporary engine without the database
    url = url.set(database=None)
    tmp_engine = sqlalchemy.create_engine(url)

    with tmp_engine.connect() as conn:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ База данных '{db_name}' проверена или создана.")

def create_ohlcv_tables(engine, symbol, timeframes):
    """
    Create tables for different timeframes if they do not exist.
    """
    metadata = MetaData()
    for tf in timeframes:
        table_name = f"{symbol.replace('/', '_')}_{tf}"
        table = Table(
            table_name,
            metadata,
            Column("timestamp", DateTime, primary_key=True),
            Column("open", Float),
            Column("high", Float),
            Column("low", Float),
            Column("close", Float),
            Column("volume", Float),
            extend_existing=True,
        )
        table.create(bind=engine, checkfirst=True)
        print(f"✅ Table '{table_name}' checked or created.")

def main():
    create_database_if_not_exists(DB_URL)
    engine = create_engine(DB_URL)
    create_ohlcv_tables(engine, SYMBOL, TIMEFRAMES)

if __name__ == "__main__":
    main()
