from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_doctor(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        return self.create_user(username, password, **extra_fields)

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=255, blank=True)
    genotype = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    marital_status = models.CharField(max_length=255, blank=True)
    allergies = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

