from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Dashboard(models.Model):
    """
    :param: field
    :param: publication

    collection of submitted keys/words to track- users' dashboard is
    distinguished with both attributes for uniqueness. each object has
    ratio one field : one publication && one field : multiple publications
    only
    """
    field = models.ManyToManyField('Field', related_name='dashboard_field')
    publication = models.ManyToManyField('publication.'
                                         'Publication',
                                         related_name='dashboard_publication')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    objects = models.Manager()

    class Meta:
        ordering = ['created']

    def get_absolute_url(self):
        return reverse('dashboard:detail', kwargs={'pk': self.pk})


class Field(models.Model):
    # field attribute need not be unique -> A and B can both submit
    # `Why are we here` without failing on unique constraints- but,
    # getting field is made unique by filtering with user param,
    # it gets the instance object- consider:
    # Dashboard.objects.get(user=user, field__field='Why are we here')
    # and Dashboard.objects.get(user=user)- the latter may
    # encounter Dashboard.MultipleObjectsReturned
    # todo if one user submits same field, it raises MultipleObjectsReturned-
    #  instead of get specific get all as sub list, put it in try block to
    #  avoid exception
    # TODO this way you can get how many users searched a key: analytics
    field = models.CharField(max_length=255, help_text='Train \
    as a/an (Programmer/Accountant/etc)')
    # aoc, to help boost keywords for google api
    aoc = models.CharField(_('area of concentration'), max_length=255,
                           help_text='simple field description')
    # one field, one guide
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE,
                              null=True, blank=True, related_name='field_guide')
    objects = models.Manager()

    class Meta:
        ordering = ['field']

    def get_absolute_url(self):
        pass


class Guide(models.Model):
    """
    Guide is a data model, each member attribute made up of links generated with
    google api on chosen field, it has starter, intermediate, and advanced
    many2many attributes.
    starter guide for instance gathers links to books, blogs, pdfs & videos
    from google using field and aoc as keywords, eg: field: software engineer
    aoc: python devops engineer. The eventual links will be collected as
    many2many and attributed to starter... and so on
    """
    starter = models.ManyToManyField('StarterGuide', related_name='guide_starter')
    intermediate = models.ManyToManyField('IntermediateGuide', related_name='guide_inter')
    advanced = models.ManyToManyField('AdvancedGuide', related_name='guide_adv')
    objects = models.Manager()


class StarterGuide(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link = models.URLField()
    objects = models.Manager()


class IntermediateGuide(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link = models.URLField()
    objects = models.Manager()


class AdvancedGuide(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link = models.URLField()
    objects = models.Manager()
