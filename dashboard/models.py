from django.db import models
from django.urls import reverse

from dashboard.managers import DashboardObjectManager
from track.mixins import TimeStampMixin


class Dashboard(TimeStampMixin):
    field = models.ForeignKey('field.Field', related_name='dashboard_field', on_delete=models.CASCADE)
    publication = models.ManyToManyField('publication.Publication', related_name='dashboard_publication')
    objects = DashboardObjectManager()

    class Meta:
        ordering = ['updated_at']

    def get_absolute_url(self):
        return reverse('dashboard:detail', kwargs={'pk': self.pk})
