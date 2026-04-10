from django.db import models


class Answer(models.Model):
    text = models.CharField(max_length=200, null=False)
    counter = models.IntegerField(default=0)


class Questions(models.Model):
    question = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=True)
    cost = models.IntegerField(null=False)


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False)
    questions = models.ManyToManyField(Questions, blank=True)
