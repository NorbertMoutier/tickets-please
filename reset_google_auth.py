import os
import django
import sys

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site

def reset_google_auth():
    # 1. Supprimer toutes les applications sociales Google
    print("Suppression de toutes les applications sociales Google...")
    SocialApp.objects.filter(provider='google').delete()
    
    # 2. Supprimer tous les comptes sociaux Google (optionnel, peut être commenté si vous voulez garder les comptes)
    # print("Suppression de tous les comptes sociaux Google...")
    # SocialAccount.objects.filter(provider='google').delete()
    
    # 3. Supprimer tous les tokens sociaux Google (optionnel, peut être commenté)
    # print("Suppression de tous les tokens sociaux Google...")
    # SocialToken.objects.filter(app__provider='google').delete()
    
    # 4. Créer une nouvelle application sociale Google
    print("Création d'une nouvelle application sociale Google...")
    site = Site.objects.get(id=1)
    
    # Vérifier si le site existe
    if not site:
        print("Erreur: Site avec ID 1 introuvable. Création du site...")
        site = Site.objects.create(domain='localhost:8000', name='localhost')
    
    # Créer la nouvelle application
    app = SocialApp.objects.create(
        provider='google',
        name='Google',
        client_id='1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com',
        secret='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'
    )
    
    # Associer l'application au site
    app.sites.add(site)
    
    print(f"Application Google créée avec succès (ID: {app.id})")
    print(f"L'application est associée au site: {site.domain}")
    
    return True

if __name__ == "__main__":
    print("Réinitialisation de l'authentification Google...")
    success = reset_google_auth()
    if success:
        print("Réinitialisation terminée avec succès!")
    else:
        print("Erreur lors de la réinitialisation.")
        sys.exit(1)
