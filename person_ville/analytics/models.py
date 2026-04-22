__all__ = ('CompletedQuizSession',)
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class CompletedQuizSession(models.Model):
    session_key = models.CharField(
        max_length=40,
        db_index=True,
        verbose_name=_('Ключ сессии'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Пользователь'),
    )
    started_at = models.DateTimeField(
        verbose_name=_('Начало сессии'),
    )
    completed_at = models.DateTimeField(
        verbose_name=_('Завершение сессии'),
    )
    duration_seconds = models.PositiveIntegerField(
        verbose_name=_('Длительность (сек)'),
    )
    final_character = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('Итоговый персонаж'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Создано'),
    )

    class Meta:
        verbose_name = _('Завершённая сессия теста')
        verbose_name_plural = _('Завершённые сессии тестов')
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['completed_at']),
        ]
