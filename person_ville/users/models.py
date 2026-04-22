__all__ = (
    'User',
    'UserResultHistory',
    'EmailChangeCode',
    'PasswordChangeCode',
)

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from core.models import BaseUpdate
from users.managers import UserManager
from users.validators import RoleValidate


class User(AbstractUser, BaseUpdate):
    objects = UserManager()

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    role = models.CharField(
        max_length=30,
        null=False,
        default='player',
        validators=[RoleValidate()],
    )
    city = models.CharField(max_length=40, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_change_cooldown_until = models.DateTimeField(
        null=True,
        blank=True,
    )
    password_change_cooldown_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class UserResultHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='result_history',
        verbose_name='Пользователь',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название результата',
    )
    short_summary = models.TextField(
        verbose_name='Краткий итог',
    )
    snapshot = models.JSONField(
        verbose_name='Снимок результата',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'История прохождения'
        verbose_name_plural = 'История прохождений'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.title}'


class EmailChangeCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_change_codes',
    )
    new_email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    resend_available_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_expired(self):
        return timezone.now() > self.expires_at


class PasswordChangeCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_change_codes',
    )
    new_password_hash = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    resend_available_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_expired(self):
        return timezone.now() > self.expires_at
