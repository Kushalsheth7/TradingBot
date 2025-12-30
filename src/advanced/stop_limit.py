from ..utils import logger, validate_input

def execute_stop_limit_order(client, symbol, side, quantity, price, stop_price):
    try:
        validate_input(symbol, quantity, side, price)
        if stop_price <= 0:
            raise ValueError("Stop price must be greater than 0")
            
        response = client.place_futures_order(
            symbol=symbol,
            side=side,
            order_type='STOP',
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            timeInForce='GTC'
        )
        return response
    except Exception as e:
        logger.error(f"Stop-Limit order failed: {str(e)}")
        return None
