from celery import group
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Dashboard
from field import tasks
from field.models import Field
from guide.models import Guide, Article, PDF, Klass, Video, Question
from publication.models import Publication


@receiver(post_save, sender=Field)
def create_field_guide(sender, instance, created, **kwargs):
    if created:
        import inspect
        for frame in inspect.stack():
            if frame[3] == 'get_response':
                request = frame[0].f_locals['request']
                break
        else:
            request = None
        if request is None:
            raise PermissionDenied
        else:
            guide = Guide().save()
            article = Article().save()
            pdf = PDF().save()
            klass = Klass().save()
            video = Video().save()
            question = Question().save()
            guide.article = article
            guide.pdf = pdf
            guide.klass = klass
            guide.video = video
            guide.question = question
            instance.guide = guide

            user = request.user
            publication = Publication()
            publication.author = user
            publication.save()
            dashboard = Dashboard()
            dashboard.field = instance
            dashboard.save()
            dashboard.publication.add(publication)

            # start tracking
            keys = (article.pk, pdf.pk, klass.pk, video.pk, question.pk)
            link_set = {}
            transaction.on_commit(
                lambda: group(p.delay(instance.pk, keys, link_set) for p in tasks.parallels)()
            )
