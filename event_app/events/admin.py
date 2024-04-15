from django.contrib import admin

from .models import Event, EventRegistration, Speaker, Subevent


class EventRegistrationInline(admin.options.InlineModelAdmin):
    template = 'admin/edit_inline/yandex_events_inline.html'
    model = EventRegistration
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'datetime',
        'registered',
        'registration_status',
        'organizer_name',
        'organizer_contacts',
        'description',
        'format',
        'participant_limit',
        'location_address',
        'location_coordinates',
        'image',
        'published_date',
        'host_photo',
        'host_full_name',
        'host_contacts',
        'host_company',
        'host_position',
        'event_link',
        'recording_link',
        'recording_link_start_date',
        'recording_link_end_date',
        'online_stream_link',
        'online_stream_link_start_date',
        'online_stream_link_end_date',
    )

    inlines = (EventRegistrationInline,)

    def registered(self, obj):
        return obj.registrations.count()


@admin.register(Subevent)
class SubeventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'time',
        'event',
        'speaker',
    )


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'company',
        'contacts',
        'position',
        'photo',
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'participant',
        'event',
        'registration_date',
        'approved',
    )
    list_filter = (
        'event',
        'participant',
        'registration_date')
    search_fields = (
        'event__title',
        'participant__email',
        'participant__first_name',
        'participant__last_name',)
