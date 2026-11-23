"""Turn ticks into 1-minute OHLCV bars."""
from dataclasses import dataclass

from backend.config import BAR_SECONDS

BAR_MS = BAR_SECONDS * 1000


@dataclass
class Bar:
    symbol: str
    start_ms: int  # start of the bar, milliseconds since 1970 (UTC)
    open: float
    high: float
    low: float
    close: float
    volume: float
    n_ticks: int


def bar_start(ts_ms, bar_ms=BAR_MS):
    """Round a timestamp down to the start of its bar."""
    return ts_ms - ts_ms % bar_ms


class BarBuilder:
    """Feed ticks in time order and get finished bars back."""

    def __init__(self, bar_ms=BAR_MS):
        self.bar_ms = bar_ms
        self._open_bars = {}  # symbol -> the Bar still being built

    def add(self, tick):
        """Add one tick.

        Returns the finished Bar if this tick started a new bar, otherwise None.
        """
        start = bar_start(tick.ts_ms, self.bar_ms)
        bar = self._open_bars.get(tick.symbol)

        # first tick for this symbol, or a new minute has begun
        if bar is None or start > bar.start_ms:
            self._open_bars[tick.symbol] = Bar(
                symbol=tick.symbol,
                start_ms=start,
                open=tick.price,
                high=tick.price,
                low=tick.price,
                close=tick.price,
                volume=tick.volume,
                n_ticks=1,
            )
            return bar  # the previous bar, now finished (None if there was none)

        # late tick that belongs to an older bar: ignore for now
        if start < bar.start_ms:
            return None

        # same minute: update the open bar
        bar.high = max(bar.high, tick.price)
        bar.low = min(bar.low, tick.price)
        bar.close = tick.price
        bar.volume += tick.volume
        bar.n_ticks += 1
        return None

    def flush_all(self):
        """Return and clear all unfinished bars (use when shutting down)."""
        bars = list(self._open_bars.values())
        self._open_bars.clear()
        return bars