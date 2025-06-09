"""
URL configuration for pocketpass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import GoogleAuthPopupView, AccountView, ForcePopupCloseView, CustomLogoutView, CheckAuthStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='ticketsplease.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('sign-in/', TemplateView.as_view(template_name='sign_in.html'), name='sign_in'),
    path('google-auth-popup/', GoogleAuthPopupView.as_view(), name='google_auth_popup'),
    path('force-popup-close/', ForcePopupCloseView.as_view(), name='force_popup_close'),
    path('account/', AccountView.as_view(), name='account'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
    path('check-auth-status/', CheckAuthStatusView.as_view(), name='check_auth_status'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
