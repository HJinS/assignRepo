import datetime

from .test_routine import RoutineTest


class TestRoutineList(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(TestRoutineList, cls).setUpClass()

    def test_get_routine_list(self):
        self.client.force_authenticate(user=self.user)
        today = self.datetime.today().strftime('%Y-%m-%d')
        self.create_routine(2)
        response = self.client.get(f'/api/v1/routines/?today={today}')
        self.assertContains(response, 'ROUTINE_LIST_OK', status_code=200)
        self.assertGreaterEqual(len(response.data), 1)
        expected_data_key = "routine_id"
        self.assertContains(response, expected_data_key, status_code=200)

    def test_get_routine_list_future(self):
        self.client.force_authenticate(user=self.user)
        self.create_routine(2)
        today = self.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        response = self.client.get(f'/api/v1/routines/?today={tomorrow}')
        expected_response = "Can't get future's result"
        self.assertContains(response, expected_response, status_code=400)