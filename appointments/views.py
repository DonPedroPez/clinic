from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.template import RequestContext

from forms import UserRegistrationForm, PatientRegistrationForm


def register_patient(request):
    user_form = UserRegistrationForm(request.POST or None)
    patient_form = PatientRegistrationForm(request.POST or None)
    if user_form.is_valid() and patient_form.is_valid():
        user = user_form.save()
        patient_form.save(user)
        return redirect('waiting_room')
    return render(request, 'appointments/patient_registration.html',
                  {'user_form': user_form, 'patient_form': patient_form})


def waiting_room(request):
    return render(request, 'appointments/waiting_room.html',
                  context_instance=RequestContext(request))

def patients_visits(request):
    return render(request, 'appointments/patients_visits.html')
