__all__ = 'User'
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseUpdate
from users.managers import UserManager


class User(AbstractUser, BaseUpdate):
    objects = UserManager()

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    role = models.CharField(max_length=30, null=False, default='player')
    city = models.CharField(max_length=40, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
