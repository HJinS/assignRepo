from .test_routine import RoutineTest


class RoutineCreateTest(RoutineTest):

    @classmethod
    def setUpClass(cls):
        super(RoutineCreateTest, cls).setUpClass()

    def test_create_routine(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()

        response = self.client.post('/api/v1/routine', request_data)
        self.assertContains(response, "ROUTINE_CREATE_OK", status_code=201)

    def test_create_routine_with_wrong_category(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data["category"] = "ABCD"
        expected_response = "This field must be HOMEWORK or MIRACLE"
        response = self.client.post('/api/v1/routine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_create_routine_with_wrong_day(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data["days"] = ["FID", "TUE", "ABC"]
        expected_response = f'This is not a day'
        response = self.client.post('/api/v1/routine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_create_routine_with_no_day(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data.pop("days")
        expected_response = f'This field is required'
        response = self.client.post('/api/v1/routine', request_data)
        self.assertContains(response, expected_response, status_code=400)

    def test_create_routine_with_alarm_integer(self):
        self.client.force_authenticate(user=self.user)
        request_data = self.get_create_request_data()
        request_data["is_alarm"] = 2
        expected_response = f'Must be a valid boolean'
        response = self.client.post('/api/v1/routine', request_data)
        self.assertContains(response, expected_response, status_code=400)
