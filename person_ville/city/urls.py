from django.urls import path

from city.views import city

app_name = 'city'
urlpatterns = [
    path('', city, name='city'),
]
