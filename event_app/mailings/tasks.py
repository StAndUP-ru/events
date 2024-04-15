from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# from mailings.models import TopEvents
from users.models import User


# @shared_task
# def send_weekly_email():
#     top_events = TopEvents.objects.select_related('event').values_list(
#         'event__title',
#         'event__pk',
#     )
#     links_events = []
#     for title_event, id__event in top_events:
#         links_events.append(
#             {
#                 'title': title_event,
#                 'url': f'{settings.URL_EVENTS}{id__event}',
#             },
#         )
#     template_name = 'email_weekly.html'
#     context = {
#         'links_events': links_events,
#     }
#     html_message = render_to_string(template_name, context)
#     recipient_list = list(
#         User.objects.filter(
#             subscribed=True,
#         ).values_list(
#             'email',
#             flat=True,
#         ),
#     )
#     subject = settings.WEEKLY_SUBJECT
#     from_email = settings.EMAIL_HOST_USER

#     for recipient_email in recipient_list:
#         email = EmailMultiAlternatives(
#             subject=subject,
#             from_email=from_email,
#             to=[recipient_email],
#         )
#         email.attach_alternative(html_message, 'text/html')
#         email.send()
