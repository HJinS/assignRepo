from routine_user.tests.user_factory import UserFactory
from .test_routine import RoutineTest


class RoutineDeleteTest(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineDeleteTest, cls).setUpClass()

    def test_delete_routine(self):
        self.client.force_authenticate(user=self.user)
        routine = self.create_routine(2)
        response = self.client.delete(f'/api/v1/routine/{routine.routine_id}')
        self.assertContains(response, "ROUTINE_DELETE_OK", status_code=200)

    def test_delete_routine_with_wrong_routine_id(self):
        self.client.force_authenticate(user=self.user)
        self.create_routine(2)
        expected_data = "Invalid data"
        response = self.client.delete(f'/api/v1/routine/1824427')
        self.assertEqual(expected_data, response.data)

    def test_delete_routine_another_users_routine(self):
        self.client.force_authenticate(user=self.user)
        another_user = UserFactory.create()
        routine = self.create_routine(2, another_user)
        expected_data = "No data"
        response = self.client.delete(f'/api/v1/routine/{routine.routine_id}')
        self.assertEqual(expected_data, response.data)
