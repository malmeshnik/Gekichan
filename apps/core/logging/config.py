import os
from pathlib import Path
from .formatters import get_console_formatter

def get_logging_config(
    log_level=os.getenv('LOG_LEVEL', 'INFO'),
    log_dir=os.getenv('LOG_DIR', 'logs'),
    log_json=os.getenv('LOG_JSON', 'false').lower() == 'true',
    log_rotation_size=int(os.getenv('LOG_ROTATION_SIZE', 10 * 1024 * 1024)),  # 10MB default
    is_bot=False
):
    base_log_path = Path(log_dir)
    component = 'bot' if is_bot else 'backend'
    log_path = base_log_path / component

    # Ensure directory exists
    log_path.mkdir(parents=True, exist_ok=True)

    # Common handlers
    handlers = {
        'console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'json' if log_json and not os.getenv('DEBUG', 'False').lower() == 'true' else 'colored',
            'filters': ['sensitive_data', 'correlation_id'],
        },
        'file_main': {
            'level': log_level,
            'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
            'filename': str(log_path / ('bot.log' if is_bot else 'django.log')),
            'maxBytes': log_rotation_size,
            'backupCount': 5,
            'formatter': 'json' if log_json else 'standard',
            'filters': ['sensitive_data', 'correlation_id'],
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
            'filename': str(log_path / 'errors.log'),
            'maxBytes': log_rotation_size,
            'backupCount': 10,
            'formatter': 'json' if log_json else 'standard',
            'filters': ['sensitive_data', 'correlation_id'],
        },
    }

    # Component-specific loggers
    loggers = {
        'django': {
            'handlers': ['console', 'file_main', 'file_errors'],
            'level': log_level,
            'propagate': True,
        },
        'security': {
            'handlers': ['console', 'file_main', 'file_errors'],
            'level': log_level,
            'propagate': False,
        },
        'websocket': {
            'handlers': ['console', 'file_main', 'file_errors'],
            'level': log_level,
            'propagate': False,
        },
    }

    if not is_bot:
        # Backend specific handlers
        handlers.update({
            'file_api': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'api.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
            'file_celery': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'celery.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
            'file_auth': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'auth.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
        })
        # Backend specific loggers
        loggers.update({
            'apps.api': {
                'handlers': ['console', 'file_api', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
            'apps.users': {
                'handlers': ['console', 'file_auth', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
            'celery': {
                'handlers': ['console', 'file_celery', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
            'tasks': {
                'handlers': ['console', 'file_celery', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
        })
    else:
        # Bot specific handlers
        handlers.update({
            'file_handlers': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'handlers.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
            'file_callbacks': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'callbacks.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
            'file_payments': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'payments.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
            'file_bot_main': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'bot.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
            'file_api_client': {
                'level': log_level,
                'class': 'apps.core.logging.handlers.AutoCreatingRotatingFileHandler',
                'filename': str(log_path / 'api.log'),
                'maxBytes': log_rotation_size,
                'backupCount': 5,
                'formatter': 'json' if log_json else 'standard',
                'filters': ['sensitive_data', 'correlation_id'],
            },
        })
        # Bot specific loggers
        loggers.update({
            'bot': {
                'handlers': ['console', 'file_bot_main', 'file_errors'],
                'level': log_level,
                'propagate': True,
            },
            'handlers': {
                'handlers': ['console', 'file_handlers', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
            'callbacks': {
                'handlers': ['console', 'file_callbacks', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
            'payments': {
                'handlers': ['console', 'file_payments', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
            'apps.api': {
                'handlers': ['console', 'file_api_client', 'file_errors'],
                'level': log_level,
                'propagate': False,
            },
        })

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'sensitive_data': {
                '()': 'apps.core.logging.filters.SensitiveDataFilter',
            },
            'correlation_id': {
                '()': 'apps.core.logging.correlation.CorrelationIdFilter',
            },
        },
        'formatters': {
            'standard': {
                '()': 'apps.core.logging.formatters.get_console_formatter',
                'use_colors': False,
            },
            'colored': {
                '()': 'apps.core.logging.formatters.get_console_formatter',
                'use_colors': True,
            },
            'json': {
                '()': 'apps.core.logging.formatters.CustomJsonFormatter',
            },
        },
        'handlers': handlers,
        'loggers': loggers,
        'root': {
            'handlers': ['console', 'file_main', 'file_errors'],
            'level': log_level,
        },
    }

    return config
