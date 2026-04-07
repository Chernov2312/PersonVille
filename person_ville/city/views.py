from django.shortcuts import render


def city_view(request):
    return render(request, 'city/city.html')
