from .exceptions import InvalidExchangeError, InvalidSymbolError


def normalize_exchange(exchange: str) -> str:
    if not exchange:
        raise InvalidExchangeError("Exchange cannot be empty")

    ex = exchange.lower().strip()

    if not ex.isalpha():
        raise InvalidExchangeError(f"Invalid exchange '{exchange}'")

    return ex


def normalize_symbol(symbol: str) -> str:
    if not symbol:
        raise InvalidSymbolError("Symbol cannot be empty")

    sym = symbol.upper().strip()

    if "/" not in sym:
        raise InvalidSymbolError(f"Invalid symbol '{symbol}'. Expected format BASE/QUOTE like BTC/USDT")

    return sym
