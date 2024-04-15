from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from events.models import Event, EventRegistration, Photo, Speaker, Subevent


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
    subevents = SubeventSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    my_participation = serializers.SerializerMethodField()
    registration_status = serializers.SerializerMethodField()
    format = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)


    class Meta:
        model = Event
        exclude = ['participants']

    def get_registration_status(self, obj):
        return obj.get_registration_status_display()
    
    def get_format(self, obj):
        return obj.get_format_display()
        

    def get_participant_count(self, obj):
        return obj.registrations.count()
    
    def get_my_participation(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return EventRegistration.objects.filter(event=obj, participant=user).exists()
        return "Not authenticated"


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
        return EventRegistration.objects.create(approved=True, **validated_data) # Stub for now
    
    def validate(self, attrs):
        event_id = self.context['view'].kwargs.get('event_id')
        user = self.context['request'].user
        if EventRegistration.objects.filter(event=event_id, participant=user).exists():
            raise serializers.ValidationError('Вы уже зарегистрированы на это событие')
        return super().validate(attrs)
