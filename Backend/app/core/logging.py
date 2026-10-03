#app/core/logging.py

import logging
import os


_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def _configured_level() -> int:
    value = os.getenv("LOG_LEVEL", "INFO").upper()
    level = logging.getLevelName(value)
    return level if isinstance(level, int) else logging.INFO


def configure_logging() -> None:
    logging.basicConfig(
        level=_configured_level(),
        format=_LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


logger = logging.getLogger("inventory_management")
