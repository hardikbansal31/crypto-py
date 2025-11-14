# **MCP Crypto Market Data Server**

A lightweight, modular **Python MCP server** that provides:

* **Real-time cryptocurrency prices**
* **Historical OHLCV data**
* **Exchange-normalized symbol handling**
* **Error handling & validation**
* **In-memory TTL caching**
* **FastAPI-based API endpoints**
* **Unit tests for reliability**

This project is built as part of the internship assignment and focuses on clean structure, correctness, and essential MCP features — without unnecessary complexity.

---

## 🚀 **Features**

### ✔ Real-time market data

Fetches live crypto prices using **CCXT**, supporting major exchanges like Binance, CoinbasePro, and Kraken.

### ✔ Historical OHLCV data

Pulls candlestick data (1m, 5m, 1h, 1d etc.) with configurable limits.

### ✔ TTL Cache

Improves performance by caching exchange responses for a short duration.

### ✔ Robust error handling

Fails gracefully for:

* invalid exchange
* invalid trading pair (symbol)
* unreachable API
* malformed query parameters

### ✔ Simple structure

Organized for clarity and easy extension with more exchanges or endpoints.

### ✔ Full unit tests

Handlers, server routes, and utilities are tested with mocks — ensuring high reliability.

---

## 🗂 **Project Structure**

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

---

## 🔧 **Installation**

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/mcp-crypto-server.git
cd mcp-crypto-server
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ **Running the Server**

Use Uvicorn to start:

```bash
python -m uvicorn mcp_server.server:app --reload --host 127.0.0.1 --port 8000
```

---

## 📡 **API Endpoints**

### **1. Health Check**

```
GET /ping
```

Response:

```json
{ "status": "ok" }
```

---

### **2. Real-Time Price**

```
GET /price?exchange=binance&symbol=BTC/USDT
```

Response:

```json
{
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "price": 57382.15
}
```

---

### **3. Historical OHLCV**

```
GET /ohlcv?exchange=binance&symbol=BTC/USDT&limit=50
```

Response:

```json
{
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "timeframe": "1m",
  "data": [...]
}
```

---

## 🧪 **Running Tests**

Install pytest (already in requirements) and run:

```bash
pytest -q
```

Tests include:

* handler logic
* error cases
* server routes
* ccxt mock responses

---

## 📝 **Assumptions**

* Default timeframe is **1m** unless specified.
* Symbols are normalized to `BASE/QUOTE` format.
* TTL cache uses small expiration (5–10 seconds) suitable for crypto tickers.
* Only widely used exchanges are supported (Binance, Kraken, Coinbase Pro etc.).

---

## 🌱 **Extending the Project**

You can easily add:

* more exchanges
* WebSocket real-time streaming
* rate limiting
* Redis/memory caching
* additional MCP tools

## 📬 **Submission**

This project is developed for the internship coding assignment.
Upload to GitHub and share the repository link by **Nov 16, 2025**.

