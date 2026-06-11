"""Trading Bot Package"""

__version__ = "1.0.0"
__author__ = "Trading Bot Developer"

from bot.client import BinanceClient
from bot.orders import OrderExecutor

__all__ = ["BinanceClient", "OrderExecutor"]
