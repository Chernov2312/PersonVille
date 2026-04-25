__all__ = ('BaseUpdate', 'BaseChange')
from datetime import timedelta

from django.db import models
from django.utils import timezone


def default_expires_at():
    return timezone.now() + timedelta(hours=1)


def default_resend_available_at():
    return timezone.now() + timedelta(minutes=1)


class BaseUpdate(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        abstract = True


class BaseChange(models.Model):
    code = models.CharField(max_length=8)
    expires_at = models.DateTimeField(
        default=default_expires_at,
        verbose_name='Срок действия',
    )
    resend_available_at = models.DateTimeField(
        default=default_resend_available_at,
        verbose_name='Доступность повторной отправки',
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name='Использован',
    )

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        abstract = True
