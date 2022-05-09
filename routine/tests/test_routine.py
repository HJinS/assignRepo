from rest_framework.test import APIClient, APITestCase
from ..tests.routine_factory import RoutineFactory
from routine_day.routine_day_factory import RoutineDayFactory
from routine_result.routine_result_factory import RoutineResultFactory
from routine_user.user_factory import UserFactory
from datetime import datetime


class RoutineTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(RoutineTest, cls).setUpClass()
        cls.client = APIClient()
        cls.user = UserFactory.create()

    def create_routine(self, routine_cnt):
        for _ in range(routine_cnt):
            routine = RoutineFactory.create(account_id=self.user)
            RoutineResultFactory.create(routine_id=routine)
            RoutineDayFactory.create_batch(3, routine_id=routine)
        return routine

    def get_create_request_data(self):
        request_data = {
            "title": "test_title",
            "category": "MIRACLE",
            "goal": "test_goal",
            "is_alarm": False,
            "days": ["MON", "TUE", "WED"]
        }
        return request_data

    def get_routine_list_request_data(self, today):
        request_data = {
            "account_id": self.user.id,
            "today": today
        }
        return request_data

    def get_routine_request_data_or_delete_request_data(self, routine_id):
        request_data = {
            "account_id": self.user.id,
            "routine_id": routine_id
        }
        return request_data

    def get_update_request_data_partial(self, routine_id):
        request_data = {
            "routine_id": routine_id,
            "title": "new title for test",
            "category": "HOMEWORK"
        }
        return request_data

    def get_update_request_data_full(self, routine_id):
        request_data = {
            "routine_id": routine_id,
            "title": "second new title for test",
            "category": "HOMEWORK",
            "goal": "new goal",
            "is_alarm": False,
            "days": ["FRI", "SUN"]
        }
        return request_data

    def get_user_register_request(self):
        request_data = {
            "email": "user@example.com",
            "password1": "password123!@#$",
            "password2": "password123!@#$"
        }
        return request_data

    def get_user_login_request(self):
        requests_data = {
            "email": "user@example.com",
            "password": "password123!@#$"
        }
        return requests_data

    def test_create_routine(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()

        response = self.client.post('/api/routine/createRoutine', request_data)
        self.assertContains(response, "ROUTINE_CREATE_OK", status_code=201)

    def test_create_routine_with_wrong_category(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data["category"] = "ABCD"
        expected_response = "This field must be HOMEWORK or MIRACLE"
        response = self.client.post('/api/routine/createRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_create_routine_with_wrong_day(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data["days"] = ["FID", "TUE", "ABC"]
        expected_response = f'This is not a day'
        response = self.client.post('/api/routine/createRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_create_routine_with_no_day(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data.pop("days")
        expected_response = f'This field is required'
        response = self.client.post('/api/routine/createRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_create_routine_with_alarm_integer(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data["is_alarm"] = 2
        expected_response = f'Must be a valid boolean'
        response = self.client.post('/api/routine/createRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_get_routine_list(self):
        self.client.force_authenticate(user=self.user)
        today = datetime.today().strftime('%Y-%m-%d')
        self.create_routine(2)
        request_data = self.get_routine_list_request_data(today)
        response = self.client.post('/api/routine/getRoutineList', request_data)
        self.assertContains(response, "ROUTINE_LIST_OK", status_code=200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_routine_list_with_wrong_account_id(self):
        self.client.force_authenticate(user=self.user)
        today = datetime.today().strftime('%Y-%m-%d')
        self.create_routine(2)
        request_data = self.get_routine_list_request_data(today)
        request_data["account_id"] = 123456229
        expected_data = {
            'data': [],
            'message': {
                'msg': '루틴 조회 성공', 'status': 'ROUTINE_LIST_OK'
            }
        }
        response = self.client.post('/api/routine/getRoutineList', request_data)
        self.assertDictEqual(expected_data, response.data)

    def test_get_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_routine_request_data_or_delete_request_data(routine.routine_id)
        response = self.client.post('/api/routine/getRoutine', request_data)
        self.assertContains(response, "ROUTINE_DETAIL_OK", status_code=200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_routine_with_wrong_account_id_or_wrong_routine_id(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_routine_request_data_or_delete_request_data(routine.routine_id)
        request_data["account_id"] = 2039387
        expected_data = {
            'data': [],
            'message': {
                'msg': '루틴 조회 성공', 'status': 'ROUTINE_DETAIL_OK'
            }
        }
        response = self.client.post('/api/routine/getRoutine', request_data)
        self.assertDictEqual(expected_data, response.data)
        request_data['account_id'] = self.user.id
        request_data['routine_id'] = 2932692
        response = self.client.post('/api/routine/getRoutine', request_data)
        self.assertDictEqual(expected_data, response.data)

    def test_delete_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_routine_request_data_or_delete_request_data(routine.routine_id)
        response = self.client.post('/api/routine/deleteRoutine', request_data)
        self.assertContains(response, "ROUTINE_DELETE_OK", status_code=200)

    def test_delete_routine_with_wrong_account_id(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_routine_request_data_or_delete_request_data(routine.routine_id)
        request_data["account_id"] = 25418924
        expected_data = "Invalid data"
        response = self.client.post('/api/routine/deleteRoutine', request_data)
        self.assertEqual(expected_data, response.data)

    def test_delete_routine_with_wrong_routine_id(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_routine_request_data_or_delete_request_data(routine.routine_id)
        request_data["routine_id"] = 345678
        expected_data = "Invalid data"
        response = self.client.post('/api/routine/deleteRoutine', request_data)
        self.assertEqual(expected_data, response.data)

    def test_delete_routine_with_another_users_routine(self):
        self.client.force_authenticate(user=self.user)
        another_user = UserFactory.create()
        routine = self.create_routine(2)
        request_data = self.get_routine_request_data_or_delete_request_data(routine.routine_id)
        request_data["account_id"] = another_user.id
        expected_data = "Invalid data"
        response = self.client.post('/api/routine/deleteRoutine', request_data)
        self.assertEqual(expected_data, response.data)

    def test_update_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_partial(routine.routine_id)
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, "ROUTINE_UPDATE_OK", status_code=200)

        request_data = self.get_update_request_data_full(routine.routine_id)
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, "ROUTINE_UPDATE_OK", status_code=200)

    def test_update_routine_with_wrong_category(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_full(routine.routine_id)
        request_data["category"] = "TSSEODJ"
        expected_response = "This field must be HOMEWORK or MIRACLE"
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_update_routine_with_wrong_days(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_full(routine.routine_id)
        request_data["days"] = ["FRI", "SUN", "JSI"]
        expected_response = "This is not a day"
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_update_routine_with_is_alarm_str(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_full(routine.routine_id)
        request_data["is_alarm"] = "fjidf"
        expected_response = "Must be a valid boolean"
        response = self.client.post('/api/routine/updateRoutine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register(self):
        request_data = self.get_user_register_request()
        response = self.client.post('/api/routine_user/', request_data)
        expected_response = "access_token"
        self.assertContains(response, expected_response, status_code=201)

    def test_routine_user_register_with_short_password(self):
        request_data = self.get_user_register_request()
        request_data["password1"] = "abcd2"
        request_data["password2"] = "abcd2"
        expected_response = "This password is too short. It must contain at least 8 characters."
        response = self.client.post('/api/routine_user/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register_with_different_password_1_2(self):
        request_data = self.get_user_register_request()
        request_data["password2"] = "sdhfdhdhih19!"
        expected_response = "The two password fields didn't match."
        response = self.client.post('/api/routine_user/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register_with_no_special_word(self):
        request_data = self.get_user_register_request()
        request_data["password1"] = "abcddihdihd213"
        request_data["password2"] = "abcddihdihd213"
        expected_response = "The password must contain at least 1 symbol"
        response = self.client.post('/api/routine_user/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register_with_no_digit(self):
        request_data = self.get_user_register_request()
        request_data["password1"] = "abcddihdihd!@#"
        request_data["password2"] = "abcddihdihd!@#"
        expected_response = "The password must contain at least 1 digit"
        response = self.client.post('/api/routine_user/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user/', request_data)
        self.client.logout()
        expected_response = "access_token"
        request_data = self.get_user_login_request()
        response = self.client.post('/api/routine_user/login/', request_data)
        self.assertContains(response, expected_response, status_code=200)

    def test_routine_user_login_with_wrong_password(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user/', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        request_data['password'] = 'hr992'
        expected_response = "non_field_errors"
        response = self.client.post('/api/routine_user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login_with_wrong_email(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user/', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        request_data['email'] = 'wrong_email@email.com'
        expected_response = "non_field_errors"
        response = self.client.post('/api/routine_user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login_with_no_password(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user/', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        del request_data['password']
        expected_response = "This field is required"
        response = self.client.post('/api/routine_user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login_with_no_email(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user/', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        del request_data['email']
        expected_response = "non_field_errors"
        response = self.client.post('/api/routine_user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

