__all__ = 'UserManager'
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_user_by_username(self, username: str):
        return self.filter(username=username).first()

    def get_user_by_email(self, email: str):
        return self.filter(email=email).first()

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('Superuser must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
