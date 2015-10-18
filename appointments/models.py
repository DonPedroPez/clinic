from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (RegexValidator, MinLengthValidator,
    MaxLengthValidator)
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Patient(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='patients')
    accepted = models.BooleanField(default=False)

    pesel = models.CharField(unique=True,
                             max_length=11,
                             validators=[
                                 RegexValidator(
                                     regex='\d+',
                                     message='PESEL contains only numbers.',
                                     code='NotNumber'
                                 ),
                                 MinLengthValidator(
                                     11,
                                     message='PESEL has exactly 11 digits.'
                                 ),
                                 MaxLengthValidator(
                                     11,
                                     message='PESEL has exactly 11 digits.'
                                 )
                             ])
    address = models.TextField()

    def __unicode__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Doctor(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='doctors')
    license = models.CharField(unique=True, max_length=20)

    def __unicode__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Clinic(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Duty(models.Model):
    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start = models.TimeField()
    end = models.TimeField(blank=True)

    doctor = models.ForeignKey('Doctor')
    clinic = models.ForeignKey('Clinic')

    class Meta:
        verbose_name_plural = 'duties'

    def clean(self):
        if not self.start:
            return
        if not self.end:
            self.end = (datetime.combine(now().date(), self.start)
                        + timedelta(hours=8)).time()

        duties = Duty.objects.filter(doctor=self.doctor, weekday=self.weekday)
        for duty in duties:
            if (self.start < duty.start < self.end) or \
               (self.start < duty.end < self.end) or \
               (self.start >= duty.start and self.end <= duty.end):
                raise ValidationError('Duty collides with another in clinic'
                                      ' {clinic}. {doctor} works there between'
                                      ' {start} and {end} on {weekday}s'
                                      .format(clinic=duty.clinic.name,
                                              doctor=duty.doctor,
                                              start=duty.start,
                                              end=duty.end,
                                              weekday=Duty.WEEKDAY_CHOICES[
                                                  duty.weekday][1]))

    def save(self, *args, **kwargs):
        self.clean()
        super(Duty, self).save(*args, **kwargs)


class Appointment(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField(blank=True)

    doctor = models.ForeignKey('Doctor')
    clinic = models.ForeignKey('Clinic')
    patient = models.ForeignKey('Patient')

    def clean(self):
        if not self.start:
            return
        if self.end is None:
            self.end = (datetime.combine(self.date, self.start)
                        + timedelta(minutes=29, seconds=59)).time()
        elif self.end.minute == 30 or self.end.minute == 0:
            self.end = (datetime.combine(self.date, self.end)
                        - timedelta(seconds=1)).time()
        appointments = Appointment.objects.filter(clinic=self.clinic,
                                                  doctor=self.doctor)
        for appointment in appointments:
            if (self.start < appointment.start < self.end) or \
               (self.start < appointment.end < self.end) or \
               (self.start >= appointment.start and
               self.end <= appointment.end):
                if self.id != appointment.id:
                    raise ValidationError('Appointment collides with another'
                                          ' ({start} - {end})'.format(
                        start=appointment.start, end=appointment.end))
        duties = Duty.objects.filter(doctor=self.doctor, clinic=self.clinic,
                                     weekday=self.date.weekday())
        if not duties:
            raise ValidationError('Doctor {doctor} doesn\'t work at {clinic}'
                                  ' on {weekday}s'.format(
                doctor=self.doctor, clinic=self.clinic,
                weekday=Duty.WEEKDAY_CHOICES[self.date.weekday()][1]))
        for duty in duties:
            if (self.start < duty.start < self.end) or \
               (self.start < duty.end < self.end) or \
               (self.end <= duty.start) or (self.start >= duty.end):
                raise ValidationError('Doctor {doctor} is present between'
                                      ' {start} and {end}'.format(
                    doctor=self.doctor, start=duty.start, end=duty.end))

    def save(self, *args, **kwargs):
        if self.end is None:
            self.end = (datetime.combine(self.date, self.start)
                        + timedelta(minutes=29, seconds=59)).time()
        elif self.end.minute == 30 or self.end.minute == 0:
            self.end = (datetime.combine(self.date, self.end)
                        - timedelta(seconds=1)).time()
        self.clean()
        super(Appointment, self).save(*args, **kwargs)
