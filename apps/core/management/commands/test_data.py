from django.core.management import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create Admin Account
        User.objects.create_user(
            email="raheem@docampaign.com",
            password="admin@123",
            is_superuser=True,
            is_staff=True,
            first_name="Abdur",
            last_name="Raheem",
        )

        # Load more staff users
        for i in range(1, 20):
            User.objects.create_user(
                email=f"test_{i}@docampaign.com",
                password=f"admin@123_{i}",
                first_name=f"Test {i}",
                last_name=f"User {i}",
            )

        print("Test data loaded successfully")
