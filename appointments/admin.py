from django.contrib import admin

from .models import Patient, Doctor, Clinic, Duty, Appointment


class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'address')
    search_fields = ('user__last_name',)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_first_name.short_description = 'First name'
    get_first_name.admin_order_field = 'user__first_name'
    get_last_name.short_description = 'Last name'
    get_last_name.admin_order_field = 'user__last_name'


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'license')
    search_fields = ('user__last_name',)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_first_name.short_description = 'First name'
    get_first_name.admin_order_field = 'user__first_name'
    get_last_name.short_description = 'Last name'
    get_last_name.admin_order_field = 'user__last_name'


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class DutyAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'doctor', 'weekday', 'start', 'end')
    list_filter = ('clinic', 'doctor')
    search_fields = ('clinic', 'doctor')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'doctor', 'patient', 'date', 'start')
    list_filter = ('clinic', 'doctor', 'patient')
    search_fields = ('clinic', 'doctor', 'patient')


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Duty, DutyAdmin)
admin.site.register(Appointment, AppointmentAdmin)
