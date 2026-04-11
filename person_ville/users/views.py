from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import AuthorizationForm, RegisterForm
from users.utils import check_password, hash_password


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if (
                form.cleaned_data['password']
                == form.cleaned_data['confirm_password']
            ):
                form.changed_data['password'] = hash_password(
                    form.cleaned_data['password'],
                )
                form.save()
                return redirect(reverse('homepage:main'))
    context = {'form': RegisterForm()}
    template = 'user/user_form.html'
    return render(request=request, template_name=template, context=context)


def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            if check_password(
                form.cleaned_data['email'], form.cleaned_data['password'],
            ):
                return redirect(reverse('homepage:main'))
            else:
                form.add_error(
                    'password', 'Неверный пароль или логин',
                )
    context = {'form': AuthorizationForm()}
    template = 'user/user_form.html'
    return render(request=request, template_name=template, context=context)
