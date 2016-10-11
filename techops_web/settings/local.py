from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += ("debug_toolbar", 'uber')

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

UBER_API_URI = 'https://uber.joecooter.com:4444/jsonrpc/'

