from .utils import logger, validate_input

def execute_market_order(client, symbol, side, quantity):
    try:
        validate_input(symbol, quantity, side)
        response = client.place_futures_order(
            symbol=symbol,
            side=side,
            order_type='MARKET',
            quantity=quantity
        )
        return response
    except Exception as e:
        logger.error(f"Market order failed: {str(e)}")
        return None
