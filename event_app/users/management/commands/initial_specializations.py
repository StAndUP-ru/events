from django.core.management.base import BaseCommand

from users.models import Specialization

class Command(BaseCommand):
    help = 'Initial specializations'

    def handle(self, *args, **options):
        Specialization.objects.get_or_create(name='Backend', description='Разработка серверной части')
        Specialization.objects.get_or_create(name='Frontend', description='Разработка клиентской части')
        Specialization.objects.get_or_create(name='Mobile', description='Разработка мобильных приложений')
        Specialization.objects.get_or_create(name='QA', description='Тестирование программного обеспечения')
        Specialization.objects.get_or_create(name='ML', description='Машинное обучение')
        Specialization.objects.get_or_create(name='Other', description='Другое')
        print('Specializations created') # Add to log
