# Binance Futures Testnet Trading Bot

## Overview

This is a Python command-line application that places BUY and SELL orders on the Binance USDT-M Futures Testnet.

The application supports both Market and Limit orders. The code is organized into separate modules for client setup, input validation, order execution and logging to keep it simple and maintainable.

## Features

- Place Market orders
- Place Limit orders
- BUY and SELL support
- Input validation before API requests
- Secure API key management using `.env`
- Logging of requests, responses and errors
- Secret redaction in log files
- Exception handling for invalid input, API errors and network errors

## Project Structure

```
binance-futures-testnet-trading-bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│
├── sample_logs/
│   ├── market_order.log
│   └── limit_order.log
│
├── cli.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Requirements

- Python 3.10 or later
- Binance Futures Testnet account
- Binance Futures Testnet API Key and Secret

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd binance-futures-testnet-trading-bot
```

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Binance Futures Testnet Setup

1. Create a Binance Futures Testnet account.
2. Generate a Testnet API Key and Secret.
3. Create a `.env` file in the project root.
4. Add your credentials.

Example:

```env
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
TEST_MODE=true
```

## Running the Application

### Place a Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a Limit Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000
```

## Sample Output

### Market Order

```
========== REQUEST ==========
Symbol   : BTCUSDT
Side     : BUY
Type     : MARKET
Quantity : 0.001
=============================

========== RESPONSE ==========
Order ID       : 18545708075
Status         : FILLED
Executed Qty   : 0.0010
Executed Price : Market Price
==============================

Order placed successfully.
```

### Limit Order

```
========== REQUEST ==========
Symbol   : BTCUSDT
Side     : BUY
Type     : LIMIT
Quantity : 0.001
Price    : 50000
=============================

========== RESPONSE ==========
Order ID       : 18543782776
Status         : NEW
Executed Qty   : 0.0000
Executed Price : 50000.00
==============================

Order placed successfully.
```

## Logging

All requests, responses and errors are written to:

```
logs/trading_bot.log
```

Sample log files for one successful Market order and one successful Limit order are included in the `sample_logs` folder.

Sensitive information such as API keys and secrets is automatically redacted before writing logs.

## Security

- API credentials are loaded from environment variables.
- API keys are never hardcoded.
- Secrets are removed from log files.
- User input is validated before API requests.
- API requests use explicit timeouts.
- The application is configured to use Binance Futures Testnet only.

**Note:** This project is intended for Binance Futures Testnet only. Before using it with a live trading account, additional security measures such as secure secret management, IP whitelisting and restricted API permissions should be implemented.

## Assumptions

- A Binance Futures Testnet account is available.
- Valid Testnet API credentials are configured in the `.env` file.
- The Testnet account has sufficient virtual funds.
- Internet connectivity is available while placing orders.

## Dependencies

- python-binance
- python-dotenv
- requests

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Author

Minal Chaudhari