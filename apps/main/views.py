# coding: utf-8

# Django import
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.views.decorators.http import require_safe, require_GET
from django.conf import settings

# Main app models
from .models.users import DashboardUser
# Main app forms
from .forms.users import (
    PatientSignupForm,
)


@require_safe
def home(request):
    return render(
        request,
        'main/index.html',
        {
        })


class PatientSignupView(CreateView):
    model = DashboardUser
    form_class = PatientSignupForm
    template_name = 'main/signup_user_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # Create the dashboard user
        user = form.save()
        # Then send an email for account validation via Celery tasks
        if not settings.CELERY_DEV:
            # send_dashboard_user_account_validation_email.delay(user.pk)
            pass
        else:
            # send_dashboard_user_account_validation_email(user.pk)
            pass
        # And redirect the user to the signup confirmation page
        return redirect('main:signup_user_confirmation')

    def form_invalid(self, form):
        # add error message
        if len(form.errors) == 1:
            messages.error(
                self.request,
                "Veuillez corriger l'erreur ci-dessous.")
        else:
            messages.error(
                self.request,
                "Veuillez corriger les erreurs ci-dessous.")
        return super().form_invalid(form)


@require_GET
def signup_user_confirmation(request):
    return render(
        request,
        'main/signup_user_confirmation.html',
        {})
