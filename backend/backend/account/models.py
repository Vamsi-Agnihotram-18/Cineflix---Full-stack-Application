from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User(AbstractBaseUser):
    MEMBER = 'member'
    PREMIUM_MEMBER = 'premiumMember'
    ADMIN = 'admin'
    ROLE_CHOICES = [(MEMBER, 'member'), (PREMIUM_MEMBER, 'premiumMember'), (ADMIN, 'admin')]
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField()
    username = models.CharField(max_length=24, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=24)
    phoneNumber = PhoneNumberField()
    def __str__(self):
        return f'<User {self.user_id} | {self.username} | {self.email} | {self.role}>'