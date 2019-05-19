from logging.handlers import SysLogHandler

import raven

from utility.environments import PRODUCTION
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'affiliate.halanx.com']

# Environment Settings
ENVIRONMENT = PRODUCTION
ENVIRONMENT_NAME = 'PRODUCTION ENVIRONMENT'
ENVIRONMENT_COLOR = '#FF0000'

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# SSL Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# AWS S3 Settings
AWS_S3_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION = config('AWS_DEFAULT_REGION')
AWS_S3_HOST = config('AWS_S3_HOST')
AWS_STORAGE_BUCKET_NAME = config('AWS_S3_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'

# Staticfiles Settings
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_dev'),
)
AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

# Public Media Settings
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'custom_storages.PublicMediaStorage'

# Private Media Settings
AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'custom_storages.PrivateMediaStorage'


# Logging Settings
INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
    'storages'
]

RAVEN_CONFIG = {
    'dsn': config('SENTRY_RAVEN_URL'),
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

MIDDLEWARE = [
                 'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
             ] + MIDDLEWARE

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/ubuntu/logs/backend.log',
        },
        # Send info messages to syslog
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': '/dev/log',
            'formatter': 'verbose',
        },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # critical errors are logged to sentry
        'sentry': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'syslog', 'mail_admins', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
