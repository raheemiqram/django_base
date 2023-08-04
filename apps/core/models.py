from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords

from apps.core.middleware import get_current_authenticated_user
from apps.core.mixins import CachedQuerySetMixin
from apps.users.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        related_name="created_%(app_label)s_%(class)s",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        related_name="updated_%(app_label)s_%(class)s",
        on_delete=models.SET_NULL,
    )
    history = HistoricalRecords(inherit=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_by = get_current_authenticated_user()
        self.updated_by = get_current_authenticated_user()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Configuration(BaseModel, CachedQuerySetMixin):
    # OpenAI configuration
    openai_api_key = models.CharField(max_length=100)

    # Social media configurations
    facebook_app_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_app_secret = models.CharField(max_length=100, blank=True, null=True)
    facebook_access_token = models.CharField(max_length=100, blank=True, null=True)
    instagram_access_token = models.CharField(max_length=100, blank=True, null=True)
    twitter_api_key = models.CharField(max_length=100, blank=True, null=True)
    twitter_api_secret_key = models.CharField(max_length=100, blank=True, null=True)

    # Site configurations
    site_name = models.CharField(max_length=100)
    site_description = models.TextField()
    site_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    site_email = models.EmailField()
    site_phone = models.CharField(max_length=20, blank=True, null=True)
    site_address = models.CharField(max_length=200, blank=True, null=True)
    site_favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    site_header_image = models.ImageField(upload_to='header_images/', blank=True, null=True)
    site_footer_text = models.TextField(blank=True, null=True)
    site_twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    site_facebook_url = models.URLField(blank=True, null=True)
    site_instagram_url = models.URLField(blank=True, null=True)
    site_linkedin_url = models.URLField(blank=True, null=True)
    site_youtube_url = models.URLField(blank=True, null=True)

    # Additional configurations
    enable_cache = models.BooleanField(default=True)
    enable_notifications = models.BooleanField(default=False)
    default_language = models.CharField(max_length=5, default='en')

    def __str__(self):
        return self.site_name

    @classmethod
    def get_config(cls):
        data, created = cls.objects.get_or_create()
        assert isinstance(data, Configuration)
        return data
