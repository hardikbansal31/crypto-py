from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ohlcv")
def ohlcv(
    exchange: str = Query(...),
    symbol: str = Query(...),
    since: int = Query(None),
    limit: int = Query(100)
):
    try:
        data = get_ohlcv(exchange, symbol, since=since, limit=limit)
        return {"ohlcv": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
