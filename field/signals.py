from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseForbidden

from dashboard.models import Dashboard
from field.models import Field
from guide.models import Guide
from publication.models import Publication


@receiver(post_save, sender=Field)
def create_field_guide(sender, instance, created, **kwargs):
    if created:
        guide = Guide()
        guide.save()
        instance.guide = guide
        instance.save()
        dashboard = Dashboard()
        dashboard.save()

        import inspect
        for frame in inspect.stack():
            if frame[3] == 'get_response':
                request = frame[0].f_locals['request']
                break
        else:
            request = None
        if request is not None:
            publication = Publication()
            publication.author = request.user
            publication.save()
            dashboard.field = instance
            dashboard.publication.add(publication)
            dashboard.save()
        else:
            raise HttpResponseForbidden()
