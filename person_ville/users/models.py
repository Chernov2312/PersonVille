from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=30, null=False)
    city = models.CharField(max_length=40, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
