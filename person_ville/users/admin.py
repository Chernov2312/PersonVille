from django.contrib import admin

from users.models import User


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = (User.username.field.name,)
