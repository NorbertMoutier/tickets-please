import os
import sys
import django
from django.core.management import call_command

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

# Importer les modèles nécessaires
from django.contrib.sessions.models import Session
from allauth.socialaccount.models import SocialAccount, SocialToken

def clear_all_sessions():
    """Effacer toutes les sessions et comptes sociaux."""
    print("Nettoyage des sessions et des comptes sociaux...")
    
    # Supprimer toutes les sessions
    Session.objects.all().delete()
    print("Sessions supprimées.")
    
    # Supprimer tous les tokens sociaux
    SocialToken.objects.all().delete()
    print("Tokens sociaux supprimés.")
    
    print("Nettoyage terminé.")

if __name__ == "__main__":
    clear_all_sessions()
