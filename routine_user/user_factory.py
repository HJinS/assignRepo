from .models import RoutineUser
from faker import Faker

import uuid
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutineUser
        django_get_or_create = ('id', )
    id = factory.LazyAttribute(lambda _: uuid.uuid4())
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.lazy_attribute(lambda o: '{}.{}@example.com'.format(o.first_name, o.last_name))
