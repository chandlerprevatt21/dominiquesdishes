from pathlib import Path

import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

env = environ.Env(
    DEBUG=(bool, False)
)

SECRET_KEY = env('SECRET_KEY')
GOOGLE_API_KEY = env('GOOGLE_API_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost']

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'base',
    'billing',
    'carts',
    'catering',
    'customers',
    'dashboard',
    'emails',
    'events',
    'gallery',
    'menus',
    'orders',
    'privatedining',
    #other_apps
    'address',
    'ckeditor',
    'phonenumber_field',
    'sweetify',
    "whitenoise.runserver_nostatic",
]

STRIPE_API_KEY = env('STRIPE_API_KEY')
STRIPE_PUB_KEY = env('STRIPE_PUB_KEY')
STRIPE_CONNECT_ACCT = env('STRIPE_CONNECT_ACCT')

CHECKOUT_RETURN_URL = env('CHECKOUT_RETURN_URL')

RECAPTCHA_SITE_KEY = env('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = env('RECAPTCHA_SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'dd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dd.context_processors.get_session_cart',
                'dd.context_processors.get_services',
            ],
        },
    },
]

WSGI_APPLICATION = 'dd.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': env('DB_NAME'),                     
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PW'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),                     
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = 'https://pub-22ad366cb0cc4fe784b80ee361417b38.r2.dev/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = 'https://pub-22ad366cb0cc4fe784b80ee361417b38.r2.dev/'
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
