__all__ = ()
from django.urls import path

from homepage.views import main

app_name = 'main'
urlpatterns = [
    path('', main, name='main'),
]
