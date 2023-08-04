from .base import *
import os

# Debug settings
DEBUG = False
ALLOWED_HOSTS = ['<staging_domain_name>']

# Static files settings
STATIC_URL = 'https://<staging_domain_name>/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files settings
MEDIA_URL = 'https://<staging_domain_name>/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'media')


# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<staging_db_name>',
        'USER': '<staging_db_user>',
        'PASSWORD': '<staging_db_password>',
        'HOST': '<staging_db_host>',
        'PORT': 5432,
    }
}

# Celery settings
CELERY_BROKER_URL = 'redis://<staging_redis_host>:6379'
CELERY_RESULT_BACKEND = 'redis://<staging_redis_host>:6379'

# Elasticsearch settings
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': '<staging_es_host>:9200'
    },
}