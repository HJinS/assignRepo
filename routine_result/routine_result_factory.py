from .models import RoutineResult
from datetime import datetime
from pytz import timezone
from routine.tests.routine_factory import RoutineFactory

import factory.fuzzy
import uuid


class RoutineResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutineResult
        django_get_or_create = ('routine_result_id', )
    routine_result_id = factory.LazyAttribute(lambda _: uuid.uuid4())
    routine_id = factory.SubFactory(RoutineFactory)
    result = factory.fuzzy.FuzzyChoice(["N", "T", "D"])
    is_deleted = False
    created_at = factory.fuzzy.FuzzyDateTime(datetime(2022, 5, 4, tzinfo=timezone('Asia/Seoul')))
    modified_at = factory.fuzzy.FuzzyDateTime(datetime(2022, 5, 4, tzinfo=timezone('Asia/Seoul')))

