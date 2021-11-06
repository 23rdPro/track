import pytest
from pytest import raises

from dashboard.factories import FieldFactory, DashboardFactory, StarterGuideFactory, IntermediateGuideFactory, \
    AdvancedGuideFactory, GuideFactory
from dashboard.models import Field, Dashboard, StarterGuide, IntermediateGuide
from publication.factories import PublicationFactory
from publication.models import Publication


@pytest.mark.django_db
def test_instance():
    field = FieldFactory()
    guide = GuideFactory()
    field.guide = guide
    starter = StarterGuideFactory()
    inter = IntermediateGuideFactory()
    adv = AdvancedGuideFactory()
    guide.starter.add(starter)
    # publication = PublicationFactory()
    dashboard = DashboardFactory()
    # print(field, publication, dashboard)
    assert isinstance(dashboard.pk, int)
    assert isinstance(field, Field)
    assert field.field == 'search-key1'
    assert field.guide == guide
    # assert isinstance(starter, StarterGuide)
    # assert isinstance(inter, IntermediateGuide)
    assert guide.starter.first().title == 'title1'
    # assert isinstance(publication, Publication)
    # assert raises
    # dashboard.meta todo


if __name__ == '__main__':
    pytest.main()
