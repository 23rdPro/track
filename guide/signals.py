from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Dashboard
from field.models import Field
from guide.models import Guide
from publication.models import Publication


