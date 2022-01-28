from celery import chain
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Dashboard
from field import tasks
from field.models import Field
from guide.models import Guide, Article, PDF, Klass, Video, Question


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
            article = Article()
            article.save()
            pdf = PDF()
            pdf.save()
            klass = Klass()
            klass.save()
            video = Video()
            video.save()
            question = Question()
            question.save()
            guide = Guide()
            guide.article = article
            guide.pdf = pdf
            guide.klass = klass
            guide.video = video
            guide.question = question
            guide.save()
            instance.guide = guide

            user = request.user
            dashboard = Dashboard()
            dashboard.field = instance
            dashboard.user = user
            dashboard.save()

            # start tracking
            transaction.on_commit(lambda: chain(
                tasks.starter.s(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk),
                tasks.intermediate.s(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk),
                tasks.advance.s(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk)
            ).delay())
