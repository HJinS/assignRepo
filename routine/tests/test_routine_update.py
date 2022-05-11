from .test_routine import RoutineTest
from routine_user.tests.user_factory import UserFactory


class RoutineUpdateTest(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineUpdateTest, cls).setUpClass()

    def test_update_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_partial()
        response = self.client.patch(f'/api/v1/routine/{routine.routine_id}', request_data)
        self.assertContains(response, "ROUTINE_UPDATE_OK", status_code=200)
        request_data = self.get_update_request_data_full()
        response = self.client.patch(f'/api/v1/routine/{routine.routine_id}', request_data)
        self.assertContains(response, "ROUTINE_UPDATE_OK", status_code=200)

    def test_update_routine_with_wrong_category(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_full()
        request_data["category"] = "TSSEODJ"
        expected_response = "This field must be HOMEWORK or MIRACLE"
        response = self.client.patch(f'/api/v1/routine/{routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_update_routine_with_wrong_days(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_full()
        request_data["days"] = ["FRI", "SUN", "JSI"]
        expected_response = "This is not a day"
        response = self.client.patch(f'/api/v1/routine/{routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_update_routine_with_is_alarm_str(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        request_data = self.get_update_request_data_full()
        request_data["is_alarm"] = "fjidf"
        expected_response = "Must be a valid boolean"
        response = self.client.patch(f'/api/v1/routine/{routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_update_routine_another_users_routine(self):
        self.client.force_authenticate(user=self.user)
        another_user = UserFactory.create()
        routine = self.create_routine(2, another_user)
        request_data = self.get_update_request_data_full()
        expected_response = "No data"
        response = self.client.patch(f'/api/v1/routine/{routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)
