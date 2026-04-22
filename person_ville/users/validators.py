__all__ = ('RoleValidate',)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RoleValidate:
    ALLOWED_ROLES = ['admin', 'player']

    def __call__(self, value):
        if value not in self.ALLOWED_ROLES:
            raise ValidationError(
                _('Роль может быть только admin или player'),
                params={'value': value},
            )
