from django.urls import path

from users.views import authorization
from users.views import character
from users.views import logout_view
from users.views import registration
from users.views import verify_email


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
