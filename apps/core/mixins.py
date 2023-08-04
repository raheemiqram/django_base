import hashlib

from django.core.cache import cache
from django.db.models import QuerySet


class CachedQuerySetMixin:
    @property
    def cached_queryset(self) -> QuerySet:
        # Generate a unique hash key for the model
        model_name = self.__class__.__name__
        model_hash = hashlib.md5(model_name.encode('utf-8')).hexdigest()

        # Check if the queryset is already cached
        queryset_key = f'{model_name}_{model_hash}_queryset'
        queryset = cache.get(queryset_key)
        if queryset is None:
            queryset = self.__class__.objects.all()
            cache.set(queryset_key, queryset)

        return queryset

    def save(self, *args, **kwargs):
        # Generate a new hash key for the model
        model_name = self.__class__.__name__
        model_hash = hashlib.md5(model_name.encode('utf-8')).hexdigest()

        # Delete the cached queryset for the old hash key
        old_queryset_key = f'{model_name}_{self._meta.pk.hash}_queryset'
        cache.delete(old_queryset_key)

        # Update the model's hash key
        self._meta.pk.hash = model_hash

        # Call the base class's save method
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Generate a unique hash key for the model
        model_name = self.__class__.__name__
        model_hash = hashlib.md5(model_name.encode('utf-8')).hexdigest()

        # Delete the cached queryset for the model
        queryset_key = f'{model_name}_{model_hash}_queryset'
        cache.delete(queryset_key)

        # Call the base class's delete method
        super().delete(*args, **kwargs)
