import logging
import re

class SensitiveDataFilter(logging.Filter):
    SENSITIVE_KEYS = {
        'password', 'token', 'access', 'refresh', 'authorization',
        'cookie', 'session', 'csrf', 'secret', 'key', 'api_key'
    }

    def __init__(self, name=''):
        super().__init__(name)
        self.patterns = [
            re.compile(rf'({key})["\']?\s*[:=]\s*["\']?([^"\'\s,]+)["\']?', re.IGNORECASE)
            for key in self.SENSITIVE_KEYS
        ]

    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = self.sanitize(record.msg)
        elif isinstance(record.msg, dict):
            record.msg = self.sanitize_dict(record.msg)

        if hasattr(record, 'args') and record.args:
            if isinstance(record.args, dict):
                record.args = self.sanitize_dict(record.args)
            elif isinstance(record.args, tuple):
                record.args = tuple(self.sanitize(str(arg)) if isinstance(arg, str) else arg for arg in record.args)

        return True

    def sanitize(self, text):
        for pattern in self.patterns:
            text = pattern.sub(r'\1: [REDACTED]', text)
        return text

    def sanitize_dict(self, data):
        if not isinstance(data, dict):
            return data

        sanitized = {}
        for k, v in data.items():
            if any(key in k.lower() for key in self.SENSITIVE_KEYS):
                sanitized[k] = '[REDACTED]'
            elif isinstance(v, dict):
                sanitized[k] = self.sanitize_dict(v)
            elif isinstance(v, list):
                sanitized[k] = [self.sanitize_dict(i) if isinstance(i, dict) else i for i in v]
            else:
                sanitized[k] = v
        return sanitized
