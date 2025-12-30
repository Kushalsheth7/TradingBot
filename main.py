import argparse
import sys
from src.client import BinanceClient
from src.utils import logger, load_env_vars
from src.market_orders import execute_market_order
from src.limit_orders import execute_limit_order
from src.advanced.stop_limit import execute_stop_limit_order
from src.advanced.oco import execute_oco_order

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI")
    
    parser.add_argument("symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("type", choices=["MARKET", "LIMIT", "STOP_LIMIT", "OCO"], help="Order type")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Limit price (required for LIMIT, STOP_LIMIT, OCO)")
    parser.add_argument("--stop_price", type=float, help="Stop price (required for STOP_LIMIT, OCO)")
    parser.add_argument("--stop_limit_price", type=float, help="Stop limit price (required for OCO)")

    args = parser.parse_args()

    try:
        api_key, api_secret, use_testnet = load_env_vars()
        client = BinanceClient(api_key, api_secret, testnet=use_testnet)

        if args.type == "MARKET":
            execute_market_order(client, args.symbol, args.side, args.quantity)
        elif args.type == "LIMIT":
            if not args.price:
                print("Error: --price is required for LIMIT orders")
                return
            execute_limit_order(client, args.symbol, args.side, args.quantity, args.price)
        elif args.type == "STOP_LIMIT":
            if not args.price or not args.stop_price:
                print("Error: --price and --stop_price are required for STOP_LIMIT orders")
                return
            execute_stop_limit_order(client, args.symbol, args.side, args.quantity, args.price, args.stop_price)
        elif args.type == "OCO":
            if not args.price or not args.stop_price or not args.stop_limit_price:
                print("Error: --price, --stop_price, and --stop_limit_price are required for OCO orders")
                return
            execute_oco_order(client, args.symbol, args.side, args.quantity, args.price, args.stop_price, args.stop_limit_price)

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
