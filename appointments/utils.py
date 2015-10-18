from datetime import datetime, timedelta

from .models import Duty, Appointment


def get_suggested_appointments(doctor, clinic, date):
    duties = Duty.objects.filter(doctor=doctor, clinic=clinic,
                                 weekday=date.weekday())
    if not duties:
        return None
    appointments = Appointment.objects.filter(doctor=doctor, clinic=clinic,
                                              date=date)
    suggested = []
    for duty in duties:
        proposition = duty.start
        while proposition < duty.end:
            if not appointments.filter(start__lte=proposition,
                                       end__gte=proposition):
                suggested.append(proposition)
            proposition = (datetime.combine(date, proposition)
                           + timedelta(minutes=30)).time()
    return suggested
