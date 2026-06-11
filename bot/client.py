"""Binance Futures API client wrapper."""

import hashlib
import hmac
import json
import logging
import os
import time
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger("trading_bot")
api_logger = logging.getLogger("api_requests")


class BinanceClient:
    """Binance Futures API client for testnet trading."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """Initialize Binance client.
        
        Args:
            api_key: Binance API key (defaults to env variable)
            api_secret: Binance API secret (defaults to env variable)
            
        Raises:
            ValueError: If API credentials are not provided or invalid
        """
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = os.getenv(
            "BINANCE_TESTNET_BASE_URL", "https://testnet.binancefuture.com"
        )

        if not self.api_key or not self.api_secret:
            logger.error("Missing API credentials")
            raise ValueError(
                "API key and secret must be provided or set in .env file. "
                "See .env.example for format."
            )

        logger.info(f"Initialized Binance client with base URL: {self.base_url}")

    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC SHA256 signature for API request.
        
        Args:
            params: Request parameters
            
        Returns:
            HMAC SHA256 signature
        """
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False,
    ) -> Dict[str, Any]:
        """Make HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint path
            params: Request parameters
            signed: Whether request requires signature
            
        Returns:
            Response data
            
        Raises:
            requests.RequestException: If request fails
            ValueError: If response is invalid
        """
        if params is None:
            params = {}

        url = f"{self.base_url}{endpoint}"
        headers = {"X-MBX-APIKEY": self.api_key}

        # Add timestamp for signed requests
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)

        try:
            api_logger.debug(f"Request: {method} {endpoint} with params: {params}")
            logger.debug(f"Making {method} request to {endpoint}")

            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, params=params, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, params=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Log response
            api_logger.debug(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = response.text
                api_logger.error(f"API error: {response.status_code} - {error_msg}")
                logger.error(f"API error: {response.status_code} - {error_msg}")
                raise requests.RequestException(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            data = response.json()
            api_logger.debug(f"Response data: {json.dumps(data, indent=2)}")
            logger.debug(f"Request successful")
            
            return data

        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            api_logger.error(f"Request failed: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {str(e)}")
            api_logger.error(f"Failed to parse response: {str(e)}")
            raise ValueError(f"Invalid API response: {str(e)}")

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Place an order on Binance Futures.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            
        Returns:
            Order response data
            
        Raises:
            ValueError: If parameters are invalid
            requests.RequestException: If API request fails
        """
        logger.info(
            f"Placing {order_type} {side} order: {quantity} {symbol} "
            + (f"@ {price}" if price else "at market")
        )

        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good-Till-Cancel

        try:
            response = self._request(
                method="POST",
                endpoint="/fapi/v1/order",
                params=params,
                signed=True,
            )
            logger.info(f"Order placed successfully. Order ID: {response.get('orderId')}")
            return response
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise

    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Get status of an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Order details
            
        Raises:
            requests.RequestException: If API request fails
        """
        params = {"symbol": symbol.upper(), "orderId": order_id}
        return self._request(
            method="GET",
            endpoint="/fapi/v1/order",
            params=params,
            signed=True,
        )

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information.
        
        Returns:
            Account data
            
        Raises:
            requests.RequestException: If API request fails
        """
        logger.debug("Fetching account information")
        return self._request(
            method="GET",
            endpoint="/fapi/v2/account",
            params={},
            signed=True,
        )
