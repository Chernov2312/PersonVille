from django.contrib.auth.models import AbstractUser
from django.db import models
from quizzes.models import Quiz, Answer
from city.models import City
from core.models import BaseUpdate


class Character(models.Model):
    quality_name = models.CharField(max_length=40, null=False)
    quality_count = models.IntegerField(null=False)
    description = models.CharField(max_length=200, null=False)


class User(AbstractUser, BaseUpdate):
    role = models.CharField(max_length=30, null=False)
    city = models.CharField(max_length=40, null=True)
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        null=True,
    )
    cities = models.OneToManyField(City, related_name='users')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AnswerHistory(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='answer_history',
    )
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answer_history',
    )
