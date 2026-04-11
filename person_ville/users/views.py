from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import AuthorizationForm, RegisterForm


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return redirect(reverse('homepage:main'))
    context = {'form': RegisterForm()}
    template = 'user/user_form.html'
    return render(request=request, template_name=template, context=context)


def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            return redirect(reverse('homepage:main'))
    context = {'form': AuthorizationForm()}
    template = 'user/user_form.html'
    return render(request=request, template_name=template, context=context)