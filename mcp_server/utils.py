from .exceptions import InvalidParameter


def normalize_symbol(symbol: str) -> str:
    if not symbol or "/" not in symbol:
        raise InvalidParameter("symbol must be in the form BTC/USDT")
    return symbol.strip().upper()


def normalize_exchange(exchange: str) -> str:
    if not exchange:
        raise InvalidParameter("exchange is required")
    return exchange.strip().lower()
