"""
Secure Logging Configuration

Handles secret redaction for the Trading Bot.
"""

import logging
import os
import re
from logging.handlers import RotatingFileHandler


# Patterns used to redact secrets from logs
REDACT_PATTERNS = [
    (
        re.compile(
            r'(api_key|api_secret|secret|key)\s*=\s*["\'][^"\']+["\']',
            re.IGNORECASE,
        ),
        r"\1=REDACTED",
    ),
    (
        re.compile(
            r'(api_key|api_secret|secret|key)\s*:\s*["\'][^"\']+["\']',
            re.IGNORECASE,
        ),
        r"\1:REDACTED",
    ),
    (
        re.compile(
            r'(api_key|api_secret|secret|key)\s*=\s*\S+',
            re.IGNORECASE,
        ),
        r"\1=REDACTED",
    ),
    (
        re.compile(
            r'(api_key|api_secret|secret|key)\s*:\s*\S+',
            re.IGNORECASE,
        ),
        r"\1:REDACTED",
    ),
]


class SecretRedactingFormatter(logging.Formatter):
    """Formatter that removes secrets from log messages."""

    def format(self, record):
        message = super().format(record)

        for pattern, replacement in REDACT_PATTERNS:
            message = pattern.sub(replacement, message)

        return message


def setup_logging(
    log_file: str = "logs/trading_bot.log",
    level: int = logging.INFO,
):
    """
    Configure application logging.

    Args:
        log_file:
            Log file path.

        level:
            Logging level.

    Returns:
        Configured logger.
    """

    # Create logs directory
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = SecretRedactingFormatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger = logging.getLogger("trading_bot")
    logger.setLevel(level)

    # Prevent duplicate log entries
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "trading_bot"):
    """Return an existing logger."""

    return logging.getLogger(name)