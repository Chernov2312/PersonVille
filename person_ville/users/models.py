from django.contrib.auth.models import AbstractUser
from django.db import models
from quises.models import Quiz


class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=30, null=False)
    city = models.CharField(max_length=40, null=True)
    quises = models.ManyToManyField(Quiz, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
