import os
import django
import sys

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.db import connection

def inspect_database():
    # Afficher toutes les applications sociales
    print("\n=== APPLICATIONS SOCIALES ===")
    apps = SocialApp.objects.all()
    print(f"Nombre total d'applications sociales: {apps.count()}")
    
    for app in apps:
        print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
        print(f"  Client ID: {app.client_id}")
        print(f"  Sites associés: {[site.domain for site in app.sites.all()]}")
        print("")
    
    # Afficher tous les sites
    print("\n=== SITES ===")
    sites = Site.objects.all()
    print(f"Nombre total de sites: {sites.count()}")
    
    for site in sites:
        print(f"ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
    
    # Vérifier les tables de jointure
    print("\n=== TABLES DE JOINTURE ===")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM socialaccount_socialapp_sites")
        rows = cursor.fetchall()
        print(f"Nombre d'entrées dans socialaccount_socialapp_sites: {len(rows)}")
        for row in rows:
            print(f"  SocialApp ID: {row[1]}, Site ID: {row[2]}")

def clean_database():
    print("\n=== NETTOYAGE DE LA BASE DE DONNÉES ===")
    
    # 1. Supprimer toutes les applications sociales
    print("Suppression de toutes les applications sociales...")
    SocialApp.objects.all().delete()
    
    # 2. S'assurer qu'il n'y a qu'un seul site avec ID=1
    print("Vérification du site avec ID=1...")
    try:
        site = Site.objects.get(id=1)
        site.domain = 'localhost:8000'
        site.name = 'localhost'
        site.save()
        print(f"Site mis à jour: {site.domain}")
    except Site.DoesNotExist:
        site = Site.objects.create(id=1, domain='localhost:8000', name='localhost')
        print(f"Site créé: {site.domain}")
    
    # Supprimer tous les autres sites
    Site.objects.exclude(id=1).delete()
    
    # 3. Créer une nouvelle application sociale Google
    print("Création d'une nouvelle application sociale Google...")
    app = SocialApp.objects.create(
        provider='google',
        name='Google',
        client_id='1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com',
        secret='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'
    )
    
    # 4. Associer l'application au site
    app.sites.add(site)
    print(f"Application Google créée avec succès (ID: {app.id})")
    
    # 5. Vérifier que tout est correct
    inspect_database()
    
    return True

if __name__ == "__main__":
    print("=== INSPECTION DE LA BASE DE DONNÉES ===")
    inspect_database()
    
    choice = input("\nVoulez-vous nettoyer la base de données? (o/n): ")
    if choice.lower() == 'o':
        clean_database()
        print("\nBase de données nettoyée avec succès!")
    else:
        print("\nAucune modification apportée à la base de données.")
