import pytest
from unittest.mock import Mock, patch
from mcp_server.handlers import get_price, get_ohlcv
from mcp_server.exceptions import InvalidExchangeError, InvalidSymbolError
from unittest.mock import Mock

@patch("mcp_server.handlers.ccxt")
def test_get_price_success(mock_ccxt):
    mock_exchange = Mock()
    mock_exchange.fetch_ticker.return_value = {"last": 30000}

    mock_ccxt.binance.return_value = mock_exchange

    result = get_price("binance", "BTC/USDT")

    assert result["exchange"] == "binance"
    assert result["symbol"] == "BTC/USDT"
    assert result["price"] == 30000


@patch("mcp_server.handlers.ccxt")
def test_get_price_invalid_exchange(mock_ccxt):
    setattr(mock_ccxt, 'invalidex', None)


    from mcp_server.handlers import get_price
    with pytest.raises(InvalidExchangeError):
        get_price("invalidex", "BTC/USDT")


@patch("mcp_server.handlers.ccxt")
def test_get_price_invalid_symbol(mock_ccxt):
    mock_exchange = Mock()
    mock_exchange.fetch_ticker.side_effect = Exception("bad symbol")

    mock_ccxt.binance.return_value = mock_exchange

    with pytest.raises(InvalidSymbolError):
        get_price("binance", "INVALID")


@patch("mcp_server.handlers.ccxt")
def test_get_ohlcv_success(mock_ccxt):
    mock_exchange = Mock()
    mock_exchange.fetch_ohlcv.return_value = [
        [1000, 1, 2, 0.5, 1.5, 1000]
    ]

    mock_ccxt.binance.return_value = mock_exchange

    result = get_ohlcv("binance", "BTC/USDT", "1m", 1)

    assert result["exchange"] == "binance"
    assert result["symbol"] == "BTC/USDT"
    assert result["data"][0][1] == 1  # open price 


@patch("mcp_server.handlers.ccxt")
def test_get_ohlcv_invalid_symbol(mock_ccxt):
    mock_exchange = Mock()
    mock_exchange.fetch_ohlcv.side_effect = Exception("no such pair")

    mock_ccxt.binance.return_value = mock_exchange

    with pytest.raises(InvalidSymbolError):
        get_ohlcv("binance", "INVALID", "1m", 10)
