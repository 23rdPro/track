# flake8: noqa

import pytest
from dashboard.models import (
    Field,
    Dashboard,
    StarterGuide,
    IntermediateGuide,
    Guide,
    AdvancedGuide
)
from publication.models import Publication
from users.factories import UserFactory


@pytest.mark.django_db
class TestDashboardInstance:
    # todo field factory seems to be generating an extra guide
    #  object, this is unexpected

    def test_dashboard_attributes(self):
        # instance = DashboardFactory()
        # starter = StarterGuideFactory()
        # inter = IntermediateGuideFactory()
        # adv = AdvancedGuideFactory()
        #
        # guide = GuideFactory()
        # guide.starter.add(starter)
        # guide.intermediate.add(inter)
        # guide.advanced.add(adv)
        # assert Guide.objects.count() == 1
        #
        # field = FieldFactory()
        # assert Guide.objects.count() == 2
        # # those 2 asserts should be the same todo factory
        #
        # field.guide = guide
        # publication = PublicationFactory()
        # assert User.objects.count() == 1
        # also not expected, switch to django orm

        Dashboard().save()
        instance = Dashboard.objects.get()
        StarterGuide(title='1', description='11', link='www.111.com').save()
        starter = StarterGuide.objects.get()
        IntermediateGuide(title='1', description='11', link='www.111.com').save()
        intermediate = IntermediateGuide.objects.get()
        AdvancedGuide(title='1', description='11', link='www.111.com').save()
        advanced = AdvancedGuide.objects.get()
        assert Dashboard.objects.count() == 1
        assert StarterGuide.objects.count() == 1
        assert IntermediateGuide.objects.count() == 1
        assert AdvancedGuide.objects.count() == 1
        Field(field='bone', aoc='medicine').save()
        field = Field.objects.get()
        assert Field.objects.count() == 1
        Guide().save()
        guide = Guide.objects.get()
        assert Guide.objects.count() == 1
        field.guide = guide
        assert Guide.objects.count() == 1
        guide.starter.add(starter)
        guide.intermediate.add(intermediate)
        guide.advanced.add(advanced)
        assert Guide.objects.count() == 1

        user = UserFactory()
        Publication(author=user).save()
        publication = Publication.objects.get()
        instance.field.add(field)
        instance.publication.add(publication)
        assert instance.publication.first() == publication
        assert instance.field.first() == field


if __name__ == '__main__':
    pytest.main()
