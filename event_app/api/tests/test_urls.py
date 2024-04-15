from django.test import Client, TestCase

from events.models import Event, Speaker, Subevent


class TestUrls(TestCase):
    @classmethod
    def setUpTestData(cls):
        event = Event.objects.create(
            title='Test event',
            event_status='on_time',
            registration_status='open',
            description='Test description',
            datetime='2021-10-10 00:00:00',
            location_address='Test address',
            location_coordinates='Test coordinates',
            format='online',
            organizer_name='Test organizer',
            organizer_contacts='Test contacts',
            participant_limit=100,
            host_full_name='Test host',
            host_contacts='Test host contacts',
            host_company='Test company',
            host_position='Test position',
            event_link='www.testlink.org',
            recording_link='www.testrecordinglink.org',
            recording_link_start_date='2021-10-10 00:00:00',
            recording_link_end_date='2021-10-10 00:00:00',
            online_stream_link='www.teststreamlink.org',
            online_stream_link_start_date='2021-10-10 00:00:00',
            online_stream_link_end_date='2021-10-10 00:00:00'
        )
        speaker = Speaker.objects.create(
            first_name='Test first name',
            last_name='Test last name',
            contacts='Test contacts',
            company='Test company',
            position='Test position',
            photo='www.testphoto.org'
        )
        Subevent.objects.create(
            title='Test subevent title',
            time='00:00:00',
            event=event,
            speaker=speaker
        )

    def setUp(self):
        self.client = Client()

    def test_event_list_url(self):
        response = self.client.get('/api/v1/events/')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_url(self):
        response = self.client.get('/api/v1/events/1/')
        self.assertEqual(response.status_code, 200)

    def test_subevent_list_url(self):
        response = self.client.get('/api/v1/events/1/subevents/')
        self.assertEqual(response.status_code, 200)

    def test_subevent_detail_url(self):
        response = self.client.get('/api/v1/events/1/subevents/1/')
        self.assertEqual(response.status_code, 200)

    def test_speaker_list_url(self):
        response = self.client.get('/api/v1/speakers/')
        self.assertEqual(response.status_code, 200)

    def test_speaker_detail_url(self):
        response = self.client.get('/api/v1/speakers/1/')
        self.assertEqual(response.status_code, 200)
