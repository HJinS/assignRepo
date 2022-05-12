from rest_framework.test import APIClient, APITestCase


class UserTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(UserTest, cls).setUpClass()
        cls.client = APIClient()

    def get_user_register_request(self):
        request_data = {
            'email': 'user@example.com',
            'password1': 'password123!@#$',
            'password2': 'password123!@#$'
        }
        return request_data

    def get_user_login_request(self):
        requests_data = {
            'email': 'user@example.com',
            'password': 'password123!@#$'
        }
        return requests_data
