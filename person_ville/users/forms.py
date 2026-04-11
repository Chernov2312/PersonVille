from django import forms

from users.models import User

__all__ = ['RegisterForm', 'AuthorizationForm']


class AuthorizationForm(forms.Form):
    login = forms.CharField(label='логин', max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Пароль',
    )


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Подтвердите пароль',
            },
        ),
        label='Подтверждение пароля',
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Ваше имя',
            'email': 'Email',
            'password': 'Пароль',
        }
        help_texts = {
            'username': 'Ваше имя',
            'email': 'Ваша почта',
            'password': 'Пароль',
        }
