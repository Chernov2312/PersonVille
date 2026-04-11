from django.urls import path

from users.views import authorization, character, registration

app_name = 'user'
urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('registration/', registration, name='registration'),
    path('character/', character, name='character'),
]
