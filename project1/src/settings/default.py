import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qweqweqwe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'src.apps.frontend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project',
        'USER': 'project',
        'PASSWORD': 'project',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATIC_ROOT = os.path.join("/", "srv", "project", "public", 'static')

MEDIA_URL = '/media/'

# Only for production
MEDIA_ROOT = os.path.join("..", "..", "media")

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
        'django.command': {
            'handlers': ['command_error.log', 'command_debug.log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
