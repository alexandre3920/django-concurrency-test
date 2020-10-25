# coding: utf-8

# Django
from django.contrib import admin

# Main app models
from apps.main.models.users import DashboardUser, PatientUser


@admin.register(DashboardUser)
class DashboardUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'creation_date', 'type', 'email', 'is_active', 'has_been_validated', 'last_login')
    list_filter = ('creation_date', 'is_active', 'has_been_validated', 'is_doctor', 'is_patient', 'is_staff',)
    search_fields = ('first_name', 'last_name', 'email',)
    list_per_page = 20


@admin.register(PatientUser)
class PatientUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'patient_id', 'creation_date', 'is_active', 'has_been_validated')
    list_filter = ('user__creation_date', 'user__has_been_validated', 'user__is_active')
    search_fields = ('patient_id', 'doctor__user__first_name', 'doctor__user__last_name')
    list_per_page = 20
