from django.db import models

from users.models import User


class Photo(models.Model):
    '''
    Модель для фотографии.
    '''

    image = models.ImageField(
        upload_to='events/photo/',
        verbose_name='Фотография',
        blank=False,
        null=False
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Событие, к которому относится фотография',
        null=False,
        blank=False
    )
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'{self.event.title} - {self.image.name}'


class Event(models.Model):
    '''
    Модель события.
    '''

    EVENT_STATUS_CHOICES = [
            ('on_time', 'По расписанию'),
            ('scheduled', 'Запланировано'),
            ('canceled', 'Отменено'),
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
        verbose_name='Название'
    )
    event_status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS_CHOICES,
        verbose_name='Статус'
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
        verbose_name='Описание'
    )
    datetime = models.DateTimeField(
        verbose_name='Дата и время начала',
        blank=True,
        null=True
    )
    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        verbose_name='Формат'
    )
    participant_limit = models.PositiveIntegerField(
        verbose_name='Лимит участников'
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Участники'
    )
    location_address = models.CharField(
        max_length=200,
        verbose_name='Место проведения',
        blank=True,
        null=True
    )
    location_coordinates = models.CharField(
        max_length=100,
        verbose_name='Координаты места проведения',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='events/image/',
        verbose_name='Обложка события',
        blank=True,
        null=True
    )
    banner = models.ImageField(
        upload_to='events/banner/',
        verbose_name='Баннер события',
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
        verbose_name='Ссылка на событие',
        blank=True,
        null=True
    )
    recording_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Ссылка на запись'
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
        verbose_name='Ссылка на онлайн-трансляцию'
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
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    company = models.CharField(
        max_length=100,
        verbose_name='Компания',
        blank=True,
        null=True
    )
    contacts = models.CharField(
        max_length=100,
        verbose_name='Контакты'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность',
        blank=True,
        null=True
    )
    photo = models.ImageField(
        upload_to='events/speakers/image/',
        verbose_name='Фото',
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
        verbose_name='Название'
    )
    time = models.TimeField(
        verbose_name='Время начала'
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
        verbose_name = 'Программа события'
        verbose_name_plural = 'Программы событий'

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
        verbose_name='Участник события',
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
