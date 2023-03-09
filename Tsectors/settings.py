"""
Django settings for Tsectors project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2mb^%5$6bz8i*&1v@ahlgtgf9mcj5rl!a1e77z#)jq_fjf*r4x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'admin_notification',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my app
    'app.apps.AppConfig',
    'mainapp',
    'cryptocoin',
    'deposit',
    'withdraw',
    'fund_transfer',

    # Third party
    'django_numerators',
    'mptt',
    'polymorphic',
    'widget_tweaks',
    'workdays',
    'simple_history',
]

# -------------------------------
#                                |
#           Configure New Library
#                                |
# -------------------------------
NOTIFICATION_MODEL = 'deposit.DepositRequestConfirmation'
# NOTIFICATION_MODEL = 'withdraw.WithdrawalRequest'


# -------------------------------
#                                |
#           End - Configure New Library
#                                |
# -------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django_auto_logout.middleware.auto_logout',
    'simple_history.middleware.HistoryRequestMiddleware',
    # cache
    # 'django.middleware.cache.UpdateCacheMiddleware', #new
    # 'django.middleware.cache.FetchFromCacheMiddleware', #new
]
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     }
# }

ROOT_URLCONF = 'Tsectors.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # !!! Add this !!!
                # 'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'Tsectors.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'photos')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Backend

#MY EMAIL SETTING
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.meekbroker.com'  #Hosted on namecheap Ex: mail.pure.com
EMAIL_USE_TLS = False
EMAIL_PORT = 26 #This will be different based on your Host, for Namecheap I use this`
EMAIL_HOST_USER = 'company@meekbroker.com' # Ex: info@pure.com
EMAIL_HOST_PASSWORD = '0gJCbV7Jm6gC' # for the email you created through cPanel. The password for that

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ---------- auto logout
# from datetime import timedelta
#
# AUTO_LOGOUT = {
#     'IDLE_TIME': timedelta(minutes=10),
#     'SESSION_TIME': timedelta(minutes=40),
#     'MESSAGE': 'The session has expired. Please login again to continue.',
#     'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
# }


from decouple import config
import django.core.management.commands.runserver as runserver

runserver.Command.default_port = config('WebServer_Port', default = "8088")

# GeoPath
# GEOIP_PATH =os.path.join(BASE_DIR, 'geoip/')
GEOIP_PATH =os.path.join('geoip')