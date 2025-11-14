import ccxt

from .cache import get_cached, set_cached
from .utils import normalize_symbol, normalize_exchange
from .exceptions import ExchangeError


def _load_exchange(exchange_id: str):
    try:
        ex_class = getattr(ccxt, exchange_id)
        return ex_class({})
    except Exception:
        raise ExchangeError(f"Unknown or unsupported exchange '{exchange_id}'")


def get_ticker(exchange: str, symbol: str):
    exchange_id = normalize_exchange(exchange)
    symbol_n = normalize_symbol(symbol)

    cache_key = f"ticker:{exchange_id}:{symbol_n}"
    cached = get_cached(cache_key)
    if cached:
        return {"from_cache": True, **cached}

    ex = _load_exchange(exchange_id)
    try:
        ticker = ex.fetch_ticker(symbol_n)
    except Exception as e:
        raise ExchangeError(f"failed to fetch ticker: {e}")

    result = {
        "symbol": symbol_n,
        "timestamp": ticker.get("timestamp"),
        "datetime": ticker.get("datetime"),
        "last": ticker.get("last"),
        "high": ticker.get("high"),
        "low": ticker.get("low"),
        "bid": ticker.get("bid"),
        "ask": ticker.get("ask"),
        "info": ticker.get("info", {}),
    }

    set_cached(cache_key, result)
    return {"from_cache": False, **result}


def get_ohlcv(exchange: str, symbol: str, since: int = None, limit: int = 100):
    exchange_id = normalize_exchange(exchange)
    symbol_n = normalize_symbol(symbol)

    cache_key = f"ohlcv:{exchange_id}:{symbol_n}:{since}:{limit}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    ex = _load_exchange(exchange_id)
    try:
        ohlcv = ex.fetch_ohlcv(symbol_n, timeframe="1m", since=since, limit=limit)
    except Exception as e:
        raise ExchangeError(f"failed to fetch ohlcv: {e}")

    set_cached(cache_key, ohlcv)
    return ohlcv
