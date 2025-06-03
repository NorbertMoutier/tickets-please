#!/usr/bin/env python
"""
Script pour configurer l'authentification Google OAuth2 dans Django-allauth.
"""

import os
import django

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

# Importer les modèles après avoir configuré Django
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_auth():
    # Configurer le site
    site = Site.objects.get(id=1)
    site.domain = 'localhost:8000'
    site.name = 'TicketsPlease'
    site.save()
    print(f"Site configuré: {site.domain}")
    
    # Configurer l'application Google
    app, created = SocialApp.objects.get_or_create(provider='google', name='Google')
    app.client_id = '1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com'
    app.secret = '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'
    app.save()
    
    # Associer l'application au site
    app.sites.add(site)
    
    status = "créée" if created else "mise à jour"
    print(f"Application Google {status}")
    print("Configuration terminée avec succès!")

if __name__ == '__main__':
    setup_google_auth()
