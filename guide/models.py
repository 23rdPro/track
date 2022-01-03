from django.db import models
from django.utils.translation import gettext_lazy as _


class Guide(models.Model):
    """
    Guide is a data model, each member attribute made up of links
    generated with google-cse api on chosen field/keyword, it has
    starter, intermediate, and advanced many2many attributes.
    starter guide, for instance gathers links to books, blogs,
    pdfs & videos from google using field and aoc as keywords,
    eg: field: software engineer, aoc: python devops engineer.
    The eventual links will be collected as many2many and attributed
    to starter... and so on
    """
    article = models.ForeignKey(
        'Article', on_delete=models.CASCADE, blank=True,
        related_name='guide_article', null=True
    )
    pdf = models.ForeignKey(
        'PDF', on_delete=models.CASCADE, blank=True,
        related_name='guide_pdf', null=True
    )
    klass = models.ForeignKey(
        "Klass", on_delete=models.CASCADE, blank=True,
        related_name='guide_klass', null=True
    )
    video = models.ForeignKey(
        "Video", on_delete=models.CASCADE, blank=True,
        related_name='guide_video', null=True
    )
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, blank=True,
        related_name='guide_question', null=True
    )
    objects = models.Manager()

    def __class_name__(self):  # todo return class name as str
        pass


class Article(models.Model):
    starter = models.ManyToManyField(
        'StarterGuide', related_name='article_starter',
    )
    intermediate = models.ManyToManyField(
        'IntermediateGuide', related_name='article_inter',
    )
    advanced = models.ManyToManyField(
        'AdvancedGuide', related_name='article_adv',
    )
    objects = models.Manager()


class PDF(models.Model):
    starter = models.ManyToManyField(
        'StarterGuide', related_name='pdf_starter',
    )
    intermediate = models.ManyToManyField(
        'IntermediateGuide', related_name='pdf_inter',
    )
    advanced = models.ManyToManyField(
        'AdvancedGuide', related_name='pdf_adv',
    )
    objects = models.Manager()


class Klass(models.Model):
    starter = models.ManyToManyField(
        'StarterGuide', related_name='klass_starter',
    )
    intermediate = models.ManyToManyField(
        'IntermediateGuide', related_name='klass_inter',
    )
    advanced = models.ManyToManyField(
        'AdvancedGuide', related_name='klass_adv',
    )
    objects = models.Manager()


class Video(models.Model):
    starter = models.ManyToManyField(
        'StarterGuide', related_name='video_starter',
    )
    intermediate = models.ManyToManyField(
        'IntermediateGuide', related_name='video_inter',
    )
    advanced = models.ManyToManyField(
        'AdvancedGuide', related_name='video_adv',
    )
    objects = models.Manager()


class Question(models.Model):
    starter = models.ManyToManyField(
        'StarterGuide', related_name='question_starter',
    )
    intermediate = models.ManyToManyField(
        'IntermediateGuide', related_name='question_inter',
    )
    advanced = models.ManyToManyField(
        'AdvancedGuide', related_name='question_adv',
    )
    objects = models.Manager()


class StarterGuide(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    link = models.URLField()
    objects = models.Manager()

    # to bulk_create and save
    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None
    ):
        instance = super(StarterGuide, self).save(
            force_insert, force_update, using,
            update_fields
        )
        return instance


class IntermediateGuide(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    link = models.URLField()
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        instance = super(IntermediateGuide, self).save(
            force_insert, force_update, using, update_fields
        )
        return instance


class AdvancedGuide(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    link = models.URLField()
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        instance = super(AdvancedGuide, self).save(
            force_insert, force_update, using, update_fields
        )
        return instance
