from binance import Client
from .utils import logger

class BinanceClient:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client = Client(api_key, api_secret, testnet=testnet)
        
        if testnet:
            # For Futures Testnet, we often need to set the base URL explicitly if not handled by the lib
            # However, python-binance's Client handles testnet parameter for Futures too in recent versions.
            # We will use the Futures specific methods.
            pass
        
        logger.info(f"Binance Client initialized (Testnet: {testnet})")

    def place_futures_order(self, symbol, side, order_type, quantity, price=None, **kwargs):
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }
            if price:
                params['price'] = price
            
            params.update(kwargs)
            
            # Log order request with details
            price_info = f" @ ${price}" if price else " at market price"
            logger.info(f"[ORDER REQUEST] {side} {quantity} {symbol} ({order_type}){price_info}")
            
            response = self.client.futures_create_order(**params)
            
            # Log successful order with important details
            order_id = response.get('orderId')
            status = response.get('status', 'UNKNOWN')
            executed_qty = response.get('executedQty', quantity)
            logger.info(f"[ORDER SUCCESS] ID={order_id} | Status={status} | Executed={executed_qty} {symbol}")
            
            return response
        except Exception as e:
            logger.error(f"[ORDER FAILED] {side} {quantity} {symbol} - {str(e)}")
            raise e

    def get_futures_account_balance(self):
        try:
            return self.client.futures_account_balance()
        except Exception as e:
            logger.error(f"Error fetching account balance: {str(e)}")
            raise e
