from utility.environments import DEVELOPMENT
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Environment Settings
ENVIRONMENT = DEVELOPMENT
ENVIRONMENT_NAME = 'DEVELOPMENT ENVIRONMENT'
ENVIRONMENT_COLOR = '#808080'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# static and media files settings
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_dev'),
)
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_root')

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
