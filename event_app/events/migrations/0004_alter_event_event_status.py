# Generated by Django 5.0.3 on 2024-04-15 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_options_alter_subevent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.CharField(choices=[('on_time', 'По расписанию'), ('scheduled', 'Запланировано'), ('canceled', 'Отменено')], max_length=20, verbose_name='Статус'),
        ),
    ]