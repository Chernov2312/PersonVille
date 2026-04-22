from django.urls import path

from users.views import (
    authorization,
    change_email,
    change_password,
    character,
    history_detail,
    history_list,
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
    path('history/', history_list, name='history_list'),
    path('history/<int:history_id>/', history_detail, name='history_detail'),
    path('change-email/', change_email, name='change_email'),
    path('change-password/', change_password, name='change_password'),
    path(
        'verify/<uidb64>/<token>/',
        verify_email,
        name='verify_email',
    ),
]
