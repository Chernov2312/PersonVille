from django.db import models
from users.models import User


class Answer(models.Model):
    text = models.CharField(max_length=200, null=False)
    counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Questions(models.Model):
    question = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=True)
    cost = models.IntegerField(null=False)


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False)
    questions = models.ManyToManyField(Questions, blank=True)
