from django.urls import path

from city.views import city_view

app_name = 'city'
urlpatterns = [
    path('', city_view, name='city'),
]
