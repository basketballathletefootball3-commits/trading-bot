"""Input validation for trading bot."""

import logging
from typing import Tuple

logger = logging.getLogger("trading_bot")

# Valid order sides
VALID_SIDES = ["BUY", "SELL"]

# Valid order types
VALID_ORDER_TYPES = ["MARKET", "LIMIT"]

# Minimum/Maximum constraints
MIN_QUANTITY = 0.001
MAX_QUANTITY = 10000
MIN_PRICE = 0.01
MAX_PRICE = 1000000


def validate_symbol(symbol: str) -> Tuple[bool, str]:
    """Validate trading symbol format.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not symbol:
        return False, "Symbol cannot be empty"
    
    symbol = symbol.upper().strip()
    
    if len(symbol) < 6:
        return False, f"Symbol '{symbol}' too short. Expected format: BTCUSDT"
    
    if not symbol.isalnum():
        return False, f"Symbol '{symbol}' contains invalid characters. Only alphanumeric allowed"
    
    # Check if it ends with a valid quote asset
    valid_quotes = ["USDT", "BUSD", "USDC", "TUSD"]
    has_valid_quote = any(symbol.endswith(quote) for quote in valid_quotes)
    
    if not has_valid_quote:
        return False, f"Symbol '{symbol}' should end with USDT, BUSD, USDC, or TUSD"
    
    return True, ""


def validate_side(side: str) -> Tuple[bool, str]:
    """Validate order side (BUY or SELL).
    
    Args:
        side: Order side
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not side:
        return False, "Side cannot be empty"
    
    side = side.upper().strip()
    
    if side not in VALID_SIDES:
        return False, f"Invalid side '{side}'. Must be {' or '.join(VALID_SIDES)}"
    
    return True, ""


def validate_order_type(order_type: str) -> Tuple[bool, str]:
    """Validate order type (MARKET or LIMIT).
    
    Args:
        order_type: Order type
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not order_type:
        return False, "Order type cannot be empty"
    
    order_type = order_type.upper().strip()
    
    if order_type not in VALID_ORDER_TYPES:
        return False, f"Invalid order type '{order_type}'. Must be {' or '.join(VALID_ORDER_TYPES)}"
    
    return True, ""


def validate_quantity(quantity: float) -> Tuple[bool, str]:
    """Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if quantity is None:
        return False, "Quantity cannot be empty"
    
    try:
        quantity = float(quantity)
    except (ValueError, TypeError):
        return False, f"Invalid quantity '{quantity}'. Must be a number"
    
    if quantity <= 0:
        return False, f"Quantity must be positive, got {quantity}"
    
    if quantity < MIN_QUANTITY:
        return False, f"Quantity {quantity} is below minimum {MIN_QUANTITY}"
    
    if quantity > MAX_QUANTITY:
        return False, f"Quantity {quantity} exceeds maximum {MAX_QUANTITY}"
    
    return True, ""


def validate_price(price: float) -> Tuple[bool, str]:
    """Validate order price.
    
    Args:
        price: Order price
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if price is None:
        return False, "Price cannot be empty"
    
    try:
        price = float(price)
    except (ValueError, TypeError):
        return False, f"Invalid price '{price}'. Must be a number"
    
    if price <= 0:
        return False, f"Price must be positive, got {price}"
    
    if price < MIN_PRICE:
        return False, f"Price {price} is below minimum {MIN_PRICE}"
    
    if price > MAX_PRICE:
        return False, f"Price {price} exceeds maximum {MAX_PRICE}"
    
    return True, ""


def validate_limit_order_params(
    symbol: str, side: str, order_type: str, quantity: float, price: float = None
) -> Tuple[bool, str]:
    """Validate all order parameters together.
    
    Args:
        symbol: Trading symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate symbol
    valid, msg = validate_symbol(symbol)
    if not valid:
        return False, msg
    
    # Validate side
    valid, msg = validate_side(side)
    if not valid:
        return False, msg
    
    # Validate order type
    valid, msg = validate_order_type(order_type)
    if not valid:
        return False, msg
    
    # Validate quantity
    valid, msg = validate_quantity(quantity)
    if not valid:
        return False, msg
    
    # Validate price for LIMIT orders
    if order_type.upper() == "LIMIT":
        if price is None:
            return False, "Price is required for LIMIT orders"
        valid, msg = validate_price(price)
        if not valid:
            return False, msg
    
    return True, ""
