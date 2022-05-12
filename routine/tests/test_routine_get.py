from .test_routine import RoutineTest


class RoutineDeleteTest(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineDeleteTest, cls).setUpClass()

    def test_get_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        response = self.client.get(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertContains(response, 'ROUTINE_DETAIL_OK', status_code=200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_routine_with_or_wrong_routine_id(self):
        self.client.force_authenticate(user=self.user)
        self.create_routine(2)
        response = self.client.get('/api/v1/routines/?routine_id=29282')
        expected_data = 'Invalid data'
        self.assertEqual(expected_data, response.data)
