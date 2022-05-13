from routine_result.models import RoutineResult
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
    result = factory.fuzzy.FuzzyChoice(['NOT', 'TRY', 'DONE'])
    is_deleted = False
    created_at = factory.fuzzy.FuzzyDateTime(datetime.now(timezone('Asia/Seoul')))
    modified_at = factory.fuzzy.FuzzyDateTime(datetime.now(timezone('Asia/Seoul')))

