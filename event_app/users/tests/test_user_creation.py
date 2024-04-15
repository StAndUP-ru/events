from datetime import datetime
import pytz

from django.test import TestCase

from event_app.settings import TIME_ZONE
from users.models import Specialization, User, UserManager


class SpecializationCreationTestCase(TestCase):
    def setUp(self):
        Specialization.objects.create(name='TestSpecialization')

    def test_specialization_name(self):
        specialization = Specialization.objects.get(name='TestSpecialization')
        self.assertEqual(specialization.name, 'TestSpecialization')
        self.assertEqual(specialization.__str__(), 'TestSpecialization')

    def test_specialization_name_fail(self):
        specialization = Specialization.objects.get(name='TestSpecialization')
        self.assertNotEqual(specialization.name, 'TestSpecialization1')

class UserCreationBaseTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='testemail@example.com', password='usertestpasSW1#')
        with self.settings(TIME_ZONE='UTC'):
            User.objects.create(email='testemail2@example.com', password='usertestpasSW1#',
                                first_name='Test', last_name='User', role='user', phone='1234567890',
                                employer='TestEmployer', occupation='TestOccupation',
                                experience='more_1_year', preferred_format='offline',
                                consent_personal_data_processing=True, 
                                consent_personal_data_date=datetime(2021, 1, 5, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)),
                                consent_vacancy_data_processing=True,
                                consent_vacancy_data_date=datetime(2021, 1, 6, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)),
                                consent_random_coffee=True)

    def test_user_password(self):
        user = User.objects.get(email='testemail@example.com')
        self.assertEqual(user.password, 'usertestpasSW1#')

    def test_user_password_fail(self):
        user = User.objects.get(email='testemail@example.com')
        self.assertNotEqual(user.password, 'usertestpasSW1#1')

    def test_user_profile_full_fail(self):
        user = User.objects.get(email='testemail@example.com')
        self.assertEqual(user.profile_full, False)

    def test_user_info(self):
        user = User.objects.get(email='testemail2@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.employer, 'TestEmployer')
        self.assertEqual(user.occupation, 'TestOccupation')
        self.assertEqual(user.experience, 'more_1_year')
        self.assertEqual(user.preferred_format, 'offline')
        self.assertEqual(user.consent_personal_data_processing, True)
        self.assertEqual(user.consent_personal_data_date, datetime(2021, 1, 5, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)))
        self.assertEqual(user.consent_vacancy_data_processing, True)
        self.assertEqual(user.consent_vacancy_data_date, datetime(2021, 1, 6, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)))
        self.assertEqual(user.consent_random_coffee, True)
        self.assertEqual(user.__str__(), 'testemail2@example.com')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.profile_full, True)
        self.assertEqual(user.is_admin, False)


class UserCreationExtendedTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='testemail2@example.com', password='usertestpasSW1#')

    def test_user_uodate_info(self):
        User.objects.filter(email='testemail2@example.com').update(
            first_name='Test2', last_name='User2', role='user', phone='1234567800',
            employer='TestEmployer', occupation='TestOccupation',
            experience='more_1_year', preferred_format='offline',
            consent_personal_data_processing=True, 
            consent_personal_data_date=datetime(2021, 1, 5, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)),
            consent_vacancy_data_processing=True,
            consent_vacancy_data_date=datetime(2021, 1, 6, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)),
            consent_random_coffee=False)
        user = User.objects.get(email='testemail2@example.com')
        self.assertEqual(user.first_name, 'Test2')
        self.assertEqual(user.last_name, 'User2')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.phone, '1234567800')
        self.assertEqual(user.employer, 'TestEmployer')
        self.assertEqual(user.occupation, 'TestOccupation')
        self.assertEqual(user.experience, 'more_1_year')
        self.assertEqual(user.preferred_format, 'offline')
        self.assertEqual(user.consent_personal_data_processing, True)
        self.assertEqual(user.consent_personal_data_date, datetime(2021, 1, 5, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)))
        self.assertEqual(user.consent_vacancy_data_processing, True)
        self.assertEqual(user.consent_vacancy_data_date, datetime(2021, 1, 6, 0, 0, tzinfo=pytz.timezone(TIME_ZONE)))
        self.assertEqual(user.consent_random_coffee, False)


class CustomUserManagerTestCase(TestCase):
    def setUp(self):
        self.manager = UserManager()
        
    def test_create_user(self):
        user = User.objects.create_user("test0@example.com", "usertestpasSW1#")
        self.assertIsInstance(user, User)

    def test_create_user_fail(self):
        self.assertRaises(ValueError, User.objects.create_user, email="", password="usertestpasSW1#")

    def test_create_superuser(self):
        user = User.objects.create_superuser("test2@example.com", "usertestpasSW1#")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_fail(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser("", "usertestpasSW1#")
