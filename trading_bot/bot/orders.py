"""Order-related helpers (placeholder).
"""

def place_market_order(symbol: str, side: str, quantity: float):
    """Placeholder for placing a market order."""
    return {"symbol": symbol, "side": side, "quantity": quantity, "status": "simulated"}

import logging

def place_order(client, symbol, side, order_type, quantity, price=None):
    try:
        logging.info(f"Placing order: {symbol} {side} {order_type} {quantity}")

        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )

        elif order_type == "LIMIT":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

        logging.info(f"Order Response: {order}")
        return order

    except Exception as e:
        logging.error(f"Error placing order: {str(e)}")
        raise