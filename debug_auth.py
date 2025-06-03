import os
import django
import sys
import json

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site
from django.conf import settings

def debug_auth_config():
    print("\n=== CONFIGURATION D'AUTHENTIFICATION ===")
    
    # Informations sur les sites
    print("\n--- SITES ---")
    sites = Site.objects.all()
    print(f"Nombre de sites: {sites.count()}")
    for site in sites:
        print(f"ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
    
    # Informations sur les applications sociales
    print("\n--- APPLICATIONS SOCIALES ---")
    apps = SocialApp.objects.all()
    print(f"Nombre d'applications sociales: {apps.count()}")
    for app in apps:
        print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
        print(f"  Client ID: {app.client_id}")
        print(f"  Secret: {app.secret}")
        print(f"  Sites associés: {[site.domain for site in app.sites.all()]}")
    
    # Informations sur les comptes sociaux
    print("\n--- COMPTES SOCIAUX ---")
    accounts = SocialAccount.objects.all()
    print(f"Nombre de comptes sociaux: {accounts.count()}")
    for account in accounts:
        print(f"ID: {account.id}, Provider: {account.provider}, UID: {account.uid}")
        print(f"  User: {account.user.username} (ID: {account.user.id}, Email: {account.user.email})")
    
    # Informations sur les tokens sociaux
    print("\n--- TOKENS SOCIAUX ---")
    tokens = SocialToken.objects.all()
    print(f"Nombre de tokens sociaux: {tokens.count()}")
    for token in tokens:
        print(f"ID: {token.id}, App: {token.app.provider if token.app else 'None'}")
        print(f"  Account: {token.account.uid if token.account else 'None'}")
    
    # Configuration django-allauth
    print("\n--- CONFIGURATION DJANGO-ALLAUTH ---")
    print(f"ACCOUNT_EMAIL_VERIFICATION: {settings.ACCOUNT_EMAIL_VERIFICATION}")
    print(f"ACCOUNT_LOGIN_METHODS: {settings.ACCOUNT_LOGIN_METHODS}")
    print(f"ACCOUNT_SIGNUP_FIELDS: {settings.ACCOUNT_SIGNUP_FIELDS}")
    
    try:
        print(f"SOCIALACCOUNT_PROVIDERS (Google):")
        google_config = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
        for key, value in google_config.items():
            if key != 'APP':  # Ne pas afficher les informations sensibles
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"Erreur lors de l'affichage de la configuration SOCIALACCOUNT_PROVIDERS: {e}")
    
    # Utilisateurs
    print("\n--- UTILISATEURS ---")
    users = User.objects.all()
    print(f"Nombre d'utilisateurs: {users.count()}")
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    
    return True

if __name__ == "__main__":
    print("=== DÉBOGAGE DE LA CONFIGURATION D'AUTHENTIFICATION ===")
    success = debug_auth_config()
    if success:
        print("\nDébogage terminé avec succès!")
    else:
        print("\nErreur lors du débogage.")
        sys.exit(1)
