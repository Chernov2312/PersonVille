from django.db import models

from users.models import User


class CompletedQuizSession(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    duration_seconds = models.PositiveIntegerField()
    final_character = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['completed_at']),
        ]

    def __str__(self):
        return f'Session {self.session_key[:8]}... ({self.duration_seconds}s)'
