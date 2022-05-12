from routine_user.tests.user_factory import UserFactory
from .test_routine import RoutineTest
from uuid import uuid4

class RoutineDeleteTest(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineDeleteTest, cls).setUpClass()

    def test_delete_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        response = self.client.delete(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertContains(response, 'ROUTINE_DELETE_OK', status_code=200)

        routine_id = routine.routine_id
        response = self.client.get(f'/api/v1/routines/?routine_id={routine_id}')
        data = response.data
        self.assertEqual("Invalid data", data)

    def test_delete_routine_with_wrong_routine_id(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        expected_data = 'Invalid data'
        response = self.client.delete('/api/v1/routines/?routine_id=1824427')
        self.assertEqual(expected_data, response.data)

        routine_id = routine.routine_id
        response = self.client.get(f'/api/v1/routines/?routine_id={routine_id}')
        data = response.data['data']['routine_id']
        self.assertEqual(type(data), type(uuid4()))

    def test_delete_routine_another_users_routine(self):
        self.client.force_authenticate(user=self.user)
        another_user = UserFactory.create()
        routine = self.create_routine(2, another_user)
        expected_data = 'No data'
        response = self.client.delete(f'/api/v1/routines/?routine_id={routine.routine_id}')
        self.assertEqual(expected_data, response.data)

        self.client.logout()
        self.client.force_authenticate(user=another_user)

        routine_id = routine.routine_id
        response = self.client.get(f'/api/v1/routines/?routine_id={routine_id}')
        data = response.data['data']['routine_id']
        self.assertEqual(type(data), type(uuid4()))
