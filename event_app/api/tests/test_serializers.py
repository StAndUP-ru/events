from django.test import Client, TestCase

from .fixtures import EventFactory, UserFactory, request_user_token
from events.models import Event


class TestEventViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        EventFactory.create(title='Test event past 1', datetime='2010-10-10 00:00:00')
        EventFactory.create(title='Test event past 2', datetime='2015-10-10 00:00:00')
        EventFactory.create(title='Test event future 1', datetime='2025-10-10 00:00:00')
        EventFactory.create(title='Test event future 2', datetime='2030-10-10 00:00:00')
        EventFactory.create(title='Test event scheduled', event_status='scheduled')
        EventFactory.create(title='Test event canceled', event_status='canceled', datetime='2025-10-10 00:00:00')

    def setUp(self):
        self.client = Client()

    def test_event_format(self):
        event = Event.objects.first()
        response = self.client.get(f'/api/v1/events/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['format'], event.get_format_display())

    def test_event_registration_status(self):
        event = Event.objects.first()
        response = self.client.get(f'/api/v1/events/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['registration_status'], event.get_registration_status_display())

    def test_event_my_participation_unauthorized(self):
        event = Event.objects.first()
        response = self.client.get(f'/api/v1/events/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['my_participation']['result'])
        self.assertEqual(response.json()['my_participation']['detailed_result'], 'Not authenticated')

    def test_event_my_participation_no_registration(self):
        event = Event.objects.first()
        UserFactory.create(email='notparticipant@example.com')

        user_token = request_user_token(self.client, 'notparticipant@example.com')
        response = self.client.get(f'/api/v1/events/{event.id}/', HTTP_AUTHORIZATION=f'Token {user_token}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['my_participation']['result'])
        self.assertEqual(response.json()['my_participation']['detailed_result'], 'Not registered')

    def test_event_my_participation_with_registration(self):
        event = Event.objects.first()
        UserFactory.create(email='participant@example.com')

        user_token = request_user_token(self.client, 'participant@example.com')
        self.client.post(f'/api/v1/events/{event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {user_token}')
        response = self.client.get(f'/api/v1/events/{event.id}/', HTTP_AUTHORIZATION=f'Token {user_token}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['my_participation']['result'])
        self.assertEqual(response.json()['my_participation']['detailed_result'], 'Registered')
        self.assertEqual(response.json()['my_participation']['data']['participant'], 'participant@example.com')


class TestEventRegistrationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        EventFactory.create(participant_limit=2)
        cls.event = Event.objects.first()
        cls.client = Client()
        UserFactory.create(email="firstparticipant@example.com")
        UserFactory.create(email="secondparticipant@example.com")
        UserFactory.create(email="attemptparticipant@example.com")
        cls.firstparticipant_token = request_user_token(cls.client, "firstparticipant@example.com")
        secondparticipant_token = request_user_token(cls.client, "secondparticipant@example.com")
        cls.attemptparticipant_token = request_user_token(cls.client, "attemptparticipant@example.com")
        cls.client.post(f'/api/v1/events/{cls.event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {cls.firstparticipant_token}')
        cls.client.post(f'/api/v1/events/{cls.event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {secondparticipant_token}')

    def test_event_registration_unauthorized(self):
        response = self.client.post(f'/api/v1/events/{self.event.id}/registrations/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_event_registration_max_attempts(self):
        response = self.client.post(f'/api/v1/events/{self.event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {self.attemptparticipant_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], 'Достигнуто максимальное количество участников')

    def test_event_registration_already_registered(self):
        response = self.client.post(f'/api/v1/events/{self.event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {self.firstparticipant_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'][0], 'Вы уже зарегистрированы на это событие')

    def test_event_registration_cancel_successful(self):
        registration_id = self.client.get(f'/api/v1/events/{self.event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {self.firstparticipant_token}').json()['results'][0]['id']
        response = self.client.delete(f'/api/v1/events/{self.event.id}/registrations/{registration_id}/', HTTP_AUTHORIZATION=f'Token {self.firstparticipant_token}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(self.event.registrations.filter(id=registration_id).exists())

    def test_event_registration_successful(self):
        self.event.participant_limit = 3
        self.event.save()
        response = self.client.post(f'/api/v1/events/{self.event.id}/registrations/', HTTP_AUTHORIZATION=f'Token {self.attemptparticipant_token}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['participant'], 'attemptparticipant@example.com')
