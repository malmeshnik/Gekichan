import os
import json
import logging
from datetime import datetime, timezone
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        log_record['module'] = record.module
        log_record['funcName'] = record.funcName
        log_record['correlation_id'] = getattr(record, 'correlation_id', None)

        if record.exc_info:
            log_record['traceback'] = self.formatException(record.exc_info)

def get_console_formatter(use_colors=True):
    if use_colors:
        from colorlog import ColoredFormatter
        return ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    return logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
