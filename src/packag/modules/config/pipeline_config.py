import os
from pathlib import Path

from .config import LOG_DIR

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # keep third-party loggers
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'pipeline_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'pipeline.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
            'level': 'DEBUG',
        },
        'task_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'task.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
            'level': 'DEBUG',
        },
        'operations_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'operations.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
            'level': 'DEBUG',
        },
        'utils_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'utils.log'),
            'maxBytes': 5_000_000,
        },
    },
    'loggers': {
        'pipeline': {
            'handlers': ['console', 'pipeline_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'task': {
            'handlers': ['console', 'task_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'operations': {
            'handlers': ['console', 'operations_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'utils': {
            'handlers': ['console', 'utils_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}