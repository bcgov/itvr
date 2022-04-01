from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.viewsets.application_form import ApplicationFormViewset

ROUTER = routers.DefaultRouter()
ROUTER.register(r'application-form', ApplicationFormViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(ROUTER.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
