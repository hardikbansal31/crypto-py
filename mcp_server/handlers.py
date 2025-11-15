# mcp_server/handlers.py
from .cache import get_cached, set_cached
import ccxt
from .utils import normalize_exchange, normalize_symbol
from .exceptions import InvalidExchangeError, InvalidSymbolError, ExchangeError


def _load_exchange(exchange_id: str):
    ex_class = getattr(ccxt, exchange_id, None)

    if ex_class is None:
        try:
            ex_class = ccxt.__dict__.get(exchange_id)
        except Exception:
            ex_class = None

    if ex_class is None:
        raise InvalidExchangeError("Invalid exchange")

    try:
        return ex_class()
    except Exception:
        return ex_class


def get_price(exchange: str, symbol: str):
    exchange_id = normalize_exchange(exchange)
    symbol_n = normalize_symbol(symbol)

    ex = _load_exchange(exchange_id)

    try:
        ticker = ex.fetch_ticker(symbol_n)
    except Exception as e:
        raise InvalidSymbolError(str(e))

    return {
        "exchange": exchange_id,
        "symbol": symbol_n,
        "price": ticker.get("last"),
    }


def get_ticker(exchange: str, symbol: str):
    return get_price(exchange, symbol)


def get_ohlcv(exchange: str, symbol: str, timeframe: str = "1m", limit: int = 100):
    exchange_id = normalize_exchange(exchange)
    symbol_n = normalize_symbol(symbol)

    cache_key = f"ohlcv:{exchange_id}:{symbol_n}:{timeframe}:{limit}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    ex = _load_exchange(exchange_id)
    try:
        ohlcv = ex.fetch_ohlcv(symbol_n, timeframe=timeframe, limit=limit)
    except Exception as e:
        raise InvalidSymbolError(str(e))

    result = {"exchange": exchange_id, "symbol": symbol_n, "data": ohlcv}
    set_cached(cache_key, result)
    return result
