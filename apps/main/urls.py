# coding: utf-8

# Django import
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="index"),
    path('mon-compte/creer/patient/', views.PatientSignupView.as_view(), name='patient_signup'),
    path('mon-compte/creer/confirmation/', views.signup_user_confirmation, name='signup_user_confirmation'),
]
