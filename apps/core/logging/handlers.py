import os
import logging
from logging.handlers import RotatingFileHandler

class AutoCreatingRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super().__init__(filename, *args, **kwargs)
