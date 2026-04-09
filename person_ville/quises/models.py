from django.db import models
from users.models import User


class Answer(models.Model):
    text = models.CharField(max_length=200, null=False)
    counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False)
    answers = models.ManyToManyField(Answer, blank=True)
