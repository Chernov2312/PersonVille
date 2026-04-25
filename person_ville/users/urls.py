from django.urls import path

from users.views import (
    authorization,
    change_email,
    change_password,
    forgot_password,
    history_detail,
    history_list,
    logout_view,
    registration,
    reset_password_confirm,
    verify_email,
)

app_name = 'user'

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration, name='registration'),
    path('history/', history_list, name='history_list'),
    path('history/<int:history_id>/', history_detail, name='history_detail'),
    path('change-email/', change_email, name='change_email'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path(
        'reset-password/<uidb64>/<token>/',
        reset_password_confirm,
        name='reset_password_confirm',
    ),
    path(
        'verify/<uidb64>/<token>/',
        verify_email,
        name='verify_email',
    ),
]
