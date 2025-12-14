# BTC OHLCV Data Collector

A Python script for collecting and continuously updating historical **OHLCV** (Open, High, Low, Close, Volume) data for **Bitcoin (BTC)** from the **Binance API** and storing it in a database.

The project is designed to:
- Download full historical data starting from 2020
- Support multiple timeframes (`1h`, `4h`, `1d`)
- Safely resume from the last stored candle
- Avoid duplicate records
- Be easily extendable to other symbols and databases

---

## Features

- Fetches OHLCV data from Binance
- Supports multiple timeframes
- Automatic resume from last stored candle
- Handles Binance API limits correctly
- Prevents infinite loops on the last candle
- Database-ready architecture (SQLAlchemy)
- Can be scheduled for periodic updates

---

## Project Structure
OHLCV-data/
├── config.py # Database configuration
├── create_db.py # Database / tables creation
├── fetch_ohlcv.py # Main data collection script
├── requirements.txt # Python dependencies
└── README.md


---

## Requirements

- Python 3.10+
- MySQL / MariaDB
- Binance public API (no API key required)

---

## Installation

1. Clone the repository:
git clone https://github.com/your-username/OHLCV-data.git
cd OHLCV-data

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux / macOS

3. Install dependencies:
pip install -r requirements.txt

---

## Database Setup

1. Create a database manually (for example via MySQL Workbench):
    CREATE DATABASE crypto_data;

2. Update database credentials in config.py:
    DB_URL = "mysql+pymysql://user:password@localhost/crypto_data"

3. Create tables:
python create_db.py


---

## Future Improvements

Add more trading pairs

Add CLI arguments (--update, --symbol)

Logging and monitoring

Docker support

Data validation and gap detection

---

## Disclaimer

This project is for educational and research purposes only.
No financial advice is provided.

---

## License

MIT License