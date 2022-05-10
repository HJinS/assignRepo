from .test_user import UserTest


class TestRoutineUserLogin(UserTest):

    @classmethod
    def setUpClass(cls):
        super(TestRoutineUserLogin, cls).setUpClass()

    def test_routine_user_register(self):
        request_data = self.get_user_register_request()
        response = self.client.post('/api/routine-user', request_data)
        expected_response = "access_token"
        self.assertContains(response, expected_response, status_code=201)

    def test_routine_user_register_with_short_password(self):
        request_data = self.get_user_register_request()
        request_data["password1"] = "abcd2"
        request_data["password2"] = "abcd2"
        expected_response = "This password is too short. It must contain at least 8 characters."
        response = self.client.post('/api/routine-user', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register_with_different_password_1_2(self):
        request_data = self.get_user_register_request()
        request_data["password2"] = "sdhfdhdhih19!"
        expected_response = "The two password fields didn't match."
        response = self.client.post('/api/routine-user', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register_with_no_special_word(self):
        request_data = self.get_user_register_request()
        request_data["password1"] = "abcddihdihd213"
        request_data["password2"] = "abcddihdihd213"
        expected_response = "The password must contain at least 1 symbol"
        response = self.client.post('/api/routine-user', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_register_with_no_digit(self):
        request_data = self.get_user_register_request()
        request_data["password1"] = "abcddihdihd!@#"
        request_data["password2"] = "abcddihdihd!@#"
        expected_response = "The password must contain at least 1 digit"
        response = self.client.post('/api/routine-user', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine-user', request_data)
        self.client.logout()
        expected_response = "access_token"
        request_data = self.get_user_login_request()
        response = self.client.post('/api/routine-user/login/', request_data)
        self.assertContains(response, expected_response, status_code=200)

    def test_routine_user_login_with_wrong_password(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        request_data['password'] = 'hr992'
        expected_response = "non_field_errors"
        response = self.client.post('/api/routine-user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login_with_wrong_email(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        request_data['email'] = 'wrong_email@email.com'
        expected_response = "non_field_errors"
        response = self.client.post('/api/routine-user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login_with_no_password(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        del request_data['password']
        expected_response = "This field is required"
        response = self.client.post('/api/routine-user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_routine_user_login_with_no_email(self):
        request_data = self.get_user_register_request()
        self.client.post('/api/routine_user', request_data)
        self.client.logout()
        request_data = self.get_user_login_request()
        del request_data['email']
        expected_response = "non_field_errors"
        response = self.client.post('/api/routine-user/login/', request_data)
        self.assertContains(response, expected_response, status_code=400)
