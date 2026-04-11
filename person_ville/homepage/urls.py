from django.urls import path
from homepage.views import main

app_name = 'homepage'
urlpatterns = [
    path('', main, name='main'),
]
