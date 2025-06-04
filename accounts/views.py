from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class GoogleAuthPopupView(TemplateView):
    """Vue pour afficher la page intermédiaire de la popup d'authentification Google."""
    template_name = 'google_popup.html'

class AccountView(TemplateView):
    """Vue pour afficher la page Mon compte."""
    template_name = 'account.html'
