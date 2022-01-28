import factory

from users.models import User

start = 1


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda i: i)
    email = factory.Sequence(lambda i: 'mail@track%d.com' % i)
    username = factory.Sequence(lambda i: 'user0%d' % i)
    password = factory.PostGenerationMethodCall(
        'set_password', 'sekret@5o5')
    is_active = True

    @classmethod
    def _setup_next_sequence(cls):
        return start
