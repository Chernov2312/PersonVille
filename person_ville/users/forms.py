from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

from users.models import User

__all__ = ['RegisterForm', 'AuthorizationForm']


class AuthorizationForm(forms.Form):
    login = forms.CharField(label='логин', max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Пароль',
    )

    def clean(self):
        cleaned_data = super().clean()
        user = User.objects.get_user_by_username(cleaned_data['login'])
        if not user:
            user = User.objects.get_user_by_email(cleaned_data['login'])
        if not user:
            self.add_error(
                'login',
                'Пользователь с таким логином или email не найден',
            )
        elif not check_password(cleaned_data['password'], user.password):
            self.add_error('password', 'Неверный пароль')
        self.user = user


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите имя'},
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'example@mail.ru',
                },
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Придумайте пароль',
                },
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Повторите пароль',
                },
            ),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов.',
            'email': 'Укажите действующий email.',
        }
