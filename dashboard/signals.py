from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from dashboard.models import Dashboard


@receiver(post_delete, sender=Dashboard, dispatch_uid='dashboard_deleted')
def dashboard_delete_handler(sender, instance, *args, **kwargs):
    if isinstance(instance, Dashboard):
        cache.delete('dashboards')


@receiver(post_save, sender=Dashboard, dispatch_uid='dashboard_created')
def dashboard_create_handler(sender, instance, created, **kwargs):
    if isinstance(instance, Dashboard) and created:
        cache.delete('dashboards')
