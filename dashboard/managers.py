from django.db import models
from django.db.models import Q


class DashboardObjectQuerySet(models.QuerySet):
    def filter_by_field(self, query):
        lookup = (
            Q(field__field__icontains=query) |

            Q(field__aoc__icontains=query) |

            Q(field__guide__starter_title__icontains=query) |

            Q(field__guide__intermediate_title__icontains=query) |

            Q(field__guide__advanced_title__icontains=query)
        )
        return self.filter(lookup)

    def filter_by_publication(self, query):
        lookup = (
            Q(publication__title__icontains=query) |

            Q(publication__description__icontains=query)
        )
        return self.filter(lookup)


class DashboardObjectManager(models.Manager):
    def get_queryset(self):
        return DashboardObjectQuerySet(self.model, using=self._db)

    def filter_by_field(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().filter_by_field(query)

    def filter_by_publication(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().filter_by_publication(query)
