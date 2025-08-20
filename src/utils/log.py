# coding=utf-8
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))  # Default to a 'logs' folder
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # Default to INFO level
LOG_FILE = LOG_DIR / "crime-data-analyzer.log"


def setup_logging():
    """
    Sets up a dual-output logger: one for the console and one for a rotating file.
    The log level is configurable via the LOG_LEVEL environment variable.
    """
    # Ensure the log directory exists
    LOG_DIR.mkdir(exist_ok=True)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # --- Console Handler (for clean, simple output) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)

    # --- File Handler (for detailed, rotating logs) ---
    # RotatingFileHandler keeps log files from growing too large.
    # maxBytes=5MB, backupCount=3 means it will keep app.log, app.log.1, app.log.2
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to the root logger
    # Check if handlers are already added to avoid duplication in some environments
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
