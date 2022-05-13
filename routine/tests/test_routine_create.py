from .test_routine import RoutineTest
from routine.response_data_form import *


class RoutineCreateTest(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineCreateTest, cls).setUpClass()

    def test_create_routine(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        expected_response = ResponseDataForm(ResponseStatusEnum.CREATE_OK, ResponseMessageEnum.MSG_CREATE).get_form
        response = self.client.post('/api/v1/routines/', request_data)
        self.assertEqual(response.data['message'], expected_response['message'])
        routine_id = response.data['data']['routine_id']
        get_response = self.client.get(f'/api/v1/routines/?routine_id={routine_id}')
        expected_response = ResponseDataForm(ResponseStatusEnum.DETAIL_OK, ResponseMessageEnum.MSG_DETAIL).get_form
        expected_response['data'] = {
            'result': 'NOT',
            'goal': request_data['goal'],
            'routine_id': routine_id,
            'title': request_data['title'],
            'days': request_data['days']
        }
        self.assertDictEqual(get_response.data, expected_response)

    def test_create_routine_with_wrong_category(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data['category'] = 'ABCD'
        expected_response = 'This field must be HOMEWORK or MIRACLE'
        response = self.client.post('/api/v1/routines/', request_data)
        self.assertContains(response, expected_response, status_code=400)

        today = self.datetime.strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/routines/?today={today}')
        data = response.data['data']
        self.assertEqual([], data)

    def test_create_routine_with_wrong_day(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data['days'] = ['FID', 'TUE', 'ABC']
        expected_response = 'This is not a day'
        response = self.client.post('/api/v1/routines/', request_data)
        self.assertContains(response, expected_response, status_code=400)

        today = self.datetime.strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/routines/?today={today}')
        data = response.data['data']
        self.assertEqual([], data)

    def test_create_routine_with_no_day(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data.pop('days')
        expected_response = 'This field is required'
        response = self.client.post('/api/v1/routines/', request_data)
        self.assertContains(response, expected_response, status_code=400)

        today = self.datetime.strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/routines/?today={today}')
        data = response.data['data']
        self.assertEqual([], data)

    def test_create_routine_with_alarm_integer(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data['is_alarm'] = 2
        expected_response = 'Must be a valid boolean'
        response = self.client.post('/api/v1/routines/', request_data)
        self.assertContains(response, expected_response, status_code=400)

        today = self.datetime.strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/routines/?today={today}')
        data = response.data['data']
        self.assertEqual([], data)
