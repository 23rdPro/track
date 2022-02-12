from celery import group
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
            Dashboard.objects.create(user=user, field=instance)

            link_set = dict()
            job = group([
                tasks.create_article_objects.si(article.pk, instance.pk, link_set),
                tasks.create_pdf_objects.si(pdf.pk, instance.pk, link_set),
                tasks.create_klass_objects.si(klass.pk, instance.pk, link_set),
                tasks.create_video_objects.si(video.pk, instance.pk, link_set),
                tasks.create_question_objects.si(question.pk, instance.pk, link_set)
            ])
            transaction.on_commit(lambda: job.apply_async(
                expires=240,
                retry=True,
                retry_policy={'max_retries': None, 'interval_start': 0, 'interval_step': 0.2,
                              'interval_max': 0.2
                              },
                compression='gzip',
                ignore_result=True
            ))
