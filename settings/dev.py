from .base import *

SECRET_KEY = os.environ.get('DEV_SECRET_KEY')

DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = ["localhost", '0.0.0.0']

INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ("127.0.0.1", )

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EXTRA_SIGNALS = [
    'field.signals.create_field_handler',
    'field.signals.delete_field_handler',
    'dashboard.signals.dashboard_delete_handler',
    'dashboard.signals.dashboard_create_handler',
]

DEBUG_TOOLBAR_CONFIG = {
    'ENABLE_STACKTRACES': False,
    'ENABLE_STACKTRACES_LOCALS': False,
    'PRETTIFY_SQL':  False,
    'SHOW_TEMPLATE_CONTEXT': False,
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
