# Generated by Django 5.0.3 on 2024-04-12 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Участники мероприятия'),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.event', verbose_name='Событие, на которое регистрация'),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to=settings.AUTH_USER_MODEL, verbose_name='Зарегистрировавшийся пользователь'),
        ),
        migrations.AddField(
            model_name='event',
            name='speaker',
            field=models.ManyToManyField(related_name='events', to='events.speaker', verbose_name='Спикер части программы этого события'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subevents', to='events.event', verbose_name='Мероприятие, в котором эта программа'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subevents', to='events.speaker', verbose_name='Спикер, участвующий в части программы'),
        ),
        migrations.AddField(
            model_name='event',
            name='subevent',
            field=models.ManyToManyField(related_name='events', to='events.subevent', verbose_name='Часть программы события'),
        ),
        migrations.AddConstraint(
            model_name='eventregistration',
            constraint=models.UniqueConstraint(fields=('event', 'participant'), name='unique_registration'),
        ),
    ]