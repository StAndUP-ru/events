from django.core.mail import send_mail
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from events.models import Event, EventRegistration, Photo, Speaker, Subevent
from event_app.settings import DEFAULT_FROM_EMAIL


class SpeakerSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для спикера.
    '''
    subevent = serializers.StringRelatedField(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(validators=[RegexValidator(
        regex=r'^[a-zA-Zа-яА-Я]+$',
        message='Имя может содержать только русские либо латинские буквы!')])
    last_name = serializers.CharField(validators=[RegexValidator(
        regex=r'^[a-zA-Zа-яА-Я\-]+$',
        message='Фамилия может содержать только русские либо латинские'
                ' буквы, а также тире!')])
    contacts = serializers.CharField(
        validators=[UniqueValidator(queryset=Speaker.objects.all())]
    )

    class Meta:
        model = Speaker
        fields = '__all__'

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class SubeventSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для части программы.
    '''
    event = serializers.StringRelatedField(read_only=True)
    speaker = SpeakerSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Subevent


class PhotoSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для фото.
    '''
    class Meta:
        model = Photo
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для мероприятия.
    '''
    subevents = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    my_participation = serializers.SerializerMethodField()
    event_status = serializers.SerializerMethodField()
    registration_status = serializers.SerializerMethodField()
    format = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)


    class Meta:
        model = Event
        exclude = ['participants']

    def get_subevents(self, obj):
        ordered_queryset = obj.subevents.order_by('time')
        return SubeventSerializer(ordered_queryset,
                                  many=True,
                                  read_only=True,
                                  context=self.context).data

    def get_registration_status(self, obj):
        return obj.get_registration_status_display()
    
    def get_event_status(self, obj):
        return obj.get_event_status_display()
    
    def get_format(self, obj):
        return obj.get_format_display()
        

    def get_participant_count(self, obj):
        return obj.registrations.count()
    
    def get_my_participation(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            queryset = EventRegistration.objects.filter(event=obj, participant=user)
            if queryset.exists():
                return {"result": True,
                        "detailed_result": "Registered",
                        "data": EventRegistrationSerializer(queryset.first()).data}
            return {"result": False,
                    "detailed_result": "Not registered"}
        return {"result": False,
                "detailed_result": "Not authenticated"}


class EventRegistrationSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для регистрации на мероприятие.
    '''
    event = serializers.StringRelatedField(read_only=True)
    participant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EventRegistration
        fields = '__all__'
        read_only_fields = ['approved']

    def create(self, validated_data):
        current_count = EventRegistration.objects.filter(event=validated_data['event']).count()
        if current_count >= validated_data['event'].participant_limit:
            raise serializers.ValidationError('Достигнуто максимальное количество участников')
        if validated_data['event'].registration_status != 'open':
            raise serializers.ValidationError('Регистрация на это мероприятие невозможна в данный момент')
        msg_place = ("Событие пройдет онлайн\nДоступ по ссылке в описании события" 
                     if validated_data['event'].format == 'online'
                     else f"Место проведения: {validated_data['event'].location_address}")
        message=(f'Рады подтвердить ваше участие в предстоящем событии {validated_data["event"]}\n'
                 f'Дата: {validated_data["event"].datetime.strftime("%d.%m.%Y")}\n'
                 f'Время: {validated_data["event"].datetime.strftime("%H:%M")}\n'
                 f'{msg_place}\n\n'
                 f'Ссылка на событие: {validated_data["event"].event_link}\n\n'
                 f'С нетерпением ждем вас!\n\n'
                 f'С уважением, команда {validated_data["event"].organizer_name}'
                 )
        send_mail(
            subject=f'Подтверждение участия в событии {validated_data["event"]}',
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[validated_data['participant'].email],
            fail_silently=False,)
        return EventRegistration.objects.create(approved=True, **validated_data) # Stub for now
    
    def validate(self, attrs):
        event_id = self.context['view'].kwargs.get('event_id')
        user = self.context['request'].user
        if EventRegistration.objects.filter(event=event_id, participant=user).exists():
            raise serializers.ValidationError('Вы уже зарегистрированы на это событие')
        return super().validate(attrs)
