from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'created_by', 'created_at']
    list_filter = ['gender', 'created_at', 'created_by']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'experience_years', 'is_available']
    list_filter = ['specialization', 'is_available', 'created_at']
    search_fields = ['name', 'specialization', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'assigned_date', 'is_active']
    list_filter = ['assigned_date', 'is_active']
    search_fields = ['patient__name', 'doctor__name']
