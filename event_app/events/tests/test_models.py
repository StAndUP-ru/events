from django.db.utils import IntegrityError
from django.test import Client, TestCase

from events.admin import EventAdmin
from events.models import Event, EventRegistration, Photo, Speaker, Subevent
from users.models import User


class EventModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.event = Event.objects.create(
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

    def test_title_label(self):
        field_label = self.event._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_event_status_label(self):
        field_label = self.event._meta.get_field('event_status').verbose_name
        self.assertEqual(field_label, 'Статус')

    def test_registration_status_label(self):
        field_label = self.event._meta.get_field('registration_status').verbose_name
        self.assertEqual(field_label, 'Статус регистрации')

    def test_description_label(self):
        field_label = self.event._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Описание')

    def test_datetime_label(self):
        field_label = self.event._meta.get_field('datetime').verbose_name
        self.assertEqual(field_label, 'Дата и время начала')

    def test_location_address_label(self):
        field_label = self.event._meta.get_field('location_address').verbose_name
        self.assertEqual(field_label, 'Место проведения')

    def test_location_coordinates_label(self):
        field_label = self.event._meta.get_field('location_coordinates').verbose_name
        self.assertEqual(field_label, 'Координаты места проведения')

    def test_format_label(self):
        field_label = self.event._meta.get_field('format').verbose_name
        self.assertEqual(field_label, 'Формат')

    def test_organizer_name_label(self):
        field_label = self.event._meta.get_field('organizer_name').verbose_name
        self.assertEqual(field_label, 'Название организатора')

    def test_organizer_contacts_label(self):
        field_label = self.event._meta.get_field('organizer_contacts').verbose_name
        self.assertEqual(field_label, 'Контакты организатора')

    def test_participants_limit_label(self):
        field_label = self.event._meta.get_field('participant_limit').verbose_name
        self.assertEqual(field_label, 'Лимит участников')

    def test_host_full_name_label(self):
        field_label = self.event._meta.get_field('host_full_name').verbose_name
        self.assertEqual(field_label, 'ФИО ведущего')

    def test_host_contacts_label(self):
        field_label = self.event._meta.get_field('host_contacts').verbose_name
        self.assertEqual(field_label, 'Контакты ведущего')

    def test_host_company_label(self):
        field_label = self.event._meta.get_field('host_company').verbose_name
        self.assertEqual(field_label, 'Компания ведущего')

    def test_host_position_label(self):
        field_label = self.event._meta.get_field('host_position').verbose_name
        self.assertEqual(field_label, 'Должность ведущего')

    def test_event_link_label(self):
        field_label = self.event._meta.get_field('event_link').verbose_name
        self.assertEqual(field_label, 'Ссылка на событие')

    def test_recording_link_label(self):
        field_label = self.event._meta.get_field('recording_link').verbose_name
        self.assertEqual(field_label, 'Ссылка на запись')

    def test_recording_link_start_date_label(self):
        field_label = self.event._meta.get_field('recording_link_start_date').verbose_name
        self.assertEqual(field_label, 'Начало срока ссылки записи')

    def test_recording_link_end_date_label(self):
        field_label = self.event._meta.get_field('recording_link_end_date').verbose_name
        self.assertEqual(field_label, 'Конец срока ссылки записи')

    def test_online_stream_link_label(self):
        field_label = self.event._meta.get_field('online_stream_link').verbose_name
        self.assertEqual(field_label, 'Ссылка на онлайн-трансляцию')

    def test_online_stream_start_date_label(self):
        field_label = self.event._meta.get_field('online_stream_link_start_date').verbose_name
        self.assertEqual(field_label, 'Начало срока ссылки трансляции')

    def test_online_stream_end_date_label(self):
        field_label = self.event._meta.get_field('online_stream_link_end_date').verbose_name
        self.assertEqual(field_label, 'Конец срока ссылки трансляции')
    
    def test_verbose_name(self):
        self.assertEqual(str(Event._meta.verbose_name), 'Событие')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Event._meta.verbose_name_plural), 'События')

    def test_object_name_is_title(self):
        event = Event.objects.first()
        expected_object_name = event.title + ' - ' + str(event.datetime.date())
        self.assertEqual(expected_object_name, event.__str__())


class EventRegistrationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.event = Event.objects.create(
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
        cls.user = User.objects.create(
            email="test@example.com",
            password="testpassword")

        cls.event_registration = EventRegistration.objects.create(
            event=cls.event,
            participant=cls.user,
            approved=True)
        
    def test_event_label(self):
        field_label = self.event_registration._meta.get_field('event').verbose_name
        self.assertEqual(field_label, 'Событие, на которое регистрация')

    def test_participant_label(self):
        field_label = self.event_registration._meta.get_field('participant').verbose_name
        self.assertEqual(field_label, 'Пользователь, зарегистрировавшийся на событие')

    def test_approved_label(self):
        field_label = self.event_registration._meta.get_field('approved').verbose_name
        self.assertEqual(field_label, 'Регистрация подтверждена')

    def test_registration_date_label(self):
        field_label = self.event_registration._meta.get_field('registration_date').verbose_name
        self.assertEqual(field_label, 'Дата регистрации')

    def test_verbose_name(self):
        self.assertEqual(str(EventRegistration._meta.verbose_name), 'Регистрация')

    def test_verbose_name_plural(self):
        self.assertEqual(str(EventRegistration._meta.verbose_name_plural), 'Регистрации')

    def test_object_name_is_event_title(self):
        event_registration = EventRegistration.objects.first()
        expected_object_name = (f'{event_registration.registration_date.strftime("%d.%m.%Y %H:%M")}.'
                                f' {event_registration.participant} - {event_registration.event}.')
        self.assertEqual(expected_object_name, str(event_registration))

    def test_restrict_more_than_one_registration(self):
        self.assertRaises(IntegrityError, EventRegistration.objects.create,
                          event=self.event, participant=self.user, approved=True)


class SpeakerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.speaker = Speaker.objects.create(
            first_name='Test first name',
            last_name='Test last name',
            contacts='Test contacts',
            company='Test company',
            position='Test position',
            photo='www.testphoto.org'
        )

    def test_first_name_label(self):
        field_label = self.speaker._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'Имя')

    def test_last_name_label(self):
        field_label = self.speaker._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'Фамилия')

    def test_contacts_label(self):
        field_label = self.speaker._meta.get_field('contacts').verbose_name
        self.assertEqual(field_label, 'Контакты')

    def test_company_label(self):
        field_label = self.speaker._meta.get_field('company').verbose_name
        self.assertEqual(field_label, 'Компания')

    def test_position_label(self):
        field_label = self.speaker._meta.get_field('position').verbose_name
        self.assertEqual(field_label, 'Должность')

    def test_photo_label(self):
        field_label = self.speaker._meta.get_field('photo').verbose_name
        self.assertEqual(field_label, 'Фото')

    def test_object_name_is_full_name(self):
        expected_object_name = self.speaker.full_name
        self.assertEqual(expected_object_name, str(self.speaker))

    def test_fullname(self):
        expected_fullname = self.speaker.first_name + ' ' + self.speaker.last_name
        self.assertEqual(expected_fullname, self.speaker.full_name)

    def test_str(self):
        speaker = Speaker.objects.first()
        expected_str = speaker.first_name + ' ' + speaker.last_name
        self.assertEqual(expected_str, str(speaker))

    def test_verbose_name(self):
        self.assertEqual(str(Speaker._meta.verbose_name), 'Спикер')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Speaker._meta.verbose_name_plural), 'Спикеры')


class SubeventModelTest(TestCase):
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
        cls.subevent = Subevent.objects.create(
            title='Test subevent title',
            time='00:00:00',
            event=event,
            speaker=speaker
        )

    def test_title_label(self):
        field_label = self.subevent._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_time_label(self):
        field_label = self.subevent._meta.get_field('time').verbose_name
        self.assertEqual(field_label, 'Время начала')

    def test_event_label(self):
        field_label = self.subevent._meta.get_field('event').verbose_name
        self.assertEqual(field_label, 'Событие, в котором эта программа')

    def test_speaker_label(self):
        field_label = self.subevent._meta.get_field('speaker').verbose_name
        self.assertEqual(field_label, 'Спикер, участвующий в программе')

    def test_verbose_name(self):
        self.assertEqual(str(Subevent._meta.verbose_name), 'Часть программы события')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Subevent._meta.verbose_name_plural), 'Части программы события')

    def test_str(self):
        expected_str = self.subevent.title
        self.assertEqual(expected_str, str(self.subevent))


class EventAdminTest(TestCase):
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
        user = User.objects.create(
            email="test@example.com",
            password="testpassword#21",
            is_superuser=True,
            is_staff=True)
        user2 = User.objects.create(
            email="test2@example.com",
            password="testpassword#21",
        )
        EventRegistration.objects.create(
            event=event,
            participant=user,
            approved=True
        )
        EventRegistration.objects.create(
            event=event,
            participant=user2,
            approved=False
        )

    def test_registered_field(self):
        event = Event.objects.first()
        event_admin = EventAdmin(Event, None)
        self.assertEqual(event_admin.registered(event), 2)


class PhotoModelTest(TestCase):
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
        cls.photo = Photo.objects.create(
            event=event,
            image='www.testphoto.org'
        )

    def test_event_label(self):
        field_label = self.photo._meta.get_field('event').verbose_name
        self.assertEqual(field_label, 'Событие, к которому относится фотография')

    def test_image_label(self):
        field_label = self.photo._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'Фотография')

    def test_verbose_name(self):
        self.assertEqual(str(Photo._meta.verbose_name), 'Фотография')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Photo._meta.verbose_name_plural), 'Фотографии')

    def test_str(self):
        photo = Photo.objects.first()
        expected_str = photo.event.title + ' - ' + photo.image.name
        self.assertEqual(expected_str, str(photo))
