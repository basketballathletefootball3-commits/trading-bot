"""Logging configuration for the trading bot."""

import logging
import os
from pathlib import Path


def setup_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Main logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (INFO level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (DEBUG level)
    file_handler = logging.FileHandler(logs_dir / "trading_bot.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # API Request logger
    api_logger = logging.getLogger("api_requests")
    api_logger.setLevel(logging.DEBUG)
    api_logger.handlers.clear()

    api_formatter = logging.Formatter(
        "%(asctime)s - API - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    api_file_handler = logging.FileHandler(logs_dir / "api_requests.log")
    api_file_handler.setLevel(logging.DEBUG)
    api_file_handler.setFormatter(api_formatter)
    api_logger.addHandler(api_file_handler)

    return logger, api_logger


if __name__ == "__main__":
    logger, api_logger = setup_logging()
    logger.info("Logging configured successfully")
    api_logger.info("API logging configured successfully")
