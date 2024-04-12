from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


class Event(models.Model):
    '''
    Модель события.
    '''

    EVENT_STATUS_CHOICES = [
            ('on_time', 'По расписанию'),
            ('scheduled', 'Запланировано'),
            ('cancelled', 'Отменено'),
        ]

    REGISTRATION_STATUS_CHOICES = [
            ('not_started', 'Регистрация еще не началась'),
            ('open', 'Идет регистрация'),
            ('closed', 'Регистрация закрыта'),
        ]

    FORMAT_CHOICES = [
            ('online', 'Онлайн'),
            ('offline', 'Офлайн'),
        ]

    title = models.CharField(
        max_length=100,
        verbose_name='Название события'
    )
    event_status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS_CHOICES,
        verbose_name='Статус события'
    )
    registration_status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS_CHOICES,
        verbose_name='Статус регистрации'
    )
    organizer_name = models.CharField(
        max_length=100,
        verbose_name='Название организатора'
    )
    organizer_contacts = models.CharField(
        max_length=100,
        verbose_name='Контакты организатора'
    )
    description = models.TextField(
        verbose_name='Описание события'
    )
    datetime = models.DateTimeField(
        verbose_name='Дата и время начала события'
    )
    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        verbose_name='Формат события'
    )
    participant_limit = models.PositiveIntegerField(
        verbose_name='Лимит участников'
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Участники события'
    )
    location_address = models.CharField(
        max_length=200,
        verbose_name='Место проведения события',
        blank=True,
        null=True
    )
    location_coordinates = models.CharField(
        max_length=100,
        verbose_name='Координаты места проведения события',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='events/image/',
        verbose_name='Обложка события',
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    host_photo = models.ImageField(
        upload_to='events/hosts/image/',
        verbose_name='Фото ведущего',
        blank=True,
        null=True
    )
    host_full_name = models.CharField(
        max_length=100,
        verbose_name='ФИО ведущего'
    )
    host_contacts = models.CharField(
        max_length=100,
        verbose_name='Контакты ведущего'
    )
    host_company = models.CharField(
        max_length=100,
        verbose_name='Компания ведущего'
    )
    host_position = models.CharField(
        max_length=100,
        verbose_name='Должность ведущего'
    )
    event_link = models.URLField(
        max_length=200,
        verbose_name='Ссылка на событие'
    )
    recording_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Ссылка на запись события'
    )
    recording_link_start_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Начало срока ссылки записи'
    )
    recording_link_end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Конец срока ссылки записи'
    )
    online_stream_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Ссылка на онлайн-трансляцию события'
    )
    online_stream_link_start_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Начало срока ссылки трансляции'
    )
    online_stream_link_end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Конец срока ссылки трансляции'
    )

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f"{self.title} - {self.datetime.date()}"


class Speaker(models.Model):
    '''
    Модель для спикера.
    '''
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя спикера'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия спикера'
    )
    company = models.CharField(
        max_length=100,
        verbose_name='Компания спикера',
        blank=True,
        null=True
    )
    contacts = models.CharField(
        max_length=100,
        verbose_name='Контакты спикера'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность спикера',
        blank=True,
        null=True
    )
    photo = models.ImageField(
        upload_to='events/speakers/image/',
        verbose_name='Фото спикера',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Спикер'
        verbose_name_plural = 'Спикеры'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Subevent(models.Model):
    '''
    Модель для части программы события.
    '''

    title = models.CharField(
        max_length=100,
        verbose_name='Название программы'
    )
    time = models.TimeField(
        verbose_name='Время начала программы'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='subevents',
        verbose_name='Событие, в котором эта программа'
    )

    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.CASCADE,
        related_name='subevents',
        verbose_name='Спикер, участвующий в программе'
    )

    class Meta:
        verbose_name = 'Часть программы'
        verbose_name_plural = 'Части программы'

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    '''
    Модель для регистрации на событие.
    '''

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Событие, на которое регистрация',
        null=False, blank=False,
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Пользователь, зарегистрировавшийся на событие',
        null=False, blank=False
    )
    registration_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    approved = models.BooleanField(
        default=False,
        verbose_name='Регистрация подтверждена'
    )

    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'
        constraints = [
            models.UniqueConstraint(fields=['event', 'participant'], name='unique_registration')
        ]

    def __str__(self):
        return f'{self.registration_date.strftime("%d.%m.%Y %H:%M")}. {self.participant} - {self.event}.'
