from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length= 100,blank= False)
    last_name = models.CharField(max_length= 100,blank= False)
    phone_number = models.CharField(unique= True,max_length=10,blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_superuser = models.BooleanField(default=False) 
    email = models.EmailField(blank=True)
    is_manager = models.BooleanField(default=False) 
    password = models.CharField(max_length=100,blank= False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name','last_name','is_active','is_staff','is_superuser','email','is_manager','password']

    objects = UserManager()

    class Meta:
        verbose_name = "User Model"
        
    # [self.first_name,self.last_name,self.is_active,self.is_staff,self.is_superuser,self.email,self.security_access_level,self.password]
    def __str__(self):
        return self.phone_number