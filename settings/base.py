import dj_database_url
import environ
import os
from pathlib import Path


env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

    'crispy_forms',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'search',
    'users',
    'dashboard.apps.DashboardConfig',
    'field.apps.FieldConfig',
    'guide.apps.GuideConfig',
    'publication.apps.PublicationConfig',

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

# Cross-Origin Resource Sharing (CORS)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000"
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000"
]

ROOT_URLCONF = 'track.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR / 'templates'),
            os.path.join(BASE_DIR / 'auth_templates'),
        ],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.PageNumberPagination',
    "PAGE_SIZE": 5,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}

SITE_ID = 2

AUTH_USER_MODEL = 'users.User'

# allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Genesis"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 6
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 1800
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# TODO check PasswordChangeView
ACCOUNT_ADAPTER = 'users.adapter.UserAccountAdapter'

LOGIN_REDIRECT_URL = 'publication:list'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

WSGI_APPLICATION = 'track.wsgi.application'

# Database
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
        "TEST": {
            "NAME": 'test-track'
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR / 'assets')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CELERY
CELERY_BROKER_URL = os.environ.get('REDIS_TLS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_TLS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_ALWAYS_EAGER = True
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 64
# CELERY_CACHE_BACKEND = 'default'
CELERY_TASK_TRACK_STARTED = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SESSIONS_ENGINE = 'django.contrib.sessions.backends.cache'

if not os.environ.get('MEMCACHIER_PASSWORD') and not os.environ.get('MEMCACHIER_SERVERS') \
        and not os.environ.get('MEMCACHIER_USERNAME'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
            'OPTIONS': {
                'no_delay': True,
                'ignore_exc': True,
                'max_pool_size': 4,
                'use_pooling': True
            },
            'TIMEOUT': None,
            'KEY_PREFIX': os.environ.get('KEY_PREFIX'),
            'VERSION': os.environ.get('VERSION'),
            'KEY_FUNCTION': 'helpers.functions.make_key'

        }
    }

else:

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'TIMEOUT': None,
            'LOCATION': os.environ.get('MEMCACHIER_SERVERS'),
            'OPTIONS': {
                'binary': True,
                'username': os.environ.get('MEMCACHIER_USERNAME'),
                'password': os.environ.get('MEMCACHIER_PASSWORD'),
                'behaviors': {
                    'no_block': True,
                    'tcp_nodelay': True,
                    'tcp_keepalive': True,
                    'connect_timeout': 2000,
                    'send_timeout': 750 * 1000,
                    'receive_timeout': 750 * 1000,
                    '_poll_timeout': 2000,
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30
                }
            },
            'KEY_PREFIX': os.environ.get('KEY_PREFIX'),
            'VERSION': os.environ.get('VERSION'),
            'KEY_FUNCTION': 'helpers.functions.make_key'
        }
    }

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
