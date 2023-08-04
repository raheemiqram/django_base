import os
from .base import *

# Static files settings
STATIC_URL = 'https://<production_domain_name>/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files settings
MEDIA_URL = 'https://<production_domain_name>/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'media')

# Debug settings
DEBUG = False
ALLOWED_HOSTS = ['<production_domain_name>']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<production_db_name>',
        'USER': '<production_db_user>',
        'PASSWORD': '<production_db_password>',
        'HOST': '<production_db_host>',
        'PORT': 5432,
    }
}

# Celery settings
CELERY_BROKER_URL = 'redis://<production_redis_host>:6379'
CELERY_RESULT_BACKEND = 'redis://<production_redis_host'