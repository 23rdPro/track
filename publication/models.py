from django.conf import settings
from django.db import models
from django.urls import reverse

from helpers.functions import upload_to_path


class Publication(models.Model):
    # each dashboard object is initialized with one publication
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='publication_user')
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    upload_pdf = models.FileField(upload_to=upload_to_path, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('publication:detail', kwargs={'pk': self.pk})

    # def delete(self, using=None, keep_parents=False):  over network instead raise method not allowed todo
    #     pass

    class Meta:
        ordering = ['timestamp']
