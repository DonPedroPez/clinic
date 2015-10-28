from django.conf.urls import url
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.views import logout

from views import (register_patient, waiting_room, patients_visits,
                   reserve_appointment)


urlpatterns = [
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register_patient, name='register'),
    url(r'^waiting_room/$', waiting_room, name='waiting_room'),
    url(r'^visits/$', patients_visits, name='patients_visits'),
    url(r'^reserve_appointment/$', reserve_appointment,
        name='reserve_appointment')
]
