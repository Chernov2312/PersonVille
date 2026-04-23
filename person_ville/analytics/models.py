__all__ = ('CompletedQuizSession',)
from django.db import models

from users.models import User


class CompletedQuizSession(models.Model):
    session_key = models.CharField(
        max_length=40,
        db_index=True,
        verbose_name='Ключ сессии',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь',
    )
    started_at = models.DateTimeField(
        verbose_name='Начало сессии',
    )
    completed_at = models.DateTimeField(
        verbose_name='Завершение сессии',
    )
    duration_seconds = models.PositiveIntegerField(
        verbose_name='Длительность (сек)',
    )
    final_character = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Итоговый персонаж',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )

    class Meta:
        verbose_name = 'Завершённая сессия теста'
        verbose_name_plural = 'Завершённые сессии тестов'
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['completed_at']),
        ]
