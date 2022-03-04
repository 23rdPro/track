from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('PROD_DEBUG')

ALLOWED_HOSTS = ['.herokuapp.com', ]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
