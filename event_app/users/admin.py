from django.contrib import admin

from .models import User, Specialization

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'full_name',
        'employer',
        'occupation',
        'consent_personal_data_processing',
        'profile_full',
    )
    list_filter = ('experience', 'consent_personal_data_processing',
                   'preferred_format', 'consent_vacancy_data_processing',
                   'consent_random_coffee')
    search_fields = ('email__startswith', 'full_name')
    ordering = ('id',)
    list_display_links = ('email',)

    @admin.display(description='Полное имя')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
