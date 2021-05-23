import factory
from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username_{0}'.format(n))
    email = factory.Sequence(lambda n: 'test_{0}@mail.ru'.format(n))
    password = 'test12TeST'
