from enum import unique
from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserCustomerManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('Email should be provided'))
        email=self.normalize_email(email)
        new_user=self.model(email=email,**extra_fields)
        new_user.set_password(password)
        new_user.save()
        return new_user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('The superuser should be a staff'))
        
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('The superuser should be a active'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('This is for superuser only '))
        
        return self.create_superuser(email,password,**extra_fields)
    
    
class User(AbstractUser):
    
    Options={
        ('U','User'),
        ('P','Psychologists')
    }
    
    
    SignUp_as=models.CharField(choices=Options, max_length=100)
    full_name=models.CharField(default=True, max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    is_active=models.BooleanField(default=True)
    phone = models.IntegerField(blank=False)
    create_on=models.DateTimeField(auto_now_add=True)
    
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS= []
    objects=UserCustomerManager()
    
    def __str__(self):
        return f"<User {self.email}"