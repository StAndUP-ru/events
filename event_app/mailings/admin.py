from django.contrib import admin

# from mailings.models import TopEvents


# @admin.register(TopEvents)
# class TopArticleAdmin(admin.ModelAdmin):
#     list_display = (
#         'event',
#         'event_author',
#     )

#     def get_queryset(self, request):
#         return TopEvents.objects.select_related('event', 'event__author')

#     @admin.display()
#     def event_author(self, obj):
#         return obj.event.author
