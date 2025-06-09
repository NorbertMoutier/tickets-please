from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
import re
import logging

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptateur personnalisé pour les comptes sociaux.
    Permet de rediriger vers une page spécifique après l'authentification Google.
    """
    
    def get_login_redirect_url(self, request):
        """
        Redirige vers la page de succès d'authentification Google si l'utilisateur
        vient de s'authentifier via Google dans une popup.
        """
        # Vérification complète pour détecter une authentification Google via popup
        referer = request.META.get('HTTP_REFERER', '')
        query_string = request.META.get('QUERY_STRING', '')
        
        # Log pour débogage
        logger.debug(f"Referer: {referer}")
        logger.debug(f"Query string: {query_string}")
        logger.debug(f"GET params: {request.GET}")
        
        # Vérifier si c'est une authentification Google
        is_google_auth = ('google' in referer or '/accounts/google/' in referer or
                        'google' in request.META.get('PATH_INFO', ''))
        
        # Vérifier si c'est une popup - plusieurs indicateurs possibles
        is_popup = (request.GET.get('popup') == '1' or
                   'popup=1' in query_string or
                   'popup=1' in referer or
                   'google-auth-popup' in referer)
        
        # Si c'est une authentification Google dans une popup, rediriger vers la page de fermeture forcée
        if is_google_auth and is_popup:
            logger.debug("Redirection vers la page de fermeture FORCÉE de popup")
            return reverse('force_popup_close')
        
        # Obtenir l'URL de redirection par défaut
        default_url = super().get_login_redirect_url(request)
        logger.debug(f"Redirection par défaut vers: {default_url}")
        return default_url
