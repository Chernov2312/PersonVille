__all__ = ['urlpatterns', 'app_name']

from django.urls import path

from city import views


app_name = 'city'

urlpatterns = [
    path('', views.city_view, name='city'),
    path('<str:trait>/', views.street_view, name='street'),
]
