"""
Input validation for trading bot operations.
Validates symbol, side, order type, quantity, and price parameters.
"""

from typing import Dict, Any, Tuple, Optional
import re

# Validation constants
MIN_QUANTITY = 0.001
MAX_QUANTITY = 1000.0

MIN_PRICE = 0.01
MAX_PRICE = 1000000.0

VALID_SYMBOLS = {
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOTUSDT",
    "AVAXUSDT",
}

VALID_SIDES = {"BUY", "SELL"}

VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> Tuple[bool, str]:
    """Validate trading symbol."""

    if not symbol:
        return False, "Symbol cannot be empty"

    symbol = symbol.upper().strip()

    if not re.match(r"^[A-Z]{2,20}USDT$", symbol):
        return False, "Symbol must be in format XXXUSDT (e.g. BTCUSDT)"

    if symbol not in VALID_SYMBOLS:
        return False, f"Unsupported symbol: {symbol}"

    return True, symbol


def validate_side(side: str) -> Tuple[bool, str]:
    """Validate BUY / SELL."""

    if not side:
        return False, "Side cannot be empty"

    side = side.upper().strip()

    if side not in VALID_SIDES:
        return False, "Side must be BUY or SELL"

    return True, side


def validate_order_type(order_type: str) -> Tuple[bool, str]:
    """Validate order type."""

    if not order_type:
        return False, "Order type cannot be empty"

    order_type = order_type.upper().strip()

    if order_type not in VALID_ORDER_TYPES:
        return False, "Order type must be MARKET or LIMIT"

    return True, order_type


def validate_quantity(quantity: Any, symbol: str) -> Tuple[bool, str]:
    """Validate quantity."""

    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        return False, "Quantity must be numeric"

    if quantity <= 0:
        return False, "Quantity must be greater than zero"

    if quantity < MIN_QUANTITY:
        return False, f"Minimum quantity is {MIN_QUANTITY}"

    if quantity > MAX_QUANTITY:
        return False, f"Maximum quantity is {MAX_QUANTITY}"

    return True, quantity


def validate_price(price: Any, symbol: str) -> Tuple[bool, str]:
    """Validate price."""

    try:
        price = float(price)
    except (TypeError, ValueError):
        return False, "Price must be numeric"

    if price <= 0:
        return False, "Price must be greater than zero"

    if price < MIN_PRICE:
        return False, f"Minimum price is {MIN_PRICE}"

    if price > MAX_PRICE:
        return False, f"Maximum price is {MAX_PRICE}"

    return True, price


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Validate all order parameters.
    """

    results = {
        "valid": True,
        "validated_params": {},
        "errors": [],
    }

    order_type = order_type.upper()

    validations = [
        ("symbol", validate_symbol(symbol)),
        ("side", validate_side(side)),
        ("order_type", validate_order_type(order_type)),
        ("quantity", validate_quantity(quantity, symbol)),
    ]

    # LIMIT orders require a price
    if order_type == "LIMIT":
        if price is None:
            results["valid"] = False
            results["errors"].append(
                "Price is required for LIMIT orders"
            )
        else:
            validations.append(
                ("price", validate_price(price, symbol))
            )

    # MARKET orders must NOT include a price
    elif order_type == "MARKET":
        if price is not None:
            results["valid"] = False
            results["errors"].append(
                "Price should not be provided for MARKET orders"
            )

    # Process validations
    for field, (success, value) in validations:

        if success:
            results["validated_params"][field] = value
        else:
            results["valid"] = False
            results["errors"].append(f"{field}: {value}")

    return results


def validate_symbol_price_compatibility(
    symbol: str,
    price: float,
) -> Tuple[bool, str]:
    """Basic sanity checks for price."""

    symbol = symbol.upper()

    if symbol == "BTCUSDT":
        if not (100 <= price <= 1000000):
            return False, "BTC price outside reasonable range"

    elif symbol == "ETHUSDT":
        if not (10 <= price <= 100000):
            return False, "ETH price outside reasonable range"

    return True, "OK"


def validate_risk_management(
    quantity: float,
    price: float,
    max_exposure: float = 1000.0,
) -> Tuple[bool, str]:
    """Simple risk management."""

    order_value = quantity * price

    if order_value > max_exposure:
        return (
            False,
            f"Order value (${order_value:.2f}) exceeds maximum exposure (${max_exposure:.2f})",
        )

    if order_value < 1:
        return False, "Order value too small (minimum $1)"

    return True, "OK"