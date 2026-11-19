"""A trade tick, plus a simple store that saves ticks to Parquet files."""
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Tick:
    symbol: str       # e.g. "NVDA"
    ts_ms: int        # trade time, milliseconds since 1970 (UTC), from the exchange
    price: float
    volume: float
    recv_ms: int = 0  # when WE received it; later used to measure feed delay


class TickStore:
    """Collects ticks in memory and writes them to disk in batches."""

    def __init__(self, root, flush_every=5000):
        self.root = Path(root)
        self.flush_every = flush_every
        self._buf = []
        self._part = 0

    def add(self, tick):
        self._buf.append(tick)
        if len(self._buf) >= self.flush_every:
            self.flush()

    def flush(self):
        if not self._buf:
            return
        df = pd.DataFrame({
            "symbol": [t.symbol for t in self._buf],
            "ts_ms": [t.ts_ms for t in self._buf],
            "price": [t.price for t in self._buf],
            "volume": [t.volume for t in self._buf],
            "recv_ms": [t.recv_ms for t in self._buf],
        })
        # one folder per day: date=2026-11-20
        df["date"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True).dt.strftime("%Y-%m-%d")
        for date, part in df.groupby("date"):
            folder = self.root / f"date={date}"
            folder.mkdir(parents=True, exist_ok=True)
            stamp = int(datetime.now(timezone.utc).timestamp() * 1000)
            part.drop(columns="date").to_parquet(folder / f"part-{stamp}-{self._part}.parquet", index=False)
            self._part += 1
        self._buf.clear()


def read_ticks(root):
    """Read all saved ticks back, sorted by trade time."""
    frames = [pd.read_parquet(f) for f in sorted(Path(root).glob("date=*/*.parquet"))]
    if not frames:
        return pd.DataFrame(columns=["symbol", "ts_ms", "price", "volume", "recv_ms"])
    df = pd.concat(frames, ignore_index=True)
    return df.sort_values(["ts_ms", "symbol"], kind="stable").reset_index(drop=True)