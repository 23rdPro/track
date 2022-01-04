from django.db import models
from django.urls import reverse

from dashboard.managers import DashboardObjectManager
from track.mixins import TimeStampMixin


class Dashboard(TimeStampMixin):
    """
    collection of submitted keys/words to track- user's dashboard is distinguished with both attributes for
    uniqueness. each object has ratio one field : one publication && one field : multiple publications only
    """
    field = models.ManyToManyField('field.Field', related_name='dashboard_field')
    publication = models.ManyToManyField('publication.Publication', related_name='dashboard_publication')
    objects = DashboardObjectManager()

    class Meta:
        ordering = ['updated']

    def get_absolute_url(self):
        return reverse('dashboard:detail', kwargs={'pk': self.pk})
