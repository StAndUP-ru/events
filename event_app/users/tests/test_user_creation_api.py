from django.test import Client, TestCase, override_settings

from users.models import Specialization, User


class UserApiCreationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            "email": "user3@example.com",
            "password": "usertestpasSW1#",
        }
        
    def test_user_creation(self):
        self.client.post('/api/v1/users/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.email, self.user_data['email'])

    def test_user_creation_fail(self):
        self.client.post('/api/v1/users/', self.user_data)
        response = self.client.post('/api/v1/users/', self.user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['email'][0], 'Пользователь с таким Адрес электронной почты уже существует.')
        response = self.client.post('/api/v1/users/', {"email": "abc", "password": "usertestpasSW1#"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['email'][0], 'Введите правильный адрес электронной почты.')

    def test_user_creation_password_fail(self):
        email = "user4@example.com"
        response = self.client.post('/api/v1/users/', {"email": email, "password": "password"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['password'][0], 'Введённый пароль слишком широко распространён.')
        response = self.client.post('/api/v1/users/', {"email": email, "password": email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['password'][0], 'Введённый пароль слишком похож на Адрес электронной почты.')
        response = self.client.post('/api/v1/users/', {"email": email, "password": "pass"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Введённый пароль слишком короткий.', response.json()['password'][0])
        user_found = User.objects.filter(email="user4@example.com").exists()
        self.assertFalse(user_found)

class UserApiTokenTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "email": "user4@example.com",
            "password": "usertestpasSW1#",
        }

    @override_settings(DJOSER={'SEND_ACTIVATION_EMAIL': False})
    def test_user_is_active(self):
        self.client.post('/api/v1/users/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.is_active, True)

    @override_settings(DJOSER={'SEND_ACTIVATION_EMAIL': False})
    def test_get_user_token(self):
        self.client.post('/api/v1/users/', self.user_data)
        response = self.client.post('/api/v1/auth/token/login/', self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.json())


class UserApiUpdateTestCase(TestCase):
    @classmethod
    @override_settings(DJOSER={'SEND_ACTIVATION_EMAIL': False})
    def setUpClass(cls):
        Specialization.objects.get_or_create(name='TestSpecialization')
        Specialization.objects.get_or_create(name='TestSpecialization2')
        cls.user_data = {
            "email": "user5@example.com",
            "password": "usertestpasSW1#",
        }
        cls.client = Client()
        response = cls.client.post('/api/v1/users/', cls.user_data)
        cls.user_id = response.json()['id']
        super().setUpClass()
    
    @override_settings(DJOSER={'SEND_ACTIVATION_EMAIL': False})
    def setUp(self):
        self.token = self.client.post('/api/v1/auth/token/login/', self.user_data).json()['auth_token']
    
    def test_user_request(self):
        response = self.client.get('/api/v1/users/me/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], self.user_data['email'])

    def test_user_request_no_token(self):
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, 401)

    def test_get_only_own_user(self):
        response = self.client.get('/api/v1/users/1/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], self.user_data['email'])

    def test_hide_other_user(self):
        response = self.client.get('/api/v1/users/2/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/api/v1/users/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['email'], self.user_data['email'])

    def test_user_patch_update(self):
        data = {
            "email": "user4@example.com",
            "password": "usertestpasSW1#",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
            "phone": "1234567890",
            "employer": "TestEmployer",
            "occupation": "TestOccupation",
            "experience": "more_1_year",
            "preferred_format": "offline",
            "consent_personal_data_processing": True,
            "consent_vacancy_data_processing": True,
            "consent_random_coffee": True,
            "specialization": ["TestSpecialization", "TestSpecialization2"]
        }
        response = self.client.patch(f'/api/v1/users/{self.user_id}/', data, HTTP_AUTHORIZATION=f'Token {self.token}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.role, data['role'])
        self.assertEqual(user.phone, data['phone'])
        self.assertEqual(user.employer, data['employer'])
        self.assertEqual(user.occupation, data['occupation'])
        self.assertEqual(user.experience, data['experience'])
        self.assertEqual(user.preferred_format, data['preferred_format'])
        self.assertEqual(user.consent_personal_data_processing, data['consent_personal_data_processing'])
        self.assertIsNotNone(user.consent_personal_data_date)
        self.assertEqual(user.consent_vacancy_data_processing, data['consent_vacancy_data_processing'])
        self.assertIsNotNone(user.consent_vacancy_data_date)
        self.assertEqual(user.consent_random_coffee, data['consent_random_coffee'])
        self.assertEqual(user.specialization.count(), 2)
        self.assertEqual(user.specialization.first().name, 'TestSpecialization')
        self.assertEqual(user.specialization.last().name, 'TestSpecialization2')
        self.assertEqual(user.profile_full, True)

    def test_patch_password(self):
        data = {
            "password": "usertestpasSW1#1"
        }
        response = self.client.patch(f'/api/v1/users/{self.user_id}/', data, HTTP_AUTHORIZATION=f'Token {self.token}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.json())
