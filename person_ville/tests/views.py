from django.shortcuts import redirect, render
from django.urls import reverse


def first(request):
    template = 'tests/test_form.html'
    if request.POST:
        template = 'city/city.html'
        return redirect(reverse('city:city'))
    return render(request=request, template_name=template)


def test_house(request):
    template = 'tests/test_form.html'
    context = {''}
    if request.POST:
        template = 'city/city.html'
        return redirect(reverse('city:city'))
    return render(request=request, template_name=template)