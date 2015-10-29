from django.conf.urls import url
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.views import logout

from views import (register_patient, waiting_room, patients_visits,
                   reserve_appointment, doctors_visits, doctors_duties_list,
                   doctors_duty_details)


urlpatterns = [
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register_patient, name='register'),
    url(r'^waiting_room/$', waiting_room, name='waiting_room'),
    url(r'^visits/$', patients_visits, name='patients_visits'),
    url(r'^agenda/$', doctors_visits, name='doctors_visits'),
    url(r'^reserve_appointment/$', reserve_appointment,
        name='reserve_appointment'),
    url(r'^duties/$', doctors_duties_list, name='duties_list'),
    url(r'^duties/(?P<duty_id>\d+)/$', doctors_duty_details,
        name='duty_details'),
    url(r'^add_duty/$', doctors_duty_details, name='add_duty')
]
