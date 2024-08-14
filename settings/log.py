import logging
from logging import config
from settings.base import configs

logging_config = {
    'version': 1,
    'disabel_existing_loggers': False,
    'formatters': {
        'standart': {
            'format': '%(levelname)s-%(asctime)s-%(message)s',
        },
        'describe': {
            'format': '%(levelname)s-%(asctime)s-%(filename)s-%(funcName)s-%(lineno)d-%(message)s'
        }
    },
    'filter': {

    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standart'
        },
        'file': {
            'class': 'settings.base.MyWatchHandler',
            'formatter': 'describe',
            'file_path': 'logs',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        f'{configs.PRODUCTION_NAME}': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
logging.config.dictConfig(logging_config)
logger = logging.getLogger(f'{configs.PRODUCTION_NAME}')


def log_debug(*args):
    logger.debug(args[0] if len(args) == 1 else args)


def log_info(*args):
    logger.info(args[0] if len(args) == 1 else args)


def log_error(*args):
    logger.error(args[0] if len(args) == 1 else args)
