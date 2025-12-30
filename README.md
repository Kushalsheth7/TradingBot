# Binance Futures Trading Bot

A CLI-based trading bot for Binance USDT-M Futures that supports multiple order types with robust logging and validation.

## Features
- **Market Orders**: Buy or Sell at current market price.
- **Limit Orders**: Buy or Sell at a specific price.
- **Stop-Limit Orders**: Trigger a limit order when a stop price is hit.
- **OCO (One-Cancels-the-Other)**: Simulated OCO strategy using Take Profit and Stop Loss orders.
- **Robust Logging**: All actions and errors are logged to `bot.log`.
- **Environment Driven**: API keys are securely loaded from a `.env` file.
- **Web UI**: Modern web interface with glassmorphism design.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   Copy `.env.example` to `.env` and fill in your Binance API credentials.
   ```bash
   cp .env.example .env
   ```
   Ensure `USE_TESTNET=True` if you are using the Binance Futures Testnet.

## Usage

### CLI Mode

Run the bot using `main.py` with the required arguments.

**Market Order**:
```bash
python main.py BTCUSDT BUY MARKET 0.001
```

**Limit Order**:
```bash
python main.py BTCUSDT SELL LIMIT 0.001 --price 60000
```

**Stop-Limit Order**:
```bash
python main.py BTCUSDT BUY STOP_LIMIT 0.001 --price 61000 --stop_price 60500
```

**OCO Order**:
```bash
python main.py BTCUSDT SELL OCO 0.001 --price 65000 --stop_price 59000 --stop_limit_price 58500
```

### Web UI (Bonus)

For a user-friendly web interface, run the Flask server:

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

The web interface provides:
- Beautiful modern UI with dark mode and glassmorphism
- Interactive order form with dynamic fields based on order type
- Real-time log viewer
- Order status tracking

## Project Structure
- `src/`: Core source code.
  - `client.py`: API client wrapper.
  - `market_orders.py`: Market order logic.
  - `limit_orders.py`: Limit order logic.
  - `utils.py`: Logging and validation.
  - `advanced/`: Bonus order types (Stop-Limit, OCO).
- `main.py`: CLI entry point.
- `app.py`: Web UI Flask server.
- `static/`: Web interface files (HTML, CSS, JS).
- `bot.log`: Log file for tracking executions.
