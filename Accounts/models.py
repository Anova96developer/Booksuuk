
from ast import mod
from email.headerregistry import Address
from lib2to3.pgen2 import token
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(("Email should be provided")) 
        else:
            email = self.normalize_email(email)
            
            new_user = self.model(email,**extra_fields)
            
            new_user.set_password(password)
            
            new_user.save()
            
            return new_user
        
    
    def create_superuser(self,email,password,**extra_fields):
       extra_fields.setdefault('is_staff',True)
       extra_fields.setdefault('is_superuser',True)
       extra_fields.setdefault('is_active',True)
       
       if extra_fields.get('is_staff') is not True:
           raise ValueError (("Super User should have is_staff as True"))
       
       if extra_fields.get('is_superuser') is not True:
           raise ValueError (("Super User should have is_superuser as True"))
    
    
       if extra_fields.get('is_active') is not True:
           raise ValueError (("Super User should have is_active as True"))
      
       return self.create_user(email,password,**extra_fields)
  
  
  
class User(AbstractUser):
    username =models.CharField(max_length=25,unique=True)
    email = models.EmailField(max_length=80,unique=True)
    token = models.CharField(max_length=60,unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    address = models.CharField(max_length=150)
    phone_number=PhoneNumberField(unique=True,null=False,blank=False)
    date_joined=models.DateTimeField(('Date'),auto_now_add=True)

    is_verified= models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','token','phone_number']
    
    objects: CustomUserManager ()
     
    def __str__(self):
        return self.email
    
    
        
     