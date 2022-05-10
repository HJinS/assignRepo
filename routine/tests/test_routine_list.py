from .test_routine import RoutineTest


class TestRoutineList(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(TestRoutineList, cls).setUpClass()

    def test_get_routine_list(self):
        self.client.force_authenticate(user=self.user)
        today = self.datetime.today().strftime('%Y-%m-%d')
        self.create_routine(2)
        response = self.client.get(f'/api/v1/routine?today={today}')
        self.assertContains(response, "ROUTINE_LIST_OK", status_code=200)
        self.assertGreaterEqual(len(response.data), 1)
