__all__ = ()
from django.urls import path

from quizzes import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.first, name='first'),
    path('close/', views.close_test, name='close'),
    path('restart/', views.restart_test, name='restart'),
    path(
        'street/<str:trait>/correction/',
        views.street_correction,
        name='street_correction',
    ),
]
