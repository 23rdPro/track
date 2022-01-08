from django.db import models
from django.utils.translation import gettext_lazy as _


class Field(models.Model):
    field = models.CharField(max_length=255, help_text='Train as a/an (Programmer/Accountant/etc)')

    # aoc, to help boost keywords for search api
    aoc = models.CharField(_('area of concentration'), max_length=255, help_text='simple field description')

    # one field, one guide
    guide = models.ForeignKey('guide.Guide', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='field_guide')
    objects = models.Manager()

    class Meta:
        pass

    def get_absolute_url(self):
        pass
