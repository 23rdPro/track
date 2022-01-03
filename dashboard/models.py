from django.db import models
from django.urls import reverse

from dashboard.managers import DashboardObjectManager


class Dashboard(models.Model):
    """
    :param: field
    :param: publication

    collection of submitted keys/words to track- user's
    dashboard is distinguished with both attributes for
    uniqueness. each object has ratio one field : one
    publication && one field : multiple publications
    only
    """
    field = models.ManyToManyField(
        'field.Field', related_name='dashboard_field'
    )
    publication = models.ManyToManyField(
        'publication.Publication',
        related_name='dashboard_publication'
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    updated = models.DateTimeField(auto_now=True, editable=False)
    objects = DashboardObjectManager()

    class Meta:
        ordering = ['updated']

    def get_absolute_url(self):
        return reverse(
            'dashboard:detail', kwargs={'pk': self.pk}
        )
