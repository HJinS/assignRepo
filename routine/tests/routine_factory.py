from ..models import Routine
from datetime import datetime
from pytz import timezone
from routine_user.tests.user_factory import UserFactory

import factory.fuzzy
import uuid


class RoutineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Routine
        django_get_or_create = ('routine_id', )
    routine_id = factory.LazyAttribute(lambda _: uuid.uuid4())
    account_id = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=2)
    category = factory.fuzzy.FuzzyChoice(['MIRACLE', 'HOMEWORK'])
    goal = factory.Faker('sentence', nb_words=4)
    is_alarm = factory.fuzzy.FuzzyInteger(0, 1)
    is_deleted = False
    created_at = factory.fuzzy.FuzzyDateTime(datetime(2022, 5, 4, tzinfo=timezone('Asia/Seoul')))
    modified_at = factory.fuzzy.FuzzyDateTime(datetime(2022, 5, 4, tzinfo=timezone('Asia/Seoul')))

