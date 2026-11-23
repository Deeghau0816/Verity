"""Central config: tickers, paths, bar settings."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # reads FINNHUB_API_KEY from the .env file

# Stocks we watch. NVDA is our example.
TICKERS = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META",
           "TSLA", "AMD", "AVGO", "JPM", "XOM", "NFLX"]

# Market and sector funds. They tell us if a dip is market-wide or just one stock.
CONTEXT_TICKERS = ["QQQ", "SPY", "SMH"]

ALL_SYMBOLS = TICKERS + CONTEXT_TICKERS

BAR_SECONDS = 60                # 1-minute bars
BACKFILL_START = "2018-01-01"   # includes the 2020 crash and 2022 rate hikes

# Where data is saved
DATA_DIR = Path(os.getenv("VERITY_DATA_DIR", "./data_store")).resolve()
TICKS_DIR = DATA_DIR / "ticks"
BARS_DIR = DATA_DIR / "bars"
DAILY_DIR = DATA_DIR / "daily"

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
FINNHUB_WS_URL = "wss://ws.finnhub.io"