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
