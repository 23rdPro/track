# flake8: noqa

import factory

from dashboard import signals

start = 1


# todo mock instead
# @factory.django.mute_signals(signals.m2m_changed, signals.pre_delete)
class DashboardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dashboard.Dashboard'
    id = factory.Sequence(lambda i: i)

    @classmethod
    def _setup_next_sequence(cls):
        return start

    @factory.post_generation
    def field(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.field.add(*extracted)

    @factory.post_generation
    def publication(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.publication.add(*extracted)


class FieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dashboard.Field'

    id = factory.Sequence(lambda i: i)
    field = factory.Sequence(lambda i: 'search-key%d' % i)
    aoc = factory.Sequence(lambda i: "boost-key%d" % i)
    guide = factory.SubFactory("dashboard.factories.GuideFactory")

    @classmethod
    def _setup_next_sequence(cls):
        return start


class GuideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dashboard.Guide'

    id = factory.Sequence(lambda i: i)

    @classmethod
    def _setup_next_sequence(cls):
        return start

    @factory.post_generation
    def starter(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.starter.add(*extracted)

    @factory.post_generation
    def intermediate(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.intermediate.add(*extracted)

    @factory.post_generation
    def advanced(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.advanced.add(*extracted)


class StarterGuideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dashboard.StarterGuide'

    id = factory.Sequence(lambda i: i)
    title = factory.Sequence(lambda i: 'title%d' % i)
    description = factory.Sequence(lambda i: 'description%d' % i)
    link = factory.Sequence(lambda i: 'link%d' % i)

    @classmethod
    def _setup_next_sequence(cls):
        return start


class IntermediateGuideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dashboard.IntermediateGuide'

    id = factory.Sequence(lambda i: i)
    title = factory.Sequence(lambda i: 'title%d' % i)
    description = factory.Sequence(lambda i: 'description%d' % i)
    link = factory.Sequence(lambda i: 'link%d' % i)

    @classmethod
    def _setup_next_sequence(cls):
        return start


class AdvancedGuideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dashboard.AdvancedGuide'

    id = factory.Sequence(lambda i: i)
    title = factory.Sequence(lambda i: 'title%d' % i)
    description = factory.Sequence(lambda i: 'description%d' % i)
    link = factory.Sequence(lambda i: 'link%d' % i)

    @classmethod
    def _setup_next_sequence(cls):
        return start
