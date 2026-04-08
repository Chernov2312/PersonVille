from django.urls import path
from tests.views import first, test_house

app_name = 'tests'
urlpatterns = [
    path('first/', first, name='first'),
    path('test/', test_house, name='test_house'),
]
