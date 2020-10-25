# coding: utf-8

# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.validators import RegexValidator

# Main app models
from ..models.users import (
    DashboardUser, PatientUser
)


class PatientSignupForm(UserCreationForm):
    first_name_validator = RegexValidator(
        regex=r'^[a-zA-Z]{1}$',
        message="Veuillez indiquer la première lettre de votre prénom")
    first_name = forms.CharField(
        help_text="Indiquez la première lettre de votre prénom.",
        max_length=1,
        required=True,
        validators=[first_name_validator])
    last_name_validator = RegexValidator(
        regex=r'^[a-zA-Z]{2}$',
        message="Veuillez indiquer les deux premières lettres de votre nom de famille")
    last_name = forms.CharField(
        help_text="Indiquez les deux premières lettres de votre nom de famille.",
        max_length=2,
        required=True,
        validators=[last_name_validator])
    patient_age_validator = RegexValidator(
        regex=r'^\d{1,3}$')
    patient_age = forms.CharField(
        help_text="Indiquez votre âge.",
        validators=[patient_age_validator],
        max_length=3,
        required=True)
    guc_agreement = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=True)

    class Meta(UserCreationForm.Meta):
        model = DashboardUser
        fields = (
            'first_name',
            'last_name',
            'email')
        help_texts = {
            'first_name': '',
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.has_been_validated = True
        user.save()
        patient = PatientUser.objects.create(user=user)
        patient.patient_age = self.cleaned_data.get('patient_age')
        patient.save()
        return user
