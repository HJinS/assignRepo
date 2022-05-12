from rest_framework.test import APIClient, APITestCase
from ..tests.routine_factory import RoutineFactory
from routine_day.routine_day_factory import RoutineDayFactory
from routine_result.routine_result_factory import RoutineResultFactory
from routine_user.tests.user_factory import UserFactory
from datetime import datetime
from pytz import timezone


class RoutineTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(RoutineTest, cls).setUpClass()
        cls.client = APIClient()
        cls.user = UserFactory.create()
        cls.datetime = datetime.now(timezone('Asia/Seoul'))

    def create_routine(self, routine_cnt, user=None):
        if user is None:
            user = self.user
        for _ in range(routine_cnt):
            routine = RoutineFactory.create(account_id=user)
            RoutineResultFactory.create(routine_id=routine)
            RoutineDayFactory.create_batch(3, routine_id=routine)
        return routine

    def get_create_request_data(self):
        request_data = {
            'title': 'test_title',
            'category': 'MIRACLE',
            'goal': 'test_goal',
            'is_alarm': False,
            'days': ['MON', 'TUE', 'WED', 'THU', 'FRI']
        }
        return request_data

    def get_update_request_data_full(self):
        request_data = {
            'title': 'test_title',
            'category': 'MIRACLE',
            'goal': 'test_goal',
            'is_alarm': False,
            'days': ['MON', 'TUE', 'WED']
        }
        return request_data

    def get_update_request_data_partial(self):
        request_data = {
            'title': 'new title for test',
            'category': 'HOMEWORK'
        }
        return request_data
