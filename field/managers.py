from django.core.cache import cache
from django.db import models
from django.utils import timezone


class FieldQuerySet(models.QuerySet):
    def update(self, **kwargs):
        super(FieldQuerySet, self).update(updated=timezone.now(), **kwargs)


class FieldManager(models.Manager):
    def get_queryset(self):
        return FieldQuerySet(self.model, using=self._db)
