import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from mcp_server.server import app


client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("mcp_server.handlers.ccxt")
def test_price_route_success(mock_ccxt):    
    mock_exchange = Mock()
    mock_exchange.fetch_ticker.return_value = {"last": 35000}
    mock_ccxt.binance.return_value = mock_exchange

    response = client.get("/price?exchange=binance&symbol=BTC/USDT")
    body = response.json()

    assert response.status_code == 200
    assert body["price"] == 35000


# tests/test_server.py

# tests/test_server.py

@patch("mcp_server.handlers.ccxt")
def test_price_route_invalid_exchange(mock_ccxt):
    # This one line correctly simulates a missing exchange
    setattr(mock_ccxt, 'invalidex', None)
    
    # REMOVE this line, it caused the AttributeError:
    # mock_ccxt.__dict__.get.return_value = None

    response = client.get("/price?exchange=invalidex&symbol=BTC/USDT")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid exchange"




@patch("mcp_server.handlers.ccxt")
def test_ohlcv_route_success(mock_ccxt):
    mock_exchange = Mock()
    mock_exchange.fetch_ohlcv.return_value = [
        [1000, 1, 2, 0.5, 1.5, 1000]
    ]
    mock_ccxt.binance.return_value = mock_exchange

    response = client.get("/ohlcv?exchange=binance&symbol=BTC/USDT&limit=1")
    body = response.json()

    assert response.status_code == 200
    assert len(body["data"]) == 1


@patch("mcp_server.handlers.ccxt")
def test_ohlcv_route_invalid_symbol(mock_ccxt):
    mock_exchange = Mock()
    mock_exchange.fetch_ohlcv.side_effect = Exception("invalid symbol")
    mock_ccxt.binance.return_value = mock_exchange

    response = client.get("/ohlcv?exchange=binance&symbol=BAD")
    assert response.status_code == 400
    assert "invalid symbol" in response.json()["detail"].lower()
