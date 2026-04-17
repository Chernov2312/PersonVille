from django.urls import path

from users.views import (
    authorization,
    character,
    logout_view,
    registration,
    verify_email,
)

app_name = 'user'

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration, name='registration'),
    path('character/', character, name='character'),
    path(
        'verify/<uidb64>/<token>/',
        verify_email,
        name='verify_email',
    ),
]
