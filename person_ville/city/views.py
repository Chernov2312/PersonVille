__all__ = ()
from django.shortcuts import render


def city(request):
    return render(request, 'city/city.html')
