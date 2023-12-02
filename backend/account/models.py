from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string
import uuid
from enum import Enum


class Role(str, Enum):
    member = 'member'
    premiumMember = 'premiumMember'
    admin = 'admin'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username, phoneNumber, role, is_admin, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("user_id", uuid.uuid4())
        user = self.model(email=email, username=username, phoneNumber=phoneNumber, role=role, is_admin=is_admin, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, phoneNumber, role, **extra_fields):
        return self.create_user(email, password, username, phoneNumber, role, **extra_fields)


class CustomUser(AbstractBaseUser):
    MEMBER = "member"
    GUEST_USER = "guestUser"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (MEMBER, "Member"),
        (GUEST_USER, "Guest User"),
        (ADMIN, "Admin"),
    ]
    REGULAR = "regular"
    PREMIUM = "premium"
    MEMBERSHIP_CHOICES = [(REGULAR, "Regular"), (PREMIUM, "Premium")]
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=24, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=24)
    phoneNumber = PhoneNumberField()
    rewardPoints = models.FloatField(default=0)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"<User {self.user_id} | {self.username} | {self.email} | {self.role}>"


class CustomToken(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.key)
