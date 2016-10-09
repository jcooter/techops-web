from .base import *

DEBUG = False

ALLOWED_HOSTS = ['techops.magfe.st']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env_variable("DJANGO_DB_NAME"),
        "USER": get_env_variable("DJANGO_DB_USERNAME"),
        "PASSWORD": get_env_variable("DJANGO_DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}