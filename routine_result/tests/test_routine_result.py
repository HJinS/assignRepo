from rest_framework.test import APIClient, APITestCase
from routine.tests.routine_factory import RoutineFactory
from routine_day.routine_day_factory import RoutineDayFactory
from routine_result.tests.routine_result_factory import RoutineResultFactory
from routine_user.tests.user_factory import UserFactory
from datetime import datetime
from pytz import timezone


class RoutineResultTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(RoutineResultTest, cls).setUpClass()
        cls.client = APIClient()
        cls.user = UserFactory.create()
        cls.datetime = datetime.now(timezone('Asia/Seoul'))

    def create_routine(self, routine_cnt, user=None):
        if user is None:
            user = self.user
        for _ in range(routine_cnt):
            routine = RoutineFactory.create(account_id=user)
            routine_result = RoutineResultFactory.create(routine_id=routine)
            RoutineDayFactory.create_batch(3, routine_id=routine)
        return [routine, routine_result]

    def get_update_request_data(self):
        request_data = {
            'result': 'DONE'
        }
        return request_data
