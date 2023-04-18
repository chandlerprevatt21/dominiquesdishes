import environ
from .production import *

env = environ.Env(
    DEBUG=(bool, False)
)

DEBUG = False

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['dominiquesdishes.com','www.dominiquesdishes.com','dominiquesdisheslive.herokuapp.com']
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
CAPTCHA = env('CAPTCHA')
CAPTCHA_SECRET = env('CAPTCHA_SECRET')
GOOGLE_API_KEY = env('GOOGLE_API_KEY')
STRIPE_API_KEY = env('STRIPE_API_KEY')

DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}