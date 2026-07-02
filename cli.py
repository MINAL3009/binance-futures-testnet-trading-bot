"""
CLI Entry Point

Parses command-line arguments, validates input,
logs requests/responses, and places Binance Futures Testnet orders.
"""

import argparse

from bot.orders import create_order
from bot.logging_config import setup_logging

# Initialize logger
logger = setup_logging()


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading symbol (e.g. BTCUSDT)"
    )

    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side"
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type"
    )

    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity"
    )

    parser.add_argument(
        "--price",
        type=float,
        help="Price (required only for LIMIT orders)"
    )

    return parser.parse_args()


def main():
    """CLI entry point."""

    args = parse_arguments()

    # Additional CLI validation
    if args.type == "LIMIT" and args.price is None:
        print("ERROR: LIMIT orders require --price")
        return

    if args.type == "MARKET" and args.price is not None:
        print("ERROR: MARKET orders should not include --price")
        return

    # Request summary
    print("\n========== REQUEST ==========")
    print(f"Symbol   : {args.symbol}")
    print(f"Side     : {args.side}")
    print(f"Type     : {args.type}")
    print(f"Quantity : {args.quantity}")

    if args.price is not None:
        print(f"Price    : {args.price}")

    print("=============================\n")

    logger.info(
        "Request: symbol=%s side=%s type=%s quantity=%s price=%s",
        args.symbol,
        args.side,
        args.type,
        args.quantity,
        args.price,
    )

    try:

        response = create_order(
            asset_pair=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )

        logger.info("Response: %s", response)

        print("========== RESPONSE ==========")
        print(f"Order ID       : {response.get('order_id')}")
        print(f"Status         : {response.get('status')}")
        print(f"Executed Qty   : {response.get('executed_qty')}")
        print(f"Executed Price : {response.get('executed_price')}")
        print("==============================")

        print("\n✅ Order placed successfully.")

    except ValueError as e:

        logger.error("Validation Error: %s", str(e))
        print(f"\nValidation Error:\n{e}")

    except RuntimeError as e:

        logger.error("Runtime Error: %s", str(e))
        print(f"\nRuntime Error:\n{e}")

    except Exception as e:

        logger.exception("Unexpected Error")
        print(f"\nUnexpected Error:\n{e}")


if __name__ == "__main__":
    main()