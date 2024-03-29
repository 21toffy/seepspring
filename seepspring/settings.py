"""
Django settings for seepspring project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import redis


r = redis.Redis(host='localhost', port=6379, db=0)

from dotenv import load_dotenv
load_dotenv()



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tk$b%*t*q789$r7*p2w3dy2sd4kzuktr=%3$(+ic@-rfyd_o_o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PROD = False

ALLOWED_HOSTS = ["*",'127.0.0.1','0.0.0.0', "seepspring.herokuapp.com", "seepspringbe.herokuapp.com", "141.145.213.167"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    #installed apps

    'rest_framework',
    "rest_framework_simplejwt",
    'celery',
    "corsheaders",
    'django_celery_beat',
    # "paystackapi",
    # 'drf_yasg'


    #custom apps
    'accounts',
    'common',
    'banks',
    "loan",
    "adminapp"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'seepspring.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


WSGI_APPLICATION = 'seepspring.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases



if PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
    }
}
else:
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "seepspring",
            "USER": "tofunmi",
            "PASSWORD": "toffy123",
            "HOST": "db",
            "PORT": "5432",
        }
    }







# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "accounts.CustomUser"



EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT", "2525")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")



REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
    # 'NON_FIELD_ERRORS_KEY': 'error',
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
        
    # ],
    'EXCEPTION_HANDLER': 'seepspring.exceptions.custom_exception_handler',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
   
}


from datetime import timedelta


# SIMPLE_JWT = {
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'AUTH_TOKEN_CLASSES': (
#         'rest_framework_simplejwt.tokens.AccessToken',
#     ),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True
# }

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

OTP_EXPIRY_TIME = 300


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True


# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = "*"


CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:5335',
    'https://seepspringfe.netlify.app',
    'https://seepspring.netlify.app',
    'http://seepspringfe.netlify.app',
    'http://seepspring.netlify.app',
]

CORS_ORIGIN_WHITELIST = (
    'https://seepspringfe.netlify.app',
    'https://seepspring.netlify.app',
    'http://seepspringfe.netlify.app',
    'http://seepspring.netlify.app',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:5335',
)



# SENDCHAMP_AUTHORIZATION = os.getenv("SENDCHAMP_AUTHORIZATION", "")
SENDCHAMP_URL = os.getenv("SENDCHAMP_URL", "")
SENDCHAMP_SENDER_ID = os.getenv("SENDCHAMP_SENDER_ID", "")

import json

with open('config.json') as config_file:
    config = json.load(config_file)

SENDCHAMP_AUTHORIZATION = config.get('SENDCHAMP_AUTHORIZATION')
PAYSTACK_API_KEY = config.get('PAYSTACK_API_KEY')


# BROKER_URL = "amqp://guest:guest@localhost:5672//"



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }




# CELERY CONFIGURATIONS
CELERY_BROKER_URL=os.getenv("CELERY_BROKER")
CELERY_RESULT_BACKEND=os.getenv("CELERY_BACKEND")
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "UTC"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

SENDCHAMP_EMAIL_URL=os.getenv('SENDCHAMP_EMAIL_URL', "https://api.sendchamp.com/api/v1/email/send") 

from datetime import datetime, timedelta

TOKEN_EXPIRY = 100
