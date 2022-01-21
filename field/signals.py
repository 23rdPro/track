from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Dashboard
from field.models import Field
from guide.models import Guide


@receiver(post_save, sender=Field)
def create_field_guide(sender, instance, created, **kwargs):
    if created:
        guide = Guide().save()
        instance.guide = guide
        instance.save()
        dashboard = Dashboard()
        dashboard.field = instance
        dashboard.save()
