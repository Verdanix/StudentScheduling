"""The file to access the logger to make a relatively decoupled application."""

import logging
import os

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger(__name__)
