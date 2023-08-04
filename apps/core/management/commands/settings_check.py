from django.conf import settings


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(settings.AWS_ACCESS_KEY_ID)
        print(settings.AWS_SECRET_ACCESS_KEY)
        print(settings.AWS_STORAGE_BUCKET_NAME)
