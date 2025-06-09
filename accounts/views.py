from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.views import View
from django.http import HttpResponse, JsonResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class GoogleAuthPopupView(TemplateView):
    """Vue pour afficher la page intermédiaire de la popup d'authentification Google."""
    template_name = "google_popup.html"


@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    """Vue pour afficher la page Mon compte."""
    template_name = "account.html"


class ForcePopupCloseView(TemplateView):
    """Vue ultra-simple pour forcer la fermeture de la popup et rediriger la fenêtre parente."""
    template_name = "force_popup_close.html"


class GoogleAuthSuccessView(TemplateView):
    """Vue pour afficher la page de succès après authentification Google.
    Cette page ferme automatiquement la popup et envoie un message à la fenêtre parente.
    """
    template_name = "google_auth_success.html"


class ForceCloseView(TemplateView):
    """Vue pour afficher la page de fermeture forcée."""
    template_name = "force_close.html"


class CustomLogoutView(View):
    """Vue personnalisée pour la déconnexion qui efface explicitement la session."""
    
    def get(self, request, *args, **kwargs):
        # Déconnecter l'utilisateur
        logout(request)
        
        # Effacer explicitement la session
        request.session.flush()
        
        # Effacer les cookies de session
        response = redirect('/')
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        
        return response


class CheckAuthStatusView(View):
    """Vue pour vérifier l'état d'authentification de l'utilisateur via AJAX."""
    
    def get(self, request, *args, **kwargs):
        # Préparer la réponse
        data = {
            'is_authenticated': request.user.is_authenticated,
        }
        
        # Ajouter des informations sur l'utilisateur si authentifié
        if request.user.is_authenticated:
            data['username'] = request.user.username
            data['email'] = request.user.email
        
        # Retourner en JSON
        return JsonResponse(data)
