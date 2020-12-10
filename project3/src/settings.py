import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qweqweqwe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'src.apps.api',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')

REDIS_CONFIG = {
    'port': 6379,
    'db': 0,
    'decode_responses': True
}

TEST_REDIS_CONFIG = {
    'port': 6379,
    'db': 10,
    'decode_responses': True
}

ROOT_URLCONF = 'src.urls'

TEMPLATES = []

WSGI_APPLICATION = 'src.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOG_DIR = os.path.join("..", "..", "logs")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s; %(process)d; %(thread)d; %(levelname)s; %(module)s; %(message)s'
        },
        'simple': {
            'format': '%(asctime)s; %(levelname)s; %(module)s; %(message)s'
        },
    },
    'handlers': {
        'error.log': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log')
        },
        'debug.log': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log')
        },

        'command_error.log': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'command_error.log')
        },
        'command_debug.log': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'command_debug.log')
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['error.log', 'debug.log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
