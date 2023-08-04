from .base import *
import os

# Debug settings
DEBUG = True
ALLOWED_HOSTS = ['*']

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'local', 'media')

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "localhost"),
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "django_base"),
        "USER": os.environ.get("DJANGO_DATABASE_USER", "django_base"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "django_base"),
        "PORT": "5432",
        "CONN_MAX_AGE": 60 * 10,  # 10 minutes
    },
}

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Elasticsearch settings
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}
