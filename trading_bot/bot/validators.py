"""Validation utilities (placeholder).
"""

def validate_symbol(symbol: str) -> bool:
    return isinstance(symbol, str) and len(symbol) > 0

def validate_positive_number(value) -> bool:
    try:
        return float(value) > 0
    except Exception:
        return False
    
def validate_order(symbol, side, order_type, quantity, price):
    if not symbol:
        raise ValueError("Symbol is required")

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Invalid order type")

    if float(quantity) <= 0:
        raise ValueError("Quantity must be greater than 0")

    if order_type == "LIMIT" and price is None:
        raise ValueError("Price is required for LIMIT order")