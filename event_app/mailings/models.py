from django.db import models
from django.utils.translation import gettext_lazy as _

# from events.models import Event


# class TopEvents(models.Model):
#     event = models.OneToOneField(
#         Event,
#         verbose_name=_('TopEvent'),
#         related_name='top_event',
#         on_delete=models.CASCADE,
#     )

#     class Meta:
#         verbose_name = _('TopEvent')
#         verbose_name_plural = _('TopEvents')
#         ordering = ('-pk',)

#     def __str__(self):
#         return f'TopEvent({self.event})'
