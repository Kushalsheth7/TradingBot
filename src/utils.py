import logging
import os
from dotenv import load_dotenv

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def load_env_vars():
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    use_testnet = os.getenv("USE_TESTNET", "True").lower() == "true"
    
    if not api_key or not api_secret:
        logger.error("API Key or Secret missing in .env file")
        raise ValueError("API Key or Secret missing in .env file")
        
    return api_key, api_secret, use_testnet

def validate_input(symbol, quantity, side, price=None):
    if not symbol:
        raise ValueError("Symbol is required")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if price is not None and price <= 0:
        raise ValueError("Price must be greater than 0")
    return True
