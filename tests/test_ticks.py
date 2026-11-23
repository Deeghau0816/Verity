from backend.data.ticks import parse_trade_message


def test_parses_trade_message():
    msg = {"type": "trade",
           "data": [{"c": ["1"], "p": 225.4, "s": "AAPL", "t": 1763650000000, "v": 10}]}
    ticks = parse_trade_message(msg, recv_ms=1763650000100)
    assert len(ticks) == 1
    assert ticks[0].symbol == "AAPL"
    assert ticks[0].price == 225.4
    assert ticks[0].volume == 10.0
    assert ticks[0].recv_ms == 1763650000100


def test_ping_gives_no_ticks():
    assert parse_trade_message({"type": "ping"}) == []