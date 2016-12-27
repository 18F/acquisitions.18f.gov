"""
Django settings for acquisitions project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from django.utils import crypto

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY = os.environ.get('SECRET_KEY',
                                         crypto.get_random_string(60))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', default=True) != "False"

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'projects',
    'team',
    'web',
    'nda',
    'uaa_client',
    'news',
    'acquisitions',

    'rest_framework',
    'rest_framework.authtoken',
    'markdown_deux',
    'floppyforms',
    'rest_framework_docs',
    'drf_multiple_model',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'uaa_client.authentication.UaaBackend',
)

ROOT_URLCONF = 'acquisitions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'acquisitions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(
        default="postgres://localhost/acquisitions"
        )
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "third-party/uswds-0.13.1/"),
    os.path.join(BASE_DIR, "third-party/a11y-dialog/"),
]


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Cloud.gov UAA
UAA_AUTH_URL = 'https://login.fr.cloud.gov/oauth/authorize'

UAA_TOKEN_URL = 'https://uaa.cloud.gov/oauth/token'

UAA_CLIENT_ID = os.environ.get('UAA_CLIENT_ID', 'acquisitions-dev')

UAA_CLIENT_SECRET = os.environ.get('UAA_CLIENT_SECRET')

LOGIN_URL = 'uaa_client:login'

LOGIN_REDIRECT_URL = '/'

if DEBUG:
    INSTALLED_APPS += ('fake_uaa_provider',)

if not UAA_CLIENT_SECRET:
    if DEBUG:
        # We'll be using the Fake UAA Provider.
        UAA_CLIENT_SECRET = 'fake-uaa-provider-client-secret'
        UAA_AUTH_URL = UAA_TOKEN_URL = 'fake:'
    else:
        raise Exception('UAA_CLIENT_SECRET must be defined in production.')


# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


# Markdown Deux
MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            "tables": None
        },
        "safe_mode": "escape",
    }
}
