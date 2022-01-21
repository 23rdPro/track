import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from helpers.functions import upload_to_path
from track.mixins import TimeStampMixin


class Publication(TimeStampMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publication_user')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    upload_pdf = models.FileField(upload_to=upload_to_path)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('publication:detail', kwargs={'id': self.id})

    class Meta:
        ordering = ['-updated_at']
