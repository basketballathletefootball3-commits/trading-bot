#!/usr/bin/env python3
"""Command-line interface for trading bot."""

import argparse
import logging
import sys
from typing import Optional

from bot.client import BinanceClient
from bot.logging_config import setup_logging
from bot.orders import OrderExecutor

# Setup logging
logger, api_logger = setup_logging()


def format_box(title: str, content: dict) -> str:
    """Format content in a box.
    
    Args:
        title: Box title
        content: Dictionary of key-value pairs
        
    Returns:
        Formatted box string
    """
    max_key_len = max(len(k) for k in content.keys()) if content else 0
    max_val_len = max(len(str(v)) for v in content.values()) if content else 0
    width = max(max_key_len + max_val_len + 10, len(title) + 4)

    lines = [
        "╔" + "═" * (width + 2) + "╗",
        "║" + title.center(width + 2) + "║",
        "╠" + "═" * (width + 2) + "╣",
    ]

    for key, value in content.items():
        line = f" {key}: {value}"
        lines.append("║" + line.ljust(width + 2) + "║")

    lines.append("╚" + "═" * (width + 2) + "╝")

    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        epilog="Examples:\n"
        "  python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01\n"
        "  python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 1 --price 3000",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading symbol (e.g., BTCUSDT, ETHUSDT)",
    )

    parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )

    parser.add_argument(
        "--order-type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT",
    )

    parser.add_argument(
        "--quantity",
        type=float,
        required=True,
        help="Order quantity",
    )

    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Order price (required for LIMIT orders)",
    )

    args = parser.parse_args()

    logger.info("Starting Trading Bot CLI")
    logger.info(f"Arguments: symbol={args.symbol}, side={args.side}, "
                f"order_type={args.order_type}, quantity={args.quantity}, price={args.price}")

    try:
        # Initialize client
        client = BinanceClient()

        # Initialize executor
        executor = OrderExecutor(client)

        # Display request summary
        request_summary = {
            "Symbol": args.symbol.upper(),
            "Side": args.side.upper(),
            "Order Type": args.order_type.upper(),
            "Quantity": str(args.quantity),
        }
        if args.price is not None:
            request_summary["Price"] = str(args.price)

        print("\n" + format_box("ORDER REQUEST SUMMARY", request_summary) + "\n")

        # Execute order
        success, response, message = executor.execute_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        if success:
            print(f"✅ {message}\n")

            # Display response details
            response_details = executor.format_order_response(response)
            print(format_box("ORDER RESPONSE DETAILS", response_details) + "\n")

            logger.info(f"Order placed successfully: {response.get('orderId')}")
            return 0
        else:
            print(f"❌ {message}\n")
            logger.error(f"Order placement failed: {message}")
            return 1

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(f"\n❌ Error: {str(e)}\n")
        print("Please ensure:")
        print("  1. .env file exists with BINANCE_API_KEY and BINANCE_API_SECRET")
        print("  2. API credentials are for Binance Futures Testnet")
        print("  3. Testnet account has been activated\n")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n❌ Unexpected error: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
