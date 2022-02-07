from django.db import models


class Guide(models.Model):
    article = models.ForeignKey(
        'Article', on_delete=models.CASCADE, blank=True, related_name='guide_article', null=True)
    pdf = models.ForeignKey(
        'PDF', on_delete=models.CASCADE, blank=True, related_name='guide_pdf', null=True)
    klass = models.ForeignKey(
        "Klass", on_delete=models.CASCADE, blank=True, related_name='guide_klass', null=True)
    video = models.ForeignKey(
        "Video", on_delete=models.CASCADE, blank=True, related_name='guide_video', null=True)
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, blank=True, related_name='guide_question', null=True)
    objects = models.Manager()


class Article(models.Model):
    starter = models.ManyToManyField('StarterGuide', related_name='article_starter')
    intermediate = models.ManyToManyField('IntermediateGuide', related_name='article_inter')
    advanced = models.ManyToManyField('AdvancedGuide', related_name='article_adv')
    objects = models.Manager()


class PDF(models.Model):
    starter = models.ManyToManyField('StarterGuide', related_name='pdf_starter')
    intermediate = models.ManyToManyField('IntermediateGuide', related_name='pdf_inter')
    advanced = models.ManyToManyField('AdvancedGuide', related_name='pdf_adv')
    objects = models.Manager()


class Klass(models.Model):
    starter = models.ManyToManyField('StarterGuide', related_name='klass_starter')
    intermediate = models.ManyToManyField('IntermediateGuide', related_name='klass_inter')
    advanced = models.ManyToManyField('AdvancedGuide', related_name='klass_adv')
    objects = models.Manager()


class Video(models.Model):
    starter = models.ManyToManyField('StarterGuide', related_name='video_starter')
    intermediate = models.ManyToManyField('IntermediateGuide', related_name='video_inter')
    advanced = models.ManyToManyField('AdvancedGuide', related_name='video_adv')
    objects = models.Manager()


class Question(models.Model):
    starter = models.ManyToManyField('StarterGuide', related_name='question_starter')
    intermediate = models.ManyToManyField('IntermediateGuide', related_name='question_inter')
    advanced = models.ManyToManyField('AdvancedGuide', related_name='question_adv')
    objects = models.Manager()


class StarterGuide(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    link = models.URLField(max_length=1000)
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        instance = super(StarterGuide, self).save(force_insert, force_update, using, update_fields)
        return instance


class IntermediateGuide(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    link = models.URLField(max_length=1000)
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        instance = super(IntermediateGuide, self).save(force_insert, force_update, using, update_fields)
        return instance


class AdvancedGuide(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    link = models.URLField(max_length=1000)
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        instance = super(AdvancedGuide, self).save(force_insert, force_update, using, update_fields)
        return instance
