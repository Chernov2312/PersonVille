from django.urls import path

from city import views

app_name = 'city'

urlpatterns = [
    path('', views.city_view, name='city'),
    path('character/', views.character_view, name='character'),
    path('finalize/', views.finalize_city_view, name='finalize'),
    path('street/<str:trait>/', views.street_view, name='street'),
    path(
        'street/<str:trait>/house/<str:house_id>/',
        views.house_question_view,
        name='house_question',
    ),
]
