from datetime import datetime, timedelta

from .models import Duty


def get_suggested_appointments_for_date(doctor, clinic, date):
    duties = Duty.objects.filter(doctor=doctor, clinic=clinic,
                                 weekday=date.weekday())
