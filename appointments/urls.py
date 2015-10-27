from django.conf.urls import url
from django.contrib.auth.views import login as auth_login

from views import register_patient, waiting_room


urlpatterns = [
    url(r'^register/$', register_patient, name='register'),
    url(r'^waiting_room/$', waiting_room, name='waiting_room')
]
