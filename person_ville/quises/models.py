from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False)
    counter = models.IntegerField(default=0)
