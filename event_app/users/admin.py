from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = (
        'id',
        'email',
        'full_name',
        'registrations',
        'employer',
        'occupation',
        'profile_full',
    )
    list_filter = ('experience', 'consent_personal_data_processing',
                   'preferred_format', 'consent_vacancy_data_processing',
                   'consent_random_coffee')
    fieldsets = (('Пользователь', {'fields': (('email', 'first_name', 'last_name', 'phone', 'role'),
                                            ('employer', 'occupation', 'experience', 'specialization'),
                                            'preferred_format',
                                            ('consent_personal_data_processing',
                                             'consent_personal_data_date',
                                             'consent_vacancy_data_processing',
                                             'consent_vacancy_data_date',
                                             'consent_random_coffee'),
                                             ('is_active', 'date_joined'), 'profile_full', 'password', 'is_staff', 'groups')}),)
    
    readonly_fields = ('date_joined', 'profile_full')
    search_fields = ('email__startswith', 'full_name')
    ordering = ('id',)
    list_display_links = ('email',)

    @admin.display(description='Полное имя')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description='Кол-во мероприятий')
    def registrations(self, obj):
        return obj.registrations.count()
    
    @admin.display(boolean=True, description='Анкета заполнена')
    def profile_full(self, obj):
        return obj.profile_full
