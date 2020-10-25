"""
django-concurrency-test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('apps.main.urls', namespace='main')),
    path('mon-compte/', auth_views.LoginView.as_view(
        template_name='main/login.html'), name='login'),
    path('mon-compte/login/', auth_views.LoginView.as_view(
        template_name='main/login.html'), name='login'),
    path('mon-compte/logout/', auth_views.LogoutView.as_view(
        template_name='main/logged_out.html'), name='logout'),
    path('mon-compte/reset-password/', auth_views.PasswordResetView.as_view(
        template_name='main/password_reset_form.html'), name='password_reset'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__", include(debug_toolbar.urls)),
    ]
