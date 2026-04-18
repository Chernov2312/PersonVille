__all__ = ('RegisterForm', 'AuthorizationForm')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

from users.models import User


class AuthorizationForm(forms.Form):
    login = forms.CharField(
        label='Логин или email',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
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
