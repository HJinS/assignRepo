from .test_routine_result import RoutineResultTest
from routine_user.tests.user_factory import UserFactory
from ..models import RoutineResult

class RoutineResultUpdateTest(RoutineResultTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineResultUpdateTest, cls).setUpClass()

    def test_update_routine(self):
        self.client.force_authenticate(user=self.user)
        routine, routine_result = self.create_routine(2)

        request_data = self.get_update_request_data()
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        initial_response = initial_response.data
        initial_response['data']['result'] = request_data['result']

        response = self.client.patch(f'/api/v1/routine-results/?routine_result_id={routine_result.routine_result_id}', request_data)
        self.assertContains(response, 'ROUTINE_UPDATE_OK', status_code=200)
        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        response_data = response.data
        self.assertEqual(initial_response['data']['result'], response_data['data']['result'])

    def test_update_routine_with_wrong_result(self):
        self.client.force_authenticate(user=self.user)
        routine, routine_result = self.create_routine(2)
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        request_data = self.get_update_request_data()
        request_data['result'] = 'ABC'
        expected_response = 'Invalid data'
        response = self.client.patch(f'/api/v1/routine-results/?routine_result_id={routine_result.routine_result_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response.data, response.data)

    def test_update_routine_with_another_users_result(self):
        another_user = UserFactory.create()
        routine, routine_result = self.create_routine(2, another_user)

        self.client.force_authenticate(user=another_user)
        initial_response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')

        self.client.logout()
        self.client.force_authenticate(user=self.user)
        request_data = self.get_update_request_data()
        expected_response = 'No data'
        response = self.client.patch(f'/api/v1/routine-results/?routine_result_id={routine_result.routine_result_id}', request_data)
        self.assertContains(response, expected_response, status_code=400)

        self.client.logout()
        self.client.force_authenticate(user=another_user)

        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertDictEqual(initial_response.data, response.data)

    def test_update_routine_with_try_another_field(self):
        self.client.force_authenticate(user=self.user)
        routine, routine_result = self.create_routine(2)

        request_data = self.get_update_request_data()
        request_data['modified_at'] = '2022-05-12'
        initial_date = routine_result.modified_at.strftime('%Y-%m-%d')

        response = self.client.patch(f'/api/v1/routine-results/?routine_result_id={routine_result.routine_result_id}', request_data)
        self.assertContains(response, 'ROUTINE_UPDATE_OK', status_code=200)

        query_set = RoutineResult.objects.get(routine_id__account_id=self.user.id, routine_result_id=routine_result.routine_result_id)
        self.assertEqual(initial_date, query_set.modified_at.strftime('%Y-%m-%d'))
