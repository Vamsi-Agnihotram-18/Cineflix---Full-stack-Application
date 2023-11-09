from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string

# Create your models here.


class User(AbstractBaseUser):
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
    user_id = models.UUIDField()
    username = models.CharField(max_length=24, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=24)
    phoneNumber = PhoneNumberField()
    rewardPoints = models.FloatField(default=0)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"<User {self.user_id} | {self.username} | {self.email} | {self.role}>"


class Token(BaseModel):
    key = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_string(length=64)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key
