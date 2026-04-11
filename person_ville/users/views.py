from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import AuthorizationForm, RegisterForm


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            print('Пользователь успешно зарегистрирован')
            return redirect(reverse('main:main'))
    else:
        form = RegisterForm()
    context = {'form': form, 'title': 'Регистрация'}
    template = 'user/user_form.html'
    return render(request=request, template_name=template, context=context)


def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            return redirect(reverse('main:main'))
    else:
        form = AuthorizationForm()
    context = {'form': form, 'title': 'Авторизация'}
    template = 'user/user_form.html'
    return render(request=request, template_name=template, context=context)
