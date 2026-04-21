__all__ = 'UserManager'
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_user_by_username(self, username: str):
        return self.filter(username=username).first()

    def get_user_by_email(self, email: str):
        return self.filter(email=email).first()

    def create_superuser(self, username, email, password):
        user = self.model(username=username, email=email, password=password)
        user.save()
        return user
