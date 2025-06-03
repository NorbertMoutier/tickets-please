import os
import django
import sys

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site
from django.db import connection

def clean_database():
    print("\n=== NETTOYAGE COMPLET DE LA BASE DE DONNÉES ===")
    
    # 1. Supprimer toutes les entrées dans la table de jointure
    print("Suppression des entrées dans la table de jointure...")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM socialaccount_socialapp_sites")
    
    # 2. Supprimer toutes les applications sociales
    print("Suppression de toutes les applications sociales...")
    SocialApp.objects.all().delete()
    
    # 3. Réinitialiser les séquences d'ID pour SocialApp
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='socialaccount_socialapp'")
    
    # 4. S'assurer qu'il n'y a qu'un seul site avec ID=1
    print("Réinitialisation du site avec ID=1...")
    Site.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='django_site'")
    
    site = Site.objects.create(id=1, domain='localhost:8000', name='localhost')
    print(f"Site créé: {site.domain}")
    
    # 5. Créer une nouvelle application sociale Google
    print("Création d'une nouvelle application sociale Google...")
    app = SocialApp.objects.create(
        id=1,
        provider='google',
        name='Google',
        client_id='1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com',
        secret='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'
    )
    
    # 6. Associer l'application au site
    app.sites.add(site)
    print(f"Application Google créée avec succès (ID: {app.id})")
    
    # 7. Vérifier que tout est correct
    print("\n=== VÉRIFICATION FINALE ===")
    apps = SocialApp.objects.all()
    print(f"Nombre d'applications sociales: {apps.count()}")
    
    sites = Site.objects.all()
    print(f"Nombre de sites: {sites.count()}")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM socialaccount_socialapp_sites")
        rows = cursor.fetchall()
        print(f"Nombre d'entrées dans la table de jointure: {len(rows)}")
    
    return True

if __name__ == "__main__":
    print("=== NETTOYAGE DE LA BASE DE DONNÉES ===")
    success = clean_database()
    if success:
        print("\nBase de données nettoyée avec succès!")
    else:
        print("\nErreur lors du nettoyage de la base de données.")
        sys.exit(1)
