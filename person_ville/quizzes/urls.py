from django.urls import path

from quizzes.views import first

app_name = 'quizzes'
urlpatterns = [
    path('first/', first, name='first'),
]
