# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('license', models.CharField(unique=True, max_length=20)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('pesel', models.CharField(unique=True, max_length=11, validators=[django.core.validators.RegexValidator(regex=b'\\d+', message=b'PESEL contains only numbers.', code=b'NotNumber'), django.core.validators.MinLengthValidator(11, message=b'PESEL has exactly 11 digits.'), django.core.validators.MaxLengthValidator(11, message=b'PESEL has exactly 11 digits.')])),
                ('address', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rendezvous',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.IntegerField(choices=[(1, b'Monday'), (2, b'Tuesday'), (3, b'Wednesday'), (4, b'Thursday'), (5, b'Friday'), (6, b'Saturday'), (7, b'Sunday')])),
                ('date', models.DateField(null=True, blank=True)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('clinic', models.ForeignKey(to='appointments.Clinic')),
                ('doctor', models.ForeignKey(to='appointments.Doctor')),
                ('patient', models.ForeignKey(blank=True, to='appointments.Patient', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('appointments.rendezvous',),
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('appointments.rendezvous',),
        ),
    ]
