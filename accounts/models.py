import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = None  # Removed username
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, default="", blank=True, null=True)
    phone = PhoneNumberField(region="IN", blank=True, null=True) 
    # Changed the phone from CharField to PhoneNumberField
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    # Connect the custom manager here!
    objects = CustomUserManager()

    def __str__(self):
        return self.email