import uuid
import logging
from contextvars import ContextVar

_correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')

def get_correlation_id() -> str:
    return _correlation_id.get()

def set_correlation_id(value: str):
    _correlation_id.set(value)

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        return True
