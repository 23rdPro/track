# flake8: noqa

import factory
from django.core.files.base import ContentFile


start = 1


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'publication.Publication'

    id = factory.Sequence(lambda i: i)
    author = factory.SubFactory("users.factories.UserFactory")
    title = factory.Sequence(lambda i: "title0%d" % i)
    description = factory.Sequence(lambda i: "description0%d" % i)
    # upload_pdf = factory.LazyAttribute(
    #     lambda _: ContentFile(factory.django.FileField(),
    #                           factory.Sequence(
    #                               lambda i: "sample0%d.pdf" % i
    #                           )))  todo

    @classmethod
    def _setup_next_sequence(cls):
        return start
