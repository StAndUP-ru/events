from factory.django import DjangoModelFactory, Password

from events.models import Event, Speaker, Subevent
from users.models import User


def request_user_token(client, email):
    user_token = client.post('/api/v1/auth/token/login/',
                             {"email": email,
                             "password": "usertestpasSW1#"}
                             ).json()['auth_token']
    return user_token


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    title = f'Test event'
    event_status = 'on_time'
    registration_status = 'open'
    description = 'Test description'
    datetime = '2021-10-10 00:00:00'
    location_address = 'Test address'
    location_coordinates = 'Test coordinates'
    format = 'online'
    organizer_name = 'Test organizer'
    organizer_contacts = 'Test contacts'
    participant_limit = 100
    host_full_name = 'Test host'
    host_contacts = 'Test host contacts'
    host_company = 'Test company'
    host_position = 'Test position'
    event_link = 'www.testlink.org'
    recording_link = 'www.testrecordinglink.org'
    recording_link_start_date = '2021-10-10 00:00:00'
    recording_link_end_date = '2021-10-10 00:00:00'
    online_stream_link = 'www.teststreamlink.org'
    online_stream_link_start_date = '2021-10-10 00:00:00'
    online_stream_link_end_date = '2021-10-10 00:00:00'

class SpeakerFactory(DjangoModelFactory):
    class Meta:
        model = Speaker

    first_name = 'Test speaker first name'
    last_name = 'Test speaker last name'
    position = 'Test position'
    company = 'Test company'
    contacts = 'Test contacts'
    photo = 'www.testphoto.org'

class SubeventFactory(DjangoModelFactory):
    class Meta:
        model = Subevent

    title = 'Test subevent'
    time = '16:40:00'
    event: Event = None
    speaker: Speaker = None

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = 'testemail@example.com'
    password = Password('usertestpasSW1#')
    first_name = 'Test first name'
    last_name = 'Test last name'
    role = 'user'
    phone = 'Test phone'
    employer = 'Test employer'
    occupation = 'Test occupation'
    experience = 'no_experience'
    preferred_format = 'online'
    consent_personal_data_processing = True
    consent_personal_data_date = '2021-10-10 00:00:00'
    consent_vacancy_data_processing = True
    consent_vacancy_data_date = '2021-10-10 00:00:00'
    consent_random_coffee = True
    
    is_active = True
    is_staff = False
    is_superuser = False
