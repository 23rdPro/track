from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Dashboard
from publication.models import Publication


@receiver(post_save, sender=Dashboard)
def create_dashboard_publication(sender, instance, created, **kwargs):
    if created:
        import inspect
        for frame in inspect.stack():
            if frame[3] == 'get_response':
                request = frame[0].f_locals['request']
                break
        else:
            request = None
        if request is not None:
            user = request.user
            publication = Publication()
            publication.author = user
            publication.save()
            instance.publication.add(publication)


# @receiver(m2m_changed, sender=Dashboard.field.through)
# def track_dashboard(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         # todo how to ensure each job in group completes successfully,
#         #  gracefully handle timeout- set retries: 3 in service build
#         link_set = {}  # origin
#         transaction.on_commit(
#             lambda: group(parallel.delay(instance.pk, link_set)
#                           for parallel in tasks.parallels)())
