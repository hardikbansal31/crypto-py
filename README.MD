# MCP Crypto Market Data Server

A lightweight, modular Python MCP server built with **FastAPI**, **CCXT**, and **Pytest**. It provides:

  * Real-time cryptocurrency prices
  * Historical OHLCV data
  * Exchange-normalized symbol handling
  * Error handling & validation
  * In-memory TTL caching
  * Unit tests for reliability

This project is built as part of an internship assignment and focuses on clean structure, correctness, and essential MCP features — without unnecessary complexity.

-----

### 🚀 Features

  * **✔ Real-time market data**
    Fetches live crypto prices using `CCXT`, supporting major exchanges like Binance, CoinbasePro, and Kraken.
  * **✔ Historical OHLCV data**
    Pulls candlestick data (1m, 5m, 1h, 1d etc.) with configurable limits.
  * **✔ TTL Cache**
    Improves performance by caching exchange responses for a short duration.
  * **✔ Robust error handling**
    Fails gracefully for:
      * invalid exchange
      * invalid trading pair (symbol)
      * unreachable API
      * malformed query parameters
  * **✔ Simple structure**
    Organized for clarity and easy extension with more exchanges or endpoints.
  * **✔ Full unit tests**
    Handlers, server routes, and utilities are tested with mocks — ensuring high reliability.

-----

### 💻 Key Dependencies

  * **FastAPI:** For the high-performance API.
  * **Uvicorn:** As the ASGI server.
  * **CCXT:** To connect to all crypto exchanges.
  * **Pytest:** For all unit and integration tests.
  * **Cachetools:** For the in-memory TTL cache.

-----

### 🗂 Project Structure

```
mcp-crypto-server/
├── README.md
├── requirements.txt
├── mcp_server/
│   ├── __init__.py
│   ├── server.py          # FastAPI app + route wiring
│   ├── handlers.py        # CCXT logic + business logic
│   ├── cache.py           # Tiny TTL cache
│   ├── exceptions.py      # Custom error classes
│   └── utils.py           # Normalization + validation helpers
└── tests/
    ├── test_handlers.py
    └── test_server.py
```

-----

### 🔧 Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/<your-username>/mcp-crypto-server.git
    cd mcp-crypto-server
    ```

2.  **Create a virtual environment**

    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment**

      * Windows (PowerShell):
        ```powershell
        .\.venv\Scripts\Activate
        ```
      * macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

-----

### ▶️ Running the Server

Use Uvicorn to start the server. The `--reload` flag will automatically restart the server when you make code changes.

```bash
python -m uvicorn mcp_server.server:app --reload --host 127.0.0.1 --port 8000
```

The server will be available at `http://127.0.0.1:8000`.

-----

### 📡 API Endpoints

#### 1\. Health Check

`GET /ping`

  * **Description:** Checks if the API is running.
  * **Response:**
    ```json
    { "status": "ok" }
    ```

#### 2\. Real-Time Price

`GET /price?exchange=binance&symbol=BTC/USDT`

  * **Description:** Gets the latest ticker price for a symbol on an exchange.
  * **Query Parameters:**
      * `exchange` (str, required): The exchange ID (e.g., `binance`).
      * `symbol` (str, required): The market symbol (e.g., `BTC/USDT`).
  * **Success Response (200):**
    ```json
    {
      "exchange": "binance",
      "symbol": "BTC/USDT",
      "price": 57382.15
    }
    ```
  * **Error Response (400):**
    ```json
    {
      "detail": "Invalid exchange"
    }
    ```

#### 3\. Historical OHLCV

`GET /ohlcv?exchange=binance&symbol=BTC/USDT&timeframe=5m&limit=50`

  * **Description:** Gets historical Open-High-Low-Close-Volume (candlestick) data.
  * **Query Parameters:**
      * `exchange` (str, required): The exchange ID.
      * `symbol` (str, required): The market symbol.
      * `timeframe` (str, optional): `1m`, `5m`, `1h`, `1d`, etc. (Default: `1m`).
      * `limit` (int, optional): Number of data points to return. (Default: `100`).
  * **Success Response (200):**
    ```json
    {
      "exchange": "binance",
      "symbol": "BTC/USDT",
      "data": [
        [1636992000000, 57382.15, 57400.00, 57380.00, 57390.50, 10.5],
        [1636992060000, 57390.50, 57410.20, 57390.00, 57405.10, 12.2],
        ...
      ]
    }
    ```

-----

### 🧪 Running Tests

The project uses `pytest` and `unittest.mock` to test the application in isolation. Tests are located in the `tests/` directory.

The test suite mocks all outbound calls to the `ccxt` library. This allows for fast, reliable testing of the application's core logic, including:

  * Handler and utility function correctness.
  * API route status codes and responses.
  * Correct handling of custom exceptions (e.g., `InvalidSymbolError`).

To run all tests, simply execute:

```bash
pytest -q
```

-----

### 📝 Assumptions

  * Default timeframe for OHLCV is **1m** unless specified.
  * Symbols are normalized to `BASE/QUOTE` format (e.g., `BTC/USDT`).
  * TTL cache uses a small expiration (5 seconds) suitable for crypto tickers.

-----

### 🌱 Extending the Project

You can easily add:

  * More exchanges (by updating `ccxt` config if needed).
  * WebSocket real-time streaming for prices.
  * More advanced caching (e.g., Redis).
  * API key management and rate limiting.