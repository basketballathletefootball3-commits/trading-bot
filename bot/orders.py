"""Order execution logic for trading bot."""

import logging
from typing import Any, Dict, Optional, Tuple

from bot.client import BinanceClient
from bot.validators import validate_limit_order_params

logger = logging.getLogger("trading_bot")
api_logger = logging.getLogger("api_requests")


class OrderExecutor:
    """Execute orders through Binance Futures API."""

    def __init__(self, client: BinanceClient):
        """Initialize order executor.
        
        Args:
            client: Binance API client
        """
        self.client = client
        logger.info("OrderExecutor initialized")

    def execute_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Tuple[bool, Dict[str, Any], str]:
        """Execute a market or limit order.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Tuple of (success, response_data, message)
        """
        # Validate inputs
        valid, error_msg = validate_limit_order_params(
            symbol, side, order_type, quantity, price
        )
        if not valid:
            logger.error(f"Validation error: {error_msg}")
            return False, {}, f"Validation error: {error_msg}"

        try:
            # Place order
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )

            # Extract order details
            order_id = response.get("orderId")
            status = response.get("status")
            executed_qty = float(response.get("executedQty", 0))
            avg_price = float(response.get("avgPrice", 0))
            cumulative_quote_asset_transacted = float(
                response.get("cumQuote", 0)
            )

            logger.info(
                f"Order {order_id} placed successfully. "
                f"Status: {status}, Qty: {executed_qty}"
            )

            return True, response, "Order placed successfully"

        except ValueError as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg
        except Exception as e:
            error_msg = f"Failed to place order: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg

    def format_order_response(self, response: Dict[str, Any]) -> Dict[str, str]:
        """Format order response for display.
        
        Args:
            response: Raw API response
            
        Returns:
            Formatted response data
        """
        return {
            "Order ID": str(response.get("orderId", "N/A")),
            "Status": response.get("status", "N/A"),
            "Executed Qty": str(response.get("executedQty", "0")),
            "Average Price": str(response.get("avgPrice", "0")),
            "Commission": str(response.get("commission", "0")),
            "Commission Asset": response.get("commissionAsset", "N/A"),
            "Cumulative Quote": str(response.get("cumQuote", "0")),
        }
