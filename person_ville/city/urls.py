from city.views import city
from django.urls import path

app_name = 'city'
urlpatterns = [
    path('', city, name='city'),
]
