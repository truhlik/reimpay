from .base import *

DEBUG = True
DEBUG_TOOLBAR = True
ALLOW_ROBOTS = True

INTERNAL_IPS = ['127.0.0.1']
AXES_IP_WHITELIST = INTERNAL_IPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
INSTALLED_APPS += [
    'debug_toolbar',
]
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

CORS_ORIGIN_REGEX_WHITELIST = [r'^http(.*)://localhost(.*)$', r'^http(.*)://127.0.0.1(.*)$']

try:
    from .local import *
except ImportError:
    pass
