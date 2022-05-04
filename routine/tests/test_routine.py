from rest_framework.test import APIClient, APITestCase
from ..tests.routine_factory import RoutineFactory
from routine_day.routine_day_factory import RoutineDayFactory
from routine_result.routine_result_factory import RoutineResultFactory
from user.user_factory import UserFactory


class RoutineTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(RoutineTest, cls).setUpClass()
        cls.client = APIClient()
        cls.user = UserFactory.create()

    def test_create_routine(self):
        self.client.force_authenticate(user=self.user)
        request_data = {
            "title": "test_title",
            "category": "MIRACLE",
            "goal": "test_goal",
            "is_alarm": False,
            "days": ["MON", "TUE", "WED"]
        }
        response = self.client.post('/api/routine/createRoutine', request_data)
        self.assertContains(response, "ROUTINE_CREATE_OK", status_code=201)

    def test_get_routine_list(self):
        self.client.force_authenticate(user=self.user)
        for _ in range(2):
            routine = RoutineFactory.create(account_id=self.user)
            routine_result = RoutineResultFactory.create(routine_id=routine)
            routine_day = RoutineDayFactory.create_batch(3, routine_id=routine)
        request_data = {
            "account_id": self.user.account_id,
            "today": "2022-05-04"
        }
        response = self.client.post('/api/routine/getRoutineList', request_data)
        self.assertContains(response, "ROUTINE_LIST_OK", status_code=200)

    def test_get_routine(self):
        self.client.force_authenticate(user=self.user)
        for _ in range(2):
            routine = RoutineFactory.create(account_id=self.user)
            routine_result = RoutineResultFactory.create(routine_id=routine)
            routine_day = RoutineDayFactory.create_batch(3, routine_id=routine)
        request_data = {
            "account_id": self.user.account_id,
            "routine_id": routine.routine_id
        }
        response = self.client.post('/api/routine/getRoutine', request_data)
        self.assertContains(response, "ROUTINE_DETAIL_OK", status_code=200)

    def test_delete_routine(self):
        self.client.force_authenticate(user=self.user)
        for _ in range(2):
            routine = RoutineFactory.create(account_id=self.user)
            routine_result = RoutineResultFactory.create(routine_id=routine)
            routine_day = RoutineDayFactory.create_batch(3, routine_id=routine)
        request_data = {
            "account_id": self.user.account_id,
            "routine_id": routine.routine_id
        }

        response = self.client.post('/api/routine/deleteRoutine', request_data)
        self.assertContains(response, "ROUTINE_DELETE_OK", status_code=200)

    def test_update_routine(self):
        self.client.force_authenticate(user=self.user)
        for _ in range(2):
            routine = RoutineFactory.create(account_id=self.user)
            routine_result = RoutineResultFactory.create(routine_id=routine)
            routine_day = RoutineDayFactory.create_batch(3, routine_id=routine)

        request_data = {
            "routine_id": routine.routine_id,
            "title": "new title for test",
            "category": "HOMEWORK"
        }
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, "ROUTINE_UPDATE_OK", status_code=200)

        request_data = {
            "routine_id": routine.routine_id,
            "title": "second new title for test",
            "category": "HOMEWORK",
            "goal": "new goal",
            "is_alarm": False,
            "days": ["FRI", "SUN"]
        }
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, "ROUTINE_UPDATE_OK", status_code=200)
