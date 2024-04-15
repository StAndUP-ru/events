from datetime import datetime
import pytz

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from event_app.settings import TIME_ZONE
from events.models import Event, EventRegistration, Speaker
from api.serializers import (EventSerializer, EventRegistrationSerializer,
                             SubeventSerializer, SpeakerSerializer)
from api.pagination import CustomPagination, CustomUserPagination


class EventViewSet(viewsets.ModelViewSet):
    '''
    Представление для работы с мероприятиями.
    '''
    serializer_class = EventSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.action == 'list':
            if self.request.query_params.get('status') == 'upcoming':
                now = datetime.now(tz=pytz.timezone(TIME_ZONE))
                return Event.objects.filter(event_status='on_time', datetime__gt=now).order_by('datetime')
            elif self.request.query_params.get('status') == 'past':
                now = datetime.now(tz=pytz.timezone(TIME_ZONE))
                return Event.objects.filter(event_status='on_time', datetime__lte=now).order_by('-datetime')
            elif self.request.query_params.get('status') == 'scheduled':
                return Event.objects.filter(event_status='scheduled')
            elif self.request.query_params.get('status') == 'canceled':
                return Event.objects.filter(event_status='canceled')
        return Event.objects.all()
            


class SubeventViewSet(viewsets.ModelViewSet):
    '''
    Представление для работы с программой мероприятия.
    '''
    serializer_class = SubeventSerializer

    def get_queryset(self):
        queryset = get_object_or_404(Event, id=self.kwargs.get('event_id'))
        return queryset.subevents.all()


class SpeakerViewSet(viewsets.ModelViewSet):
    '''
    Представление для работы со спикером
    '''
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class EventRegistrationViewSet(viewsets.ModelViewSet):
    '''
    Представление для работы с регистрациями на мероприятие.
    '''
    serializer_class = EventRegistrationSerializer
    pagination_class = CustomUserPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_admin:
            return EventRegistration.objects.filter(event_id=self.kwargs.get('event_id'))
        return EventRegistration.objects.filter(participant=self.request.user, event_id=self.kwargs.get('event_id'))
    
    def perform_create(self, serializer):
        if not self.request.user.profile_full:
            raise ValidationError('Заполните все поля профиля') # custom error handling
        event = Event.objects.get(id=self.kwargs.get('event_id'))
        serializer.save(event=event, participant=self.request.user)
