#!/usr/bin/env python
"""
Script pour configurer l'authentification Google OAuth2 dans Django-allauth.
Ce script crée une entrée SocialApp pour Google dans la base de données.
"""

import os
import sys
import django
from getpass import getpass

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

# Importer les modèles après avoir configuré Django
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_auth():
    """
    Configure l'authentification Google OAuth2 en créant une entrée SocialApp
    et en l'associant au site actuel.
    """
    print("\n=== Configuration de l'authentification Google OAuth2 ===\n")
    
    # Vérifier si une application Google existe déjà
    existing_app = SocialApp.objects.filter(provider='google').first()
    if existing_app:
        print(f"Une application Google existe déjà avec l'ID client: {existing_app.client_id}")
        update = input("Voulez-vous mettre à jour cette configuration? (o/n): ").lower()
        if update != 'o':
            print("Configuration annulée.")
            return
        app = existing_app
    else:
        app = SocialApp(provider='google', name='Google')
    
    # Demander les identifiants OAuth2
    print("\nVous devez créer un projet dans la console Google Cloud et configurer les identifiants OAuth2.")
    print("Visitez https://console.cloud.google.com/apis/credentials\n")
    
    client_id = input("Entrez l'ID client Google: ")
    secret = getpass("Entrez le secret client Google: ")
    
    # Mettre à jour l'application
    app.client_id = client_id
    app.secret = secret
    app.save()
    
    # Associer l'application au site actuel
    current_site = Site.objects.get_current()
    app.sites.add(current_site)
    
    print(f"\nL'authentification Google a été configurée avec succès pour le site: {current_site.domain}")
    print("Vous pouvez maintenant utiliser le bouton 'Sign in with Google' sur la page de connexion.")
    
    # Mettre à jour le domaine du site si nécessaire
    update_site = input("\nVoulez-vous mettre à jour le domaine du site? (actuellement: {}) (o/n): ".format(current_site.domain)).lower()
    if update_site == 'o':
        new_domain = input("Entrez le nouveau domaine (ex: example.com): ")
        current_site.domain = new_domain
        current_site.name = new_domain
        current_site.save()
        print(f"Le domaine du site a été mis à jour: {new_domain}")

if __name__ == '__main__':
    setup_google_auth()
