from .utils import logger, validate_input

def execute_limit_order(client, symbol, side, quantity, price):
    try:
        validate_input(symbol, quantity, side, price)
        response = client.place_futures_order(
            symbol=symbol,
            side=side,
            order_type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'  # Good 'Til Cancelled
        )
        return response
    except Exception as e:
        logger.error(f"Limit order failed: {str(e)}")
        return None
