# flake8: noqa

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from dashboard.models import Dashboard
from publication.models import Publication


# as per the workflow, an initial publication is always saved with
# dashboard object- in the case where a user deletes their first/only
# publication object, a new default is created
# @receiver(pre_delete, sender=Publication)
# def restore_related_attribute(sender, instance, *args, **kwargs):
#     dashboard = Dashboard.objects.get(publication__id=instance.pk)
#     if dashboard.publication.count() == 1:
#         new = Publication(author=instance.author)
#         new.save()
#         dashboard.publication.add(new)
