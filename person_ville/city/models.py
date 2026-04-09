from django.db import models
from quises.models import Quiz


class House(models.Model):
    name = models.CharField(max_length=40, null=False)
    houses_description = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=40, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=40, null=False)
    houses = models.ManyToManyField(House, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)