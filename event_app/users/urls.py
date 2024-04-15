from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import UserViewSet

schema_view = get_schema_view(
       openapi.Info(
           title="Event.funtech",
           default_version='v1',
           description="API description",
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
   )

router = DefaultRouter()
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
