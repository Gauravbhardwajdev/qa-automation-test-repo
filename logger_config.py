# logger_config.py
from loguru import logger
import sys

# Prevent duplicate handlers
if not logger._core.handlers:
    logger.remove()
    logger.add(sys.stdout, level="INFO", enqueue=True)
    logger.add("logs/tests.log", rotation="10 MB", level="INFO", enqueue=True)

# Export logger for use elsewhere
__all__ = ["logger"]