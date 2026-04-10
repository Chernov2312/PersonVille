from django.urls import path
from quizzes.views import first


urlpatterns = [
    path('first/', first, name='first'),
]
