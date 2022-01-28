from django.db import models
from django.urls import reverse

from dashboard.managers import DashboardObjectManager
from track.mixins import TimeStampMixin


class Dashboard(TimeStampMixin):
    user = models.OneToOneField('users.User', related_name='dashboard_user', on_delete=models.CASCADE)
    field = models.ForeignKey('field.Field', related_name='dashboard_field', on_delete=models.CASCADE)
    objects = DashboardObjectManager()

    class Meta:
        ordering = ['updated_at']

    def get_absolute_url(self):
        return reverse('dashboard:detail', kwargs={'pk': self.pk})
