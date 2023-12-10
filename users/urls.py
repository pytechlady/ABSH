from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import *

router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')
router.register(r'auth', AuthenticationViewset, basename='auth')
router.register(r'staff', DoctorViewset, basename='doctor')
router.register(r'staff-auth', DocAuthenticationViewSet, basename='doc-auth')

urlpatterns = [
    path('', include(router.urls)),
]