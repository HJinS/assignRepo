from .models import RoutineUser

import uuid
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutineUser
        django_get_or_create = ('account_id', )
    account_id = factory.LazyAttribute(lambda _: uuid.uuid4())
    username = factory.Faker('name')
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
