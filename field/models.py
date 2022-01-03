from django.db import models
from django.utils.translation import gettext_lazy as _


class Field(models.Model):
    # field attribute need not be unique -> A and B can both submit
    # `Why are we here` without failing on unique constraints- but,
    # getting field is made unique by filtering with user param,
    # it gets the instance object- consider:
    # Dashboard.objects.get(user=user, field__field='Why are
    # we here') and Dashboard.objects.get(user=user)- the latter
    # may encounter Dashboard.MultipleObjectsReturned
    # todo if one user submits same field, it raises
    #  MultipleObjectsReturned- instead of get specific, get all as
    #  sub list, put it in try block to avoid exception **

    # TODO this way you can get how many users searched
    #  a key: analytics

    field = models.CharField(max_length=255, help_text='Train \
    as a/an (Programmer/Accountant/etc)')
    # aoc, to help boost keywords for google api
    aoc = models.CharField(_(
        'area of concentration'), max_length=255,
        help_text='simple field description'
    )
    # one field, one guide
    guide = models.ForeignKey(
        'guide.Guide', on_delete=models.CASCADE, null=True,
        blank=True, related_name='field_guide'
    )
    objects = models.Manager()

    class Meta:
        ordering = ['field']

    def get_absolute_url(self):
        pass
