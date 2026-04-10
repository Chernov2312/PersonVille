from django.db import models

from city.models import Street
from core.models import BaseUpdate


class Answer(BaseUpdate):
    name = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=200, null=False)
    cost = models.IntegerField(null=False)


class Quiz(BaseUpdate):
    street = models.ForeignKey(Street, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=100)
    description = models.TextField(null=False)
    answers = models.ManyToManyField(Answer, related_name='quizzes')
