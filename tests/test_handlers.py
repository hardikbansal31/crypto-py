import pytest

from mcp_server.handlers import get_ticker, get_ohlcv
from mcp_server.cache import set_cached


def test_get_ticker_invalid_exchange():
    with pytest.raises(Exception):
        get_ticker("invalid_exchange", "BTC/USDT")


def test_get_ticker_cache(monkeypatch):
    class DummyEx:
        def fetch_ticker(self, symbol):
            return {
                "timestamp": 123,
                "datetime": "2020-01-01T00:00:00",
                "last": 100
            }

    import ccxt
    monkeypatch.setattr(ccxt, "binance", lambda params: DummyEx())

    # first call — not from cache
    res = get_ticker("binance", "btc/usdt")
    assert res["last"] == 100
    assert res["from_cache"] is False

    # second call — from cache
    res2 = get_ticker("binance", "btc/usdt")
    assert res2["from_cache"] is True


def test_get_ohlcv_invalid_symbol():
    with pytest.raises(Exception):
        get_ohlcv("binance", "BADSYMBOL")
