import os
import sys

from loguru import logger


level = (os.environ.get("LOG_LEVEL") or "DEBUG").upper()
logger.remove()
logger.add(sys.stdout, level=level)



