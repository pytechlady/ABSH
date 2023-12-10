from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments.views import *

router = DefaultRouter()
router.register(r'appointment', Appointments, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]