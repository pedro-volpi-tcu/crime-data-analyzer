# coding=utf-8
import logging
import logging.config
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = ROOT_DIR / Path(os.getenv("LOG_DIR", "logs"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging() -> None:
    """
    Sets up robust, production-grade logging.

    This function configures logging using a dictionary (dictConfig), which is more
    flexible than manually adding handlers. It establishes two main outputs:
    1.  **Console (stdout)**: Human-readable format, intended for development.
    2.  **Rotating File**: Structured JSON format, ideal for log aggregation
        systems like ELK, Splunk, or Datadog in production.

    To use this in your application:
    1. Call `setup_logging()` once at your application's entry point.
    2. In any other module, get a logger instance by calling:
       `logger = logging.getLogger(__name__)`
    """
    LOG_DIR.mkdir(exist_ok=True)
    log_file_path = LOG_DIR / "crime-data-analyzer.json.log"

    # The core configuration dictionary
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,  # Keep loggers from 3rd-party libs
        "formatters": {
            "console_formatter": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
            # JSON formatter for production-ready, machine-readable logs
            "json_formatter": {
                "()": "python_json_logger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 format
            },
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "formatter": "console_formatter",
                "stream": sys.stdout,
            },
            # Rotating file handler for detailed, structured logs
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json_formatter",
                "filename": log_file_path,
                "maxBytes": 10 * 1024 * 1024,  # 10 MB file size
                "backupCount": 5,  # Keep 5 backup logs
                "encoding": "utf-8",
            },
        },
        "root": {
            # Set the root logger level. You can override this for specific loggers.
            "level": LOG_LEVEL,
            "handlers": ["console_handler", "file_handler"],
        },
        # Example: Quieting a noisy third-party library
        "loggers": {
            "urllib3": {
                "level": "WARNING",
                "propagate": True,
            }
        },
    }

    logging.config.dictConfig(logging_config)
    logging.info("Logging configured successfully. Outputting to console and %s", log_file_path)


# --- Example of how to use it ---
if __name__ == "__main__":
    # 1. Call this ONCE at the start of your application
    setup_logging()

    # 2. In every module, get your logger instance like this.
    # The name will be the module's path (e.g., 'my_app.services.data_processing'),
    # providing automatic context.
    logger = logging.getLogger(__name__)

    logger.debug("This is a detailed debug message for developers.")
    logger.info("Application starting up...")
    logger.info("Processing user request.", extra={"user_id": "usr_123", "request_id": "abc-xyz-789"})
    logger.warning("Network connection is slow.")

    try:
        result = 1 / 0
    except ZeroDivisionError:
        # 'exc_info=True' automatically captures and logs the full exception traceback
        logger.error("Critical calculation failed", exc_info=True)

    logger.critical("A critical component has failed. Shutting down.")
