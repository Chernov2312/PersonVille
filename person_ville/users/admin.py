from django.contrib import admin

from analytics.models import CompletedQuizSession
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'is_active',
        'is_staff',
        'role',
        'created_at',
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']


@admin.register(CompletedQuizSession)
class CompletedQuizSessionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'session_key',
        'user',
        'started_at',
        'completed_at',
        'duration_seconds',
        'created_at',
    ]

    list_filter = [
        'completed_at',
        'created_at',
        'user',
    ]

    search_fields = [
        'session_key',
        'user__email',
        'user__username',
    ]

    readonly_fields = [
        'session_key',
        'user',
        'started_at',
        'completed_at',
        'duration_seconds',
        'final_character',
        'created_at',
    ]

    fieldsets = (
        (
            'Информация о сессии',
            {
                'fields': (
                    'session_key',
                    'user',
                    'started_at',
                    'completed_at',
                    'duration_seconds',
                ),
            },
        ),
        (
            'Результат',
            {
                'fields': ('final_character',),
                'classes': ('wide',),
            },
        ),
        (
            'Системная информация',
            {
                'fields': ('created_at',),
                'classes': ('collapse',),
            },
        ),
    )

    date_hierarchy = 'completed_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
