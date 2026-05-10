from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, id, **extra_fields):
        if not id:
            raise ValueError("The Telegram ID must be set")
        user = self.model(id=id, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, id, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(id, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigIntegerField(primary_key=True, help_text="Telegram User ID")
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    last_activity_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return f"{self.first_name} ({self.id})"

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()
