# coding: utf-8

# Django import
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

# Main app custom manager
from apps.main.managers import DashboardUserManager

# Python
import uuid


class DashboardUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        "adresse email",
        help_text="Indiquez votre adresse email",
        error_messages={'unique': "Un utilisateur avec cette adresse email existe déjà."},
        unique=True)
    is_staff = models.BooleanField(
        "membre du staff",
        default=False)
    is_superuser = models.BooleanField(
        "superutilisateur",
        default=False)
    is_active = models.BooleanField(
        "utilisateur activé",
        default=False)
    has_been_validated = models.BooleanField(
        "compte validé ?",
        null=True)
    is_manager = models.BooleanField(
        "est-un manager ?",
        default=False)
    is_doctor = models.BooleanField(
        "est-un docteur ?",
        default=False)
    is_patient = models.BooleanField(
        "est-un patient ?",
        default=False)
    creation_date = models.DateTimeField(
        "date création compte",
        auto_now_add=True)
    last_update_date = models.DateTimeField(
        "date dernière mise à jour",
        auto_now=True)
    first_name = models.CharField(
        "prénom",
        help_text="Indiquez votre prénom",
        max_length=100)
    last_name = models.CharField(
        "nom de famille",
        help_text="Indiquez votre nom",
        max_length=100)
    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        unique=True,
        editable=False)
    enable_notifications = models.BooleanField(
        "activer les notifications",
        default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = DashboardUserManager()

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ['-creation_date']

    def __str__(self):
        return self.full_name()

    @property
    def type(self):
        if self.is_patient:
            return "Patient"
        else:
            return "Staff"

    def full_name(self):
        if self.is_patient:
            try:
                return self.patientuser.full_name()
            except PatientUser.DoesNotExist:
                pass
        return self.first_name + " " + self.last_name
    full_name.short_description = "Nom complet"

    def save(self, *args, **kwargs):
        # Title the first name
        self.first_name = self.first_name.title()
        # Uppercase the last name
        self.last_name = self.last_name.upper()
        # Lower case the email
        self.email = self.email.lower()
        super(DashboardUser, self).save(*args, **kwargs)
        # if is a patient
        if self.is_patient:
            try:
                self.patientuser.save()
            except PatientUser.DoesNotExist:
                pass


class PatientUser(models.Model):
    user = models.OneToOneField(
        DashboardUser,
        verbose_name="utilisateur",
        on_delete=models.CASCADE,
        primary_key=True)
    patient_id = models.CharField(
        "identifiant du patient",
        max_length=5,
        default="")
    birth_year = models.CharField(
        "année de naissance",
        max_length=4,
        help_text="Année de naissance du patient",
        default="")
    patient_age = models.CharField(
        "age du patient",
        max_length=3,
        default="")

    class Meta:
        verbose_name = "patient"
        verbose_name_plural = "patients"
        ordering = ['-user__creation_date']

    def __str__(self):
        return self.full_name()

    def save(self, *args, **kwargs):
        # Set the birth year
        if self.patient_age != "":
            now_date_year = timezone.localdate().year
            self.birth_year = str(now_date_year - int(self.patient_age))
        # Short version of birth year
        birth_year_str = str(self.birth_year)
        birth_year_str_len = len(birth_year_str)
        # Keep only the last two characters
        # if the length of the birth year string
        # is stricly higher than 2
        if birth_year_str_len > 2:
            short_birth_year = birth_year_str[2:]
        # Else add a tailing 0 if the length
        # equals 1
        elif birth_year_str_len == 1:
            short_birth_year = "0" + birth_year_str
        # Else use the birth year
        else:
            short_birth_year = birth_year_str
        # Set the patient id
        self.patient_id = (self.user.first_name[:1] + self.user.last_name[:2] + short_birth_year).upper()
        super(PatientUser, self).save(*args, **kwargs)

    def creation_date(self):
        if self.user:
            return self.user.creation_date
        else:
            return "-"
    creation_date.short_description = "date création compte"

    def is_active(self):
        if self.user:
            return self.user.is_active
        else:
            return False
    is_active.short_description = "utilisateur activé"
    is_active.boolean = True

    def has_been_validated(self):
        if self.user:
            return self.user.has_been_validated
        else:
            return False
    has_been_validated.short_description = "compte validé ?"
    has_been_validated.boolean = True

    def full_name(self):
        """ Return the full name of the patient """
        if self.patient_id:
            return self.patient_id
        else:
            return "-"
    full_name.short_description = "Nom complet"
