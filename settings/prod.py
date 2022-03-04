from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['.herokuapp.com', ]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')

EMAIL_HOST = os.environ.get('EMAIL_HOST')

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

EMAIL_PORT = os.environ.get('EMAIL_PORT')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'


# SERVER_EMAIL = '************@gmail.com'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = '**********@gmail.com'
# EMAIL_HOST_PASSWORD = '**********'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_SUBJECT_PREFIX = '****'
# DEFAULT_FROM_EMAIL = '*********@gmail.com'
