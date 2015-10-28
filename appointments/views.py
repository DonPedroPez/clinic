from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .forms import (UserRegistrationForm, PatientRegistrationForm,
                    AppointmentReservationForm)
from .models import Appointment, Patient


def register_patient(request):
    user_form = UserRegistrationForm(request.POST or None)
    patient_form = PatientRegistrationForm(request.POST or None)
    if user_form.is_valid() and patient_form.is_valid():
        user = user_form.save()
        patient_form.save(user)
        return redirect('waiting_room')
    return render(request, 'appointments/patient_registration.html',
                  {'user_form': user_form, 'patient_form': patient_form})


@login_required
def waiting_room(request):
    return render(request, 'appointments/waiting_room.html',
                  context_instance=RequestContext(request))


@login_required
def patients_visits(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return redirect('waiting_room')
    appointments = Appointment.objects.filter(patient=patient) \
                                      .order_by('-date')

    return render(request, 'appointments/patients_visits.html',
                  {'appointments': appointments})


@login_required
def reserve_appointment(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return redirect('waiting_room')
    form = AppointmentReservationForm(request.POST or None)

    if form.is_valid():
        form.save(patient)
        return redirect('patients_visits')

    return render(request, 'appointments/reserve_appointment.html',
                  {'form': form})
