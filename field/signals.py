from celery import chain, group
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
            guide = Guide.objects.create(
                article=article,
                pdf=pdf,
                klass=klass,
                video=video,
                question=question
            )
            instance.guide = guide
            instance.save()

            user = request.user
            dd = Dashboard.objects.create(user=user, field=instance)

            # start tracking
            job = chain(
                tasks.basic_guide.si(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk),
                tasks.advanced_guide.si(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk)
            )
            transaction.on_commit(lambda: job.apply_async())

            # transaction.on_commit(lambda: chain(
            #     tasks.starter.delay(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk),
            #     tasks.intermediate.delay(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk),
            #     tasks.advance.delay(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk)
            # ))

            # transaction.on_commit(lambda: group([
            #     tasks.starter.delay(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk),
            #     tasks.intermediate.delay(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk),
            #     tasks.advance.delay(article.pk, pdf.pk, klass.pk, video.pk, question.pk, instance.pk, dd.pk)
            # ]))
