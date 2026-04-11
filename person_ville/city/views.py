from django.shortcuts import render

__all__ = ['city']


def city(request):
    return render(request, 'city/city.html')
