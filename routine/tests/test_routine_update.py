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
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        initial_response = initial_response.data
        initial_response['data']['title'] = request_data['title']

        response = self.client.patch(f'/api/v1/routines/?routine_id={routine.routine_id}', request_data)
        self.assertContains(response, 'ROUTINE_UPDATE_OK', status_code=200)
        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response, response.data)

        request_data = self.get_update_request_data_full()
        initial_response = response.data
        initial_response['data']['title'] = request_data['title']
        initial_response['data']['goal'] = request_data['goal']
        initial_response['data']['days'] = request_data['days']

        response = self.client.patch(f'/api/v1/routines/?routine_id={routine.routine_id}', request_data)
        self.assertContains(response, 'ROUTINE_UPDATE_OK', status_code=200)
        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response, response.data)

    def test_update_routine_with_wrong_category(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        request_data = self.get_update_request_data_full()
        request_data['category'] = 'TSSEODJ'
        expected_response = 'This field must be HOMEWORK or MIRACLE'
        response = self.client.patch(f'/api/v1/routines/?routine_id={routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response.data, response.data)

    def test_update_routine_with_wrong_days(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        request_data = self.get_update_request_data_full()
        request_data['days'] = ['FRI', 'SUN', 'JSI']
        expected_response = 'This is not a day'
        response = self.client.patch(f'/api/v1/routines/?routine_id={routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response.data, response.data)

    def test_update_routine_with_is_alarm_str(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        request_data = self.get_update_request_data_full()
        request_data['is_alarm'] = 'fjidf'
        expected_response = 'Must be a valid boolean'
        response = self.client.patch(f'/api/v1/routines/?routine_id={routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response.data, response.data)

    def test_update_routine_another_users_routine(self):
        another_user = UserFactory.create()
        routine = self.create_routine(2, another_user)
        self.client.force_authenticate(user=another_user)
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')

        self.client.logout()
        self.client.force_authenticate(user=self.user)

        request_data = self.get_update_request_data_full()
        expected_response = 'No data'
        response = self.client.patch(f'/api/v1/routines/?routine_id={routine.routine_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

        self.client.logout()
        self.client.force_authenticate(user=another_user)

        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response.data, response.data)
