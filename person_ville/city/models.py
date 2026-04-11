from django.db import models
from django.utils.safestring import mark_safe

from core.models import BaseUpdate


class City(BaseUpdate):
    name = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=200, null=False)


class Street(BaseUpdate):
    name = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=200, null=False)
    number_of_houses = models.IntegerField(null=False)
    style = models.CharField(max_length=40, null=True, default='')
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='streets',
    )
