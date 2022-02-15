from celery import group
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from dashboard.models import Dashboard
from field import tasks
from field.models import Field
from guide.models import Guide, Article, PDF, Klass, Video, Question
from users.models import User


def track_object(instance: Field, user: User) -> None:
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
    Field.objects.filter(pk=instance.pk).update(guide=guide)
    Dashboard.objects.create(user=user, field=instance)

    link_set = dict()  # todo: multiprocessing.Manager().dict()
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
    return


@receiver(post_save, sender=Field, dispatch_uid='create_field_guide')
def create_field_handler(sender, instance, created, **kwargs):
    import inspect
    request = None
    for frame in inspect.stack():
        if frame[3] == 'get_response':
            request = frame[0].f_locals['request']
            break
    if request is None:
        raise PermissionDenied
    if created:
        track_object(instance, request.user)
    else:
        instance.guide.article.basic.all().delete()
        instance.guide.article.advanced.all().delete()
        instance.guide.pdf.basic.all().delete()
        instance.guide.pdf.advanced.all().delete()
        instance.guide.klass.basic.all().delete()
        instance.guide.klass.advanced.all().delete()
        instance.guide.video.basic.all().delete()
        instance.guide.video.advanced.all().delete()
        instance.guide.question.basic.all().delete()
        instance.guide.question.advanced.all().delete()

        a = Article.objects.get(pk=instance.guide.article.pk)
        p = PDF.objects.get(pk=instance.guide.pdf.pk)
        k = Klass.objects.get(pk=instance.guide.klass.pk)
        v = Video.objects.get(pk=instance.guide.video.pk)
        q = Question.objects.get(pk=instance.guide.question.pk)
        link_set = dict()
        job = group([
            tasks.create_article_objects.si(a.pk, instance.pk, link_set),
            tasks.create_pdf_objects.si(p.pk, instance.pk, link_set),
            tasks.create_klass_objects.si(k.pk, instance.pk, link_set),
            tasks.create_video_objects.si(v.pk, instance.pk, link_set),
            tasks.create_question_objects.si(q.pk, instance.pk, link_set)
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


@receiver(post_delete, sender=Field, dispatch_uid='delete_field_guide')
def delete_field_handler(sender, instance, *args, **kwargs):
    if isinstance(instance, Field):
        instance.guide.article.basic.all().delete()
        instance.guide.article.advanced.all().delete()
        instance.guide.pdf.basic.all().delete()
        instance.guide.pdf.advanced.all().delete()
        instance.guide.klass.basic.all().delete()
        instance.guide.klass.advanced.all().delete()
        instance.guide.video.basic.all().delete()
        instance.guide.video.advanced.all().delete()
        instance.guide.question.basic.all().delete()
        instance.guide.question.advanced.all().delete()
        instance.guide.article.delete()
        instance.guide.pdf.delete()
        instance.guide.klass.delete()
        instance.guide.video.delete()
        instance.guide.question.delete()
        instance.guide.delete()
