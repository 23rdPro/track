# flake8: noqa

from django.db import transaction
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver

from dashboard import tasks
from dashboard.models import Dashboard
from helpers.functions import delete_file


@receiver(m2m_changed, sender=Dashboard.field.through)
def track_dashboard(sender, instance, action, **kwargs):
    if action is 'post_add':
        transaction.on_commit(
            lambda: tasks.track.delay(instance.pk))


@receiver(pre_delete, sender=Dashboard)
def delete_related_attributes(sender, instance, *args, **kwargs):
    field = instance.field.first()
    guide = field.guide
    for starter in guide.starter.all():
        starter.delete()
    for intermediate in guide.intermediate.all():
        intermediate.delete()
    for advanced in guide.advanced.all():
        advanced.delete()
    guide.delete()
    field.delete()
    publications = instance.publication.all()
    try:
        files = (obj.upload_pdf.path for obj in publications)
        for file in files:
            delete_file(file)
    except ValueError:
        pass
    for publication in publications:
        publication.delete()
