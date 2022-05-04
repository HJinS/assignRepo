from .models import RoutineDay
from datetime import datetime
from pytz import timezone
from routine.tests.routine_factory import RoutineFactory

import factory.fuzzy


class RoutineDayFactory(factory.django.DjangoModelFactory):
    def __init__(self):
        self.today = datetime.today()

    class Meta:
        model = RoutineDay
    routine_id = factory.SubFactory(RoutineFactory)
    day = factory.fuzzy.FuzzyChoice(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"])
    created_at = factory.fuzzy.FuzzyDateTime(datetime(2022, 5, 4, tzinfo=timezone('Asia/Seoul')))
    modified_at = factory.fuzzy.FuzzyDateTime(datetime(2022, 5, 4, tzinfo=timezone('Asia/Seoul')))

