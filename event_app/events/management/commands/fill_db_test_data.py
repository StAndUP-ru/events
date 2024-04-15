from datetime import datetime, timedelta
import pytz
from random import randint, choice

from django.core.management.base import BaseCommand

from event_app.settings import TIME_ZONE
from events.models import Event, EventRegistration, Speaker, Subevent
from users.models import User

class Command(BaseCommand):
    help = 'Fill db with test data'
    NAMES = ['John', 'Mike', 'Alice', 'Bob', 'Kate', 'Tom', 'Sara', 'Bill', 'Linda', 'Jack']
    SURNAMES = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']
    COMPANIES = ['Google', 'Apple', 'Microsoft', 'Amazon', 'Facebook', 'Twitter', 'Instagram', 'TikTok', 'Snapchat', 'LinkedIn']
    POSITION = ['Developer', 'Designer', 'Manager', 'Director', 'CEO', 'CTO', 'CFO', 'COO', 'CIO', 'CISO']
    EVENT_SECTIONS = ['Business', 'Technology', 'Science', 'Art', 'Education', 'Health', 'Sport', 'Music', 'Cinema', 'Literature']
    EVENT_TOPIC = ['New technologies', 'Business strategies', 'Healthcare innovations', 'Artificial intelligence', 'Space exploration',
                   'Music industry', 'Cinema production', 'Literature trends', 'Sport achievements', 'Education methods']
    SECTION_NAMES = ['Local management', 'IT Reliability', 'Household appliances', 'Space exploration', 'Music industry',
                     "Escaping from library", "Sport achievements", "Education methods", "Healthcare innovations", "Artificial intelligence"]
    GUEST_NAMES = ['Иван', 'Петр', 'Сергей', 'Александр', 'Андрей', 'Дмитрий', 'Михаил', 'Алексей', 'Владимир', 'Николай']
    GUEST_SURNAMES = ['Иванов', 'Петров', 'Сидоров', 'Александров', 'Андреев', 'Дмитриев', 'Михайлов', 'Алексеев', 'Владимиров', 'Николаев']
    


    def _get_random_datetime(self, upcoming=True):
        now = datetime.now(tz=pytz.timezone(TIME_ZONE))
        if upcoming:
            return datetime(now.year, (now.month + randint(0, 4)) % 12, randint(1, 28),
                            randint(14, 22), randint(0, 59), tzinfo=pytz.timezone(TIME_ZONE))
        else:
            return datetime(now.year - 1, randint(1, 12), randint(1, 28),
                            randint(14, 22), randint(0, 59), tzinfo=pytz.timezone(TIME_ZONE))
        
    def _create_speakers(self, count):
        for i in range(count):
            Speaker.objects.create(
                first_name=choice(self.NAMES),
                last_name=choice(self.SURNAMES),
                company=choice(self.COMPANIES),
                contacts=f'Contacts {i}',
                position=choice(self.POSITION),
            )
        
    def _create_subevents_with_speakers(self, event, count):
        total_speakers = Speaker.objects.count()
        for i in range(count):
            Subevent.objects.create(
                title=choice(self.SECTION_NAMES),
                time=event.datetime + timedelta(hours=i),
                event=event,
                speaker=Speaker.objects.get(id=randint(1, total_speakers))
            )


    def _create_events(self, count, subevents_count=3, upcoming=True):
        for i in range(count):
            event = Event.objects.create(
                title=choice(self.EVENT_SECTIONS) + ': ' + choice(self.EVENT_TOPIC),
                description=choice(self.EVENT_SECTIONS) + ': ' + choice(self.EVENT_TOPIC) + ' new visions',
                datetime=self._get_random_datetime(upcoming),
                format='online',
                event_status='on_time',
                participant_limit=randint(10, 10000),
                location_address='Moscow, Arbat street, 1',
                location_coordinates='55.733836, 37.588140',
                image='Image',
                host_photo='Host photo',
                host_full_name=choice(self.NAMES) + ' ' + choice(self.SURNAMES),
                host_contacts=f'No contacts',
                host_company=choice(self.COMPANIES),
                host_position=choice(self.POSITION),
                event_link='Event link',
            )
            self._create_subevents_with_speakers(event, subevents_count)

    def _create_users_and_registrations(self, count):
        total_events = Event.objects.count()
        for i in range(count):
            user = User.objects.create(
                email=f'user{i}@example.com',
                first_name=choice(self.GUEST_NAMES),
                last_name=choice(self.GUEST_SURNAMES),
                password='12345678!#Aa',
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            self._create_event_registrations(user, randint(0, 10), total_events)
    
    def _create_event_registrations(self, user, count, total_events):
        if count == 0 or total_events == 0:
            return
        for i in range(count):
            EventRegistration.objects.get_or_create(
                participant=user,
                event=Event.objects.get(id=randint(1, total_events)),
                approved=True
            )


    def handle(self, *args, **options):
        self._create_speakers(10)
        self._create_events(15, subevents_count=randint(2, 5), upcoming=True)
        self._create_events(15, subevents_count=randint(2, 5), upcoming=False)
        self._create_users_and_registrations(100)
        self.stdout.write(self.style.SUCCESS('Data filled successfully'))
