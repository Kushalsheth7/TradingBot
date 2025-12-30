from ..utils import logger, validate_input

def execute_oco_order(client, symbol, side, quantity, price, stop_price, stop_limit_price):
    """
    Binance Futures does not have a native OCO order type like Spot.
    We simulate it by placing a Take Profit and Stop Loss order.
    Note: In a real bot, we'd need to monitor and cancel the other if one fills.
    """
    try:
        validate_input(symbol, quantity, side, price)
        
        logger.info(f"Placing OCO-simulated orders for {symbol}")
        
        # 1. Take Profit Limit
        tp_side = "SELL" if side == "BUY" else "BUY"
        tp_order = client.place_futures_order(
            symbol=symbol,
            side=tp_side,
            order_type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        
        # 2. Stop Loss Limit
        sl_order = client.place_futures_order(
            symbol=symbol,
            side=tp_side,
            order_type='STOP',
            quantity=quantity,
            price=stop_limit_price,
            stopPrice=stop_price,
            timeInForce='GTC'
        )
        
        logger.info(f"OCO orders placed: TP Order {tp_order.get('orderId')}, SL Order {sl_order.get('orderId')}")
        return {"tp_order": tp_order, "sl_order": sl_order}
        
    except Exception as e:
        logger.error(f"OCO order failed: {str(e)}")
        return None
