__all__ = (
    'RegisterForm',
    'AuthorizationForm',
    'ChangeEmailRequestForm',
    'ChangeEmailConfirmForm',
    'ChangePasswordRequestForm',
    'ChangePasswordConfirmForm',
)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import User


class AuthorizationForm(forms.Form):
    login = forms.CharField(
        label='Логин или email',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин или email',
            },
        ),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        login_value = cleaned_data.get('login')
        password_value = cleaned_data.get('password')

        if not login_value or not password_value:
            return cleaned_data

        user = User.objects.get_user_by_username(login_value)
        if not user:
            user = User.objects.get_user_by_email(login_value)

        if not user:
            self.add_error(
                'login',
                'Пользователь с таким логином или email не найден.',
            )
            return cleaned_data

        if not check_password(password_value, user.password):
            self.add_error('password', 'Неверный пароль.')
            return cleaned_data

        self.user = user
        return cleaned_data


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.ru',
            },
        ),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Придумайте пароль',
            },
        ),
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль',
            },
        ),
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с такой почтой уже существует.',
            )

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangeEmailRequestForm(forms.Form):
    new_email = forms.EmailField(
        label='Новый email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите новый email',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        email = self.cleaned_data['new_email']

        if email == self.user.email:
            raise forms.ValidationError('Это уже ваша текущая почта.')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с такой почтой уже существует.',
            )

        return email


class ChangeEmailConfirmForm(forms.Form):
    code = forms.CharField(
        label='Код подтверждения',
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите код из письма',
            },
        ),
    )


class ChangePasswordRequestForm(forms.Form):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите текущий пароль',
            },
        ),
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите новый пароль',
            },
        ),
    )
    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите новый пароль',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']

        if not self.user.check_password(current_password):
            raise forms.ValidationError('Текущий пароль введён неверно.')

        return current_password

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if not new_password1 or not new_password2:
            return cleaned_data

        if new_password1 != new_password2:
            self.add_error('new_password2', 'Пароли не совпадают.')

        if current_password and new_password1 == current_password:
            self.add_error(
                'new_password1',
                'Новый пароль должен отличаться от текущего.',
            )

        try:
            validate_password(new_password1, user=self.user)
        except ValidationError as error:
            for message in error.messages:
                self.add_error('new_password1', message)

        return cleaned_data


class ChangePasswordConfirmForm(forms.Form):
    code = forms.CharField(
        label='Код подтверждения',
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите код из письма',
            },
        ),
    )
