# mcp_server/server.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .exceptions import InvalidExchangeError, InvalidSymbolError
from .handlers import get_ticker, get_ohlcv

app = FastAPI(title="MCP Crypto Server - Minimal")


class TickerQuery(BaseModel):
    exchange: str
    symbol: str


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/price")
def price(
    exchange: str = Query(...),
    symbol: str = Query(...)
):
    try:
        data = get_ticker(exchange, symbol)
        return data
    except (InvalidExchangeError, InvalidSymbolError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ohlcv")
def ohlcv_route(exchange: str = Query(...), symbol: str = Query(...), timeframe: str = Query("1m"), limit: int = Query(100)):
    try:
        data = get_ohlcv(exchange, symbol, timeframe, limit)
        return data
    except (InvalidExchangeError, InvalidSymbolError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
