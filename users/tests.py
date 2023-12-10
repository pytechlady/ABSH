from django.test import TestCase

# Create your tests here.

# Path: users/tests.py
# Compare this snippet from config/urls.py:
"""config URL Configuration
"""

from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')), # new
]
# Compare this snippet from users/tests.py:
from django.urls import reverse
from rest_framework import status

from users.models import User

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(email= "hello@test.com", password= "test1234")
        
    def test_patient_registration(self):
        data = {
            'email': 'hello@test.com',
            'password': 'test1234'
        }
        response = self.client.post(reverse('users:register_patients'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'User created successfully')
        
    def test_doctor_registration(self):
        data = {
            'email': 'hello_doctor@test.com',
            'password': 'test1234'
        }
        response = self.client.post(reverse('users:register_doctors'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Doctor account created successfully')
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['is_doctor'], True)
        self.assertEqual(response.data['data']['is_staff'], True)
        
    def test_nurse_registration(self):
        data = {
            'email': 'hello_nurse@example.com',
            'password': 'test1234'
        }
        response = self.client.post(reverse('users:register_nurses'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Nurse account created successfully')
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['is_nurse'], True)
        self.assertEqual(response.data['data']['is_staff'], True)
        
    def test_admin_registration(self):
        data = {
            'email': 'hello_admin@example.com',
            'password': 'test1234'
        }
        response = self.client.post(reverse('user:register_admin'), data)
        self.assertEqual(response.data['message'], 'Admin account created successfully')
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['is_registrar'], True)
        self.assertEqual(response.data['data']['is_staff'], True)
        
        
        
