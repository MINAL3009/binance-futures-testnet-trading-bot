"""
Order Placement Module

Handles Market and Limit BUY/SELL orders for Binance Futures Testnet.
"""

from typing import Dict, Any, Optional

from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
)

from .client import BinanceClient
from .validators import (
    validate_order_params,
    validate_symbol_price_compatibility,
    validate_risk_management,
)


def create_order(
    asset_pair: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Validate input and place an order.

    Args:
        asset_pair: Trading pair (e.g. BTCUSDT)
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Required for LIMIT orders

    Returns:
        Dictionary containing order information.

    Raises:
        ValueError:
            Invalid input.

        RuntimeError:
            API or network errors.
    """

    # -----------------------------
    # Validate input
    # -----------------------------
    validation = validate_order_params(
        symbol=asset_pair,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    if not validation["valid"]:
        raise ValueError("; ".join(validation["errors"]))

    # -----------------------------
    # Additional validation for LIMIT orders
    # -----------------------------
    if order_type.upper() == "LIMIT":

        success, message = validate_symbol_price_compatibility(
            asset_pair,
            price,
        )

        if not success:
            raise ValueError(message)

        success, message = validate_risk_management(
            quantity=quantity,
            price=price,
            max_exposure=1000.0,
        )

        if not success:
            raise ValueError(message)

    # -----------------------------
    # Initialize Binance client
    # -----------------------------
    client = BinanceClient()

    success, message = client.validate_connection()

    if not success:
        raise RuntimeError(message)

    # -----------------------------
    # Build order parameters
    # -----------------------------
    params = {
        "symbol": asset_pair.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
        "newOrderRespType": "RESULT",
    }

    if order_type.upper() == "LIMIT":
        params["price"] = round(price, 8)
        params["timeInForce"] = "GTC"

    # -----------------------------
    # Submit order
    # -----------------------------
    try:

        order = client.client.futures_create_order(**params)

        executed_price = (
            order.get("avgPrice")
            or order.get("price")
            or "Market Price"
        )

        if executed_price == "0.00":
            executed_price = "Market Price"

        return {
            "order_id": order.get("orderId"),
            "status": order.get("status"),
            "executed_qty": order.get("executedQty"),
            "executed_price": executed_price,
        }

    except BinanceAPIException as e:
        raise RuntimeError(f"Binance API Error: {e.message}")

    except BinanceRequestException as e:
        raise RuntimeError(f"Network Error: {str(e)}")

    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {str(e)}")