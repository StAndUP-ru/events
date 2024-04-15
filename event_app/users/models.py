from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Specialization(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Направление работы')
        verbose_name_plural = _('Направления работы')
    
class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    USER =  'user'
    ROLE_CHOICES = ((ADMIN, 'Admin'), (USER, 'User'))

    ONLINE = 'online'
    OFFLINE = 'offline'
    event_formats = ((ONLINE, 'Online'), (OFFLINE, 'Offline'))

    NO_EXPERIENCE = 'no_experience'
    MORE_1_YEAR = 'more_1_year'
    MORE_3_YEARS = 'more_3_years'
    MORE_5_YEARS = 'more_5_years'
    OTHER_EXPERIENCE = 'other_experience'
    experience_choices = ((NO_EXPERIENCE, 'Нет опыта'),
                          (MORE_1_YEAR, 'Более 1 года'),
                          (MORE_3_YEARS, 'Более 3 лет'),
                          (MORE_5_YEARS, 'More than 5 years'),
                          (OTHER_EXPERIENCE, 'Other experience'))

    email = models.EmailField(_('Адрес электронной почты'), unique=True, blank=False, null=False)
    password = models.CharField(_('Пароль'), max_length=128)
    first_name = models.CharField(_('Имя'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=150, blank=True, null=True)
    role = models.CharField(_('Роль'), max_length=5, choices=ROLE_CHOICES, default=USER)
    phone = models.CharField(_('Телефон'), max_length=15, blank=True, null=True)
    employer = models.CharField(_('Место работы'), max_length=100, blank=True, null=True)
    occupation = models.CharField(_('Должность'), max_length=100, blank=True, null=True)
    experience = models.CharField(_('Опыт работы'), max_length=20, choices=experience_choices, default=NO_EXPERIENCE)
    specialization = models.ManyToManyField(Specialization, verbose_name=_('Направление'), blank=True)
    preferred_format = models.CharField(_('Предпочитаемый формат'), max_length=10, choices=event_formats, default=ONLINE)
    consent_personal_data_processing = models.BooleanField(_('Согласие об обработке персональных данных'), default=False)
    consent_personal_data_date = models.DateTimeField(_('Дата согласия об обработке персональных данных'), blank=True, null=True)
    consent_vacancy_data_processing = models.BooleanField(_('Согласие об обработке персональных данных для предложения вакансий'), default=False)
    consent_vacancy_data_date = models.DateTimeField(_('Дата согласия об обработке персональных данных для предложения вакансий'), blank=True, null=True)
    consent_random_coffee = models.BooleanField(_('Согласие на участие в Random Coffee'), default=False)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
    
    @property
    def profile_full(self):
        fields = ['first_name', 'last_name', 'phone', 'employer',
                  'occupation', 'experience', 'specialization',
                  'preferred_format', 'consent_personal_data_processing']
        for field in fields:
            if not getattr(self, field):
                return False
        return True
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    
