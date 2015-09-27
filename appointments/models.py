from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (RegexValidator, MinLengthValidator,
    MaxLengthValidator)


class DutyManager(models.Manager):
    def get_queryset(self):
        return super(DutyManager, self).get_queryset() \
                                       .exclude(patient__isnull=False)


class AppointmentManager(models.Manager):
    def get_queryset(self):
        return super(AppointmentManager, self).get_queryset() \
                                              .filter(patient__isnull=False)


class Rendezvous(models.Model):
    WEEKDAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    date = models.DateField(blank=True, null=True)
    start = models.TimeField()
    end = models.TimeField()

    doctor = models.ForeignKey('Doctor')
    clinic = models.ForeignKey('Clinic')
    patient = models.ForeignKey('Patient', blank=True, null=True)


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


class Duty(Rendezvous):
    objects = DutyManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'duties'


class Appointment(Rendezvous):
    objects = AppointmentManager()

    class Meta:
        proxy = True
