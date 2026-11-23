"""Connect to Finnhub's WebSocket and print live trade ticks."""
import asyncio
import json
import sys

import websockets

from backend.config import ALL_SYMBOLS, FINNHUB_API_KEY, FINNHUB_WS_URL
from backend.data.ticks import parse_trade_message

SHOW_RAW_FIRST = 5  # print the first few raw messages so we can see what the server sends


async def stream_ticks(symbols):
    url = f"{FINNHUB_WS_URL}?token={FINNHUB_API_KEY}"
    async with websockets.connect(url) as ws:
        for symbol in symbols:
            await ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))
        print(f"Subscribed to {len(symbols)} symbols. Waiting for trades...")

        seen = 0
        async for raw in ws:
            seen += 1
            if seen <= SHOW_RAW_FIRST:
                print("RAW:", raw[:200])
            msg = json.loads(raw)
            for tick in parse_trade_message(msg):
                lag_ms = tick.recv_ms - tick.ts_ms
                print(f"{tick.symbol:8} {tick.price:>10.2f}  vol={tick.volume:<10} lag={lag_ms}ms")


if __name__ == "__main__":
    if not FINNHUB_API_KEY:
        raise SystemExit("FINNHUB_API_KEY is missing. Put it in .env")
    # Crypto trades 24/7, so --crypto lets us test when US stocks are closed
    symbols = ["BINANCE:BTCUSDT"] if "--crypto" in sys.argv else ALL_SYMBOLS
    try:
        asyncio.run(stream_ticks(symbols))
    except websockets.ConnectionClosed as e:
        print("Connection closed:", e)
    except KeyboardInterrupt:
        print("\nStopped.")