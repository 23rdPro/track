from django.db.models.signals import post_save
from django.dispatch import receiver

from guide import tasks
from guide.models import Guide, Article, PDF, Klass, Video, Question


@receiver(post_save, sender=Guide)
def create_guide_attributes(sender, created, instance, **kwargs):
    if created:
        article = Article().save()
        pdf = PDF().save()
        klass = Klass().save()
        video = Video().save()
        question = Question().save()
        instance.article = article
        instance.pdf = pdf
        instance.klass = klass
        instance.video = video
        instance.question = question
        instance.save()
    else:  # django access object attributes after post_save in signals
        print('----->', instance.field_guide)
        # field_pk = instance.field_guide.get().pk
        # keys = (article.pk, pdf.pk, klass.pk, video.pk, question.pk)
        # link_set = {}
        # transaction.on_commit(lambda: group(parallel.delay(field_pk, keys, link_set)
        #                                     for parallel in tasks.parallels)())

