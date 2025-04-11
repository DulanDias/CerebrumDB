from loguru import logger
import sys

LOG_FORMAT = "{time} | {level} | {message}"

logger.remove()  # Remove default logger
logger.add(sys.stdout, format=LOG_FORMAT, level="INFO")  # Console logging
logger.add("logs/cerebrumdb.log", format=LOG_FORMAT, level="DEBUG", rotation="10 MB", retention="7 days")  # File logging